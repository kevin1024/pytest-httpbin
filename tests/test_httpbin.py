import unittest
import requests
import pytest_httpbin


def test_httpbin_gets_injected(httpbin):
    assert httpbin.url


def test_httpbin_accepts_get_requests(httpbin):
    assert requests.get(httpbin.url + '/get').status_code == 200


def test_httpbin_secure_accepts_get_requests(httpbin_secure):
    assert requests.get(httpbin_secure.url + '/get').status_code == 200


def test_httpbin_secure_accepts_lots_of_get_requests(httpbin_secure):
    for i in range(10):
        assert requests.get(httpbin_secure.url + '/get').status_code == 200


def test_httpbin_accepts_lots_of_get_requests_in_single_session(httpbin):
    session = requests.Session()

    for i in range(10):
        assert session.get(httpbin.url + '/get').status_code == 200


def test_httpbin_both(httpbin_both):
    # this test will get called twice, once with an http url, once with an
    # https url
    assert requests.get(httpbin_both.url + '/get').status_code == 200


def test_httpbin_join(httpbin):
    assert httpbin.join('foo') == httpbin.url + '/foo'


def test_httpbin_str(httpbin):
    assert httpbin + '/foo' == httpbin.url + '/foo'

def test_chunked_encoding(httpbin_both):
    assert requests.get(httpbin_both.url + '/stream/20').status_code == 200


def test_post_chunked_binary(httpbin_both):
    data1 = iter([b'data', b'to', b'send'])
    url = httpbin_both.url + '/post'
    resp = requests.post(url, data1)
    assert resp.json()['data'] == b'datatosend'


@pytest_httpbin.use_class_based_httpbin
@pytest_httpbin.use_class_based_httpbin_secure
class TestClassBassedTests(unittest.TestCase):
    def test_http(self):
        assert requests.get(self.httpbin.url + '/get').status_code == 200

    def test_http_secure(self):
        assert requests.get(self.httpbin_secure.url + '/get').status_code == 200
