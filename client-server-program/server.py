import socket

# opening a socket of:
# AF_INET: AF = address family, INET = internet. So AF_INET allows communication over IPv4 protocol
# SOCK_STREAM: a streaming socket that receives information from the transport layer of the OSI
#               model
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# socket is an entity that receives and sends data. Socket sits at an IP and a port. This is
# done by the bind function: gethostname() is getting the hostname.
connection.bind((socket.gethostname(), 8080))

# since we are creating a server, this server should be able to LISTEN to requests coming to it.
# If it is under heavy load, we maintain a queue of 5 at a time
connection.listen(5)



while True:
    # so accept() serves to receive a connection. We receive an object of CONNECTEDSOCKET
    # and ADDRESS of the socket received. 
    connectedsocket, address = connection.accept()
    print("Connection from {address} established".format(address = address))
    
    # to send some data to the client, here you go:
    # first argument: the data in bytes, second argument: the encoding
    connectedsocket.send(bytes("Welcome to my server", "utf-8"))