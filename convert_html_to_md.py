import os
import html2text
from pathlib import Path

def convert_html_to_markdown(html_file_path, md_file_path):
    """Convert a single HTML file to Markdown."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Configure html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Don't wrap lines
        h.unicode_snob = True
        h.skip_internal_links = False
        
        # Convert to markdown
        markdown_content = h.handle(html_content)
        
        # Write markdown file
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Converted: {html_file_path} -> {md_file_path}")
        return True
    except Exception as e:
        print(f"Error converting {html_file_path}: {e}")
        return False

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\Dell_Omnia_Docs_v2.1")
    
    # Counters
    converted = 0
    skipped = 0
    errors = 0
    
    # Walk through the directory
    for html_file in source_dir.rglob("*.html"):
        # Skip 404.html and sitemap files
        if html_file.name in ['404.html', 'sitemap.xml', 'sitemap.xml.gz']:
            skipped += 1
            continue
        
        # Create corresponding markdown file path
        md_file = html_file.with_suffix('.md')
        
        # Convert
        if convert_html_to_markdown(html_file, md_file):
            converted += 1
        else:
            errors += 1
    
    print(f"\nConversion complete:")
    print(f"  Converted: {converted}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
