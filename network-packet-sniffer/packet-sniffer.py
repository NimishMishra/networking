import socket
import textwrap
import struct


'''
    @ PARAMS: mac_address (the sniffed MAC address)
    @ RETURN: the formatted mac address

    Currently, the sniffed mac address using the unpack frames method isn't human readable.
    That needs to be done, in some format like XX:XX:XX:XX:XX:XX (48 bit MAC address, arranged as 6 pairs of 12 bytes, hexadecimal format)
'''
def format_address(mac_address):
    formatted_mac_address = map('{:02X}'.format, mac_address) #:02X format will convert into captialized hexadecimal format
    


'''
    @PARAMS: data (the data, either from the computer to the router, or from the router to the computer)
    @RETURN:

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
