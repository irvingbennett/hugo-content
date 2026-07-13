import os
import re
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

# --- CONFIGURATION PATHS ---
XML_EXPORT_PATH = "export.xml"  # Replace with the actual filename/path of your .xml file
CONTENT_DIR = "content"

# Regex pattern to capture: [link id='1002' text="Zentel"] or [link id="1002" text='Zentel']
SHORTCODE_PATTERN = re.compile(r'\[link\s+id=[\'"](\d+)[\'"]\s+text=[\'"]([^\'"]+)[\'"]\]')

def parse_wordpress_xml(xml_path):
    """Parses the WordPress XML export to build an ID-to-RelativeURL map."""
    print(f"[+] Parsing WordPress XML export: {xml_path}...")
    if not os.path.exists(xml_path):
        print(f"[-] Error: XML file '{xml_path}' not found.")
        return {}

    id_to_url = {}
    
    # WordPress XML uses namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/'
    }
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Loop through all items (posts, pages, attachments)
        for item in root.findall('.//item'):
            post_id = item.find('wp:post_id', namespaces)
            link = item.find('link')
            
            if post_id is not None and link is not None and link.text:
                pid = post_id.text
                # Extract the relative path from the full absolute URL
                parsed_url = urlparse(link.text)
                relative_path = parsed_url.path
                
                # Ensure it has trailing and leading slashes clean
                if relative_path and not relative_path.endswith('/'):
                    relative_path += '/'
                
                id_to_url[pid] = relative_path
                
        print(f"[+] Successfully mapped {len(id_to_url)} IDs from XML.")
        return id_to_url
    except Exception as e:
        print(f"[-] Error parsing XML: {e}")
        return {}

def heal_markdown_links(id_to_url):
    """Scans markdown files and replaces the shortcodes with valid markdown links."""
    print(f"[+] Scanning markdown files inside: {CONTENT_DIR}...")
    
    total_fixed = 0
    files_modified = 0
    unresolved_ids = set()

    for root, _, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(('.md', '.html')):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                matches = SHORTCODE_PATTERN.findall(content)
                if not matches:
                    continue
                
                new_content = content
                file_was_modified = False
                
                for post_id, text in matches:
                    # Look up the ID in our XML map
                    if post_id in id_to_url:
                        relative_link = id_to_url[post_id]
                        markdown_link = f"[{text}]({relative_link})"
                        
                        # Rebuild the original string to replace it precisely
                        # Handles variation in single vs double quotes dynamically
                        old_string_pattern = re.compile(rf'\[link\s+id=[\'"]{post_id}[\'"]\s+text=[\'"]{re.escape(text)}[\'"]\]')
                        new_content = old_string_pattern.sub(markdown_link, new_content)
                        
                        total_fixed += 1
                        file_was_modified = True
                    else:
                        unresolved_ids.add(post_id)
                
                if file_was_modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_modified += 1

    print(f"\n[Summary]")
    print(f" -> Files Modified: {files_modified}")
    print(f" -> Broken Shortcodes Fixed: {total_fixed}")
    if unresolved_ids:
        print(f" -> Warning: {len(unresolved_ids)} IDs were not found in the XML map: {sorted(list(unresolved_ids))}")

if __name__ == "__main__":
    # If your XML filename is different, update it here
    id_map = parse_wordpress_xml(XML_EXPORT_PATH)
    if id_map:
        heal_markdown_links(id_map)