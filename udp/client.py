import socket
from datetime import datetime

print(f"Establishing Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')}")

SERVER_HOST = ''
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))

response, server_address = client.recvfrom(1024)
print(response.decode())

client.close()
