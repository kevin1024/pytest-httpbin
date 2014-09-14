import pytest

__version__ = '0.0.3'

use_class_based_httpbin = pytest.mark.usefixtures("class_based_httpbin")
use_class_based_httpbin_secure = pytest.mark.usefixtures("class_based_httpbin_secure")
