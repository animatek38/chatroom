import socket, threading, json

host = '192.168.1.13'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []

file = open('password.json')
passwords = json.load(file)
file.close()


def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            print(message)
            broadcast(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():                                                          #accepting multiple clients
    while True:
        print('[INFO] : Server is running and listening ...')
        client, address = server.accept()
        print("[CONNECTION] : Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        password = client.recv(1024).decode('ascii')
        if(nickname in passwords):
            if(passwords[nickname] == password):
                nicknames.append(nickname)
                clients.append(client)
                print("[NICK] : Nickname is '{}'".format(nickname))
                aaaaaaaa = ("[" + nickname + "]" + " : {} joined!".format(nickname)).encode('ascii')
                broadcast(aaaaaaaa)
                # client.send('[INFO] : Connected to server!'.encode('ascii'))
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send('mauvais mot de passe'.encode('ascii'))
        else:
            client.send('mauvais pseudo'.encode('ascii'))

receive()