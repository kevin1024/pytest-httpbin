from __future__ import absolute_import
import pytest
from httpbin import app as httpbin_app
from . import serve


@pytest.fixture(scope='session')
def httpbin(request):
    from pytest_httpbin import serve
    httpbin_app.debug = True
    server = serve.Server(application=httpbin_app)
    server.start()
    request.addfinalizer(server.stop)
    return server


@pytest.fixture(scope='session')
def httpbin_secure(request):
    from pytest_httpbin import serve
    httpbin_app.debug = True
    server = serve.SecureServer(application=httpbin_app)
    server.start()
    request.addfinalizer(server.stop)
    return server
