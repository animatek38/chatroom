import socket, threading, sys, datetime, sys, msvcrt
from colorama import Fore, init
from pythonping import ping
init()


print(rf"""{Fore.GREEN}
   _____ _           _   _____                       
  / ____| |         | | |  __ \                      
 | |    | |__   __ _| |_| |__) |___   ___  _ __ ___  
 | |    | '_ \ / _` | __|  _  // _ \ / _ \| '_ ` _ \ 
 | |____| | | | (_| | |_| | \ \ (_) | (_) | | | | | |
  \_____|_| |_|\__,_|\__|_|  \_\___/ \___/|_| |_| |_|    
                             | Created by animatek#7217
                             |            yourSUS#3956
                             |            fri2cool#4192
                            
{Fore.RESET}""")

ip = input(f'{Fore.CYAN} IP adress:{Fore.RESET} ')
nickname = input(f"{Fore.CYAN}\n Username:{Fore.RESET} ")
password = input(f"{Fore.CYAN} Password:{Fore.RESET} ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((ip, 7976))       

last_message_sent = ""  

current_message = ""      #connecting client to server

def write():
    while True:
        msg = input('')
        if(msg != ''):
            now = datetime.datetime.now()
            now_text = now.strftime("%H:%M:%S")
            if(msg.lower() == '/ping'):
                response_list = ping(ip, size=32, count=3)
                # print(f'{Fore.RED}[*] -' + str(response_list.rtt_avg) + f'- [*]{Fore.RESET}')

                #/ping to ping the server connected to 
                print(f'{Fore.CYAN}[*] The ping is: {Fore.RESET}{Fore.YELLOW}' + str(response_list.rtt_avg_ms) + f' ms{Fore.RESET}')
            else:
                message = f'{Fore.CYAN}[{nickname}]{Fore.RESET}: {msg}'
                #last_msg_clean = message.split(" ")
                #last_msg_clean.pop(0)
                global last_message_sent
                last_message_sent = message
                remove_txt = ""
                for i in range(len(message)):
                    remove_txt = remove_txt + " "
                print ("\033[A" + remove_txt + "\033[A")
                client.send(message.encode())

def receive():
    while True:                                                #making valid connection
        try:
            message = client.recv(1024).decode()
            if message == 'NICKNAME':
                client.send(nickname.encode())
                client.send(password.encode())
            elif(message.startswith(("[" + nickname + ']'))):
                pass
            else:
                msg_clean = message.split(" ")
                msg_clean.pop(0)
                if last_message_sent == ' '.join(msg_clean):
                    print(f'{Fore.RED}--> {Fore.RESET}' + message)
                else:
                    print(message)
        except:                                                 #case on wrong ip/port details
            print(rf"{Fore.RED}[*] - An error occured! - [*]{Fore.RESET}")
            client.close()
            break

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()