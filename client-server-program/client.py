import socket

# the similar socket as the server established
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# you are connecting to the server socket on the same machine
connection.connect((socket.gethostname(), 8080))

# receive the data, with a buffer size 1024 bytes
message = connection.recv(1024)

# decode the message
print(message.decode("utf-8"))