"""
Verify that comments were correctly parsed
"""

import pytest

from ncopa import parse

TEXT = """
# File: simple.conf
user nginx; # Default use which iteracts with the system
worker_processes auto;
http { # top comment
    # default type
	default_type application/octet-stream;
}  # bottom comment
""".strip()


STANDALONE_COMMENT = 0
USER = 1
WORKER_PROCESS = 2
HTTP = 3
NESTED_COMMENT = 0


@pytest.fixture(scope="module")
def directives():
    return parse(TEXT)


def test_count(directives):
    assert len(directives) == 4


def test_simple_standalone_comment():
    comment = "# This is  simple"
    directives = parse(comment)
    assert len(directives) == 1
    directive = directives[0]
    assert directive.is_comment()
    assert directive.name == ""
    assert directive.top_comment == ""
    assert directive.bottom_comment == comment


def test_strip_crlf():
    comment = "# Hello  world \r\n"
    directives = parse(comment)
    assert len(directives) == 1
    directive = directives[0]
    assert directive.is_comment()
    assert directive.name == ""
    assert directive.top_comment == ""
    assert directive.bottom_comment == "# Hello  world "


def test_top_bottom():
    text = "http { # Top  comment\n} # Bottom  comment"
    directives = parse(text)
    assert len(directives) == 1
    directive = directives[0]
    assert directive.name == "http"
    assert directive.has_top_comment()
    assert directive.has_bottom_comment()


def test_standalone_comment(directives):
    assert directives[STANDALONE_COMMENT].name == ""
    assert directives[STANDALONE_COMMENT].args == []
    assert directives[STANDALONE_COMMENT].bottom_comment == "# File: simple.conf"


def test_comment_at_eol(directives):
    assert directives[USER].name == "user"
    assert directives[USER].args == ["nginx"]
    assert (
        directives[USER].bottom_comment
        == "# Default use which iteracts with the system"
    )


def test_nested_comment(directives):
    assert directives[HTTP][NESTED_COMMENT].name == ""
    assert directives[HTTP][NESTED_COMMENT].args == []
    assert directives[HTTP][NESTED_COMMENT].bottom_comment == "# default type"


def test_top_comment(directives):
    assert directives[HTTP].top_comment == "# top comment"


def test_bottom_comment(directives):
    assert directives[HTTP].bottom_comment == "# bottom comment"
