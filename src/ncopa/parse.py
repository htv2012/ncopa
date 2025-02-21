#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import dataclasses
import shlex
from collections.abc import Sequence
from typing import List


@dataclasses.dataclass()
class Directive(Sequence):
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: List[str] = dataclasses.field(default_factory=list)
    children: List = dataclasses.field(default_factory=list, repr=False)

    @classmethod
    def from_list(cls, lst):
        return cls(lst[0], lst[1:])

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index: int):
        return self.children[index]


def add_semicolons_to_comments(text: str):
    """Add semicolons to comment lines"""
    # FIX: Does not work for inline comment
    return "\n".join(
        f"{line};" if line.strip().startswith("#") else line
        for line in text.splitlines()
    )


def parse(text):
    """Parse text into a list of Directive objects."""
    tokens = shlex.shlex(
        add_semicolons_to_comments(text), posix=True, punctuation_chars=";"
    )
    tokens.whitespace_split = True
    tokens.wordchars += ".:"
    tokens.commenters = ""

    directives = []
    stack = [directives]
    lst = []

    for token in tokens:
        if token == ";":
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            lst = []
        elif token == "{":
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            stack.append(directive.children)
            lst = []
        elif token == "}":
            stack.pop()
        else:
            lst.append(token)
    return directives
