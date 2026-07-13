import os
import re
from pathlib import Path

# --- CONFIGURATION ---
CONTENT_DIRECTORY = Path("/home/irving/hugo-content/content")
ORIGINALS_FILE = Path("/home/irving/hugo-content/existing_originals.txt")
TARGET_BASE = "/wp-content/uploads/gallery_backup/"

# Catch WordPress resizing suffixes (-640x480, -150x150, -scaled, etc.)
RESIZED_SUFFIX_REGEX = re.compile(r'-(?:\d+x\d+|scaled|rotated|e\d+)(?=\.[a-zA-Z]{3,4}$)')

# Core Patterns
MD_IMAGE_RE = re.compile(r'(!\[.*?\]\()(.+?)(\s*["\'].*?["\']\s*\))')
MD_LINK_RE  = re.compile(r'(\[.*?\]\()([^)]+?\.(?:jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))(\s*["\'].*?["\']\s*\))')
HTML_IMG_RE = re.compile(r'(<img[^>]+src=["\'])([^"\']+)(["\'])')
PICASA_RE   = re.compile(r'\[\!\[([^\]]+\.(?:jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))\]\([^)]+\)\]\([^)]*?picasaweb[^)]*\)')

# New Pattern: Catches Hugo shortcodes: {{< figure ... src="path" ... >}}
HUGO_SHORTCODE_RE = re.compile(r'(\{\{<\s*figure[^>]*?src=["\'])([^"\']+)(["\'][^>]*?>\}\})')

def load_originals(file_path):
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found. Please generate it in WSL first.")
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip().lower() for line in f if line.strip()}

def clean_image_url(url):
    url = url.split()[0]
    filename = url.split('/')[-1]
    cleaned_filename = RESIZED_SUFFIX_REGEX.sub('', filename)
    return cleaned_filename

def migrate():
    originals = load_originals(ORIGINALS_FILE)
    if not originals:
        return

    missing_images_report = {}
    total_files_updated = 0

    print(f"🚀 Recursively scanning and fixing ALL markdown files in: {CONTENT_DIRECTORY}")

    for md_file in CONTENT_DIRECTORY.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        
        # --- PROCESS 1: MARKDOWN IMAGES ---
        def replace_md_img(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name.lower() not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = MD_IMAGE_RE.sub(replace_md_img, new_content)

        # --- PROCESS 2: TEXT LINKS WRAPPING IMAGES ---
        def replace_md_link(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name.lower() not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = MD_LINK_RE.sub(replace_md_link, new_content)

        # --- PROCESS 3: HTML IMG TAGS ---
        def replace_html(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name.lower() not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = HTML_IMG_RE.sub(replace_html, new_content)

        # --- PROCESS 4: CLEAN PICASA WRAPPERS ---
        def replace_picasa(match):
            filename = match.group(1)
            clean_name = clean_image_url(filename)
            if clean_name.lower() not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"![{clean_name}]({TARGET_BASE}{clean_name})"
        new_content = PICASA_RE.sub(replace_picasa, new_content)

        # --- PROCESS 5: HUGO SHORTCODES ---
        # Converts: src="//wp-content/uploads/2017/03/P2180270-150x150.jpg" -> src="/wp-content/uploads/gallery_backup/P2180270.jpg"
        def replace_shortcode(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name.lower() not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = HUGO_SHORTCODE_RE.sub(replace_shortcode, new_content)

        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            total_files_updated += 1

    print("\n" + "="*60)
    print(f"🏁 Migration Complete! Updated {total_files_updated} markdown files across posts and pages.")
    print("="*60)
    
    if missing_images_report:
        print(f"\n❌ Found missing files. Use quotes in Google Photos to find them:")
        for post, imgs in sorted(missing_images_report.items()):
            print(f"\n📄 File: {post}")
            for img in sorted(imgs):
                print(f"   Missing token: \"{img.split('.')[0]}\"")

if __name__ == "__main__":
    migrate()