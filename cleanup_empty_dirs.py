import os
from pathlib import Path

def remove_empty_dirs(source_dir):
    """Remove empty directories."""
    removed = 0
    for dirpath, dirnames, filenames in os.walk(source_dir, topdown=False):
        for dirname in dirnames:
            dir_path = Path(dirpath) / dirname
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"Removed empty directory: {dir_path}")
                removed += 1
    return removed

def main():
    source_dir = Path(r"c:\Working Folder\Autogeneration\Omnia_new_template\Doc-Generation\docs\source")
    removed = remove_empty_dirs(source_dir)
    print(f"\nRemoved {removed} empty directories")

if __name__ == "__main__":
    main()
