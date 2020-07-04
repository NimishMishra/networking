# New utilities learnt. Use --help or manpage for details

`tr`: translate, delete 

`uniq`: unique lines in a file

`strings`: display printable strings in files

`base64`: encoding, decoding

`tar, gz, bzip2`: compression 

`xxd`: reverse hexdump (see challenge 12)

`nc`: netcat to send and receive data. Server mode nc -l host -p  port and client mode nc host port

`openssl s_client`: sets up a TLS/SSL connection

`nmap`: all time great network mapper

`diff`: comparison of files

`cron`: scheduler

`grep`: great for searching. Ex. `grep -rnw ./ -e password` recursively searches all files within the current directory for the string password

# Level 0: 


Host: bandit.labs.overthewire.org
Port: 2220

Initial connection: ssh bandit0@bandit.labs.overthewire.org -p 2220

Password for level 0: bandit0


`cat readme`

Password for level 1: boJ9jbbUNNfktd78OOpsqOltutMc3MY1

# Level 1: 

Connection: ssh `bandit1@bandit.labs.overthewire.org -p 2220`

Since the filename is a special character, it is opened using `cat ./-` [Source](https://stackoverflow.com/questions/42187323/how-to-open-a-f-dashed-filename-using-terminal)

Password for level 2: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9

# Level 2 

Connection: `ssh bandit2@bandit.labs.overthewire.org -p 2220`

Filename has spaces. A simple `cat 'file name'` does the trick.

Password for level 3: UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK

# Level 3

`ssh bandit3@bandit.labs.overthewire.org -p 2220`

The file is hidden. A simple `ls -la` reveals the file .hidden. Then a simple `cat '.hidden'`

Password for level 4: pIwrPrtPN36QITSp3EQaw936yaFoFgAB

# Level 4

`ssh bandit4@bandit.labs.overthewire.org -p 2220`

## A simple solution 

`cat ./-file07`

## Python solution

```python
file_list = [x for x in os.listdir(os.getcwd())]

for i in file_list:
    file_object = open(i, 'r')
    print(file_object.read())
```

All non human-readable files will give errors in decoding utf-8. Only the one with worth decoding gives the password

Password: koReBOKuIDDepwhWk7jZC0RTdopnAYKh

# Level 5

`ssh bandit5@bandit.labs.overthewire.org -p 2220`

Find a file human readable, size 1033 bytes, and non-executable.

`find . -type f -size 1033c -readable ! -executable`

`find . -type f -size 1033c ! -executable`

Password: DXjZPULLxYr17uwoI01bNLQbtFemEgo7

# Level 6

`ssh bandit6@bandit.labs.overthewire.org -p 2220`

The main trick was to search in the entire server. Accomplished by `find / -user bandit7 -group bandit6 -size 33c` instead of `find . -user bandit7 -group bandit6 -size 33c`

Password: HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs

# Level 7

`ssh bandit7@bandit.labs.overthewire.org -p 2220`

In a huge file, password was next to the word 'millionth'

## Simple solution

`cat data.txt | grep millionth`

## Python solution

```python
data = open('data.txt', 'r').read()
print(data[data.index('millionth'):data.index('millionth')+100])
```

Password: cvX2JJa4CFALtqS87jk27qwqGhBM9plV

# Level 8

`ssh bandit8@bandit.labs.overthewire.org -p 2220`

In a huge file, find the only line of text that occurs only once. A simple grep without duplicates should do. Or better, unique command on sorted file.

`sort data.txt | uniq -u`

UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR

# Level 9

`ssh bandit9@bandit.labs.overthewire.org -p 2220`

A semi human readable file containing lots of things. Password was ============== followed by the password. I used `strings -d -n 40 data.txt` to extract that line (-d means to look only at the data section. -n means to have 40 bytes).

Another approach: `strings data.txt | grep "="`

truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk

# Level 10

ssh bandit10@bandit.labs.overthewire.org -p 2220

The file was base 64 encoding. A simple cat `data.txt | base64 -d` decoded the entire thing.

Password: IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR

# Level 11

ssh bandit11@bandit.labs.overthewire.org -p 2220

Decoding a rot13 cipher in linux. Perfect task for `tr. cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'` Note how the rotataions happen

Password: 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu

# Level 12

ssh bandit12@bandit.labs.overthewire.org -p 2220

A hexdump file was compressed several times. The basic idea is to use xxd to reverse hexdump and store with original format. Let's say gzip compression. Convert filename mv data data.gz and run `gzip -d data.gz`. Now check file data, you get bzip file. Convert again mv data data.bz and run `bzip2 -d data.bz`. Do this again and again until you reach ASCII text.

`tar -xf data6`, `mv data8.bin data8.gz`, `gzip -d data8.gz`. 

Password: 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL

# Level 13

`ssh bandit13@bandit.labs.overthewire.org -p 2220`

The idea was to login as another user from the connection itself. Thus from bandit13, use `ssh bandit14@localhost -i sshkey.private`

-i provides access to the private RSA key used to authenticate the connection

Password: 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e

# Level 14

`ssh bandit14@bandit.labs.overthewire.org -p 2220`

Send data to another port, use nc (netcat). Thus `echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e | nc localhost 30000`

Password: BfMYroe26WYalil77FoDi9qh59eK5xNr

# Level 15

`ssh bandit15@bandit.labs.overthewire.org -p 2220`

This level had to use SSL encryption to send data over the network. Unlike last level, echo ... | ... didn't work. First establish the connection using `openssl s_client -connect localhost:30001`. All the certificates will appear and a blocking wait will come, as if the server is waiting to have some data. Send data and the reply will come.

Password: cluFn7wTiGryunymYOu4RcffSxQluehd

# Level 16

`ssh bandit16@bandit.labs.overthewire.org -p 2220`

To send a SSL to one of open ports in 31000 to 32000. A simple nmap scan (TCP connect scan since it doesn't require admin controls) of the form `nmap -sT 192.168.101.80 -p 31000-32000`. Five ports reported open status with service unknown.

PORT      STATE SERVICE

31046/tcp open  unknown

31518/tcp open  unknown

31691/tcp open  unknown

31790/tcp open  unknown

31960/tcp open  unknown

Try out `openssl s_client -connect localhost:port_number` for each. For me, port 31790 worked.

Password/RSA private key: 

-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

# Level 17

`ssh bandit17@bandit.labs.overthewire.org -p 2220 -i sshkey.private`

In order to proceed, create a file sshkey.private, load the entire key (START AND END headers are also important. Without it, it doesn't work!!!). And fire `ssh bandit17@bandit.labs.overthewire.org -p 2220 -i sshkey.private` (remember to be in the same directory where the key is stored before firing the command). Also, make you ssh key private. Do `chmod 600 keyname.private`

Idea is to find difference between two files. A simple diff passwords.new passwords.old does the trick.

Password: kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd or w0Yfolrc5bwjS4qw5mq1nnQi6mF03bii

Do a simple `cat passwords.new | grep kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd` to see which string belongs to passwords.new

# Level 18

`ssh bandit18@bandit.labs.overthewire.org -p 2220`

Here, you are not allowed to access the ssh server, someone keeps you logging out. But you can execute one command with the normal ssh login attempt.

`ssh bandit18@bandit.labs.overthewire.org -p 2220 cat readme` 

Password: IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x

# Level 19

`ssh bandit19@bandit.labs.overthewire.org -p 2220`

There is password stored in `/etc/bandit_pass/bandit20` but cat is denied for current user. However there is a setuid binary `bandit20-do` that runs a command as another user (bandit20). Thus, run

`./bandit20-do cat /etc/bandit_pass/bandit20`

Password: GbKksEFF4yrVs6il55v6gwY5aVje5f0j

# Level 20

`ssh bandit20@bandit.labs.overthewire.org -p 2220`

I had almost figured out the method. It was working fine, except I kept targeting a wrong port. I ran a nmap, and targeted an open port. Had I run nc first, it would have open another port of my choosing. Hence the idea is to run nc first, then ./suconnect.

`nc localhost 40000` doesn't run (that's the client code). Use `nc -l localhost -p 40000` to open up the port.

Connect using `./suconnect 40000` (use another login or set up the first command in the background using &)

Send data from nc.

Note: only nc can open the port. Running `./succonnect 40000` will not run the port. A good way is to use tmux or screen to do this.

Password: gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr

# Level 21

`ssh bandit21@bandit.labs.overthewire.org -p 2220`

cron is the scheduler that runs jobs at regular intervals. Directory structure is like `/etc/cron/daily`, `/etc/cron/weekly`, `/etc/cron/monthly`. In this case, there is a directory `/etc/cron.d` having some information. Some shell script was running. Upon further investigation, `/etc/bandit_pass/bandit22` is non-readable. But the shell script was writing its contents to a readable file in an accessable location. Reaching out to it did the trick.

Password: Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
# Level 22

`ssh bandit22@bandit.labs.overthewire.org -p 2220`

Similar as in previous level. Investigation leads to a shell script that has the following:

```shell
myname=$(whoami)

mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

Quite evidently, firing whoami and placing that in the second line yields 8169b67bd894ddbb4412f91573b38db3, and upon investigating `cat /tmp/8169b67bd894ddbb4412f91573b38db3`, the password below is obtained. 

Looking at shell scripts can be a useful way to notice changes.

Password: jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n

# Level 23

`ssh bandit23@bandit.labs.overthewire.org -p 2220`

The following cron job was running:

``` shell
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
```

Which has the following script:

```shell
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```
It is clear owner 'bandit23' files are run by user 'bandit 24'. The only thing is to create a script that copies password and move that to directory `/var/spool/bandit24`. The script should run automatically and deliver results.

`cat /etc/band_pass/bandit24 > /tmp/my_dir/data.txt`

Now give decent permissions (chmod 777) to the shell script as well as to the text file and `cp file.sh /var/spool/bandit24`.

Password: UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ

# Level 24

`ssh bandit24@bandit.labs.overthewire.org -p 2220`

A daemon running on port 30002 answers queries of the form UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ xxxx. 

A simple python script (run as `python3 script.py > data.txt`):
```python
for i in range(10000):
        pin = "0"*(4-len(str(i))) + str(i)
        print('UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ' + " " + pin)
```

And run `cat data.txt | nc localhost 30002`

Password: uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

# Level 25

`ssh bandit25@bandit.labs.overthewire.org -p 2220` 

Found a private RSA. Copied it into the system and make it private (`chmod 600`). Ran the next level.

# Level 26

`chmod 600 sshkeyname.private`

`ssh bandit26@bandit.labs.overthewire.org -p 2220 -i sshkeyname.private`

This is an interesting level. It uses a different shell than bash. Going into the previous level shell and investigating /etc/passwd tells the shell being used. Opening the code for the shell points to a `more` command. Thus, resizing the terminal to force the `more` command is the trick.

Password: 3ba3118a22e93127a4ed485be72ef5ea

# Level 27

`ssh bandit27@bandit.labs.overthewire.org -p 2220`

Cloning a git repo and reading a README file.

Password: 0ef186ac70e04ea33b4c1853d2526fa2

# Level 28

`ssh bandit28@bandit.labs.overthewire.org -p 2220`

`git log -p` tells the differences between commits. The recent version denotes a password as xxxxxxxxxx. A `git log -p` gives the updated password.

Password: bbc96594b4e001778eee9975372716b2

# Level 29

`ssh bandit29@bandit.labs.overthewire.org -p 2220`

The password was hidden in another branch which was unreachable from a simple `git branch`. `git branch -r` did the trick, followed by a simple `git log -p`.

Password: 5b90576bedb2cc04c86a9e924ce42faf

# Level 30

`ssh bandit30@bandit.labs.overthewire.org -p 2220`

This time the password was hidden in a git tag. A simple `git show secret` did the trick

Password: 47e603bb428404d265f59c42920d81e5

# Level 31

`ssh bandit31@bandit.labs.overthewire.org -p 2220`

The task was to create a file and push it to a remote repo. 

Password: 56a9bf19c63d650ce78e6ec0354ee45e

# Level 32

`ssh bandit32@bandit.labs.overthewire.org -p 2220`

A user defined shell was present. Shells are rerun using `$0`. That is the escape!

Password: c9c3199ddf4121b10cf581a98d51caee