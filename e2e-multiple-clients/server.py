import socket
import threading
import rsa


# Connection Data
host = '127.0.0.1'
port = 65535

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
keys = []
partners = []

def ind(list, client):
    try:
        index = list.index(client)
        return index
    
    except:
        return -1

# Sending Messages To All Connected Clients
def broadcast(message, client0):
    index = clients.index(client0)
    client = partners[index]
    client.send('MESSAGE'.encode('ascii'))
    client.send(message)

# Sending Messages To All Connected Clients
def broadcast2(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            index0 = clients.index(client)
            print(nicknames[index0])
            #print(message)
            if(message!=b''):
             broadcast(message, client)
        except:
            # Removing And Closing Clients
            index1 = ind(clients, client)
            if(index1==-1): break
        
            index2 = ind(partners, client)
            
            if(index2!=-1):
                client2 = clients[index2]
                client2.send('CLOSE'.encode('ascii'))
                clients.remove(client)
                clients.remove(client2)
                partners.remove(client)
                partners.remove(client2)
                client.close()
                client2.close()
                nickname = nicknames[index1]
                nickname2 = nicknames[index2]
                nicknames.remove(nickname)
                nicknames.remove(nickname2)
                key1 = keys[index1]
                key2 = keys[index2]
                keys.remove(key1)
                keys.remove(key2)
                break
            clients.remove(client)
            client.close()
            nickname = nicknames[index1]
            #broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            key1 = keys[index1]
            keys.remove(key1)

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

        i = len(clients)

        if(i!=0 and i%2==0):
            client.send('PARTNER'.encode('ascii'))
            client.send(keys[i-2].save_pkcs1("PEM"))
            print(key)
            client2 = clients[i-2]
            client2.send('PARTNER'.encode('ascii'))
            client2.send(keys[i-1].save_pkcs1("PEM"))
            partners.append(client)
            partners.append(client2)
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
