import os

import pytest

from .version import __version__

use_class_based_httpbin = pytest.mark.usefixtures("class_based_httpbin")
use_class_based_httpbin_secure = pytest.mark.usefixtures("class_based_httpbin_secure")
