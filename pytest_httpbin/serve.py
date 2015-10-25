import os
import pytest_httpbin
import threading
import ssl
from werkzeug.serving import ThreadedWSGIServer, load_ssl_context, WSGIRequestHandler
from six.moves.urllib.parse import urljoin

CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs')

class Handler(WSGIRequestHandler):
    server_version = 'pytest-httpbin/' + pytest_httpbin.__version__

    def make_environ(self):
        """
        werkzeug server adds content-type text/plain to everything, this
        removes it if it's not actually in the headers.
        """
        # Note: Can't use super since this is an oldstyle class in python 2.x
        environ = super(Handler, self).make_environ().copy()
        if self.headers.get('content-type') is None:
            del environ['CONTENT_TYPE']
        return environ

class MyThreadedWSGIServer(ThreadedWSGIServer):

    def __init__(self, *args, **kwargs):
        self.protocol = kwargs.pop('protocol')
        super(MyThreadedWSGIServer, self).__init__(*args, **kwargs)

    def finish_request(self, request, client_address):
        """
        Negotiates SSL and then mimics BaseServer behavior.
        """
        if self.protocol == 'https':
            request.settimeout(1.0)
            ssock = ssl.wrap_socket(
                request,
                keyfile=os.path.join(CERT_DIR, 'key.pem'),
                certfile=os.path.join(CERT_DIR, 'cert.pem'),
                server_side=True
            )
            self.RequestHandlerClass(ssock, client_address, self)
        else:
            self.RequestHandlerClass(request, client_address, self)

class Server(threading.Thread):
    """
    HTTP server running a WSGI application in its own thread.
    """

    def __init__(self, host='127.0.0.1', port=0, application=None, protocol='http', **kwargs):
        self.app = application
        self._server = MyThreadedWSGIServer(
            host,
            port,
            self.app,
            handler=Handler,
            protocol=protocol,
            **kwargs
        )
        self.host = self._server.server_address[0]
        self.port = self._server.server_address[1]
        self.protocol = protocol

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
        super(SecureServer, self).__init__(host, port, application, protocol='https', **kwargs)
        self.protocol = 'https'
