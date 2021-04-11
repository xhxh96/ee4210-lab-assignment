import socket
from datetime import datetime

print(f"Establishing Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')}")

SERVER_HOST = ''
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER_HOST, SERVER_PORT))

request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.send(request.encode())

response = client.recv(1024).decode()
print(response)

client.close()
