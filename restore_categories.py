import os
import re
import xml.etree.ElementTree as ET

XML_FILE = "export.xml"
CONTENT_DIR = "content"

def parse_xml_categories():
    """Parses the export.xml file and maps post titles/slugs to their categories."""
    # Handle standard WordPress XML namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/'
    }
    
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    except Exception as e:
        print(f"Error reading {XML_FILE}: {e}")
        return {}

    xml_data = {}
    
    # Iterate through every post item in the XML archive
    for item in root.findall('.//item'):
        title_node = item.find('title')
        slug_node = item.find('wp:post_name', namespaces)
        
        title = title_node.text.strip() if title_node is not None and title_node.text else ""
        slug = slug_node.text.strip() if slug_node is not None and slug_node.text else ""
        
        # Extract tags that match domain="category"
        categories = []
        for cat in item.findall('category'):
            if cat.attrib.get('domain') == 'category':
                categories.append(cat.text.strip())
        
        if categories:
            if title:
                xml_data[title.lower()] = categories
            if slug:
                xml_data[slug.lower()] = categories

    return xml_data

def update_markdown_front_matter(xml_categories):
    """Scans Hugo markdown files and injects categories matching the XML data."""
    updated_count = 0
    
    # Regex strings to navigate front matter
    title_regex = re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.MULTILINE)
    categories_regex = re.compile(r'^categories:\s*\n(\s*-\s*.*\n)*', re.MULTILINE)

    for root_dir, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root_dir, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()

                # Try matching by checking the file name slug
                file_slug = os.path.splitext(file)[0].lower()
                if file_slug == "index" or file_slug == "_index":
                    file_slug = os.path.basename(root_dir).lower()
                
                # Try matching by extracting the front matter title
                title_match = title_regex.search(file_content)
                fm_title = title_match.group(1).lower() if title_match else ""

                # Look for a match in our XML dictionary mapping
                matched_categories = xml_categories.get(file_slug) or xml_categories.get(fm_title)
                
                if matched_categories:
                    # Format the categories list block cleanly into YAML syntax
                    yaml_categories = "categories:\n" + "".join([f'  - "{cat}"\n' for cat in matched_categories])
                    
                    # Split the markdown file at front matter boundaries
                    parts = file_content.split('---', 2)
                    if len(parts) >= 3:
                        front_matter = parts[1]
                        
                        # Check if a categories parameter block already exists to avoid duplication
                        if "categories:" in front_matter:
                            front_matter = categories_regex.sub(yaml_categories, front_matter)
                        else:
                            # Append it cleanly right before the closing front matter lines
                            front_matter += yaml_categories
                        
                        # Reassemble the file components seamlessly
                        new_content = f"---{front_matter}---{parts[2]}"
                        
                        if new_content != file_content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            updated_count += 1

    print(f"\n[Execution Summary]\n -> Successfully scanned text assets and restored categories to {updated_count} files.")

if __name__ == "__main__":
    print("Beginning XML collection mapping...")
    categories_map = parse_xml_categories()
    if categories_map:
        print(f"Loaded {len(categories_map)} post configurations from XML indices. Syncing markdown entries...")
        update_markdown_front_matter(categories_map)