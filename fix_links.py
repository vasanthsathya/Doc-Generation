import os
import re
from pathlib import Path

def fix_markdown_links(md_file_path):
    """Fix HTML links in markdown files to point to .md files."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace .html links with .md links
        content = re.sub(r'\.html', '.md', content)
        
        # Write fixed content
        if content != original_content:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed links in: {md_file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error fixing links in {md_file_path}: {e}")
        return False

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\docs\source")
    
    fixed = 0
    skipped = 0
    errors = 0
    
    for md_file in source_dir.rglob("*.md"):
        if fix_markdown_links(md_file):
            fixed += 1
        else:
            skipped += 1
    
    print(f"\nLink fixing complete:")
    print(f"  Fixed: {fixed}")
    print(f"  Skipped (no changes): {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
