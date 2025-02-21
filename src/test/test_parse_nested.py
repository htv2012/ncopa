"""
Parse nested directives
"""

import pytest

from ncopa import Directive, parse

CONFIG = """
user nginx;
error_log /var/log/nginx/error.log notice;
http {
	default_type application/octet-stream;
}
"""


@pytest.fixture(scope="module")
def directives() -> list[Directive]:
    return parse(CONFIG)


@pytest.fixture(scope="module")
def user(directives):
    return directives[0]


@pytest.fixture(scope="module")
def elog(directives):
    return directives[1]


@pytest.fixture(scope="module")
def http(directives):
    return directives[2]


@pytest.fixture(scope="module")
def default_type(directives):
    return directives[2].children[0]


# ======================================================================


def test_count(directives):
    assert len(directives) == 3


# ======================================================================


def test_user_name(user):
    assert user.name == "user"


def test_user_args(user):
    assert user.args == ["nginx"]


def test_user_children(user):
    assert user.children == []


# ======================================================================


def test_elog_name(elog):
    assert elog.name == "error_log"


def test_elog_args(elog):
    assert elog.args == ["/var/log/nginx/error.log", "notice"]


def test_elog_children(elog):
    assert elog.children == []


# ======================================================================


def test_http_name(http):
    assert http.name == "http"


def test_http_args(http):
    assert http.args == []


def test_http_children(http):
    assert len(http.children) == 1


def test_http_comment(http):
    assert http.bottom_comment == ""


# ======================================================================


def test_default_type_name(default_type):
    assert default_type.name == "default_type"


def test_default_type_args(default_type):
    assert default_type.args == ["application/octet-stream"]


def test_default_type_children(default_type):
    assert default_type.children == []


def test_defaullt_type_comment(default_type):
    assert default_type.bottom_comment == ""
