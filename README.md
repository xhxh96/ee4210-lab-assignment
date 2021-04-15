# README
Both server files are written in Python 3.8. No extra Python dependencies are required. 

The TCP server file is `/tcp/server.py` while the UDP server file is `/udp/server.py`.

Linux-based operating system is recommended to run both server files. 

## TCP HTTP SERVER
To launch the TCP server:
1. Ensure that you're in the `tcp` directory with `$ cd tcp`.
2. Launch the TCP server with the command `$ python3 server.py`.
3. By default, the server will be running on port `8080`. To specify a port number to be used for the server, enter the desired port number as an additional argument e.g. `$ python3 server.py 8081` will launch the server on port `8081`

There are 2 ways to access server:
1. Through a web-browser: Launch a web-browser and access the URL `localhost:8080`. If you're using a different port number for your server, replace `8080` with the correct port number. 
2. Through `client.py`: In the `tcp` directory, launch `client.py` with the command `$ python3 client.py`. If you're using a different port number for your server, input the correct port number as an additional argument e.g. `$ python3 client.py 8081`.

To test concurrency:
1. Open `server.py` with an editor. 
2. Uncomment `sleep(3)` in <b>line 72</b>. This adds a 3 second delay before the server sends the response to the client.
3. Launch the `start.sh` bash script with the command `$ bash start.sh 8080`. This script automatically runs 3 `client.py` processes in parallel. If your server is running on a different port number, replace `8080` with the correct port number e.g. `$ bash start.sh 8081`.
4. Verify that all 3 clients receive the response from the server simultaneously (~3 seconds after the script was launched). 

## UDP HTTP SERVER
To launch the UDP server:
1. Ensure that you're in the `UDP` directory with `$ cd udp`.
2. Launch the UDP server with the command `$ python3 server.py`.
3. By default, the server will be running on port `8080`. To specify a port number to be used for the server, enter the desired port number as an additional argument e.g. `$ python3 server.py 8081` will launch the server on port `8081`

To access the server:
1. In the `udp` directory, launch `client.py` with the command `$ python3 client.py`. If you're using a different port number for your server, input the correct port number as an additional argument e.g. `$ python3 client.py 8081`.
2. A HTML file should be downloaded in the same folder with the name `response_<process ID>.html`. Open the HTML file with a web browser to view the server's response. 

To test concurrency:
1. Open `server.py` with an editor. 
2. Uncomment `sleep(3)` in <b>line 37</b>. This adds a 3 second delay before the server sends the response to the client.
3. Launch the `start.sh` bash script with the command `$ bash start.sh 8080`. This script automatically runs 3 `client.py` processes in parallel. If your server is running on a different port number, replace `8080` with the correct port number e.g. `$bash start.sh 8081`.
4. Verify that all 3 clients receive the response from the server simultaneously (~3 seconds after the script was launched). 