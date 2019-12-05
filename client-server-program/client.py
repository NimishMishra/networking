import socket

# the similar socket as the server established
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# you are connecting to the server socket on the same machine
connection.connect((socket.gethostname(), 8080))

full_msg = ''

while True:
    # receive the data, with a buffer size 1024 bytes
    message = connection.recv(8)
    print(len(message))
    if(len(message) <= 0):
        break
    # decode the message and add that to the main string
    full_msg = full_msg + message.decode("utf-8")


print(full_msg)