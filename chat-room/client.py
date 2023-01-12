import socket
import threading

# choosing nickname
nickname = input("Choose your nickname: ")

# connecting to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65500))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break

# sending message to server
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

# Wait for the threads to finish execution before client close
receive_thread.join()
write_thread.join()
client.close()
