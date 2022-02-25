import contextlib
import os
import re
import socket

import pytest
import requests
from httpbin import app as httpbin_app
from util import get_raw_http_response

from pytest_httpbin import serve


def test_content_type_header_not_automatically_added(httpbin):
    """
    The server was automatically adding this for some reason, see issue #5
    """
    resp = requests.get(httpbin + "/headers").json()["headers"]
    assert "Content-Type" not in resp


def test_unicode_data(httpbin):
    """
    UTF-8 was not getting recognized for what it was and being encoded as if it
    was binary, see issue #7
    """
    resp = requests.post(
        httpbin + "/post",
        data="оживлённым".encode(),
        headers={
            "content-type": "text/html; charset=utf-8",
        },
    )
    assert resp.json()["data"] == "оживлённым"


def test_server_should_be_http_1_1(httpbin):
    """
    The server should speak HTTP/1.1 since we live in the future, see issue #6
    """
    resp = get_raw_http_response(httpbin.host, httpbin.port, "/get")
    assert resp.startswith(b"HTTP/1.1")


def test_dont_crash_on_certificate_problems(httpbin_secure, capsys):
    with socket.socket() as sock:
        sock.connect((httpbin_secure.host, httpbin_secure.port))
        # this request used to hang
        assert sock.recv(1) == b""

    assert (
        re.match(
            r"pytest-httpbin server hit an exception serving request: .* The "
            "handshake operation timed out\nattempting to ignore so the rest "
            "of the tests can run\n",
            capsys.readouterr().out,
        )
        is not None
    )

    # and this request would never happen
    requests.get(
        httpbin_secure + "/get",
        verify=True,
    )


@pytest.mark.parametrize("protocol", ("http", "https"))
def test_fixed_port_environment_variables(protocol):
    """
    Note that we cannot test the fixture here because it is session scoped
    and was already started. Thus, let's just test a new Server instance.
    """
    if protocol == "http":
        server_cls = serve.Server
        envvar = "HTTPBIN_HTTP_PORT"
    elif protocol == "https":
        server_cls = serve.SecureServer
        envvar = "HTTPBIN_HTTPS_PORT"
    else:
        raise RuntimeError(f"Unexpected protocol param: {protocol}")

    # just have different port to avoid adrress already in use
    # if the second test run too fast after the first one (happens on pypy)
    port = 12345 + len(protocol)
    server = contextlib.nullcontext()

    try:
        envvar_original = os.environ.get(envvar, None)
        os.environ[envvar] = str(port)
        server = server_cls(application=httpbin_app)
        assert server.port == port
    finally:
        # if we don't do this, it blocks:
        with server:
            pass

        # restore the original environ:
        if envvar_original is None:
            del os.environ[envvar]
        else:
            os.environ[envvar] = envvar_original


def test_redirect_location_is_https_for_secure_server(httpbin_secure):
    assert httpbin_secure.url.startswith("https://")
    response = requests.get(
        httpbin_secure + "/redirect-to?url=/html", allow_redirects=False
    )
    assert response.status_code == 302
    assert response.headers.get("Location")
    assert response.headers["Location"].startswith("https://")
