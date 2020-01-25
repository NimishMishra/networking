import socket

target_host = "www.google.com" # This shall be resolved by DNS
target_port = 80 # the web server sitting on the above IP

#create a socket
# AF_INET: IPv4 socket
# SOCK_STREAM: TCP client up here
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

result = client.connect_ex((target_host, target_port))
if(result == 0):
    client.send(bytes("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n", 'utf-8'))
    data = client.recv(4096)
    print(data)
