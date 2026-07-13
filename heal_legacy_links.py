import os
import re

CONTENT_DIR = "content"
GALLERY_DIR = "static/wp-content/uploads/gallery_backup"

def load_physical_gallery_map(base_path):
    """Walks the gallery folder to match lowercased paths with actual file casings."""
    path_map = {}
    if not os.path.exists(base_path):
        return path_map
    for root, _, files in os.walk(base_path):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_path).replace("\\", "/")
            path_map[rel_path.lower()] = rel_path
    return path_map

def fix_link_string(link, file_map):
    """Applies pattern rewriting logic to legacy shortcodes and absolute paths."""
    cleaned = link.strip()
    
    # 1. Clean up double forward slashes
    if cleaned.startswith("//wp-content/"):
        cleaned = cleaned[1:]
        
    # 2. Redirect bare aconcagua paths
    if cleaned.startswith("/aconcagua/"):
        cleaned = "/wp-content/uploads/gallery_backup" + cleaned

    # 3. Strip out old Gallery3 / Gallery2 app layout variables
    if cleaned.startswith(("/g3/", "/gallery3/", "/gallery/")):
        # Extract filename and section subfolder
        parts = [p for p in cleaned.split('/') if p and p != "var" and p != "resizes" and not p.endswith(".php")]
        if parts and parts[0] in ("g3", "gallery3", "gallery"):
            parts.pop(0)
        if parts:
            cleaned = "/wp-content/uploads/gallery_backup/" + "/".join(parts)

    # 4. Remove empty trailing path errors
    if cleaned.endswith("/wp-content/uploads/gallery_backup/"):
        return None

    # Strip any hanging web variables like .html extensions or query arguments from old app links
    cleaned = re.sub(r'\.html?$', '', cleaned)
    cleaned = cleaned.split('?')[0]

    # Verify lookups against your physical disk inventory
    if "gallery_backup/" in cleaned:
        sub_path = cleaned.split("gallery_backup/")[-1].lower()
        if sub_path in file_map:
            return f"/wp-content/uploads/gallery_backup/{file_map[sub_path]}"
            
    return cleaned

def process_markdown_files():
    file_map = load_physical_gallery_map(GALLERY_DIR)
    print(f"[+] Loaded {len(file_map)} items from your image archive repository.")
    
    # Matches both standard markdown links [text](link) and image structures ![alt](link)
    link_pattern = re.compile(r'(!?\[.*?\]\()(.*?)(\))')
    modified_files = 0
    total_fixed = 0

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                def replacer(match):
                    nonlocal total_fixed
                    prefix, old_link, suffix = match.groups()
                    new_link = fix_link_string(old_link, file_map)
                    
                    if new_link is None: # Is a broken hanging link string, remove markdown packaging
                        return ""
                    if new_link != old_link:
                        total_fixed += 1
                        return f"{prefix}{new_link}{suffix}"
                    return match.group(0)

                new_content = link_pattern.sub(replacer, content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    modified_files += 1

    print(f"\n[Execution Summary]\n -> Total Markdown Files Adjusted: {modified_files}\n -> Legacy Hyperlinks Healed: {total_fixed}")

if __name__ == "__main__":
    process_markdown_files()
