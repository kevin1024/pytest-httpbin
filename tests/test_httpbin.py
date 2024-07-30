import ssl
import sys
import unittest
import urllib.request

import pytest
import requests.exceptions
import urllib3

import pytest_httpbin.certs


def test_httpbin_gets_injected(httpbin):
    assert httpbin.url


def test_httpbin_accepts_get_requests(httpbin):
    assert requests.get(httpbin.url + "/get").status_code == 200


def test_httpbin_secure_accepts_get_requests(httpbin_secure):
    assert requests.get(httpbin_secure.url + "/get").status_code == 200


def test_httpbin_secure_accepts_lots_of_get_requests(httpbin_secure):
    for i in range(10):
        assert requests.get(httpbin_secure.url + "/get").status_code == 200


def test_httpbin_accepts_lots_of_get_requests_in_single_session(httpbin):
    session = requests.Session()

    for i in range(10):
        assert session.get(httpbin.url + "/get").status_code == 200


def test_httpbin_both(httpbin_both):
    # this test will get called twice, once with an http url, once with an
    # https url
    assert requests.get(httpbin_both.url + "/get").status_code == 200


def test_httpbin_join(httpbin):
    assert httpbin.join("foo") == httpbin.url + "/foo"


def test_httpbin_str(httpbin):
    assert httpbin + "/foo" == httpbin.url + "/foo"


def test_chunked_encoding(httpbin):
    assert requests.get(httpbin.url + "/stream/20").status_code == 200


@pytest.mark.xfail(
    condition=sys.version_info < (3, 8) and ssl.OPENSSL_VERSION_INFO >= (3, 0, 0),
    reason="fails on python3.7 openssl 3+",
    raises=requests.exceptions.SSLError,
)
def test_chunked_encoding_secure(httpbin_secure):
    assert requests.get(httpbin_secure.url + "/stream/20").status_code == 200


@pytest_httpbin.use_class_based_httpbin
@pytest_httpbin.use_class_based_httpbin_secure
class TestClassBassedTests(unittest.TestCase):
    def test_http(self):
        assert requests.get(self.httpbin.url + "/get").status_code == 200

    def test_http_secure(self):
        assert requests.get(self.httpbin_secure.url + "/get").status_code == 200


def test_with_urllib2(httpbin_secure):
    url = httpbin_secure.url + "/get"
    context = ssl.create_default_context(cafile=pytest_httpbin.certs.where())
    with urllib.request.urlopen(url, context=context) as response:
        assert response.getcode() == 200


def test_with_urllib3(httpbin_secure):
    with urllib3.PoolManager(
        cert_reqs="CERT_REQUIRED",
        ca_certs=pytest_httpbin.certs.where(),
    ) as pool:
        pool.request(
            "POST", httpbin_secure.url + "/post", {"key1": "value1", "key2": "value2"}
        )
