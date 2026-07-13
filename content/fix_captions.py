import os
import re
from pathlib import Path

# Paths based on your setup
BASE_DIR = Path("/home/irving/hugo-content")
LIST_FILE = BASE_DIR / "caption.txt"

def fast_repair():
    if not LIST_FILE.exists():
        print(f"❌ Could not find {LIST_FILE.name}! Make sure it's in the same directory.")
        return

    # Read target files from your checklist
    with open(LIST_FILE, "r", encoding="utf-8") as f:
        target_files = [line.strip() for line in f if line.strip()]

    # A bulletproof regex matching the specific structure:
    # 1. Escaped open bracket: \[caption
    # 2. Extract the true alt text from: caption="Text"
    # 3. Match any messy inner links/brackets, including empty image tags !\[\]
    # 4. Extract the final high-res target destination URL
    # 5. Handle the escaped closing bracket: \[/caption\]
    caption_regex = re.compile(
        r'\\?\[caption[^\]]*?caption="([^"]*?)"[^\]]*?\]'  # Group 1: Alt text
        r'.*?'                                            # Interstitial garbage
        r'\((//wp-content/[^)]+)\)'                       # Group 2: Full-res URL
        r'\s*\\?\[/caption\]',                            # Closing container
        re.IGNORECASE | re.DOTALL
    )

    updated_count = 0
    print(f"⚡ Processing {len(target_files)} targeted files from caption.txt...")

    for relative_path in target_files:
        # Strip leading dot if present (e.g. ./posts/file.md -> posts/file.md)
        clean_path = relative_path.lstrip("./")
        file_path = BASE_DIR / "content" / clean_path

        if not file_path.exists():
            # Try matching directly in case 'content' is already in your structure
            file_path = BASE_DIR / clean_path
            if not file_path.exists():
                print(f"   ⚠️  Skipping (File not found): {clean_path}")
                continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        def substitute_caption(match):
            alt_text = match.group(1).strip()
            large_url = match.group(2).strip()
            # Clean up residual quote strings if they leaked into the group
            large_url = large_url.split('"')[0].split("'")[0].strip()
            
            # Formats clean Markdown image block with essential padding lines
            return f"\n\n![{alt_text}]({large_url})\n\n"

        new_content = caption_regex.sub(substitute_caption, new_content)
        
        # Standardize empty rows so Hugo parses blocks cleanly
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"   ✓ Fixed: {file_path.name}")
            updated_count += 1

    print(f"\n🏁 Finished! Successfully fixed {updated_count} files in milliseconds.")

if __name__ == "__main__":
    fast_repair()