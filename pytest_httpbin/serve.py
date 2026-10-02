import io
import os
import re
import ssl
import threading
from urllib.parse import urljoin
from wsgiref.handlers import SimpleHandler
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
HEX_DIGITS = re.compile(rb"[0-9A-Fa-f]+")


class ServerHandler(SimpleHandler):
    server_software = "Pytest-HTTPBIN/0.1.0"
    http_version = "1.1"

    def cleanup_headers(self):
        SimpleHandler.cleanup_headers(self)
        self.headers["Connection"] = "Close"

    def close(self):
        try:
            self.request_handler.log_request(
                self.status.split(" ", 1)[0], self.bytes_sent
            )
        finally:
            SimpleHandler.close(self)


class Handler(WSGIRequestHandler):
    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline()
        if not self.parse_request():  # An error code has been sent, just exit
            return

        stdin = self.rfile
        environ = self.get_environ()
        if self.headers.get("Transfer-Encoding", "").strip().lower() == "chunked":
            # wsgiref doesn't decode chunked request bodies, and httpbin answers
            # them with a 501 without reading them, so a client still sending the
            # body gets a broken pipe. Decode the body here and give it to the
            # application with a Content-Length instead, see issue #33
            try:
                body = self.read_chunked_body()
            except ValueError:
                self.send_error(400, "Bad chunked request body")
                return
            stdin = io.BytesIO(body)
            environ["CONTENT_LENGTH"] = str(len(body))
            del environ["HTTP_TRANSFER_ENCODING"]

        handler = ServerHandler(stdin, self.wfile, self.get_stderr(), environ)
        handler.request_handler = self  # backpointer for logging
        handler.run(self.server.get_app())

    def read_chunked_body(self):
        """
        Read a request body sent with Transfer-Encoding: chunked, and return it
        decoded. Chunk extensions and trailer fields are ignored.
        """
        chunks = []
        while True:
            size_line = self.rfile.readline(65537)
            size = size_line.split(b";", 1)[0].strip()
            if not size_line.endswith(b"\n") or not HEX_DIGITS.fullmatch(size):
                raise ValueError(f"bad chunk size line: {size_line!r}")
            size = int(size, 16)
            if size == 0:
                break
            chunk = self.rfile.read(size)
            if len(chunk) != size or self.rfile.readline(3) not in (b"\r\n", b"\n"):
                raise ValueError("chunk data doesn't match its size")
            chunks.append(chunk)
        # Skip the trailer section, which ends with an empty line
        while self.rfile.readline(65537) not in (b"\r\n", b"\n", b""):
            pass
        return b"".join(chunks)

    def get_environ(self):
        """
        wsgiref simple server adds content-type text/plain to everything, this
        removes it if it's not actually in the headers.
        """
        # Note: Can't use super since this is an oldstyle class in python 2.x
        environ = WSGIRequestHandler.get_environ(self).copy()
        if self.headers.get("content-type") is None:
            del environ["CONTENT_TYPE"]
        return environ


class SecureWSGIServer(WSGIServer):
    def get_request(self):
        socket, address = super().get_request()
        try:
            socket.settimeout(1.0)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(
                os.path.join(CERT_DIR, "server.pem"),
                os.path.join(CERT_DIR, "server.key"),
            )
            return (
                context.wrap_socket(
                    socket, server_side=True, suppress_ragged_eofs=True
                ),
                address,
            )
        except Exception as e:
            print("pytest-httpbin server hit an exception serving request: %s" % e)
            print("attempting to ignore so the rest of the tests can run")
            raise

    def setup_environ(self):
        super().setup_environ()
        self.base_environ["HTTPS"] = "yes"


class Server:
    """
    HTTP server running a WSGI application in its own thread.
    """

    port_envvar = "HTTPBIN_HTTP_PORT"

    def __init__(self, host="127.0.0.1", port=0, application=None, **kwargs):
        self.app = application
        if self.port_envvar in os.environ:
            port = int(os.environ[self.port_envvar])
        self._server = make_server(
            host, port, self.app, handler_class=Handler, **kwargs
        )
        self.host = self._server.server_address[0]
        self.port = self._server.server_address[1]
        self.protocol = "http"

        self._thread = threading.Thread(
            name=self.__class__,
            target=self._server.serve_forever,
        )

    def __del__(self):
        if hasattr(self, "_server"):
            self.stop()

    def start(self):
        self._thread.start()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
        suppress_exc = self._server.__exit__(*args, **kwargs)
        self._thread.join()
        return suppress_exc

    def __add__(self, other):
        return self.url + other

    def stop(self):
        self._server.shutdown()

    @property
    def url(self):
        return f"{self.protocol}://{self.host}:{self.port}"

    def join(self, url, allow_fragments=True):
        return urljoin(self.url, url, allow_fragments=allow_fragments)


class SecureServer(Server):
    port_envvar = "HTTPBIN_HTTPS_PORT"

    def __init__(self, host="127.0.0.1", port=0, application=None, **kwargs):
        kwargs["server_class"] = SecureWSGIServer
        super().__init__(host, port, application, **kwargs)
        self.protocol = "https"
