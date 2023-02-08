import socket, threading, json

host = ''                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []

BLACK=30
RED=31
GREEN=32
YELLOW=33
BLUE=34
MAGENTA=35
CYAN=36
WHITE=37

def color(text: str, textColor: int, bg: int):
    bg = str(bg+10)
    textColor = str(textColor)
    result = '\x1b[0;'+textColor+';'+bg+'m' + text + '\x1b[0m'
    return result


file = open('password.json')
passwords = json.load(file)
file.close()

def logMessage(message):
    f = open("log.log", 'a')
    f.write((str(message)[1:].strip("'") + '\n'))
    f.close()


def broadcast(message):
    print(message)
    logMessage(message)
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                
            message = client.recv(1024)                               #recieving valid messages from client
            msg = message.decode().split(' ')
            if (msg[1] == '/ping'):
                broadcast(color("[*] - TG TU EST GAY - [*]".encode(), RED, BLACK))
            if(msg[1] == '/online'):
                listOfUser = ('---------------------------------\nonline: ' + (str(nicknames).strip('[]').replace("'", '')) + '\n---------------------------------')
                listOfUser = color(listOfUser, RED, BLACK)
                broadcast(listOfUser.encode())
                
            broadcast(message)

        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('[*] - {} left!'.format(nickname).encode('ascii'))
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
