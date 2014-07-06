import requests


def test_httpbin_gets_injected(httpbin):
    assert httpbin.url


def test_httpbin_accepts_get_requests(httpbin):
    assert requests.get(httpbin.url + '/get').status_code == 200


def test_httpbin_secure_accepts_get_requests(httpbin_secure):
    assert requests.get(httpbin_secure.url + '/get').status_code == 200


def test_httpbin_secure_accepts_lots_of_get_requests(httpbin_secure):
    for i in range(10):
        assert requests.get(httpbin_secure.url + '/get').status_code == 200


def test_httpbin_both(httpbin_both):
    # this test will get called twice, once with an http url, once with an
    # https url
    assert requests.get(httpbin_both.url + '/get').status_code == 200


def test_httpbin_join(httpbin):
    assert httpbin.join('foo') == httpbin.url + '/foo'


def test_httpbin_str(httpbin):
    assert httpbin + '/foo' == httpbin.url + '/foo'
