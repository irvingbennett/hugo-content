from datetime import datetime
import os
import re

# Define the target directory
TARGET_DIR = "content/pages/panama-paso-a-paso"

# Regex to find the front matter block (YAML style, between ---)
FRONT_MATTER_REGEX = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL | re.MULTILINE)
# Regex to extract the date line
DATE_REGEX = re.compile(r'^date:\s*["\']?([^"\']+)["\']?')
# Regex to check if a weight tag already exists
WEIGHT_REGEX = re.compile(r"^weight:\s*\d+", re.MULTILINE)


def get_file_date(file_path):
    """Reads a file, extracts its front matter date, and returns a datetime object."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = FRONT_MATTER_REGEX.search(content)
        if not match:
            return None

        front_matter = match.group(1)
        for line in front_matter.splitlines():
            date_match = DATE_REGEX.match(line.strip())
            if date_match:
                date_str = date_match.group(1)
                return datetime.fromisoformat(date_str)
    except Exception as e:
        print(f"Error reading date from {file_path}: {e}")

    return None


def update_file_weight(file_path, weight_value):
    """Injects or updates the weight tag inside the front matter of the file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    fm_match = FRONT_MATTER_REGEX.search(content)
    if not fm_match:
        print(f"Could not find front matter in {file_path}")
        return

    full_fm_block = fm_match.group(0)  # Includes the --- markers
    inner_fm = fm_match.group(1)

    # Format weight with 4-digit padding (e.g., 0010, 0020)
    weight_str = f"weight: {weight_value:04d}"

    # Check if 'weight:' already exists inside the front matter
    if WEIGHT_REGEX.search(inner_fm):
        # Update existing weight
        new_inner_fm = WEIGHT_REGEX.sub(weight_str, inner_fm)
    else:
        # Append new weight right before the closing front matter marker
        new_inner_fm = inner_fm.rstrip() + f"\n{weight_str}"

    # Reconstruct the full file content
    new_fm_block = f"---\n{new_inner_fm}\n---\n"
    new_content = content.replace(full_fm_block, new_fm_block, 1)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        return

    page_data = []

    # 1. Collect all Markdown files and their dates
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".md"):
            file_path = os.path.join(TARGET_DIR, filename)
            file_date = get_file_date(file_path)

            if file_date:
                page_data.append({"path": file_path, "date": file_date})
            else:
                print(f"Skipping {filename}: No valid date found in front matter.")

    # 2. Sort pages chronologically (earliest first)
    page_data.sort(key=lambda x: x["date"])

    print(f"\nFound {len(page_data)} pages to process. Updating weights...")

    # 3. Iterate and apply the weight starting at 10, step by 10
    current_weight = 10
    for page in page_data:
        update_file_weight(page["path"], current_weight)
        print(
            f"-> Assigned weight {current_weight:04d} to {os.path.basename(page['path'])} ({page['date'].date()})"
        )
        current_weight += 10

    print("\nDone! All files successfully sorted and updated.")


if __name__ == "__main__":
    main()