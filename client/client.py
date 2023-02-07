import socket, threading, sys
ip = input('quelle address: ')
nickname = input("[WELCOME] \nThe best command-line server \n\nChoose your nickname: ")
password = input("and your password: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((ip, 7976))                             #connecting client to server

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
                client.send(password.encode('ascii'))
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break
def write():
    while True:                                                 #message layout
        message = '[{}]: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()