import sys
import socket
import os
from time import sleep
from datetime import datetime

# HTML content to be served when client is connected
def default_content():
    content = '''
<html>
<head>
    <title>EE4210 CA2 UDP Application</title>
</head>
<body>
    <p>EE-4210: Continuous Assessment</p>
</body>
</html>
'''

    return content

def handle_request(request):
    # Process headers
    headers = request.split('\r\n')
    request_path = headers[0].split()[1]
    
    # If path is root, load HTML_CONTENT
    if request_path == '/':
        response = 'HTTP/1.1 200 OK\r\n' + default_content()
    
    # Any other request_path is deemed invalid
    else:
        response = 'HTTP/1.1 404 NOT FOUND\r\nInvalid URL'

    # Pause 3 seconds to simulate page loading
    # Uncomment following line to test server concurrency
    # sleep(3)

    return response


# Equivalent to INADDR_ANY in C -- use any interface available
SERVER_HOST = ''

# Port number is either system argument or default to 8080
if len(sys.argv) > 1:
    SERVER_PORT = int(sys.argv[1])
else:
    SERVER_PORT = 8080

# Initailize socket using IPv4 address and UDP
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    print(f'Server Started!\nListening to port {SERVER_PORT} ...')
except Exception as e:
    print(f'Unable to start server at port {SERVER_PORT}!\nError: {e}')

while True:
    # Wait for client connections with 1MB MTU
    data, client_address = server.recvfrom(1024)

    # fork process only when there is data
    if data:
        pid = os.fork()

    # handle client request in child process
    if pid == 0:
        print(f"Received connection from {client_address} at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")
        
        # Get the client request
        request = data.decode()
        print(request)

        # Return an HTTP response
        response = handle_request(request)
        server.sendto(response.encode(), client_address)

        # Exit child process
        os._exit(0)

# Close socket
server.close()
