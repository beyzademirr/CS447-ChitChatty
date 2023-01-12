import rsa
import subprocess

host = '127.0.0.1'
choice = input("Private Chat(1) or Group Chat(2):")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

if host == '127.0.0.1':
    if choice == "1":
        server=subprocess.Popen(["python3", "e2e-multiple-clients/server.py"])
    elif choice == "2":
        server=subprocess.Popen(["python", "chat-room/server.py"])
    else:
        exit()

if choice == "1":
    client = subprocess.Popen(["python3", "e2e-multiple-clients/client.py"])
elif choice == "2":
    client = subprocess.Popen(["python", "chat-room/client.py"])
else:
    exit()

server.wait()
client.wait()