# Beginner Penetration Tester

[Youtube link](https://www.youtube.com/watch?v=WnN6dbos5u8)

[Github link](https://github.com/hmaverickadams/Beginner-Network-Pentesting)

# Week 4

## Passive recon: OSINT (Open Source Intelligence)

Recon wherein you do not actively engage with the target. You gather information about the target from external sources like social media or websites. An image about office workspace can give ideas about letterheads, badges etc. which may be cloned for further impersonation.

    1. Target validation: WHOIS, nslookup, dnsrecon

    2. Finding subdomains: Google Fu, dig, nmap, sublist3r, bluto, crt.sh

    3. Fingerprinting: nmap, wappalyzer, whatweb, builtwith, netcat

    4. DataBreaches: HaveIbeenPwned 


`hunter.io` finds email addresses related to a domain as well as the most common pattern of those emails. List of [1.4 billion passwords in plaintext](https://github.com/philipperemy/tensorflow-1.4-billion-password-analysis). If you get a list of breached passwords here, you might get into the way of how people develop these passwords.

Going to the website is also a good thing (if there is one). There are a lot of cool information to find: `contacts`, `satellite images` (yeah Google maps and street views can be really informative in some cases: the security, the parking, the backdoors, the map etc.), `people` (compare with `hunter.io` or the data breach information you have). Search facebook, linkedin, twitter, and others.

Some Google searches:

```s
site:upwork.com -www
site:upwork.com filetype:pdf
```

Automating all these:

```s
theHarvester -d upwork.com -l 500 -b google
```

Go to `crt.sh` and search the domain `%.upwork.com` to get the certificates as well as all the domains related to the search term.

## Active recon

`Bluto`: DNS zone transfers, DNS recons, and more others. Shows the `name` and `mail` servers. It functions as a brute forcer of subdomains too: given the domain `xyz.com` and it goes through all the subdomains in a wordlist and tries to `GET` `word.xyz.com` and analyze the HTTP response codes. At the end, it displays the ones found. This is quite similar to brute forcing directories in websites.

Web scanner (yields IP, cookies, and lots more...)

```s
whatweb -v upwork.com
```


### Fingerprinting

Can use `nmap` or `builtwith` for websites