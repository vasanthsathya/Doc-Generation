import os
import re
from pathlib import Path

def clean_markdown_file(md_file_path):
    """Clean a markdown file by removing navigation elements and HTML artifacts."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove navigation links at the top
        content = re.sub(r'\[ Skip to content \].*?\n', '', content)
        
        # Remove empty bracket links
        content = re.sub(r'\[ \]\(javascript:void\([^)]*\) "[^"]*"\)', '', content)
        
        # Remove duplicate headers and navigation sections
        content = re.sub(r'\[ !\[logo\].*?\]\(index\.html "Dell Omnia"\)', '', content, flags=re.MULTILINE)
        
        # Remove "Initializing search" text
        content = re.sub(r'Initializing search\s*', '', content)
        
        # Remove empty lines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove HTML-style links that are just navigation
        content = re.sub(r'\[ dell/omnia\s*\]\(https://github\.com/dell/omnia[^)]*\)', '', content)
        
        # Clean up excessive whitespace
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Remove lines that are just navigation menus
        lines = content.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            # Skip navigation menu lines
            if re.match(r'^\s*\*\s+\[.*?\]\(.*?\)\s*$', line) and i > 0:
                # Check if previous line was also a menu item
                if i > 0 and re.match(r'^\s*\*\s+\[.*?\]\(.*?\)\s*$', lines[i-1]):
                    continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Write cleaned content
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Cleaned: {md_file_path}")
        return True
    except Exception as e:
        print(f"Error cleaning {md_file_path}: {e}")
        return False

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\Dell_Omnia_Docs_v2.1")
    
    cleaned = 0
    errors = 0
    
    for md_file in source_dir.rglob("*.md"):
        if clean_markdown_file(md_file):
            cleaned += 1
        else:
            errors += 1
    
    print(f"\nCleaning complete:")
    print(f"  Cleaned: {cleaned}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
