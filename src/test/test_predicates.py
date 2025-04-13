"""
Tests the is_*() methods of a Directive
"""

import pytest

from ncopa import parse

conf = """
# simple.conf
user nginx; # comment
http { # start: http directive
    default_type application/octet-stream;
} # end: http directive
"""

STANDALONE_COMMENT = 0
USER = 1
HTTP = 2


@pytest.fixture
def directives():
    return parse(conf)


@pytest.mark.parametrize(
    ["index", "name", "expected"],
    [
        pytest.param(0, "has_bottom_comment", True, id="comment_has_bottom_comment"),
        pytest.param(0, "has_top_comment", False, id="comment_has_top_comment"),
        pytest.param(0, "is_comment", True, id="comment_is_comment"),
        pytest.param(0, "is_context", False, id="comment_is_context"),
        pytest.param(1, "has_bottom_comment", True, id="user_has_bottom_comment"),
        pytest.param(1, "has_top_comment", False, id="user_has_top_comment"),
        pytest.param(1, "is_comment", False, id="user_is_comment"),
        pytest.param(1, "is_context", False, id="user_is_context"),
        pytest.param(2, "has_bottom_comment", True, id="http_has_bottom_comment"),
        pytest.param(2, "has_top_comment", True, id="http_has_top_comment"),
        pytest.param(2, "is_comment", False, id="http_is_comment"),
        pytest.param(2, "is_context", True, id="http_is_context"),
    ],
)
def test_predicate(directives, index, name, expected):
    predicate = getattr(directives[index], name)
    assert predicate() is expected
