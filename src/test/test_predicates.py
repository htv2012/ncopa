"""
Tests the is_*() methods of a Directive
"""
from ncopa import Directive, parse

import pytest



conf = """
# simple.conf
user nginx;
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

def test_
@pytest.fixture
def standalone_comment_directive(directives):
    return directives[0]

@pytest.fixture
def user_directive(directives):
    return directives[1]

@pytest.fixture
def http_directive(directives):
    return directives[1]

