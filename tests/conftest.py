import pytest

from pytest_httpbin.plugin import httpbin_ca_bundle


@pytest.fixture(autouse=True, scope='function')
def httpbin_ca_bundle_autoused(httpbin_ca_bundle):
    pass
