#!/usr/bin/env python3
"""Check links in Markdown files under the content directory.

Usage:
    python3 check_markdown_links.py
    python3 check_markdown_links.py --root content --ext .md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, urlunparse, quote, unquote
from urllib.request import Request, urlopen

LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\(")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Markdown links under a directory")
    parser.add_argument("--root", default="content", help="Directory to scan for Markdown files")
    parser.add_argument("--ext", default=".md", help="File extension to include")
    parser.add_argument("--timeout", type=float, default=10.0, help="Timeout in seconds for remote URL checks")
    parser.add_argument("--remote", action="store_true", help="Also validate remote HTTP(S) links")
    parser.add_argument("--localhost", action="store_true", help="Check root-relative links against http://localhost:1313")
    parser.add_argument("--base-url", default=None, help="Check root-relative links against this URL, for example http://localhost:1313")
    return parser.parse_args()


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if not target:
        return ""
    if target.startswith("<") and target.endswith(">"):
        return target[1:-1].strip()

    title_match = re.search(r'\s+(?P<title>"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')\s*$', target)
    if title_match:
        target = target[: title_match.start("title")].rstrip()

    return target


def strip_fragment_and_query(target: str) -> str:
    parsed = urlparse(target)
    return parsed.path


def resolve_site_url(target: str, base_url: str | None) -> str | None:
    if not base_url:
        return None
    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        return None
    if target.startswith("//"):
        return f"{parsed.scheme}://{parsed.netloc}/{target.lstrip('/')}"
    if target.startswith("/"):
        return f"{parsed.scheme}://{parsed.netloc}{target}"
    return None


def discover_markdown_files(root: Path, ext: str) -> List[Path]:
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root}")
    return sorted(path for path in root.rglob(f"*{ext}") if path.is_file())


def extract_links(markdown_text: str) -> List[str]:
    links: List[str] = []
    index = 0

    while index < len(markdown_text):
        start = markdown_text.find("](", index)
        if start == -1:
            break
        if start > 0 and markdown_text[start - 1] == "!":
            index = start + 2
            continue

        end = start + 2
        depth = 0
        in_angle_brackets = False
        quote_char: str | None = None

        while end < len(markdown_text):
            char = markdown_text[end]

            if quote_char:
                if char == quote_char and markdown_text[end - 1] != "\\":
                    quote_char = None
                end += 1
                continue

            if in_angle_brackets:
                if char == ">":
                    in_angle_brackets = False
                end += 1
                continue

            if char == "<":
                in_angle_brackets = True
            elif char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    raw_target = markdown_text[start + 2 : end].strip()
                    target = normalize_target(raw_target)
                    if target:
                        links.append(target)
                    break
                depth -= 1
            elif char in {'"', "'"}:
                quote_char = char

            end += 1

        index = end + 1

    return links


def quote_url(url: str) -> str:
    parsed = urlparse(url)
    path = quote(unquote(parsed.path), safe="/%")
    query = quote(unquote(parsed.query), safe="=&%")
    fragment = quote(unquote(parsed.fragment), safe="%")
    return urlunparse((
        parsed.scheme,
        parsed.netloc,
        path,
        parsed.params,
        query,
        fragment
    ))


def local_target_exists(target: str, source_file: Path, repo_root: Path) -> bool:
    cleaned_target = unquote(strip_fragment_and_query(target))
    if not cleaned_target:
        return True

    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc:
        return False

    if cleaned_target.startswith("/"):
        candidates = [
            repo_root / "static" / cleaned_target.lstrip("/"),
            repo_root / "content" / cleaned_target.lstrip("/"),
            repo_root / cleaned_target.lstrip("/"),
        ]
    else:
        candidates = [
            source_file.parent / cleaned_target
        ]

    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return True

        # Handle links to directories or bare paths without an extension.
        if resolved.suffix == "":
            for extra in (resolved.with_suffix(".md"), resolved / "index.md", resolved / "index.html"):
                if extra.exists():
                    return True

    return False


def check_remote_link(target: str, timeout: float) -> bool:
    try:
        safe_target = quote_url(target)
        parsed = urlparse(safe_target)
        if not parsed.scheme or not parsed.netloc:
            return False
        req = Request(safe_target, method="HEAD")
        with urlopen(req, timeout=timeout) as response:
            return 200 <= response.getcode() < 400
    except HTTPError as exc:
        if exc.code in {405, 403}:
            try:
                safe_target = quote_url(target)
                with urlopen(safe_target, timeout=timeout) as response:
                    return 200 <= response.getcode() < 400
            except (HTTPError, URLError, TimeoutError, ValueError, ConnectionResetError):
                return False
        return False
    except (URLError, TimeoutError, ValueError, ConnectionResetError):
        return False


def check_links_in_file(markdown_file: Path, repo_root: Path, timeout: float, check_remote: bool, base_url: str | None) -> List[Tuple[str, str]]:
    issues: List[Tuple[str, str]] = []
    text = markdown_file.read_text(encoding="utf-8")
    for target in extract_links(text):
        # Normalize protocol-relative local links (e.g. starting with //wp-content)
        if target.startswith("//"):
            parsed = urlparse(target)
            if parsed.netloc == "wp-content" or "." not in parsed.netloc:
                target = "/" + target.lstrip("/")

        if target.startswith(("http://", "https://")):
            if check_remote and not check_remote_link(target, timeout):
                issues.append((target, "remote"))
        elif target.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        elif target.startswith("#"):
            continue
        elif target.startswith(("/", "//")) and base_url:
            site_url = resolve_site_url(target, base_url)
            if site_url and not check_remote_link(site_url, timeout):
                issues.append((target, "local-site"))
        elif not local_target_exists(target, markdown_file, repo_root):
            issues.append((target, "local"))
    return issues


def main() -> int:
    args = parse_args()
    repo_root = Path.cwd().resolve()
    content_root = (repo_root / args.root).resolve()

    try:
        markdown_files = discover_markdown_files(content_root, args.ext)
    except FileNotFoundError as exc:
        print(exc)
        return 2

    if not markdown_files:
        print(f"No Markdown files found under {content_root}")
        return 0

    base_url = args.base_url or ("http://localhost:1313" if args.localhost else None)

    broken: List[Tuple[Path, str, str]] = []
    for markdown_file in markdown_files:
        issues = check_links_in_file(markdown_file, repo_root, args.timeout, args.remote, base_url)
        for target, kind in issues:
            broken.append((markdown_file, target, kind))

    if broken:
        print(f"Found {len(broken)} broken link(s) across {len(markdown_files)} Markdown file(s):")
        for markdown_file, target, kind in broken:
            rel_path = markdown_file.relative_to(repo_root)
            print(f"- {rel_path}: {target} [{kind}]")
        return 1

    print(f"All links look good in {len(markdown_files)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
