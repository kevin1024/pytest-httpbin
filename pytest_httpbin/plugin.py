def pytest_funcarg_httpbin(request):
    from pytest_httpbin import serve
    server = serve.Server()
    server.start()
    request.addfinalizer(server.stop())
    return server

