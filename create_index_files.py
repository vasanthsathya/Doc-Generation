import os
from pathlib import Path

def create_index_md(dir_path):
    """Create an index.md file in a directory with links to all .md files."""
    md_files = list(dir_path.glob("*.md"))
    
    if not md_files:
        print(f"No .md files in {dir_path}")
        return False
    
    # Skip if index.md already exists
    if (dir_path / "index.md").exists():
        print(f"index.md already exists in {dir_path}")
        return False
    
    # Create index content
    dir_name = dir_path.name.replace("_", " ").title()
    content = f"# {dir_name}\n\n"
    
    for md_file in sorted(md_files):
        if md_file.name == "index.md":
            continue
        # Create a nice title from filename
        title = md_file.stem.replace("_", " ").replace("-", " ").title()
        content += f"- [{title}]({md_file.name})\n"
    
    index_path = dir_path / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created index.md in {dir_path}")
    return True

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\docs\source")
    
    created = 0
    skipped = 0
    
    # Process HowTo subdirectories
    howto_dir = source_dir / "HowTo"
    if howto_dir.exists():
        for subdir in howto_dir.iterdir():
            if subdir.is_dir():
                if create_index_md(subdir):
                    created += 1
                else:
                    skipped += 1
    
    # Process Reference subdirectories
    ref_dir = source_dir / "Reference"
    if ref_dir.exists():
        for subdir in ref_dir.iterdir():
            if subdir.is_dir():
                if create_index_md(subdir):
                    created += 1
                else:
                    skipped += 1
    
    print(f"\nIndex file creation complete:")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")

if __name__ == "__main__":
    main()
