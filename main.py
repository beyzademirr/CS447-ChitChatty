import subprocess
import rsa
choice = input("Private Chat(1) or Group Chat(2):")
public_key, private_key = rsa.newkeys(1024)
public_partner = None

if choice == "1":
    subprocess.run(["/opt/homebrew/bin/python3", "chat-room/client.py"])

elif choice == "2":
   subprocess.run(["python", "e2e-multiple-clients/client.py"])
else:
    exit()





