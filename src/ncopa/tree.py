#!/usr/bin/env python3
"""Display a tree to represent a config file"""

import argparse

from . import Directive, parse


def print_tree(directives: list[Directive], prefix=""):
    for index, directive in enumerate(directives):
        is_last = index == len(directives) - 1
        connector = "├── "
        if is_last:
            connector = "└── "

        print(f"{prefix}{connector}{directive.name}")

        if directive.children:
            print_tree(directive, prefix=prefix + ("    " if is_last else "│   "))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())

    print_tree(directives)


if __name__ == "__main__":
    main()
