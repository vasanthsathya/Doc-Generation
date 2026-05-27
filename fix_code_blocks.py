#!/usr/bin/env python3
"""
Fix RST code-block syntax to ensure proper indentation.
This script fixes the common issue where code-block content is not properly indented.
"""

import re
import os
import glob

def fix_code_blocks(content):
    """
    Fix code-block syntax in RST content.
    
    The issue is that code-block directives often look like:
    .. code-block:: shell
       cd /opt
       git clone ...
    
    But should be:
    .. code-block:: shell
    
       cd /opt
       git clone ...
    """
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line is a code-block directive
        code_block_match = re.match(r'^(\s*)\.\. code-block::\s+(\S+)', line)
        
        if code_block_match:
            indent = code_block_match.group(1)
            language = code_block_match.group(2)
            
            # Add the directive line
            fixed_lines.append(line)
            
            # Check if the next line exists and is not blank
            if i + 1 < len(lines) and lines[i + 1].strip():
                # Insert a blank line after the directive
                fixed_lines.append('')
            
            # Process the code content
            i += 1
            code_content = []
            
            # Collect all consecutive lines that look like code content
            while i < len(lines):
                next_line = lines[i]
                
                # Stop if we hit another directive or blank line followed by non-indented content
                if next_line.strip().startswith('..') and not next_line.strip().startswith('...'):
                    break
                
                # Stop if we hit a blank line followed by something that doesn't look like code
                if not next_line.strip() and i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(' '):
                    break
                
                # Stop if we hit a section header
                if re.match(r'^[=!\"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]{3,}$', next_line.strip()):
                    break
                
                # Collect the line if it's part of the code block
                if next_line.strip() or (i + 1 < len(lines) and lines[i + 1].strip()):
                    code_content.append(next_line)
                else:
                    break
                
                i += 1
            
            # Add the code content with proper indentation
            if code_content:
                # Ensure proper indentation (at least 3 spaces)
                for code_line in code_content:
                    if code_line.strip():  # Only indent non-empty lines
                        # If the line is already indented, preserve its relative indentation
                        if code_line.startswith(' '):
                            fixed_lines.append(code_line)
                        else:
                            # Add 3 spaces for indentation
                            fixed_lines.append('   ' + code_line)
                    else:
                        fixed_lines.append('')  # Preserve empty lines
            
            continue
        
        fixed_lines.append(line)
        i += 1
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single RST file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fixed_content = fix_code_blocks(content)
        
        if fixed_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {filepath}")
            return True
        else:
            print(f"No changes needed: {filepath}")
            return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Process all RST files in the source directory."""
    source_dir = 'docs/source'
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} not found")
        return
    
    # Find all RST files
    rst_files = glob.glob(os.path.join(source_dir, '**', '*.rst'), recursive=True)
    
    print(f"Found {len(rst_files)} RST files to process")
    
    fixed_count = 0
    for rst_file in rst_files:
        if process_file(rst_file):
            fixed_count += 1
    
    print(f"\nProcessed {len(rst_files)} files, fixed {fixed_count} files")

if __name__ == '__main__':
    main()