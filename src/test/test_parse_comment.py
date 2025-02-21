import shlex

import pytest

from ncopa import parse_comment


@pytest.fixture
def lex():
    lex_obj = shlex.shlex("# comment 1\n# comment 2", posix=True, punctuation_chars=";")
    lex_obj.commenters = ""
    lex_obj.whitespace = " \t"
    return lex_obj


def test_parse_to_eol(lex):
    assert parse_comment(lex) == "# comment 1"
    assert lex.get_token() == "#"
    assert parse_comment(lex) == "comment 2"
