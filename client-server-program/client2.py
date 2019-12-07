import socket


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((socket.gethostname(), 8000))

final_message = ""

while True:
    final_message = ""
    new_message = True
    while True:    
        message = connection.recv(10)
        if(new_message):
            # get the first 10 bytes that has the header length
            messageLength = int(message[0:10])
            new_message = False
        else:
            final_message = final_message + message.decode("utf-8")
            print(len(final_message))
            print((messageLength))
            if(len(final_message) - messageLength == 0):
                break

    print(final_message)