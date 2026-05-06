import os
import re
from pathlib import Path

def deep_clean_markdown(md_file_path):
    """Deep clean markdown files by removing all HTML artifacts and navigation elements."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove anchor links with [¶]
        content = re.sub(r'\[¶\]\([^)]+\s+"[^"]*"\)', '', content)
        
        # Remove navigation breadcrumbs (lines with just links like [ Home ](../index.html))
        content = re.sub(r'^\s*\d+\.\s+\[.*?\]\([^)]+\)\s*$', '', content, flags=re.MULTILINE)
        
        # Remove "Table of contents" header and its list
        content = re.sub(r'Table of contents\s*\n-+\s*\n', '', content)
        
        # Remove navigation sections (lines starting with * and containing links)
        lines = content.split('\n')
        cleaned_lines = []
        in_toc = False
        
        for line in lines:
            # Skip lines that look like navigation menu items
            if re.match(r'^\s*\*\s+\[.*?\]\([^)]+\)\s*$', line):
                # Check if this is part of a TOC section
                if 'Table of contents' in '\n'.join(cleaned_lines[-5:]):
                    in_toc = True
                    continue
                # Skip standalone navigation links
                if not in_toc:
                    continue
            # End TOC when we hit a non-list item
            if in_toc and not re.match(r'^\s*\*\s+', line) and line.strip():
                in_toc = False
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove empty lines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove lines that are just whitespace
        content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)
        
        # Remove navigation section headers like "Troubleshooting", "Contributing" when they appear as standalone
        content = re.sub(r'\n\n[A-Z][a-z]+\s*\n\n', '\n\n', content)
        
        # Remove breadcrumb-style navigation at the top
        content = re.sub(r'^.*?\[.*?\]\([^)]+\).*?\n', '', content, flags=re.MULTILINE)
        
        # Clean up excessive whitespace at start and end
        content = content.strip()
        
        # Write cleaned content
        if content != original_content:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Deep cleaned: {md_file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deep cleaning {md_file_path}: {e}")
        return False

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\docs\source")
    
    cleaned = 0
    skipped = 0
    errors = 0
    
    for md_file in source_dir.rglob("*.md"):
        if deep_clean_markdown(md_file):
            cleaned += 1
        else:
            skipped += 1
    
    print(f"\nDeep cleaning complete:")
    print(f"  Cleaned: {cleaned}")
    print(f"  Skipped (no changes): {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
