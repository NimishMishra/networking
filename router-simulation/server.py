# Assuming the server resides in the network 92.10.10.0/24

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8000))
server.listen(2)

# having sample addresses for the server
server_ip = "92.10.10.10"
server_mac = "00:00:0A:BB:28:FC"

router_mac = "05:10:0A:CB:24:EF"

while True:
    routerConnection, address = server.accept()
    if(routerConnection != None):
        print(routerConnection)
        break

while True:
    ethernet_header = ""
    IP_header = ""
    
    message = input("\nEnter the text message to send: ")
    destination_ip = input("Enter the IP of the clients to send the message to:\n1. 92.10.10.15\n2. 92.10.10.20\n3. 92.10.10.25\n")
    if(destination_ip == "92.10.10.15" or destination_ip == "92.10.10.20" or destination_ip == "92.10.10.25"):
        source_ip = server_ip
        IP_header = IP_header + source_ip + destination_ip
        
        source_mac = server_mac
        destination_mac = router_mac 
        ethernet_header = ethernet_header + source_mac + destination_mac
        
        packet = ethernet_header + IP_header + message
        
        routerConnection.send(bytes(packet, "utf-8"))  
    else:
        print("Wrong client IP inputted")