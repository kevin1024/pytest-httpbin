from __future__ import absolute_import
import pytest
from httpbin import app as httpbin_app
from . import serve

@pytest.fixture(scope='session')
def httpbin(request):
    from pytest_httpbin import serve
    httpbin_app.debug = True
    server = serve.WSGIServer(application=httpbin_app)
    server.start()
    request.addfinalizer(server.stop)
    return server
