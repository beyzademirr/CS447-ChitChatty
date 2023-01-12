import socket
import threading
from tkinter import END

import rsa
import tkinter as tk






# Choosing Nickname
nickname = input("Choose your nickname: ")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65535))
stop_event = threading.Event()

#GUI
root = tk.Tk()
root.title("ChitChatty of " + nickname)
root.geometry("500x600")
label = tk.Label(root, text="CHITCHATTY", font=('Arial', 30))
label.pack(padx=30, pady=30)
messages = tk.Text(root, width=50, padx=30, pady=30, borderwidth=2, bg="gray")
messages.pack()

yourmessage = tk.Entry(root, width=50, bg="yellow")
yourmessage.insert(0, "Write a message..")
yourmessage.pack()
# Listening to Server and Sending Nickname
def receive():
    global public_partner
    while not stop_event.set():
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
                print("Partner: " + rsa.decrypt(client.recv(1024), private_key).decode('ascii'))
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
    while not stop_event.set():
    
        message = input('')

        if(message!='' and public_partner!=None):
         client.send(rsa.encrypt(message.encode(), public_partner))
         print("You: " + message)
        else:
            print("Wait for your partner")

def close_chat():
    stop_event.set()
    client.close()


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

root.mainloop()

