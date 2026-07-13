import os
import re
from pathlib import Path

CONTENT_DIRECTORY = Path("/home/irving/hugo-content/content")

def strip_gallery_tags():
    # Regex to catch {{< gallery ... >}} or {{< gallery >}} variations
    opening_gallery_re = re.compile(r'\{\{<\s*gallery[^>]*?>\}\}\s*')
    # Regex to catch the closing {{< /gallery >}} tag
    closing_gallery_re = re.compile(r'\s*\{\{<\s*/gallery\s*>\}\}')

    updated_files = 0

    print("🧹 Hunting down and removing broken gallery shortcut wrappers...")

    for md_file in CONTENT_DIRECTORY.rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        # Remove all opening and closing gallery tags globally
        new_content = opening_gallery_re.sub('', new_content)
        new_content = closing_gallery_re.sub('', new_content)

        # Save changes if the file contained the tags
        if new_content != content:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"   ✓ Stripped gallery tags from: {md_file.name}")
            updated_files += 1

    print(f"\n🏁 Finished! Automatically cleaned {updated_files} files.")

if __name__ == "__main__":
    strip_gallery_tags()