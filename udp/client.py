import socket
import os
from datetime import datetime

print(f"Establishing Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")

SERVER_HOST = ''
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))

response, server_address = client.recvfrom(1024)
print(response)
content = response.decode().split('\r\n')[1]

f = open(f'response_{os.getpid()}.html', 'w')
f.write(content)
f.close()

client.close()
