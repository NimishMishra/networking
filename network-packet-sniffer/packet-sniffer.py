import socket
import textwrap
import struct

'''
    @PARAMS: program to help extract the IP header data
    @RETURN:

    Find the image reference: https://nmap.org/book/tcpip-ref.html

    Things to extract here:

    IP Version: 
    Protocol:
    Source IP:
    Destination IP:
    Header length: Gives the length of the entire IP header. So you know where the data starts, so you can slice accordingly

    Arrangement of the IP header:

    Version-header-length
      1 [1 nibble each]                  

'''


def unpack_IP_data(data):
    ip_version_header_length = data[0] # Pick the first byte that contains the IP version and the header length
    ip_version = ip_version_header_length >> 4 # Pick the first 4 bits (1st nibble) by removing the last 4 bits
    ip_header_length = (ip_version_header_length & 15) # Mask the entire byte by 00001111 and perform bitwise AND. It returns 0000ABCD so you get the 2nd nibble

    time_to_live, ip_protocol_ source_ip, destination_ip = struct.unpack('! 8x B B 2X 4s 4s', data[:20]) #1


'''
    @ PARAMS: mac_address (the sniffed MAC address)
    @ RETURN: the formatted mac address

    Currently, the sniffed mac address using the unpack frames method isn't human readable.
    That needs to be done, in some format like XX:XX:XX:XX:XX:XX (48 bit MAC address, arranged as 6 pairs of 12 bytes, hexadecimal format)
'''
def format_address(mac_address):
    formatted_mac_address = map('{:02X}'.format, mac_address) #:02X format will convert into captialized hexadecimal format
    # map takes the current mac_address and formats into the desired format
    formatted_mac_address = ':'.join(formatted_mac_address) # joins the little chunks AA, BB, CC etc into AA:BB:CC:...
    return formatted_mac_address



'''
    @PARAMS: data (the data, either from the computer to the router, or from the router to the computer)
    @RETURN: the formatted MAC addresses and the remaining data

    This function aids to unpack the ethernet frame to extract useful information.
    ETHERNET FRAME:

    SYNC   Receiver   Sender   Type    Payload    CRC
      8       6         6       2      46-1500     4   (all are in bytes)

    SYNC: electronic information that looks to ensure the computer and the router are in synchronization
    CRC: information that looks to ensure the data is trasmitted correctly, maybe error correcting codes
    Receiver: contains the receiver information
    Sender: contains the sender information
    Type: the ethernet protocol type
        0x0800: IPv4 frame
        0x0806: ARP request/response
        0x86DD: IPv6 frame
'''
def unpack_frames(data):
    # we'll use STRUCT to convert data (data format stored in our computer is different from how it flows across a network, computer -> little endian, network -> big endian)
    
    modified_data = data [:14] # picking up the first 14 bytes of data
    remaining_data = data[14:]
    receiver_mac_address, sender_mac_address, protocol = struct.unpack('! 6s 6s H', modified_data) # ! = designates that THIS is the network data we are processing, and breaking into 6 bytes, 6 bytes, and protocol type
    formatted_receiver_mac_address = format_address(receiver_mac_address)
    formatted_sender_mac_address = format_address(sender_mac_address)
    formatted_protocol = socket.htons(protocol) # makes sure we are endian compatible (little endian as our modern computers process out things)
    return formatted_receiver_mac_address, formatted_sender_mac_address, formatted_protocol, remaining_data



'''
    @PARAMS: none
    @RETURN: ...

    This function basically serves to setup the connections and start sniffing network traffic
    This is a complex function, hence I provide a detailed documentation and report:
    
    SOCKETS: python module to help two nodes on a network communicate with each other

    Normal layers in a typical network setup:
    Ethernet Layer Processing --> IP Layer Processing --> Transport Layer Processing --> Socket Interface --> User application
            |                                                       |
            |                                                       |
            |                                                       |
            V                                                       V
        Raw sockets                                             Other sockets
        receive data                                            receive data from
        from here                                                  here

    #1  the socket family has a component that can be used to set up a RAW SOCKET (basically a raw connection between the computer and the router)
        This raw connection bypasses the normal TCP/IP protocol. Thus the ethernet network packets are directly captured by this application, without being
        processed by the TCP/IP protocols.

        WHY raw sockets and NOT stream sockets or data gram sockets?
            Because the others receive data from the transport layer, meaning they have only the payload and no headers.
            No headers mean no information about the source, destination IP and MAC addresses

        socket.htons() --> serves to convert the data into big-endian or little-endian as desired

    #2  
'''

def main_function_to_capture_stuff():
    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3)) #1

    while True: # this runs forever and collects the data coming across the network into the raw socket we established
        raw_data, address = connection.recvfrom(65536) # @PARAM: the max buffer size: 65535
        formatted_destination_address, formatted_source_address, formatted_protocol, remaining_data = unpack_frames(raw_data)
        print('\nEthernet Frame:')
        print('\n\tDestination: {destination}, Source: {source}, Protocol: {proto}'.format(destination= formatted_destination_address, source= formatted_source_address, proto= formatted_protocol))
        




main_function_to_capture_stuff()