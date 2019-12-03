# this script isn't completed yet


#!/bin/python3 

import sys    # for command line arguments
import socket # setting up a port connection
from datetime import datetime as dt

# definition of the target through CLI argument

if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1]) # translate a host name to IPv4
    

else:
    print("Invalid amount of arguments")
    sys.exit()

print("." * 50)
print("Target: " + target)
print("Time scanning started:" + str(dt.now()))
print("." * 50)


try:
    for port in range(50, 85):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
