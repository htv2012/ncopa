"""
Format a nginx.conf file
"""

import argparse

from . import parse


def main():
    parser = argparse.ArgumentParser("nformat")
    parser.add_argument("file")
    options = parser.parse_args()

    with open(options.file) as stream:
        directives = parse(stream.read())
    assert directives is not None
