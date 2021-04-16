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
    # Configure socket for UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Established Connection at {datetime.utcnow().isoformat(sep=' ', timespec='milliseconds')} on PID {os.getpid()}")
except Exception as e:
    print(f'Unable to connect to server at port {SERVER_PORT}!\nError: {e}')

# Send request to server
request = f'GET / HTTP/1.1\r\nHost:{SERVER_HOST}\r\n\r\n'
client.sendto(request.encode(), (SERVER_HOST, SERVER_PORT))

# Receive response from server
response, server_address = client.recvfrom(1024)
content = response.decode()
print(content)

# Obtain HTML body
body = content.split('\r\n')[1]

# Save HTML body to file
f = open(f'response_{os.getpid()}.html', 'w')
f.write(body.strip())
f.close()

client.close()
