"""
Verify that comments were correctly parsed
"""

import pytest

from ncopa import parse

TEXT = """
# File: simple.conf
user nginx; # Default use which iteracts with the system
worker_processes auto;
http {
    # default type
	default_type application/octet-stream;
}
""".strip()


@pytest.fixture(scope="module")
def directives():
    return parse(TEXT)


def test_count(directives):
    assert len(directives) == 4


def test_standalone_comment(directives):
    cmt = directives[0]
    assert cmt.name == ""
    assert cmt.args == []
    assert cmt.bottom_comment == "# File: simple.conf"


def test_comment_at_eol(directives):
    user = directives[1]
    assert user.name == "user"
    assert user.args == ["nginx"]
    assert user.bottom_comment == "# Default use which iteracts with the system"


def test_nested_comment(directives):
    cmt = directives[-1][0]
    assert cmt.name == ""
    assert cmt.args == []
    assert cmt.bottom_comment == "# default type"
