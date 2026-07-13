import os
from pathlib import Path
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
WORDPRESS_XML_FILE = Path("/home/irving/hugo-content/alairelibre.WordPress.2026-06-22.xml")
OUTPUT_TABLES_DIR = Path("/home/irving/hugo-content/extracted_tables")

NAMESPACES = {
    'wp': 'http://wordpress.org/export/1.2/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'dc': 'http://purl.org/dc/elements/1.1/'
}

def clean_slug(url_or_slug):
    if not url_or_slug:
        return "untitled_page"
    slug = url_or_slug.strip().split('/')[-1] if '/' in url_or_slug else url_or_slug
    return slug.strip() if slug.strip() else "untitled_page"

def html_table_to_markdown(table_tag):
    markdown_rows = []
    rows = table_tag.find_all("tr")
    for i, row in enumerate(rows):
        cells = row.find_all(["td", "th"])
        cell_texts = [cell.get_text().strip().replace("\n", " ").replace("|", "\\|") for cell in cells]
        if not cell_texts:
            continue
        markdown_rows.append("| " + " | ".join(cell_texts) + " |")
        if i == 0:
            markdown_rows.append("| " + " | ".join(["---"] * len(cell_texts)) + " |")
    return "\n" + "\n".join(markdown_rows) + "\n"

def parse_page_tables():
    if not WORDPRESS_XML_FILE.exists():
        print(f"❌ Error: Cannot find your WordPress XML file at {WORDPRESS_XML_FILE}")
        return

    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    tables_found = 0

    print(f"📄 Hunting exclusively for static PAGES in: {WORDPRESS_XML_FILE}...")
    
    tree = ET.parse(WORDPRESS_XML_FILE)
    root = tree.getroot()

    for item in root.findall(".//item"):
        title_node = item.find("title")
        link_node = item.find("link")
        content_node = item.find("content:encoded", NAMESPACES)
        post_type_node = item.find("wp:post_type", NAMESPACES)
        
        # 🚨 STRICLY TARGET PAGES ONLY
        if post_type_node is not None and post_type_node.text == 'page':
            title = title_node.text if title_node is not None else "Untitled Page"
            slug = clean_slug(link_node.text if link_node is not None else title)
            
            if content_node is not None and content_node.text:
                html_body = content_node.text
                
                if "<table" in html_body:
                    soup = BeautifulSoup(html_body, "html.parser")
                    tables = soup.find_all("table")
                    
                    if tables:
                        # Append '_page_tables.md' so they are easy to tell apart from blog posts
                        file_output_path = OUTPUT_TABLES_DIR / f"page_{slug}_tables.md"
                        with open(file_output_path, "w", encoding="utf-8") as out_f:
                            out_f.write(f"---\ntitle: \"STATIC PAGE TABLES: {title}\"\npage_slug_match: \"{slug}\"\n---\n\n")
                            
                            for idx, table in enumerate(tables):
                                md_table = html_table_to_markdown(table)
                                out_f.write(f"### Table #{idx + 1}\n")
                                out_f.write(md_table)
                                out_f.write("\n\n")
                                
                        print(f"   ✓ Extracted {len(tables)} table(s) from static page: {slug}")
                        tables_found += 1

    print(f"\n🏁 Finished! Added {tables_found} static page table structures to your index folder.")

if __name__ == "__main__":
    parse_page_tables()