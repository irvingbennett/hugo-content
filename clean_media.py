import os
import re
import yaml

# --- CONFIGURATION ---
# Set to False when you are ready to actually delete the files
DRY_RUN = False

POSTS_DIR = "./content"
MEDIA_DIR = "./static/wp-content/uploads"
# ---------------------

def extract_used_images():
    used_images = set()
    
    # Regex to find any image path pattern inside markdown body/shortcodes
    # Captures paths starting with /wp-content/uploads/
    img_regex = re.compile(r'/wp-content/uploads/[^\s"\'>\)]+')

    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 1. Scan the raw file content for shortcodes, HTML, and inline markdown markdown
                    for match in img_regex.findall(content):
                        # Clean trailing characters like closing parentheses or brackets from regex match
                        clean_path = match.rstrip(')}]#')
                        used_images.add(os.path.normpath(clean_path.lstrip('/')))

                    # 2. Specifically scan YAML front matter for structural image references (cover, thumbnail)
                    if content.startswith('---'):
                        try:
                            parts = content.split('---', 2)
                            if len(parts) >= 2:
                                front_matter = yaml.safe_load(parts[1])
                                if isinstance(front_matter, dict):
                                    # Check common image metadata fields
                                    for key in ['image', 'cover', 'thumbnail', '_thumbnail_id']:
                                        val = front_matter.get(key)
                                        if isinstance(val, str) and 'wp-content/uploads' in val:
                                            used_images.add(os.path.normpath(val.lstrip('/')))
                                        elif isinstance(val, dict) and 'image' in val: # Nested cover fields
                                            img_path = val['image']
                                            if isinstance(img_path, str) and 'wp-content/uploads' in img_path:
                                                used_images.add(os.path.normpath(img_path.lstrip('/')))
                        except Exception:
                            # If a specific front matter has formatting issues, fall back to global regex results
                            pass
                            
    return used_images

def purge_orphaned_media():
    used_paths = extract_used_images()
    print(f"Found {len(used_paths)} unique image files referenced across your posts.\n")
    
    total_files_scanned = 0
    orphaned_count = 0
    total_bytes_saved = 0

    print("Scanning local media directory for unused files...")
    for root, dirs, files in os.walk(MEDIA_DIR):
        for file in files:
            total_files_scanned += 1
            full_path = os.path.join(root, file)
            
            # Map physical file back to its site-relative path (e.g., static/wp-content/... -> wp-content/...)
            relative_to_static = os.path.relpath(full_path, start="./static")
            normalized_rel = os.path.normpath(relative_to_static)

            if normalized_rel not in used_paths:
                orphaned_count += 1
                try:
                    file_size = os.path.getsize(full_path)
                    total_bytes_saved += file_size
                except FileNotFoundError:
                    continue
                
                if DRY_RUN:
                    print(f"[DRY RUN] Unused file would be deleted: {normalized_rel} ({file_size / 1024:.1f} KB)")
                else:
                    print(f"Deleting: {normalized_rel}")
                    os.remove(full_path)

    print("\n" + "="*40)
    if DRY_RUN:
        print(f"*** DRY RUN COMPLETE ***")
        print(f"Scanned {total_files_scanned} total physical files.")
        print(f"Found {orphaned_count} unused images.")
        print(f"Potential space savings: {total_bytes_saved / (1024*1024):.2f} MB")
        print(f"To execute deletion, open the script and change 'DRY_RUN = True' to 'DRY_RUN = False'.")
    else:
        print(f"*** PURGE COMPLETE ***")
        print(f"Deleted {orphaned_count} orphaned files.")
        print(f"Cleared space: {total_bytes_saved / (1024*1024):.2f} MB")
    print("="*40)

if __name__ == "__main__":
    # Ensure PyYAML is installed for parsing metadata strings safely
    try:
        import yaml
    except ImportError:
        print("Installing required PyYAML module package...")
        os.system("pip install pyyaml")
        import yaml
        
    purge_orphaned_media()