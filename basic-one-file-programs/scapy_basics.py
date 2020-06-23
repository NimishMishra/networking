# scapy needs root privelege for raw sockets, thus run with sudo

from scapy.all import *


def callback(packet):
    print(packet.show())
    print("-----------------")

# sniff(filter="", iface="", prn=function, count=N)
# filter: filter to the packets that scapy sniffs
# iface: the network interface on which to sniff
# prn: function callback for a matching packet
# count: frequency

sniff(prn=callback, count=10)  # the first two are left blank so no filter 
                                # means sniff all packets and no iface means on all interfaces


def extract_info(packet):

    try:
        if(packet[TCP].payload):

            mail_packet = str(packet[TCP].payload)

            if("user" in mail_packet.lower() or "pass" in mail_packet.lower()):
                print(mail_packet)
                print(packet[IP].dst)
                print(packet[TCP].payload)
    except Exception as e:
        print(str(e))


# sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=extract_info, store=0)
# sniff(filter="", prn=extract_info, store=0)


def discover_nodes(ip_address):

    # ARP ping method to discover nodes on a local ethernet network

    ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=2)
    print(ans.summary())

    # arping(ip_address) # performs both the 

# discover_nodes("192.168.43.34")

def generate_new_packets():
    # creating packets by simple concatenation 

    packet = Ether()/IP(dst="www.wikipedia.org")/TCP()/"GET /index.html HTTP/1.0 \n\n"
    print(packet.show())
    load = packet[Raw]
    print(load)
    print(hexdump(load))

# generate_new_packets()


def SYN_scan(ip_address):
    # a port scan for SYN responses, or to see which ports return
    # a SYN

    packet = IP(dst=ip_address)/TCP(dport=(100, 200), flags="S")
    answered, unanswered = sr(packet)
    print(answered.summary())

#SYN_scan("192.168.43.34")