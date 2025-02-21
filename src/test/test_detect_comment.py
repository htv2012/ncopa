"""Verify detect_comment"""

import shlex

import pytest

from ncopa import detect_comment

# @pytest.fixture(
#     params=[
#         pytest.params(" \n# my comment", False, id="comment on next line"),
#         pytest.params(" # my comment", False, id="comment on same line"),
#     ]
# )
# def lex():
#     text, expected =
#     lexer = shlex.shlex(" \n# my comment", posix=True, punctuation_chars=";")
#     lexer.commenters = ""
#     lexer.whitespace = " \t"
#     return lexer


# @pytest.fixture
# def lex_with_comment():
#     lexer = shlex.shlex(" # my comment", posix=True, punctuation_chars=";")
#     lexer.commenters = ""
#     lexer.whitespace = " \t"
#     return lexer


@pytest.mark.parametrize(
    "text,expected",
    [
        pytest.param(" \n# my comment", False, id="comment on next line"),
        pytest.param(" # my comment", True, id="comment on same line"),
    ],
)
def test_detect_comment(text, expected):
    lex = shlex.shlex(text, posix=True, punctuation_chars=";")
    lex.commenters = ""
    lex.whitespace = " \t"

    assert detect_comment(lex) is expected


# def test_detect_expect_true(lex_with_comment):
#     assert detect_comment(lex_with_comment) is True
