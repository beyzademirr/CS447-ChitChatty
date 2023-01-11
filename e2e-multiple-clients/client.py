import socket
import threading
import rsa

# Choosing Nickname
nickname = input("Choose your nickname: ")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1'
, 65535))

# Listening to Server and Sending Nickname
def receive():
    global public_partner
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'KEY':
                client.send(public_key.save_pkcs1("PEM"))
            elif message == 'PARTNER':
                public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                print("Your partner has joined")
            elif message == 'MESSAGE':
                print("Partner: " + rsa.decrypt(client.recv(1024), private_key).decode()) 
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
    
        message = input('')

        if(message!='' and public_partner!=None):
         client.send(rsa.encrypt(message.encode(), public_partner))
         print("You: " + message)
        else:
            print("Wait for your partner")
        
        


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
