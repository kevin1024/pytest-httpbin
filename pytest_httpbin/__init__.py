import pytest

with open("pytest_httpbin/version.py") as f:
    code = compile(f.read(), "pytest_httpbin/version.py", 'exec')
    exec(code)

use_class_based_httpbin = pytest.mark.usefixtures("class_based_httpbin")
use_class_based_httpbin_secure = pytest.mark.usefixtures("class_based_httpbin_secure")
