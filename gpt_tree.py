import os

def print_tree(start_path, prefix=""):
    """Recursively prints a directory tree structure similar to the `tree` command."""
    items = sorted(os.listdir(start_path))  # Sort for consistent output
    total_items = len(items)

    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = index == total_items - 1

        # Print with tree formatting
        connector = "└── " if is_last else "├── "
        print(prefix + connector + item)

        # Recurse if directory
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(path, new_prefix)

# Usage: Provide a directory path
print_tree("src")  # Replace "." with your target directory
