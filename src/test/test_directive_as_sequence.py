import pytest

from ncopa import parse

CONFIG = """
server {
    server_name 127.0.0.1;
    listen 127.0.0.1:49151;
    access_log off;
    f5_metrics off;
    location /api {
        api;
    }
}
""".strip()


@pytest.fixture(scope="module")
def server():
    """Return server directive"""
    return parse(CONFIG)[0]


def test_len(server):
    assert len(server) == 5


def test_index(server):
    assert server[0].name == "server_name"
    assert server[-1].name == "location"


def test_iter(server):
    names = [directive.name for directive in server]
    assert names == ["server_name", "listen", "access_log", "f5_metrics", "location"]
