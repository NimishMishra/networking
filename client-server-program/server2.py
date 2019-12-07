# this client-server program is for streaming data


import socket

message = "Welcome to the server"

# here we aim to generate a header that contains the length of the message
# max length = 10 (means 10 positions, or 10^10 numbers)
# like 0, 1, 2, 3, 4, ...., 9999999999
# this denotes the length of the message being transferred and thus the 
# buffer size to be used

length = len(message)
header = "" + str(length) + " " * (10 - len(str(length)))
print(header)

final_message = header + message
print(final_message)


# set up a server
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind((socket.gethostname(), 8000))
connection.listen(5)

while True:
    # accept a connection
    connectedsocket, address = connection.accept()
    print("Connection to {address} establised".format(address=address))

    # send the data
    connectedsocket.send(bytes(final_message, "utf-8"))
