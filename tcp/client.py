import socket
from datetime import datetime
import os

print(f"Establishing Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")

SERVER_HOST = ''
SERVER_PORT = 8080

# Configure socket for TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client.connect((SERVER_HOST, SERVER_PORT))

# Send request to server
request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.send(request.encode())

# Receive response from server
response = client.recv(1024).decode()
print(response)

client.close()
