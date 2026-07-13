import os
import json
import re
from pathlib import Path

# --- CONFIGURATION ---
# Path to your local Google Photos/Drive backup folder organized by year/month
PHOTOS_BACKUP_DIRECTORY = Path("/mnt/c/Users/irvin/Google Drive/Google Photos")  # <-- Change this to your actual backup path
OUTPUT_JSON_FILE = Path("/home/irving/hugo-content/photos_index.json")

# Ignore WordPress-style resized image suffixes just in case they slipped into the backup
RESIZED_SUFFIX_REGEX = re.compile(r'-(?:\d+x\d+|scaled|rotated|e\d+)(?=\.[a-zA-Z]{3,4}$)')
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

def build_photo_index():
    photo_index = {}
    
    if not PHOTOS_BACKUP_DIRECTORY.exists():
        print(f"❌ Error: Backup directory not found at {PHOTOS_BACKUP_DIRECTORY}")
        return

    print(f"🔍 Scanning for photos in: {PHOTOS_BACKUP_DIRECTORY}")
    
    # Recursively walk through all years and months
    for root, _, files in os.walk(PHOTOS_BACKUP_DIRECTORY):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                # Skip it if it's a resized duplicate pattern
                if RESIZED_SUFFIX_REGEX.search(file):
                    continue
                
                # Use lowercase filename as the unique lookup key for case-insensitivity
                photo_key = file.lower()
                absolute_path = os.path.join(root, file)
                
                # Store the exact path attribute
                photo_index[photo_key] = {
                    "filename": file,
                    "local_path": absolute_path
                }

    # Write out the JSON database
    print(f"💾 Saving index of {len(photo_index)} unique photos to {OUTPUT_JSON_FILE}...")
    with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(photo_index, f, indent=4, ensure_ascii=False)
        
    print("🏁 Indexing complete!")

if __name__ == "__main__":
    build_photo_index()
