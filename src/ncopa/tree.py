#!/usr/bin/env python3
"""Display a tree to represent a config file"""

import argparse
import importlib.metadata

from . import Directive, parse


def print_tree(directives: list[Directive], prefix: str = ""):
    # Skip Comments; must be done ahead so we can calculate the last directive
    # Do not combine it with the next for loop
    directives = [directive for directive in directives if directive.name != ""]

    for directive in directives:
        is_last = directive is directives[-1]
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{directive.name}")
        print_tree(directive, prefix=prefix + ("    " if is_last else "│   "))


def main():
    version = importlib.metadata.version("ncopa")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {version}"
    )
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())

    print_tree(directives)


if __name__ == "__main__":
    main()
