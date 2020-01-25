#!/bin/python3

import sys # (system functions and parameters)for command line arguments
from datetime import datetime as dt
import socket # for establishing connections

# Define the target to scan the ports on
# will be taken through the command line

if(len(sys.argv) == 2): # argv[0] = script name; argv[1] = hostname
    target = socket.gethostbyname(sys.argv[1]) # translates a host name to IPv4

else:
    print("Host name not provided")
    sys.exit(42) # Status returns to parent process

print("Scanning target: " + target + " starting at " + str(dt.now()))

try:
    for port in range(1, 1024):

        # create a IPv4 socket   
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # if the port is not open, move on after a second.
        # else the system hangs unitl some activity is detected
        socket.setdefaulttimeout(1)

        result = s.connect_ex((target, port)) # returns error indicator
        # returns 0 is there is no error on connection 
        print("Checking port {port}".format(port=port))
        if(result == 0):
            print("Open port detected: Port {port}".format(port=port))
            s.close()
except KeyboardInterrupt:
    print("Exiting port scanning")
    sys.exit(42)

except socket.gaierror:
    print("Hostname could not be resolved")
    sys.exit()

except socket.error:
    print("Could not establish connection to server")
    sys.exit()