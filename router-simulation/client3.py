import socket
import time

client3_ip = "92.10.10.25"
client3_mac = "AF:04:67:EF:19:DA"

router = ("localhost", 8200)
client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

time.sleep(1)
client3.connect(router)

while True:
    received_message = client3.recv(1024)
    received_message = received_message.decode("utf-8")
    source_mac = received_message[0:17]
    destination_mac = received_message[17:34]
    source_ip = received_message[34:45]
    destination_ip =  received_message[45:56]
    message = received_message[56:]

    print("\nPacket integrity:\ndestination MAC address matches client 3 MAC address: {mac}".format(mac=(client3_mac == destination_mac)))
    print("\ndestination IP address matches client 3 IP address: {mac}".format(mac=(client3_ip == destination_ip)))
    print("\nThe packed received:\n Source MAC address: {source_mac}, Destination MAC address: {destination_mac}".format(source_mac=source_mac, destination_mac=destination_mac))
    print("\nSource IP address: {source_ip}, Destination IP address: {destination_ip}".format(source_ip=source_ip, destination_ip=destination_ip))
    print("\nMessage: " + message)
    print("***************************************************************")