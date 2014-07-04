import socket

def get_raw_http_response(host, port, path):

    CRLF = b"\r\n"

    request = [
        b"GET " + path.encode('ascii') + b" HTTP/1.1",
        b"Host: " + host.encode('ascii'),
        b"Connection: Close",
        b"",
        b"",
    ]
    
    # Connect to the server
    s = socket.socket()
    s.connect((host, port))
    
    # Send an HTTP request
    s.send(CRLF.join(request))
    
    # Get the response (in several parts, if necessary)
    response = b''
    buffer = s.recv(4096)
    while buffer:
        response += buffer
        buffer = s.recv(4096)

    return response


