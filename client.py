import socket
import sys 
import selectors
import select
import argparse
from urllib.parse import urlparse

#sel = selectors.DefaultSelector()

def main(path, username):
    url = urlparse(path)
    serverPort = url.port
    serverName = url.hostname
    print('Connecting to server...')
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.setblocking(False)
    print('Connection to server established. Sending intro message...')
    clientSocket.send(username.encode())
    #sel.register(clientSocket,selectors.EVENT_READ | selectors.EVENT_WRITE,)


    print("Registration successful. Ready for Messaging!")
    while True:
        sockets_list = [sys.stdin, clientSocket]
        clientSocket.setblocking(False)
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

        for socks in read_sockets:
            if socks == clientSocket:
                message = socks.recv(1024)
                print(message.decode())
            else:
                message = sys.stdin.readline()
                message = "@" + username + " " + message
                clientSocket.send(message.encode())
                #print("<You>" + message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Client')
    parser.add_argument('path',type=str)
    parser.add_argument('username',type=str)
    arguments= parser.parse_args()
    main(arguments.path, arguments.username)
## random