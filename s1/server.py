import sys
import socket
import os
from time import sleep
from datetime import datetime
from urllib.parse import unquote

# HTML content to be served when client is connected
def default_content():
    content = '''
<html>
<head>
    <title>EE4210 CA2 TCP Application</title>
</head>
<body>
    <form action="/text-response" method="post">
        <label for="user-input">Enter text here:</label>
        <input type="text" name="user-input" id="user-input">
        <input type="submit" value="Submit">
    </form>
</body>
</html>
'''
    return content

# HTML content to display user input
def response_content(text):
    content = '''
<html>
<head>
    <title>EE4210 CA2 TCP Application</title>
</head>
<body>
    <p id="output">You typed: {text}</p>
</body>
</html>
'''
    return content.format(text=text)

# Handle client request
def handle_request(request):
    # Process headers
    headers = request.split('\r\n')
    request_path = headers[0].split()[1]

    # If path is root, load HTML_CONTENT
    if request_path == '/':
        response = 'HTTP/1.1 200 OK\r\n' + 'Content-Type: text/html\r\n' + default_content()
    
    elif request_path == '/text-response':

        # Get user-input field in request
        user_input_param = headers[len(headers) - 1]

        # Get user-input value
        user_input = user_input_param.split('=')[1]

        # Convert from URL characters to ASCI characters and replace + with space
        user_input = unquote(user_input).replace('+', ' ')

        # Get HTML content 
        content = response_content(user_input)
        
        response = 'HTTP/1.1 200 OK\r\n' + 'Content-Type: text/html\r\n' + content
    
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

# Initailize socket using IPv4 address and TCP with 3 backlog connections
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(3)
    print(f'Server Started!\nListening to port {SERVER_PORT} ...')
except Exception as e:
    print(f'Unable to start server at port {SERVER_PORT}!\nError: {e}')

while True:
    # Wait for client connections
    client_connection, client_address = server.accept()

    pid = os.fork()

    # handle client request in child process
    if pid == 0:
        print(f"Received connection from {client_address} at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")
        
        # Detach server socket from child process
        server.detach()
        
        # Get the client request with 1 MB MTU
        request = client_connection.recv(1024).decode()
        print(request)

        # Return an HTTP response
        response = handle_request(request)
        client_connection.sendall(response.encode())

        # Close connection
        client_connection.close()

        # Exit child process
        os._exit(0)
    
    # Terminate client connection request in parent process
    else:
        client_connection.close()

# Close socket
server.close()
