"""
Format a nginx.conf file
"""

import argparse
import pathlib

from . import directive, parse
from .version import version_parser


def create_backup(file: pathlib.Path):
    content = file.read_bytes()
    bak = file.with_suffix(".bak")
    bak.write_bytes(content)


def main():
    parser = argparse.ArgumentParser(parents=[version_parser])
    parser.add_argument("file", type=pathlib.Path)
    parser.add_argument(
        "-I",
        "--indent",
        default=4,
        type=int,
        metavar="NUM_SPACES",
        help="number of spaces to indent",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        default=False,
        help="Modify file in place",
    )
    group.add_argument(
        "-o", "--output", type=pathlib.Path, metavar="FILE", help="Output to a file"
    )
    options = parser.parse_args()

    if not options.file.exists():
        raise SystemExit(f"File {options.file} does not exist")

    directives = parse(options.file.read_text())
    formatted = directive.to_string(directives, indent=options.indent * " ")

    if options.inplace:
        create_backup(options.file)
        options.file.write_text(formatted)
    elif options.output:
        if options.output.exists():
            create_backup(options.output)
        options.output.write_text(formatted)
    else:
        print(formatted)
