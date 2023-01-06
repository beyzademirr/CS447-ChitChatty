import socket
import threading
import rsa


# Connection Data
host = ''
port = 3389

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
keys = []

# Sending Messages To All Connected Clients
def broadcast(message, client0):
    if len(clients)==2:
        for client in clients:
            if client0!=client:
                client.send('MESSAGE'.encode('ascii'))
                client.send(message)

# Sending Messages To All Connected Clients
def broadcast2(message):
    if len(clients)==2:
        for client in clients:
            client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message, client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client.send('KEY'.encode('ascii'))
        key = rsa.PublicKey.load_pkcs1(client.recv(1024))
        
       
        keys.append(key)
        nicknames.append(nickname)
        clients.append(client)

        if(len(clients)==2):
            client.send('PARTNER'.encode('ascii'))
            client.send(keys[0].save_pkcs1("PEM"))
            #client.send('PARTNER-NAME'.encode('ascii'))
            #client.send(nicknames[0].encode())
            
            client2 = clients[0]
            client2.send('PARTNER'.encode('ascii'))
            client2.send(keys[1].save_pkcs1("PEM"))
            #client2.send('PARTNER-NAME'.encode('ascii'))
            #client2.send(nicknames[1].encode())
        else:
            print()
            


        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast2("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
