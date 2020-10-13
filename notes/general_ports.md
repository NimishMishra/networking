# General ports

# General information

- SSL/TLS certificates allow HTTP websites to be served below TLS (HTTPS = HTTP + TLS). The main difference is SSL makes **explicit** connections via a port, while TLS makes **implicit** connections via a protocol. SSL is secure socket layer while TLS is transport layer security. Both of SSL and TLS certs are **X.509** certificates that help to authenticate the server and facilitate the handshake process to create a secure connection. 

- [Brute-force cheatsheet](https://book.hacktricks.xyz/brute-force)

# Information about general ports.

# Port 110

- POP3

# Port 143

- IMAP (Internet message access protocol) **receives** email from a server. IMAP SSL communication happens on port 993. There can be, however, TLS on port 143. Since being plaintext on 143, command-based retrival of emails can be done.


- Useful commands:

```s
nc -nv 10.10.10.197 143

nmap --script=/usr/share/nmap/scripts/imap-ntlm-info.nse 10.10.10.197 -p143 -sV -sC (get the info)

nmap --script=/usr/share/nmap/scripts/imap-brute.nse 10.10.10.197 -p143 (brute force creds)

login <TYPE MAIL HERE> <TYPE PASSWORD HERE>


```