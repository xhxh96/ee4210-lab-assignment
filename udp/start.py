import subprocess

# Runs 3 client.py processes in parallel
subprocess.run("python3 client.py & python3 client.py & python3 client.py", shell=True)