import subprocess
import rsa
choice = input("Private Chat(1) or Group Chat(2):")
public_key, private_key = rsa.newkeys(1024)
public_partner = None

#private chat with multiple clients
if choice == "1":
    subprocess.run(["/opt/homebrew/bin/python3", "e2e-multiple-clients/client.py"])

#group chat
elif choice == "2":
   subprocess.run(["python", "chat-room/client.py"])
else:
    exit()





