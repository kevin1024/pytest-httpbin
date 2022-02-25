import pytest



@pytest.fixture(autouse=True, scope='function')
def httpbin_ca_bundle_autoused(httpbin_ca_bundle):
    pass
