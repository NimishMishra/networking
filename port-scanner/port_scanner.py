from scapy.all import *
import sys

# Flags:
# SYN: first step in three way handshake
# ACK: acknowledge receipt of packet
# FIN: no more data to send
# URG: the received packets are urgent
# PSH: similar to URG
# RST: sent from receiver to sender when a packet is sent to a particular host that was not expecting it


START_PORT = 10
END_PORT = 10000

def discover(target_ip_range, time):
    ethernet_layer = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_layer = ARP(pdst= target_ip_range)
    ans, unans = srp(ethernet_layer/arp_layer, timeout=time, verbose=0)

    for sent, received in ans:
        print("[*] " + received[ARP].psrc)


def TCP_connect_scan(target_ip_address):
    # Three way handshake.
    # 1. Send SYN
    # 2. Receive SYN + ACK (0x12)
    # 3. Send ACK

    # Connection refused by target port.
    # 1. Send SYN
    # 2. Receive RST (the port wasn't expecting this connection and didn't send a SYN)
    open_ports = ""
    reset_flag_count = 0
    tcp_missing_count = 0
    for i in range(START_PORT, END_PORT, 1):
        ip_layer = IP(dst=target_ip_address)
        tcp_layer = TCP(dport=i, flags= "S")
        response = sr1(ip_layer/tcp_layer, timeout=1, verbose=0)

        try:
            flags_list = list(response['TCP'].flags)
            if("S" in flags_list and "A" in flags_list):
                tcp_layer = TCP(dport=i, flags= "A")
                response = sr(ip_layer/tcp_layer, timeout=1, verbose=0)
                open_ports = open_ports + str(i) + ", "
            elif("R" in flags_list):
                reset_flag_count = reset_flag_count + 1
        except:
            tcp_missing_count = tcp_missing_count + 1
    
    return tcp_missing_count, reset_flag_count, open_ports


def main():
    
    # discover('192.168.43.1/24', 10)
    # everything on 192.168.43.34

    tcp_missing_count, reset_flag_count, open_ports = TCP_connect_scan('192.168.43.34')

    print("******* TCP connect scan report *************")
    print("TCP header missing in " + str(tcp_missing_count) + " ports' responses")
    print("RST flag received from: " + str(reset_flag_count) + " ports")
    print("Open ports: " + open_ports)
    print("*********************************************")


main()