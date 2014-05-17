from __future__ import absolute_import
from .packages import httpbin
from . import serve

def pytest_funcarg_httpbin(request):
    from pytest_httpbin import serve
    server = serve.WSGIServer(application=httpbin.app)
    server.start()
    request.addfinalizer(server.stop())
    return server
