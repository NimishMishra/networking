import socket

# the similar socket as the server established
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# you are connecting to the server socket on the same machine
connection.connect((socket.gethostname(), 8000))

full_msg = ''

while True:
    # receive the data, with a buffer size 1024 bytes
    message = connection.recv(8)
    print(len(message))
    # decode the message and add that to the main string
    full_msg = full_msg + message.decode("utf-8")
    if(full_msg[-1] == "!"):
        break

print(full_msg)