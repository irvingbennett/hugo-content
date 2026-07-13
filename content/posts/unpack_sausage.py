import os
import re
from pathlib import Path

# Paths based on running inside content/posts/
WORKING_DIR = Path.cwd()
AI_FILE = WORKING_DIR / "ai_output.txt"

def unpack_posts():
    if not AI_FILE.exists():
        print(f"❌ Missing {AI_FILE.name} in the current directory.")
        return

    with open(AI_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Split the massive text whenever a standard front matter block begins
    # It looks for the opening dashes followed shortly by a title or author tag
    post_chunks = re.split(r'(?=^---\s*\n(?:_|[a-z]).*?title:)', raw_text, flags=re.MULTILINE | re.DOTALL)
    
    # Fallback split if the regex above is too restrictive
    if len(post_chunks) <= 1:
        post_chunks = raw_text.split("---")
        # Re-combine pieces because splitting on plain '---' breaks front matter boundaries
        reconstructed = []
        for i in range(1, len(post_chunks), 2):
            if i+1 < len(post_chunks):
                reconstructed.append("---" + post_chunks[i] + "---" + post_chunks[i+1])
        post_chunks = reconstructed

    fixed_count = 0
    print(f"✂️  Slicing and parsing the AI Studio output...")

    for chunk in post_chunks:
        chunk = chunk.strip()
        if not chunk or "title:" not in chunk:
            continue

        # Extract the title or the slug/url line to determine the correct filename
        url_match = re.search(r'^url:\s*/\d+/\d+/\d+/([^/\n\r]+)', chunk, re.MULTILINE)
        title_match = re.search(r'^title:\s*(?:"([^"]+)"|([^\n\r]+))', chunk, re.MULTILINE)

        # Determine the filename base
        if url_match:
            filename = f"{url_match.group(1).strip()}.md"
        elif title_match:
            title_text = title_match.group(1) or title_match.group(2)
            filename = f"{title_text.lower().replace(' ', '-').strip()}.md"
            # Strip out non-alphanumeric chars from fallback filename
            filename = "".join(c for c in filename if c.isalnum() or c in "-.")
        else:
            continue

        file_path = WORKING_DIR / filename

        # Write the reconstructed individual file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk + "\n")
            
        print(f"   ✓ Extracted and saved: {filename}")
        fixed_count += 1

    print(f"\n🏁 Complete! Unpacked {fixed_count} individual markdown files in a fraction of a second.")

if __name__ == "__main__":
    unpack_posts()
