import os
import sys
import threading
import ssl
import tempfile
from wsgiref.simple_server import WSGIServer, make_server, WSGIRequestHandler
from wsgiref.handlers import SimpleHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from six import BytesIO
from six.moves.urllib.parse import urljoin

CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs')
class ServerHandler(SimpleHandler):

    server_software = 'Pytest-HTTPBIN/0.1.0'
    http_version = '1.1'

    def close(self):
        try:
            self.request_handler.log_request(
                self.status.split(' ',1)[0], self.bytes_sent
            )
        finally:
            SimpleHandler.close(self)

class Handler(WSGIRequestHandler):


    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline()
        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())


class SecureWSGIServer(WSGIServer):

    def finish_request(self, request, client_address):
        """
        Negotiates SSL and then mimics BaseServer behavior.
        """
        ssock = ssl.wrap_socket(
            request,
            keyfile=os.path.join(CERT_DIR, 'key.pem'),
            certfile=os.path.join(CERT_DIR, 'cert.pem'),
            server_side=True
        )
        self.RequestHandlerClass(ssock, client_address, self)
        # WSGIRequestHandler seems to close the socket for us.
        # Thanks, WSGIRequestHandler!!


class Server(threading.Thread):
    """
    HTTP server running a WSGI application in its own thread.
    """

    def __init__(self, host='127.0.0.1', port=0, application=None):
        self.app = application
        self._server = make_server(host, port, self.app, handler_class=Handler)
        self.host = self._server.server_address[0]
        self.port = self._server.server_address[1]
        self.protocol = 'http'

        super(Server, self).__init__(
            name=self.__class__,
            target=self._server.serve_forever,
        )

    def __del__(self):
        self.stop()

    def __add__(self, other):
        return self.url + other

    def stop(self):
        self._server.shutdown()

    @property
    def url(self):
        return '{0}://{1}:{2}'.format(self.protocol, self.host, self.port)

    def join(self, url, allow_fragments=True):
        return urljoin(self.url, url, allow_fragments=allow_fragments)


class SecureServer(Server):
    def __init__(self, host='127.0.0.1', port=0, application=None, **kwargs):
        kwargs['server_class'] = SecureWSGIServer
        super(SecureServer, self).__init__(host, port, application, **kwargs)
        self.protocol = 'https'
