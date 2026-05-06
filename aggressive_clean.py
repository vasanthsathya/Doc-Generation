import os
import re
from pathlib import Path

def aggressive_clean_markdown(md_file_path):
    """Aggressively clean markdown files by removing all navigation and HTML artifacts."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        lines = content.split('\n')
        cleaned_lines = []
        in_content = False
        content_started = False
        
        for line in lines:
            # Skip until we find the first markdown heading (#)
            if not content_started:
                if re.match(r'^#+\s', line):
                    content_started = True
                    in_content = True
                    cleaned_lines.append(line)
                # Skip everything before first heading
                continue
            
            # Once we're in content, skip navigation patterns
            if in_content:
                # Skip lines that look like navigation sections
                if re.match(r'^[A-Z][a-z]+\s*$', line) and len(line) < 30:
                    # Check if next lines are bullet points with links
                    continue
                # Skip duplicate entries like "Setup Setup"
                if re.match(r'^\*\s+(\w+)\s+\1\s*$', line):
                    continue
                # Skip standalone bullet points without meaningful content
                if re.match(r'^\*\s+[A-Z][a-z]+\s+[A-Z][a-z]+\s*$', line):
                    continue
                # Skip "Table of contents" header
                if re.match(r'^Table of contents\s*$', line):
                    continue
                # Skip empty lines after table of contents
                if line.strip() == '' and 'Table of contents' in '\n'.join(cleaned_lines[-3:]):
                    continue
                # Skip lines that are just section names without content
                if re.match(r'^[A-Z][a-z]+\s*$', line) and not re.match(r'^#+', line):
                    # Check if this is a real section header or navigation
                    if cleaned_lines and not re.match(r'^#+', cleaned_lines[-1]):
                        continue
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove empty lines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Remove lines that are just whitespace
        content = re.sub(r'^\s+$', '', content, flags=re.MULTILINE)
        
        # Clean up excessive whitespace at start and end
        content = content.strip()
        
        # Write cleaned content
        if content != original_content:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Aggressively cleaned: {md_file_path}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error aggressively cleaning {md_file_path}: {e}")
        return False

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\docs\source")
    
    cleaned = 0
    skipped = 0
    errors = 0
    
    for md_file in source_dir.rglob("*.md"):
        if aggressive_clean_markdown(md_file):
            cleaned += 1
        else:
            skipped += 1
    
    print(f"\nAggressive cleaning complete:")
    print(f"  Cleaned: {cleaned}")
    print(f"  Skipped (no changes): {skipped}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
