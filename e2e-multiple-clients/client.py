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
client.connect(('127.0.0.1', 65527))
stop_event = threading.Event()

# GUI
root = tk.Tk()
root.title("ChitChatty of " + nickname)
root.geometry("500x600")
label = tk.Label(root, text="CHITCHATTY", font=('Arial', 30))
label.pack(padx=30, pady=30)
messages = tk.Text(root, width=50, padx=30, pady=30, borderwidth=2, bg="gray")
messages.pack()

yourmessage = tk.Entry(root, width=50, bg="yellow")
yourmessage.insert(END, "Write a message..")
yourmessage.pack()
yourmessage.focus()


# Listening to Server and Sending Nickname
def receive():
    global public_partner
    while not stop_event.set():
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'KEY':
                client.send(public_key.save_pkcs1("PEM"))
            elif message == 'PARTNER':
                public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                print("Your partner has joined")
                messages['state'] = 'normal'
                messages.insert(END, "Your partner has joined")
                messages['state'] = 'disabled'
            elif message == 'MESSAGE':
                received_message = rsa.decrypt(client.recv(1024), private_key).decode('ascii')
                messages['state'] = 'normal'
                messages.insert(END, "\n" + "Partner: " + received_message)
                messages['state'] = 'disabled'
                print("Partner: " + received_message)
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
    message = yourmessage.get()

    if message != '' and public_partner is not None:
        messages['state'] = 'normal'
        client.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)
        messages.insert(END, "\n" + "You: " + message)
        yourmessage.delete(0, END)
        messages['state'] = 'disabled'
    else:
        messages['state'] = 'normal'
        print("Wait for your partner")
        messages.insert(END, "\n" + "Wait for your partner")
        messages['state'] = 'disabled'


def close_chat():
    stop_event.set()
    client.close()


send_button = tk.Button(root, width=20, command=write, text="Send")
send_button.pack()

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()


