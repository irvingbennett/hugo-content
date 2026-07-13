import os
import re

# --- CONFIGURATION PATHS ---
# Adjust these if your content or static folders live elsewhere
CONTENT_DIR = "content"
STATIC_GALLERY_DIR = "static/wp-content/uploads/gallery_backup"
OUTPUT_MISSING_FILE = "missing.txt"

# Regex pattern to match markdown images and standard HTML img tags pointing to gallery_backup
# Matches names like: /wp-content/uploads/gallery_backup/FileName.jpg
IMG_PATTERN = re.compile(r'\/wp-content\/uploads\/gallery_backup\/([^\s\)\"\>]+)')

def load_physical_gallery(gallery_path):
    """Builds a map of lowercased filenames to their actual physical filename on disk."""
    if not os.path.exists(gallery_path):
        print(f"[-] Error: Gallery path '{gallery_path}' not found.")
        return {}
    
    gallery_files = {}
    for filename in os.listdir(gallery_path):
        if os.path.isfile(os.path.join(gallery_path, filename)):
            gallery_files[filename.lower()] = filename
    return gallery_files

def heal_and_audit():
    # 1. Map out what is physically present on disk
    print(f"[+] Indexing gallery files in: {STATIC_GALLERY_DIR}...")
    physical_gallery = load_physical_gallery(STATIC_GALLERY_DIR)
    print(f"[+] Found {len(physical_gallery)} assets in the backup folder.")
    
    missing_images = set()
    renamed_count = 0
    matched_count = 0

    # 2. Walk through all Hugo pages and posts
    print(f"[+] Scanning markdown files inside: {CONTENT_DIR}...")
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Find all images referenced matching our pattern
                matches = IMG_PATTERN.findall(content)
                
                for ref_filename in matches:
                    ref_lower = ref_filename.lower()
                    
                    # Exact match case: file exists precisely as written in markdown
                    if os.path.exists(os.path.join(STATIC_GALLERY_DIR, ref_filename)):
                        matched_count += 1
                        continue
                    
                    # Case-mismatch case: File exists but has different capitalization on disk
                    elif ref_lower in physical_gallery:
                        actual_disk_name = physical_gallery[ref_lower]
                        old_path = os.path.join(STATIC_GALLERY_DIR, actual_disk_name)
                        new_path = os.path.join(STATIC_GALLERY_DIR, ref_filename)
                        
                        try:
                            os.rename(old_path, new_path)
                            print(f"[~] Renamed asset: '{actual_disk_name}' -> '{ref_filename}'")
                            # Update our in-memory map to reflect the rename
                            del physical_gallery[ref_lower]
                            physical_gallery[ref_lower] = ref_filename
                            renamed_count += 1
                        except Exception as e:
                            print(f"[-] Failed to rename '{actual_disk_name}' to '{ref_filename}': {e}")
                    
                    # Complete missing case: Not found under any casing variant
                    else:
                        # Log it along with the post filename so you know where it was referenced
                        missing_images.add(f"{ref_filename}  (referenced in: {file_path})")

    # 3. Output missing files report
    with open(OUTPUT_MISSING_FILE, 'w', encoding='utf-8') as out:
        if missing_images:
            out.write("\n".join(sorted(missing_images)))
            print(f"[!] Finished! {len(missing_images)} missing assets logged to '{OUTPUT_MISSING_FILE}'.")
        else:
            out.write("No missing images found! All layout paths match cleanly.")
            print("[+] Finished! Zero missing files detected.")
            
    print(f"\n[Summary]\n -> Perfectly Matched: {matched_count}\n -> Healed via Rename: {renamed_count}\n -> Permanently Missing: {len(missing_images)}")

if __name__ == "__main__":
    heal_and_audit()