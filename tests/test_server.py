# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import requests
import pytest
from util import get_raw_http_response

try:
    from multiprocessing.pool import ThreadPool
except ImportError:
    ThreadPool = None


def test_content_type_header_not_automatically_added(httpbin):
    """
    The server was automatically adding this for some reason, see issue #5
    """
    resp = requests.get(httpbin + '/headers').json()['headers']
    assert 'Content-Type' not in resp


def test_unicode_data(httpbin):
    """
    UTF-8 was not getting recognized for what it was and being encoded as if it
    was binary, see issue #7
    """
    resp = requests.post(
        httpbin + '/post',
        data=u'оживлённым'.encode('utf-8'),
        headers={
            'content-type': 'text/html; charset=utf-8',
        }
    )
    assert resp.json()['data'] == u'оживлённым'



def test_server_should_handle_concurrent_connections(httpbin):
    url = httpbin + '/get'
    session = requests.Session()

    def do_request(i):
        r = session.get(url)
    if ThreadPool is not None:
        pool = ThreadPool(processes=50)
        pool.map(do_request, range(100))


def test_dont_crash_on_certificate_problems(httpbin_secure):
    with pytest.raises(Exception):
        # this request used to hang
        requests.get(
            httpbin_secure + '/get',
            verify = True,
            cert=__file__
        )
    # and this request would never happen
    requests.get(
        httpbin_secure + '/get',
        verify = True,
    )
