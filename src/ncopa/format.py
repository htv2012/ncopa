"""
Format a nginx.conf file
"""

import argparse

from . import directive, parse


def main():
    parser = argparse.ArgumentParser("nformat")
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())
    print(directive.to_string(directives))
