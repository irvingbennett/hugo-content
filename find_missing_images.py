import os
import re
from pathlib import Path

# Configuration
CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")
TARGET_PATH_PART = "wp-content/uploads/gallery_backup"

# Aggressive regex: matches any target gallery URL that points to an image file extension
IMAGE_URL_REGEX = r'(?:/wp-content/uploads/gallery_backup/|wp-content/uploads/gallery_backup/)([^"\'\)\s>]+?\.(?:jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF))'

missing_report = {}
total_images_found = 0
total_missing = 0

print("🔍 Scanning content files for ALL referenced gallery images (including links)...")

# Walk through all markdown files
for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith(".md"):
            file_path = Path(root) / file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find all image strings matching our target folder and extensions
            matches = re.findall(IMAGE_URL_REGEX, content)
            # Use set to avoid reporting the same image multiple times within a single post
            unique_matches = set(matches)

            file_missing_images = []
            
            for img_filename in unique_matches:
                total_images_found += 1
                
                # Reconstruct the expected physical path in static
                physical_path = STATIC_DIR / TARGET_PATH_PART / img_filename

                # Check if file exists on disk
                if not physical_path.exists():
                    total_missing += 1
                    file_missing_images.append(img_filename)

            if file_missing_images:
                # Group missing files by the post that references them
                missing_report[str(file_path)] = sorted(file_missing_images)

# Print the report
print("\n" + "="*60)
print(f"📊 SCAN COMPLETE: Found {total_images_found} total image references.")
print(f"❌ Actual Missing Files: {total_missing}")
print("="*60 + "\n")

if missing_report:
    for post, images in sorted(missing_report.items()):
        print(f"📄 Post: {post}")
        for img in images:
            print(f"   ❌ Missing: {img}")
        print("-" * 50)
else:
    print("🎉 Brilliant! Every single image link now maps to a physical file on disk.")