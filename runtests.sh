#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

REQUESTS_CA_BUNDLE=$CURRENT_DIR/certs/cacert.pem py.test tests/
