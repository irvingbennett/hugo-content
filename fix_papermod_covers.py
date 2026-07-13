import os

CONTENT_DIR = "content"

def structure_papermod_covers():
    modified_files = 0

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                new_lines = []
                has_changed = False

                for line in lines:
                    # Catch the flat cover line we made for Congo
                    if line.startswith("cover:") and not line.strip() == "cover:":
                        parts = line.split("cover:")
                        img_path = parts[1].strip().strip('"').strip("'")
                        
                        # Only convert if it looks like a valid image asset path
                        if img_path.startswith("/") or img_path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.JPG')):
                            new_lines.append("cover:\n")
                            new_lines.append(f'  image: "{img_path}"\n')
                            has_changed = True
                            continue
                    
                    new_lines.append(line)

                if has_changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    modified_files += 1

    print(f"\n[Execution Summary]\n -> Successfully adapted {modified_files} files for PaperMod's cover object layout.")

if __name__ == "__main__":
    structure_papermod_covers()