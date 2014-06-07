#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

REQUESTS_CA_BUNDLE=$CURRENT_DIR/pytest_httpbin/certs/cacert.pem py.test tests/
