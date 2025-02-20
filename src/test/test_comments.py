"""
Verify that comments were correctly parsed
"""

import pytest

from ncopa import parse

TEXT = """
# File: simple.conf

# Default use which iteracts with the system
user nginx;

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
    assert len(directives) == 5


def test_top_level_comment1(directives):
    cmt = directives[0]
    assert cmt.name == "#"
    assert cmt.args == ["File:", "simple.conf"]


def test_top_level_comment2(directives):
    cmt = directives[1]
    assert cmt.name == "#"
    assert cmt.args == "Default use which iteracts with the system".split()


def test_nested_comment(directives):
    cmt = directives[-1][0]
    assert cmt.name == "#"
    assert cmt.args == "default type".split()
