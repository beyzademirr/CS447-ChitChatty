import socket
import threading
import rsa

# Choosing Nickname
nickname = input("Choose your nickname: ")
choice = input("Group Chat (1) or Private Chat (2):")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1'
, 65535))

# Listening to Server and Sending Nickname
def receive():
    global public_partner
    global choice
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'CHOICE':
                client.send(choice.encode('ascii'))
            elif message == 'KEY':
                client.send(public_key.save_pkcs1("PEM"))
            elif message == 'PARTNER':
                public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                print("Your partner has joined")
            elif message == 'MESSAGE':
                print("Partner: " + rsa.decrypt(client.recv(1024), private_key).decode())
            elif message == 'CLOSE':
                public_partner=None
                print("Your partner has left")
            else:
                print(message)
        except Exception as e:
            # Close Connection When Error
            print(e)
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True:
        if(choice == "2"):
            message = input('')
            if(message!='' and public_partner!=None):
                client.send(rsa.encrypt(message.encode(), public_partner))
                print("You: " + message)
            else:
                print("Wait for your partner")
        else:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))
        
        


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

try:
    receive_thread.join()
    write_thread.join()
except KeyboardInterrupt:
    client.close()