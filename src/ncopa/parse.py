#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import dataclasses
import shlex
from collections.abc import Sequence
from typing import List

TOK_COMMENT = "#"
TOK_TERMINATOR = ";"
TOK_OPEN = "{"
TOK_CLOSE = "}"


@dataclasses.dataclass()
class Directive(Sequence):
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: List[str] = dataclasses.field(default_factory=list)
    bottom_comment: str = dataclasses.field(default_factory=str)
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


def detect_comment(lex: shlex.shlex) -> bool:
    token = lex.get_token()
    detected = token == TOK_COMMENT
    lex.push_token(token)
    return detected


def parse_comment(lex: shlex.shlex) -> str:
    anchor = lex.lineno
    comment = []
    for token in lex:
        comment.append(token)
        if lex.lineno != anchor:
            # We pass EOL
            break
    return " ".join(comment)


def parse(text):
    """Parse text into a list of Directive objects."""
    tokens = shlex.shlex(text, posix=True, punctuation_chars=";")
    tokens.whitespace_split = True
    tokens.wordchars += ".:"
    tokens.commenters = ""

    directives = []
    stack = [directives]
    lst = []

    for token in tokens:
        if token == TOK_TERMINATOR:
            directive = Directive.from_list(lst)
            # BUG: detect_comment might scan to the next line. It should not do that.
            if detect_comment(tokens):
                directive.bottom_comment = parse_comment(tokens)
            stack[-1].append(directive)
            lst = []
        elif token == TOK_OPEN:
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            stack.append(directive.children)
            lst = []
        elif token == TOK_CLOSE:
            stack.pop()
        elif token == TOK_COMMENT:
            tokens.push_token(token)
            stack[-1].append(Directive(name="", bottom_comment=parse_comment(tokens)))
        else:
            lst.append(token)
    return directives
