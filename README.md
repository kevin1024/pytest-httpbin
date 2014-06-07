pytest-httpbin
=======================

**UNDER DEVELOPMENT, not yet released**

[httpbin](https://httpbin.org/) is an amazing web service for testing HTTP libraries.  It has several great endpoints that can test pretty much everything you need in a HTTP library.  The only problem is: maybe you don't want to wait for your tests to travel across the Internet and back to make assertions against a remote web service.

Enter `pytest-httpbin`.  Pytest-httpbin creates a pytest "fixture" that is dependency-injected into your tests. It automatically starts up a HTTP server in a separate thread running httpbin and provides your test with the URL in the fixture.  Check out this example:

```python
def test_that_my_library_works_kinda_ok(httpbin):
    assert requests.get(httpbin.url + '/get/').status_code == 200
```

This replaces a test that might have looked like this before:

```python
def test_that_my_library_works_kinda_ok():
    assert requests.get('http://httpbin.org/get').status_code == 200
```

pytest-httpbin also supports HTTPS:

```python
def test_that_my_library_works_kinda_ok(httpbin_secure):
    assert requests.get(httpbin_secure.url + '/get/').status_code == 200
```

It's actually starting 2 web servers in separate threads in the background: one HTTP and one HTTPS.  `pytest-httpbin` includes a self-signed certificate.  If your library verifies certificates against a CA (and it should), you'll have to add the CA from pytest-httpbin.  The path to the pytest-httpbin CA bundle can by found like this `python -m pytest_httpbin.certs`.

For example in requests, you can set the `REQUESTS_CA_BUNDLE` python path.  You can run your tests like this:

```bash
REQUESTS_CA_BUNDLE=`python -m pytest_httpbin.certs` py.test tests/
```

# Installation

All you need to do is this:

```bash
pip install pytest-httpbin
```

and your tests executed by pytest all will have access to the `httpbin` and `httpbin_secure` funcargs.  Cool right?

# Support and dependencies

pytest-httpbin suports pythons 2.6, 2.7, pypy, and 3.4.  It will automatically install httpbin and flask when you install it from pypi.

# License

MIT
