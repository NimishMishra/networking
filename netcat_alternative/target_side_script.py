import socket

target_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects with the attacker 
def target_client_connector():
    # connect to the attacker
    attacker_hostname = "localhost"
    attacker_port = 1234
    while(True):
        success = target_client.connect_ex((attacker_hostname, attacker_port))
        if(not success):
            # connection established successfully
            break

def send_data(data):
    # receive data from the attacker server
    target_client.send(bytes("ACK", 'utf-8'))

def receive_data():
    # receive data from the attacker server
    data = target_client.recv(1024)
    print(data)
    target_client.send(bytes("ACK", 'utf-8'))

def main():
    # connect to the attacker
    target_client_connector()
    receive_data()

main()