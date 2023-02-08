import socket, threading, sys, datetime
from colorama import Fore
from colorama import init
init()


print(rf"""{Fore.GREEN}
   _____ _           _   _____                       
  / ____| |         | | |  __ \                      
 | |    | |__   __ _| |_| |__) |___   ___  _ __ ___  
 | |    | '_ \ / _` | __|  _  // _ \ / _ \| '_ ` _ \ 
 | |____| | | | (_| | |_| | \ \ (_) | (_) | | | | | |
  \_____|_| |_|\__,_|\__|_|  \_\___/ \___/|_| |_| |_|    
                             | Created by animatek#7217
                             | Created by yourSUS#3956
                             | Created by fri2cool#4192
                            
{Fore.RESET}""")

ip = input(f'{Fore.CYAN} IP adress:{Fore.RESET} ')
nickname = input(f"{Fore.CYAN}\n Username:{Fore.RESET} ")
password = input(f"{Fore.CYAN} Password:{Fore.RESET} ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((ip, 7976))                             #connecting client to server
 

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
                client.send(password.encode('ascii'))
            elif(message.startswith(("[" + nickname + ']'))):
                pass
            else:
                print(message)
                # print('[' + nickname + '] :', end='')
        except:                                                 #case on wrong ip/port details
            print(rf"{Fore.RED}[*] - An error occured! - [*]")
            client.close()
            break

        
def write():
    while True:
        msg = input('')
        if(msg != ''):
            now = datetime.datetime.now()
            now_text = now.strftime("%H:%M:%S")
            message = f'{Fore.GREEN}[' + str(now_text) + ']' + f'{Fore.CYAN}[{nickname}]{Fore.RESET}: {msg}'
            client.send(message.encode('ascii'))



receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()