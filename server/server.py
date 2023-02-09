import socket, threading, json, datetime
from colorama import Fore, init

host = ''
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []

last_message_per_user = { }

now = datetime.datetime.now()
now_text = now.strftime("%Y-%m-%d %H:%M")

file = open('password.json')
passwords = json.load(file)
file.close()


#log to a file
def logMessage(message):
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d %H:%M:%S")
    f = open("log.log", 'a')
    f.write("[" +(str(now_text) + "] | " + str(message)[1:].strip("'") + '\n'))
    f.close()


#send message to client
def broadcast(message):   
    logMessage(message)
    for client in clients:
        client.send(message)


#receive message
def handle(client):                                         
    while True:
        try:    
            now = datetime.datetime.now() 
            diff = now - last_message_per_user[client]
            message = client.recv(1024)
            #anti spam system
            print(diff.total_seconds()*60*60)
            if diff.total_seconds()*60*60 > 0.25:
                now = datetime.datetime.now()
                msg = message.decode().split(' ')
                last_message_per_user[client] = now
                
                if(msg[1] == '/online'):
                    listOfUser = (f'{Fore.GREEN}\n---------------------------------\n[ONLINE]: ' + (str(nicknames).strip('[]').replace("'", '')))
                    client.send(listOfUser.encode())
                    client.send('\n[Online Count]: {}\n'.format(len(clients)).encode())
                    client.send(f'---------------------------------{Fore.RESET}'.encode())
                    
                else:
                    now_text = now.strftime("%H:%M")
                    print(message)
                    messageTxt = f'{Fore.GREEN}[' + now_text + '] ' + message.decode()
                    broadcast(messageTxt.encode())
            else:
                client.send(f'{Fore.RED}[*] - TG ARRETE DE SPAM PETIT BERBERE - [*]{Fore.RESET}'.encode())
        except:                                                         #removing clients
            index = clients.index(client)
            last_message_per_user[client] = None
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{Fore.RED}[*] - [{nickname}] left the channel !{Fore.RESET}'.format(nickname).encode())
            nicknames.remove(nickname)
            break


#link client with server at the start
def receive():
    while True:
        print('[' + str(now_text) + ']' + '[INFO]: Server is running and listening ...')
        client, address = server.accept()
        print("[CONNECTION]" + ": Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode())
        nickname = client.recv(1024).decode()
        password = client.recv(1024).decode()
        #password system here
        if(nickname in passwords):
            if(passwords[nickname] == password):
                nicknames.append(nickname)
                last_message_per_user[client] = datetime.datetime.now()
                clients.append(client)
                print("[NICK] : Nickname is "+'{}'.format(nickname))
                aaaaaaaa = (f'{Fore.GREEN}[*] - [' + nickname + ']' + ' : {} joined the channel !'.format(nickname)).encode()
                broadcast(aaaaaaaa)
                client.send('[INFO] : Connected to server!'.encode())
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            else:
                client.send(f"{Fore.RED} Wrong password{Fore.RESET}".encode())
        else:
            client.send(f"{Fore.RED} Wrong Username{Fore.RESET}".encode())

receive()