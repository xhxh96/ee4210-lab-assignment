import socket
import os
import sys
from datetime import datetime

SERVER_HOST = ''

if len(sys.argv) > 1:
    SERVER_PORT = int(sys.argv[1])
else:
    SERVER_PORT = 8080

try:
    # Configure socket for TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to server
    client.connect((SERVER_HOST, SERVER_PORT))
    print(f"Established Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")
except Exception as e:
    print(f'Unable to connect to server at port {SERVER_PORT}!\nError: {e}')

# Send request to server
request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.send(request.encode())

# Receive response from server
response = client.recv(1024).decode()
print(response)

client.close()
