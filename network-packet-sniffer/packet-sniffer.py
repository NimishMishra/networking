import socket
import textwrap
import struct
import keras
from keras.models import Sequential, load_model
from keras.layers import Dense
from ids_google_colab_training import x_test


'''
    @PARAMS: the unformatted IP address
    @RETURN: the formatted IP

    This function converts the unformatted address data into the formatted IP, like xxx.yyy.zzz.www
'''

def format_IP_address(address):
    return '.'.join(map(str, address))

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

    Arrangement of the IP header (all numbers are in bytes, nibbles externally mentioned):


    Version-header-length    Type-of-service     Total Length
      1 [1 nibble each]           1                   2                  <-- 4 bytes slice: [0:3]

        Identification          IP flags         Fragment Offset
            2 bytes             1 nibble            1.5 nibbles          <-- 4 bytes slice: [4:7]

        Time to live          Protocol           Header Checksum         <-- 4 bytes slice: [8:11]
            2                     2                     2

                                    Source address
                                          4                              <-- 4 bytes [12:15]
                                    
                                    Destination address 
                                          4                              <-- 4 bytes [16:19]
'''


def unpack_IP_data(data):
    ip_version_header_length = data[0] # Pick the first byte that contains the IP version and the header length
    ip_version = ip_version_header_length >> 4 # Pick the first 4 bits (1st nibble) by removing the last 4 bits
    ip_header_length = (ip_version_header_length & 15) # Mask the entire byte by 00001111 and perform bitwise AND. It returns 0000ABCD so you get the 2nd nibble

    time_to_live, ip_protocol, source_ip, destination_ip = struct.unpack('! 8x B B 2x 4s 4s', data[:20]) #1
    return ip_version, ip_header_length, time_to_live, ip_protocol, format_IP_address(source_ip), format_IP_address(destination_ip), data[ip_header_length:] # the last argument is the data payload

def predict():
    print("The network connection is: normal" + str(model.predict(x_test)[0]))

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
    @PARAMS: the data to unpack
    @RETURN: the unpacked ICMP protocol

    This function unpacks the ICMP protocol packets
'''

def unpack_ICMP_protocol(data):
    icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
    return icmp_type, code, checksum, data[4:] # The last is the actual payload, after the header ended

'''
    @PARAMS: the data to unpack the TCP segment from
    @RETURN: the unpacked TCP packet

    This function returns the unpacked TCP segment.

    A typical TCP/IP packet looks like (1n = 1 nibble = 4 bits) Reference: https://nmap.org/book/tcpip-ref.html

    ------------------------------------------- 32 bits ----------------------------------------------
    ---------------- 16 bits ---------------------------- | ---------- 16 bits -----------------------
                                                          |                                           |
    Version (1n)  Length (1n)  Type of Service (8 bits)   |     Total length (16 bits)                |
                                                          |                                           |
                    Identification (16 bits)              | Flags (3 bits)  Fragment Offset (13 bits) |
                                                          |                                           |
    Time to live (8 bits)   Protocol (8 bits)             |       Header checksum (16 bits)           |  IPv4 Header
                                                          |                                           |
                                                    Source address (32 bits)                          |
                                                    Destination address (32 bits)                     |
                                                    Options (32 bits)                                 |
                                                    Data (32 bits)                                    |
    --------------------------------------------------------------------------------------------------

                   Source port (16 bits)                  |         Destination Port (16 bits)        |
                                                                                                      |
                                                   Sequence Number (32 bits)                          |
                                                 Acknowledgement number (32 bits)                     |
                                                                                                      |  TCP packet
    Offset (1n) Reserved (1n)  TCP flags (8 bits)         |             Window (16 bits)              |
                                                                                                      |
                    Checksum (16 bits)                    |          Urgent Pointer (16 bits)         |
                                                                                                      |
                                                   TCP options (32 bits)                              |
    ---------------- 16 bits ---------------------------- | ---------- 16 bits -----------------------
    ------------------------------------------- 32 bits ----------------------------------------------

    TCP flags: C E U A P R S F
        C: Reduced
        E: ECN Echo
        U: Urgent
        A: Ack
        P: Push
        R: Reset
        S: Syn
        F: Fin          
'''

def unpack_TCP_segment(data):
    # we have already unpacked the IP packet; now on to unpack the TCP packet
    (source_port, destination_port, sequence, ack, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14]) # H = 16 bits, L = 32 bits; total length = 14 bytes (count it)
    offset = (offset_reserved_flags >> 12) * 4 # right shift the entire thing 12 bits
    flag_urg = (offset_reserved_flags & 32) >> 5  # URGENT flag 
    flag_ack = (offset_reserved_flags & 16) >> 4  # Ack flag
    flag_psh = (offset_reserved_flags & 8) >> 3   # Push flag
    flag_rst = (offset_reserved_flags & 4) >> 2   # Reset flag
    flag_syn = (offset_reserved_flags & 2) >> 1   # Syn flag
    flag_fin = (offset_reserved_flags & 1)        # Fin flag

    return source_port, destination_port, sequence, ack, flag_ack, flag_fin, flag_psh, flag_rst, flag_syn, flag_urg, data[offset:]


'''
    @PARAMS: the data to unpack from
    @RETURN: the unpacked UDP packet

    This function unpacks the UDP packet and sends back the data

    The UDP header looks like: (https://nmap.org/book/tcpip-ref.html)

    ------------------------------------------- 32 bits ----------------------------------------------
    ---------------- 16 bits ---------------------------- | ---------- 16 bits -----------------------
                                                          |                                           |
                         Source port                      |         Destination Port                  |
                                                          |                                           |
                          Length                          |          Checksum                         |
                                                          |                                           |
    ---------------- 16 bits ---------------------------- | ---------- 16 bits -----------------------
    ------------------------------------------- 32 bits ----------------------------------------------


'''
def unpack_UDP_segment(data):
    source_port, destination_port, length = struct.unpack('! H H 2x H', data[:8]) # so we want the ports as is it, and the length
    return source_port, destination_port, length, data[8:]


