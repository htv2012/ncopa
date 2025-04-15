import argparse
import importlib.metadata

__all__ = ["version_parser"]

version = "%(prog)s " + importlib.metadata.version("ncopa")
version_parser = argparse.ArgumentParser(add_help=False)
version_parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=version,
    help="Show version",
)
