import socket, threading, json, datetime
from colorama import Fore
from colorama import init

host = ''                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []

now = datetime.datetime.now()
now_text = now.strftime("%Y-%m-%d %H:%M")

file = open('password.json')
passwords = json.load(file)
file.close()

def logMessage(message):
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d %H:%M")
    f = open("log.log", 'a')
    f.write("[" +(str(now_text) + "] | " + str(message)[1:].strip("'") + '\n'))
    f.close()

def broadcast(message):   
    logMessage(message)                                             #broadcast function declaration
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            msg = message.decode().split(' ')
            if (msg[1] == '/ping'):
                broadcast(f'{Fore.RED}[*] - TG TU EST GAY - [*]'.encode())
            if(msg[1] == '/online'):
                listOfUser = (f'{Fore.GREEN}\n---------------------------------\nonline: ' + (str(nicknames).strip('[]').replace("'", '')) + '\n---------------------------------')
                broadcast(listOfUser.encode())
                broadcast('Online Count: {}\n'.format(len(clients)).encode('ascii'))

            print(message)
            broadcast(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{Fore.RED}[*] - [{nickname}] left the channel !'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break



def receive():                                                          #accepting multiple clients
    while True:
        print('[' + str(now_text) + ']' + f'{Fore.GREEN}[INFO]: Server is running and listening ...')
        client, address = server.accept()
        print(f"{Fore.GREEN}[CONNECTION]{Fore.RESET}" + ": Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        password = client.recv(1024).decode('ascii')
        if(nickname in passwords):
            if(passwords[nickname] == password):
                nicknames.append(nickname)
                clients.append(client)
                print(f"{Fore.BLUE}[NICK] : Nickname is {Fore.RED}"+'{}'.format(nickname)+rf"{Fore.RESET}")
                aaaaaaaa = (f'{Fore.GREEN}[*] - [' + nickname + ']' + ' : {} joined the channel !'.format(nickname)).encode('ascii')
                broadcast(aaaaaaaa)
                client.send('[INFO] : Connected to server!'.encode('ascii'))
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send(f"{Fore.RED}Wrong password".encode('ascii'))
        else:
            client.send(f"{Fore.RED}Wrong Username".encode('ascii'))

receive()
