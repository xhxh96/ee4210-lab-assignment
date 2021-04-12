import sys
import socket
import os
from datetime import datetime

# Equivalent to INADDR_ANY in C -- use any interface available
SERVER_HOST = ''

# Port number is either system argument or default to 8080
if len(sys.argv) > 1:
    SERVER_PORT = int(sys.argv[1])
else:
    SERVER_PORT = 8080

# HTML Content to be served when client is connected
HTML_CONTENT = '''
<html>
<head>
    <title>EE4210 CA2 TCP Application</title>
</head>
<body>
    <input type="text" id="user-input">
    <button type="button" onclick="getUserInput();">Submit</button>
    <p id="output"></p>
</body>
<script>
    function getUserInput() {
        const input = document.getElementById("user-input").value;
        document.getElementById("output").innerHTML = "You Typed: " + input;
    }
</script>
</html>
'''

def handle_request(request):
    # Process headers
    headers = request.split('\r\n')
    request_path = headers[0].split()[1]
    
    # If path is root, load HTML_CONTENT
    if request_path == '/':
        response = 'HTTP/1.1 200 OK\r\n' + HTML_CONTENT
    
    # Any other request_path is deemed invalid
    else:
        response = 'HTTP/1.1 404 NOT FOUND\r\nInvalid URL'

    return response



# Initailize socket using IPv4 address and TCP
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
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
        
        # Get the client request
        request = client_connection.recv(1024).decode()
        print(request)

        # Return an HTTP response
        response = handle_request(request)
        client_connection.sendall(response.encode())

        # Close connection
        client_connection.close()

        # Exit
        os._exit(0)
    
    # Terminate client connection request in parent process
    else:
        client_connection.close()

# Close socket
server.close()
