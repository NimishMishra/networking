# this script does not work. It is a skeleton

import socket

# skeleton of a simple server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("hostname", "port number here"))
server.listen(5)


while True:
    client, addr = server.accept()  # Blocking operation this is

    # receive data from the client
    request = client.recv(1024) # (alter.) recvfrom() for UDP sockets

    # send data to client
    client.send(bytes("data", 'utf-8'))

    #close the socket. Takes over a minute or two 
    client.close()