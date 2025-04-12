"""
Format a nginx.conf file
"""

import argparse

from . import directive, parse


def main():
    parser = argparse.ArgumentParser("nformat")
    parser.add_argument("file")
    parser.add_argument(
        "-i", "--indent", default=4, type=int, help="number of spaces to indent"
    )
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())
    print(directive.to_string(directives, indent=options.indent * " "))
