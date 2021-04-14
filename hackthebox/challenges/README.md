# Challenges

## OSINT

The idea is to engage with data in publicy available domains to get a sense of the target in general.

### Easy Phish

[Easy Phish](https://app.hackthebox.eu/challenges/Easy-Phish)

```sh
Customers of secure-startup.com have been recieving some very convincing phishing emails, 
can you figure out why?
```
- The host is no longer accessible from public domain. This may mean it was moved or shut down.

- Internet archives, wayback machine has entries related ot his. It was indexed on Sept. 22, 2020 and has stuff like text/html and image/gif. Not that useful.

- `dnsrecon -d secure-startup.com` returns a TXT DNS record of the form

```s
TXT secure-startup.com v=spf1 a mx ?all - HTB{RIP_SPF_Always_2nd
```
A TXT resource record allows to match arbitrary text with a domain. The part within { is half the flag. From `v=spf1 a mx ?all`, this looks like a SFP (Sender policy framework) record, which is related to email authentication (the problem the challenge asks to solve in the first place).

- Using `dig secure-startup.com -t txt`

```s
;; ANSWER SECTION:
secure-startup.com.     445     IN      TXT     "v=spf1 a mx ?all - HTB{RIP_SPF_Always_2nd"
```
- The mails being recieved by the recipients are spoofs. Thereby, they may have failed the DMARC test. Thereby, it is essential to query those records too. Navigate to `mxtoolbox.com/` and query DMARC to see reporting and conformance of emails.

```s
v=DMARC1;p=none;_F1ddl3_2_DMARC}
```

Final flag: HTB{RIP_SPF_Always_2nd_F1ddl3_2_DMARC}

Better way

```s
dig TXT linuxincluded.com
dig TXT dkim._domainkey.linuxincluded.com
dig TXT _dmarc. linuxincluded.com
```
