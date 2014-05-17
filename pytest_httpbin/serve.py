import json
import sys
import threading

from werkzeug.serving import make_server
from werkzeug.wrappers import Response, Request

# Note: mostly stolen from pytest-localserver
# https://bitbucket.org/basti/pytest-localserver/src/66c7bb00d8f8e537421e66a602b6bb31ee5b6f61/pytest_localserver/http.py?at=default


class WSGIServer(threading.Thread):
    """
    HTTP server running a WSGI application in its own thread.
    """

    def __init__(self, host='127.0.0.1', port=0, application=None, **kwargs):
        self.app = application
        self._server = make_server(host, port, self.app, **kwargs)
        self.server_address = self._server.server_address

        super(WSGIServer, self).__init__(
            name=self.__class__,
            target=self._server.serve_forever)

    def __del__(self):
        self.stop()

    def stop(self):
        self._server.shutdown()
