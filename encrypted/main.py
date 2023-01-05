import socket
import threading
import rsa

choice = input("(1) or (2):")
public_key, private_key = rsa.newkeys(1024)
public_partner = None

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("172.24.128.1", 55555))
    server.listen()

    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("172.24.128.1", 55555))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))

else:
    exit()



def sending_messages(msg):
    while True:
        message = input("")
        msg.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)

def receiving_messages(msg):
    while True:       
        print("Partner: " + rsa.decrypt(msg.recv(1024), private_key).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
