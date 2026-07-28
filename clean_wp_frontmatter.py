import os
import frontmatter

# Define the directory containing your Markdown posts
POSTS_DIR = "./content/posts"

# WordPress frontmatter keys to remove
KEYS_TO_REMOVE = [
    "_edit_last",
    "_jetpack_related_posts_cache",
    "_publicize_twitter_user",
    "_thumbnail_id",
    "_wpas_done_all",
    "_wpcom_is_markdown",
    "guid"
]

def process_file(file_path):
    post = frontmatter.load(file_path)
    modified = False

    # 1. Remove unwanted WordPress metadata
    for key in KEYS_TO_REMOVE:
        if key in post.metadata:
            del post.metadata[key]
            modified = True

    # 2. Extract slug from url if url exists
    if "url" in post.metadata:
        raw_url = post.metadata["url"]
        
        if raw_url:
            # Strip trailing/leading slashes and extract the last segment
            slug = raw_url.strip("/").split("/")[-1]
            post.metadata["slug"] = slug
        
        # Remove the full url field
        del post.metadata["url"]
        modified = True

    # 3. Save modified file back using text mode ("w") with utf-8 encoding
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            frontmatter.dump(post, f)
        print(f"Cleaned: {file_path}")

def main():
    if not os.path.exists(POSTS_DIR):
        print(f"Directory '{POSTS_DIR}' not found. Please update the POSTS_DIR variable.")
        return

    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".md") or file.endswith(".markdown"):
                full_path = os.path.join(root, file)
                process_file(full_path)

if __name__ == "__main__":
    main()