# Bug Hunting

## Books

- `The web application hacker's handbook`

- `OWASP testing guide`

- `Web hacking 101`

- `Breaking into information security`

- `Mastering modern web penetration testing`

## Recon

### Discovering IP space

Finding an organisation's autonomous system number (the IP ranges they have registered) is the first step to start with. Go on to `Hurricane electric internet services`(https://bgp.he.net/) and find the organisation's space.

Or use the CLI tool `dig`.

### Online databases

**RIPE and ARIN**: Online databases for whois lookups.	

**Shodan**: Available at `shodan.io`

Some CLI tools for doing domain lookups:

```
nmap -T4 -p 53 --script dns-brute canva.com

dnsenum --noreverse -o file.xml securitytrails.com
dnsenum --dnsserver ns3.p16.dynect.net github.com -p 10 -s 50

host securitytrails.com
host -t ns securitytrails.com
host -t axfr securitytrails.com ns08.domaincontrol.com (DNS transfer)
host -l zonetransfer.me nsztm1.digi.ninja

dig axfr securitytrails.com ns08.domaincontrol.com
dig securitytrails.com +short
```
### Brand discovery

In programmes that have a wide scope, sometimes you might wish to find domains that are related to the current attack domain. Some ways to find such things:

1. Acquisitions: If a company is acquired by another company, you may look into this too. `Wikipedia` and `crunchbase acquisitions section` help with this thing. These sites stay up to date because people use these for stock exchanges.

2. 
