"""
Format a nginx.conf file
"""

import argparse

from . import directive, parse


def main():
    parser = argparse.ArgumentParser("nformat")
    parser.add_argument("file")
    parser.add_argument(
        "-I",
        "--indent",
        default=4,
        type=int,
        metavar="N",
        help="number of spaces to indent",
    )
    parser.add_argument("-i", "--inplace", help="Modify file in place")
    parser.add_argument("-o", "--output", metavar="FILE", help="Output to file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())
    print(directive.to_string(directives, indent=options.indent * " "))
