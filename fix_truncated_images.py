import os
import re
from pathlib import Path

CONTENT_DIRECTORY = Path("/home/irving/hugo-content/content")

def repair_truncated_images():
    # Regex targets the exact pattern where the file path cuts off into "caption\]"
    # Group 1 captures the caption/alt text in brackets
    # Group 2 captures the partial URL path up to the gallery_backup folder
    truncated_pattern = re.compile(
        r'!\[(.*?)\]\((.*?/gallery_backup/)caption\\?\]',
        re.IGNORECASE
    )

    updated_files = 0
    print("🛠️  Repairing images truncated during the previous cleanup pass...")

    for md_file in CONTENT_DIRECTORY.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        def replace_truncated(match):
            alt_text = match.group(1).strip()
            partial_path = match.group(2).strip()
            
            # Reconstruct the markdown image. 
            # We use a placeholder image name since the original filename was clipped.
            # You can easily find these later by searching for 'todo-placeholder.jpg'
            return f"\n\n![{alt_text}]({partial_path}todo-placeholder.jpg)\n\n"

        new_content = truncated_pattern.sub(replace_truncated, new_content)

        # Standardize empty rows
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)

        if new_content != content:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"   ✓ Fixed truncated image syntax in: {md_file.name}")
            updated_files += 1

    print(f"\n🏁 Finished! Successfully repaired {updated_files} files.")

if __name__ == "__main__":
    repair_truncated_images()