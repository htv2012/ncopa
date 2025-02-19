#!/usr/bin/env python3
"""Display a tree to represent a config file"""

import argparse

from . import depth_first_traversal, parse


def visit(directive, parents):
    print("  " * len(parents), end="- ")
    print(directive.name, " ".join(directive.args))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())

    for directive in directives:
        depth_first_traversal(directive, visit=visit)


if __name__ == "__main__":
    main()
