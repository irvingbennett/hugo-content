import os
import re
from pathlib import Path

# --- CONFIGURATION ---
CONTENT_DIRECTORY = Path("/home/irving/hugo-content/content")
ORIGINALS_FILE = Path("/home/irving/hugo-content/existing_originals.txt")
TARGET_BASE = "/wp-content/uploads/gallery_backup/"

# Catch WordPress resizing suffixes (-640x480, -150x150, -scaled, etc.)
RESIZED_SUFFIX_REGEX = re.compile(r'-(?:\d+x\d+|scaled|rotated|e\d+)(?=\.[a-zA-Z]{3,4}$)')

# Core Patterns (Soportando jpg, jpeg, png, gif, webp, svg)
MD_IMAGE_RE = re.compile(r'(!\[.*?\]\()(.+?)(\s*["\'].*?["\']\s*\))')
MD_LINK_RE  = re.compile(r'(\[.*?\]\()([^)]+?\.(?:jpg|jpeg|png|gif|webp|svg|JPG|JPEG|PNG|GIF|WEBP|SVG))(\s*["\'].*?["\']\s*\))')
HTML_IMG_RE = re.compile(r'(<img[^>]+src=["\'])([^"\']+)(["\'])')
HUGO_SHORTCODE_RE = re.compile(r'(\{\{<\s*figure[^>]*?src=["\'])([^"\']+)(["\'][^>]*?>\}\})')

def load_originals(file_path):
    if not file_path.exists():
        print(f"❌ Error: {file_path} not found. Please generate it in WSL first.")
        return set()
    with open(file_path, 'r', encoding='utf-8') as f:
        # Cargamos todo en minúsculas
        return {line.strip().lower() for line in f if line.strip()}

def clean_image_url(url):
    url = url.split()[0]
    filename = url.split('/')[-1]
    # Removemos prefijos redundantes y pasamos a minúsculas para machear con el disco
    filename_clean = re.sub(r'^fotosearch[_.-]?', '', filename.lower())
    cleaned_filename = RESIZED_SUFFIX_REGEX.sub('', filename_clean)
    return cleaned_filename

def migrate():
    originals = load_originals(ORIGINALS_FILE)
    if not originals:
        return

    missing_images_report = {}
    total_files_updated = 0

    print(f"🚀 Ejecutando migración de enlaces en minúsculas en: {CONTENT_DIRECTORY}")

    for md_file in CONTENT_DIRECTORY.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content
        
        # --- PROCESS 1: MARKDOWN IMAGES ---
        def replace_md_img(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = MD_IMAGE_RE.sub(replace_md_img, new_content)

        # --- PROCESS 2: TEXT LINKS ---
        def replace_md_link(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = MD_LINK_RE.sub(replace_md_link, new_content)

        # --- PROCESS 3: HTML IMG TAGS ---
        def replace_html(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = HTML_IMG_RE.sub(replace_html, new_content)

        # --- PROCESS 4: HUGO SHORTCODES ---
        def replace_shortcode(match):
            prefix, old_url, suffix = match.groups()
            clean_name = clean_image_url(old_url)
            if clean_name not in originals:
                missing_images_report.setdefault(md_file.name, set()).add(clean_name)
            return f"{prefix}{TARGET_BASE}{clean_name}{suffix}"
        new_content = HUGO_SHORTCODE_RE.sub(replace_shortcode, new_content)

        if new_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            total_files_updated += 1

    print("\n" + "="*60)
    print(f"🏁 ¡Migración limpia completada! Se actualizaron {total_files_updated} archivos.")
    print("="*60)

if __name__ == "__main__":
    migrate()