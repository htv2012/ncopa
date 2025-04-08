#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import dataclasses
import shlex
from collections.abc import Sequence
from itertools import takewhile

TOK_COMMENT = "#"
TOK_TERMINATOR = ";"
TOK_OPEN = "{"
TOK_CLOSE = "}"
TOK_CR = "\r"
TOK_LF = "\n"


@dataclasses.dataclass()
class Directive(Sequence):
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: list[str] = dataclasses.field(default_factory=list)
    top_comment: str = dataclasses.field(default_factory=str)
    bottom_comment: str = dataclasses.field(default_factory=str)
    children: list = dataclasses.field(default_factory=list, repr=False)

    @classmethod
    def from_list(cls, lst):
        return cls(lst[0], lst[1:])

    def __iter__(self):
        return iter(self.children)

    def __len__(self):
        return len(self.children)

    def __getitem__(self, index: int):
        return self.children[index]


def comment_ahead(lex: shlex.shlex) -> bool:
    token = lex.get_token()
    lex.push_token(token)
    return token == TOK_COMMENT


def parse_comment(lex: shlex.shlex) -> str:
    def not_eol(token: str) -> bool:
        """Return true if token is not a CR or LF character"""
        return not (token == TOK_CR or token == TOK_LF)

    return " ".join(takewhile(not_eol, lex))


def parse(text):
    """Parse text into a list of Directive objects."""
    lex = shlex.shlex(text, posix=True, punctuation_chars=";")
    lex.wordchars += ".:"
    lex.whitespace = " \t"
    lex.commenters = ""

    directives = []
    stack = [directives]
    lst = []

    for token in lex:
        if token == TOK_TERMINATOR:
            directive = Directive.from_list(lst)
            if comment_ahead(lex):
                directive.bottom_comment = parse_comment(lex)
            stack[-1].append(directive)
            lst = []
        elif token == TOK_OPEN:
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            if comment_ahead(lex):
                directive.top_comment = parse_comment(lex)
            stack.append(directive.children)
            lst = []
        elif token == TOK_CLOSE:
            stack.pop()
            if comment_ahead(lex):
                stack[-1][-1].bottom_comment = parse_comment(lex)
        elif token == TOK_COMMENT:
            lex.push_token(token)
            stack[-1].append(Directive(name="", bottom_comment=parse_comment(lex)))
        elif token == TOK_CR or token == TOK_LF:
            # CR and LF are meaningful only when parsing comments
            pass
        else:
            lst.append(token)
    return directives
