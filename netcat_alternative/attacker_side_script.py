import socket

attacker_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

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
    print("Connection established to " + str(target_client.getpeername()))
    return target_client


# connects to the client being targeted
def send_data(data, target_client):

    
    target_client.send(bytes(data, 'utf-8'))

    response = target_client.recv(1024)
    print(response)

    if(response == b'ACK'):
        print("Data received at target end")


def receive_data():
    pass

def main():
    attacker_server_binder("localhost", 1234)

    # receive connection from target client
    target_client = target_client_connection_receiver()

    send_data("ABCD", target_client)

main()