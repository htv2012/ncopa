"""
Parses a single directive and verify
"""

import pytest

from ncopa import parse


@pytest.fixture(scope="module")
def directives():
    return parse("user nginx;")


def test_count(directives):
    """Verify the number of directives parsed"""
    assert len(directives) == 1


def test_name(directives):
    """Verify the name of the directive"""
    assert directives[0].name == "user"


def test_args(directives):
    """Verify the arguments"""
    assert directives[0].args == ["nginx"]


def test_children(directives):
    """Verify the children"""
    assert directives[0].children == []


def test_comment(directives):
    assert directives[0].comment == ""
