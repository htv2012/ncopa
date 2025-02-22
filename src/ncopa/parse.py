#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import dataclasses
import enum
import shlex
from collections.abc import Sequence
from typing import List

TOK_COMMENT = "#"
TOK_TERMINATOR = ";"
TOK_OPEN = "{"
TOK_CLOSE = "}"
TOK_CR = "\r"
TOK_LF = "\n"


class CommentType(enum.Enum):
    STANDALONE = enum.auto()
    TOP = enum.auto()
    BOTTOM = enum.auto()


@dataclasses.dataclass()
class Directive(Sequence):
    """A nginx.conf directive, which could contain nested directives."""

    name: str
    args: List[str] = dataclasses.field(default_factory=list)
    top_comment: str = dataclasses.field(default_factory=str)
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


def peek(lex: shlex.shlex) -> str:
    token = lex.get_token()
    lex.push_token(token)
    return token


def parse(text):
    """Parse text into a list of Directive objects."""
    lex = shlex.shlex(text + "\n", posix=True, punctuation_chars=";")
    lex.wordchars += ".:"
    lex.whitespace = " \t"
    lex.commenters = ""

    directives = []
    stack = [directives]
    lst = []
    comment_type: CommentType = CommentType.STANDALONE

    for token in lex:
        if token == TOK_TERMINATOR:
            directive = Directive.from_list(lst)
            if peek(lex) == TOK_COMMENT:
                comment_type = CommentType.BOTTOM
            stack[-1].append(directive)
            lst = []
        elif token == TOK_OPEN:
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            if peek(lex) == TOK_COMMENT:
                comment_type = CommentType.TOP
            stack.append(directive.children)
            lst = []
        elif token == TOK_CLOSE:
            stack.pop()
            if peek(lex) == TOK_COMMENT:
                comment_type = CommentType.BOTTOM
        elif token == TOK_LF or token == TOK_LF:
            # CR and LF only are meaningful when parsing comments
            if not (lst and lst[0] == TOK_COMMENT):
                continue

            comment = " ".join(lst)
            if comment_type == CommentType.STANDALONE:
                directive = Directive(name="", bottom_comment=comment)
                stack[-1].append(directive)
            elif comment_type == CommentType.TOP:
                stack[-2][-1].top_comment = comment
            elif comment_type == CommentType.BOTTOM:
                stack[-1][-1].bottom_comment = comment

            # Reset
            comment_type = CommentType.STANDALONE
            lst = []
        else:
            lst.append(token)
    return directives
