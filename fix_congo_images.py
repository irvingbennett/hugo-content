import os

CONTENT_DIR = "content"

def flatten_cover_images():
    modified_files = 0

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                new_lines = []
                skip_counter = 0
                has_changed = False

                for i, line in enumerate(lines):
                    if skip_counter > 0:
                        skip_counter -= 1
                        continue

                    # Target the root-level "cover:" block
                    if line.strip() == "cover:":
                        try:
                            next_line_1 = lines[i+1] if i+1 < len(lines) else ""
                            next_line_2 = lines[i+2] if i+2 < len(lines) else ""
                            
                            # Case A: alt comes first, then image
                            if "alt:" in next_line_1 and "image:" in next_line_2:
                                img_path = next_line_2.split("image:")[-1].strip().strip('"').strip("'")
                                new_lines.append(f'cover: "{img_path}"\n')
                                skip_counter = 2
                                has_changed = True
                                continue
                                
                            # Case B: image comes first, then alt
                            elif "image:" in next_line_1 and "alt:" in next_line_2:
                                img_path = next_line_1.split("image:")[-1].strip().strip('"').strip("'")
                                new_lines.append(f'cover: "{img_path}"\n')
                                skip_counter = 2
                                has_changed = True
                                continue
                        except IndexError:
                            pass

                    new_lines.append(line)

                if has_changed:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    modified_files += 1

    print(f"[Execution Summary]\n -> Successfully updated {modified_files} markdown files for Congo compliance.")

if __name__ == "__main__":
    flatten_cover_images()