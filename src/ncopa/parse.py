#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import dataclasses
import shlex
from typing import List


@dataclasses.dataclass()
class Directive:
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: List[str] = dataclasses.field(default_factory=list)
    children: List = dataclasses.field(default_factory=list, repr=False)

    @classmethod
    def from_list(cls, lst):
        """
        Given a list, construct a directive.

        >>> Directive.from_list(["location", "/hello"])
        Directive(name='location', args=['/hello'])
        """
        lst = lst.copy()
        name = lst.pop(0)
        return cls(name, lst)

    def __iter__(self):
        return iter(self.children)


def parse(text):
    """Parse text into a list of Directive objects."""
    tokens = shlex.shlex(text, posix=True, punctuation_chars=";")
    tokens.whitespace_split = True
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