def format_multi_line_data(prefix, string, size = 80):
    size -= len(prefix)
    if isinstance(string, bytes):
        string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
        if(size % 2):
            size -= 1
    return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])

# Defining lists to be used
connection_duration = {} #stores the mapping between the IP pair and the time of the connection
src_bytes = {}
dest_bytes = {}

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
        formatted_destination_address, formatted_source_address, formatted_protocol, data_after_frame_unpack = unpack_frames(raw_data)
        print('\nEthernet Frame:')
        print('\n\tDestination: {destination}, Source: {source}, Protocol: {proto}'.format(destination= formatted_destination_address, source= formatted_source_address, proto= formatted_protocol))
        
        if(formatted_protocol == 8): # working with IPv4

            # capture the entire IP header
            ip_version, ip_header_length, time_to_live, ip_protocol, ip_source, ip_destination, data_after_IP_unpack= unpack_IP_data(data_after_frame_unpack) 
            print("\tIPv4 packet: ")
            print("\t\tVersion: {version}, Header length: {length}, Time to live: {ttl}\n\t\tIP Protocol: {ip_protocol}, Source IP: {source}, Destination IP: {dest}".format(version= ip_version, length= ip_header_length, ttl= time_to_live, ip_protocol= ip_protocol, source= ip_source, dest= ip_destination))

            if(ip_protocol == 1): # there's ICMP data inside
                datapoint_protocol = 'icmp'
                icmp_type, code, checksum, data_after_ICMP_unpack = unpack_ICMP_protocol(data_after_IP_unpack)
                print("\tICMP packet: ")
                print("\t\tType:{type}, Code: {code}, Checksum: {checksum}".format(type=icmp_type,code=code, checksum=checksum))
                print("\t\tData: [Uncomment line in code to see the data here]")
                #print(format_multi_line_data("\t\t\t", data_after_ICMP_unpack))            
            elif(ip_protocol == 6): # there's TCP data inside
                datapoint_protocol = 'tcp'
                source_port, destination_port, sequence, ack, flag_ack, flag_fin, flag_psh, flag_rst, flag_syn, flag_urg, data_after_TCP_unpack = unpack_TCP_segment(data_after_IP_unpack)
                print("\tTCP Packet: ")
                print("\t\tSource Port:{source_port}, Destination port:{destination_port}, Sequence:{sequence}, Acknowledgement: {ack}".format(source_port=source_port, destination_port=destination_port, sequence=sequence, ack=ack))
                print("\t\tFlag ACK: {flag_ack}, Flag FIN: {flag_fin}, FLAG PSH: {flag_psh}, Flag RST: {flag_rst}, Flag SYN: {flag_syn}, Flag URG: {flag_urg}".format(flag_urg=flag_urg, flag_syn=flag_syn, flag_rst=flag_rst, flag_psh=flag_psh, flag_fin=flag_fin, flag_ack=flag_ack))
                print("\t\tData: [Uncomment line in code to see the data here]")
                #print(format_multi_line_data("\t\t\t", data_after_TCP_unpack))
            
            elif(ip_protocol == 17): # There's UDP data inside
                datapoint_protocol = 'udp'
                source_port, destination_port, length, data_after_UDP_unpack = unpack_UDP_segment(data_after_IP_unpack)
                print("\tUDP Packet: ")
                print("\t\tSource Port: {source_port}, Destination port: {dest_port}, Lenth: {length}".format(source_port=source_port, dest_port=destination_port,length=length))
                print("\t\tData: [Uncomment line in code to see the data here]")
                #print(format_multi_line_data("\t\t\t" ,data_after_UDP_unpack))
            


            ###############################################################################################

            # Predict the nature of this packet from the model trained, is it a part of malicious activity?
            # We'll extract the information required by the model one by one, and feed into the model

            '''
                Duration: 
                    - The length (number of seconds) of the connection
                    - HOW: Get the unique source, destination IP pairing and keep adding TIME_TO_LIVE
                Protocol Type
                    - Is the connection TCP, UDP, or ICMP
                    - Access the variable ip_protocol
                Service
                    - http, telnet etc.
                    - Don't know how to extract that as of now
                src_bytes
                    - number of data bytes from source to destination
                    - the data after unpacking particular protocol is of class bytes, meaning finding
                      length of the data gives the number of bytes transmitted
                    - create a dictionary and keep adding the value to get the total number of bytes transferred
                      within a time frame
                dest_bytes
                    - number of data bytes from destination to source
                    - same as above, just a different dictionary
                flag
                    - don't know any flag as raised here
                 
            '''
            datapoint = []
            source_destination_string = str(ip_source) + '-' + str(ip_destination)
            destination_source_string = str(ip_destination) + '-' + str(ip_source)

            # duration data point generation
            if (source_destination_string not in connection_duration.keys()):
                connection_duration[source_destination_string] = time_to_live
            else:
                connection_duration[source_destination_string] += time_to_live

            datapoint.append(connection_duration[source_destination_string]) 


            predict()


            

model = Sequential()
model.add(Dense(10, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(50, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(10, input_dim=120, kernel_initializer='normal', activation='relu'))
model.add(Dense(1, kernel_initializer='normal'))
model.add(Dense(23,activation='softmax'))

model = keras.models.load_model("best_model.model")
main_function_to_capture_stuff()
