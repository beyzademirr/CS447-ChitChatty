import socket
import threading
import rsa

choice = input("(1) or (2):")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("172.24.128.1", 55555))
    server.listen()

    client, _ = server.accept()

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("172.24.128.1", 55555))
else:
    exit()



def sending_messages(msg):
    while True:
        message = input("")
        msg.send(message.encode())
        print("You: " + message)

def receiving_messages(msg):
    while True:       
        print("Partner: " + msg.recv(1024).decode())

threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()
