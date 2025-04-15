#!/usr/bin/env python3
"""
Parse nginx.conf content
"""

import shlex

from .directive import Directive

TOK_COMMENT = "#"
TOK_TERMINATOR = ";"
TOK_OPEN = "{"
TOK_CLOSE = "}"
TOK_CR = "\r"
TOK_LF = "\n"


def comment_ahead(lex: shlex.shlex) -> bool:
    token = lex.get_token()
    lex.push_token(token)
    return token == TOK_COMMENT


def parse_comment(lex: shlex.shlex) -> str:
    comment = lex.instream.readline().rstrip(f"{TOK_CR}{TOK_LF}")
    return f"{TOK_COMMENT}{comment}"


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
                next(lex)  # Discard the comment token
                directive.bottom_comment = parse_comment(lex)
            stack[-1].append(directive)
            lst = []
        elif token == TOK_OPEN:
            directive = Directive.from_list(lst)
            stack[-1].append(directive)
            if comment_ahead(lex):
                next(lex)  # Discard the comment token
                directive.top_comment = parse_comment(lex)
            stack.append(directive.children)
            lst = []
        elif token == TOK_CLOSE:
            stack.pop()
            if comment_ahead(lex):
                next(lex)  # Discard the comment token
                stack[-1][-1].bottom_comment = parse_comment(lex)
        elif token == TOK_COMMENT:
            stack[-1].append(Directive(name="", bottom_comment=parse_comment(lex)))
        elif token == TOK_CR or token == TOK_LF:
            # CR and LF are meaningful only when parsing comments
            pass
        else:
            lst.append(token)
    return directives
