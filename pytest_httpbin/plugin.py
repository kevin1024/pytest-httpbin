from __future__ import absolute_import
import pytest
from . import serve

@pytest.fixture(scope='session')
def httpbin(request):
    from pytest_httpbin import serve
    server = serve.WSGIServer(application=httpbin.app)
    server.start()
    request.addfinalizer(server.stop)
    return server
