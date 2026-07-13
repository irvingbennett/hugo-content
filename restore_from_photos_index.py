import os
import re
import json
import shutil

# --- CONFIGURATION PATHS ---
CONTENT_DIR = "content"
GALLERY_DIR = "static/wp-content/uploads/gallery_backup"
JSON_INDEX_PATH = "photos_index.json"  # Adjust if it's stored in a different path

def load_photos_index(json_path):
    """Loads the photos index and creates a lowercase lookup map."""
    print(f"[+] Loading photo index repository: {json_path}...")
    if not os.path.exists(json_path):
        print(f"[-] Error: JSON file '{json_path}' not found.")
        return {}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Map lowercase key -> full dictionary details
    index_map = {k.lower(): v for k, v in data.items()}
    print(f"[+] Successfully loaded {len(index_map)} indexed assets from Google Drive map.")
    return index_map

def restore_missing_images():
    # 1. Load the JSON mapping index
    photo_index = load_photos_index(JSON_INDEX_PATH)
    if not photo_index:
        return

    # Ensure local target gallery folder exists
    os.makedirs(GALLERY_DIR, exist_ok=True)

    # 2. Setup Regex pattern to identify standard Markdown and image link targets
    # Catches: ![alt](/wp-content/uploads/gallery_backup/image.jpg) or standard links
    link_pattern = re.compile(r'!\[.*?\]\((.*?)\)|\[.*?\]\((.*?)\)')
    
    copied_count = 0
    missing_but_not_indexed = 0
    already_present = 0

    print(f"[+] Inspecting markdown files for missing assets inside: {CONTENT_DIR}...")

    # 3. Walk through all post and page markdown structures
    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Find all hyperlinked assets inside this post
                matches = link_pattern.findall(content)
                for match in matches:
                    # re.findall with OR groups returns a tuple (group1, group2)
                    link = match[0] if match[0] else match[1]
                    
                    # We are only inspecting assets targeting your gallery backup path
                    if "gallery_backup/" in link:
                        # Extract the exact filename string from the path string
                        filename = link.split("gallery_backup/")[-1].strip()
                        # Strip any trailing web or query args if present
                        filename = filename.split('?')[0]
                        if not filename:
                            continue
                        
                        # Check if it already exists on your local linux partition
                        local_target_path = os.path.join(GALLERY_DIR, filename)
                        
                        if os.path.exists(local_target_path):
                            already_present += 1
                            continue
                        
                        # It is missing! Let's check our JSON database map
                        lowercase_filename = filename.lower()
                        if lowercase_filename in photo_index:
                            source_meta = photo_index[lowercase_filename]
                            windows_drive_path = source_meta.get("local_path")
                            correct_case_filename = source_meta.get("filename", filename)
                            
                            # Recalculate target path using correct case naming convention
                            final_target_path = os.path.join(GALLERY_DIR, correct_case_filename)
                            
                            if windows_drive_path and os.path.exists(windows_drive_path):
                                try:
                                    print(f"[Heal] Copying: {correct_case_filename} -> {final_target_path}")
                                    shutil.copy2(windows_drive_path, final_target_path)
                                    copied_count += 1
                                except Exception as e:
                                    print(f"[-] Failed to copy file {correct_case_filename}: {e}")
                            else:
                                print(f"[-] Found in index, but path missing on disk: {windows_drive_path}")
                        else:
                            missing_but_not_indexed += 1

    print(f"\n[Execution Summary]")
    print(f" -> Existing Assets Already Intact: {already_present}")
    print(f" -> Missing Assets Restored from Google Drive: {copied_count}")
    print(f" -> Permanently Missing (Not Found in Index): {missing_but_not_indexed}")

if __name__ == "__main__":
    restore_missing_images()