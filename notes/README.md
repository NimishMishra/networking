# Notes

1. General port information

2. General ideas

3. General attack vectors
    
4. PortSwigger's Web Security Academy.

5. Linux privilege escalation and the sudoers file

6. General notes on bounty hunting

7. CTFs

# General Ideas

## Privesc

- **cron** joins repeat regularly. Can you fit something there?

- Python import hijacking

- **lxd group member** based privilege escalation (using alpine image)

- **snapd** based privilege escalation (**dirty-sock**)

- Linux privilege escalation: [linpeas.sh](https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh)

- Docker container escape. Read more on the Ready writeup.

- Sometimes, linpeas will not find things. You must find them yourself.

	-- On HTB Laboratory, find the SUID binaries through: `find / -user root -perm 400 -exec ls -ldb {} 2>/dev/null`. HTB Laboratory requires hijacking a file used inside the SUID binary. This can be found through `ltrace` (which tells you what the binary is doing). Quite often, people write the binaries without giving absolute paths. These can be hijacked. It is similar to python import hijacking. 

- In some shell scripts, complete path would not be given. Like `cat .....` instead of `/bin/cat ...`. Here, the path can be hijacked through updating $PATH and creating a malicious payload through the name `cat` something in $PATH.

- In some machines (like HTB Knife), you must look at the technology supporting the server to find vulnerabilities there. For instance, HTB Knife had `X-Powered-By` header revealing a vulnerable PHP version that allowed malicious custom header `User-Agentt` to gain RCE.

## cgroups

- Very important concept in containerized technology wherein cgroups allocate resources — such as CPU time, system memory, network bandwidth, or combinations of these resources — among user-defined groups of tasks (processes) running on a system.

- How they are helpful in containers? Because the core OS is just one and there are these isolated boxes running which have different resource allocation.

- Linux process hierarchy is a tree rooted at the `init` process. cgroups hierachy consists of several trees because there are many resources: cpu, cpuset, devices etc.

## Mountpoint

Mount point is a directory in the filesystem where additional information is logically connected to a storage location outside the OS's root drive. To mount, in this context, is to make a group of files in a file system structure accessible to a user or user group.

## cewl

- creating a list of emails from a certain website `cewl -e --email_file emails http://sneakycorp.htb/`

## Evolution

- email client which allows you to select the mail server too. Thus, boxes like `sneaky mailer` used this.

- evolution allows setting server and port for SMTP and IMAP (other services as well); and a lot of other things as well like TLS things.

## Jackson Deserialization vulnerability

[Link](https://medium.com/@swapneildash/understanding-insecure-implementation-of-jackson-deserialization-7b3d409d2038)

- a java library used to interconvert between POJO (Plain old java objects) and JSON. It serializes POJO to JSON, and deserializes JSON to POJO.

```s
public class MyValue {
    public String name;
    public int age;
}

//deserialization class

ObjectMapper om = new ObjectMapper();

MyValue myvalue = om.readValue(Files.readAllBytes(Paths.get("**.json")), MyValue.class);

//PenetrationTesting 

pt = om.readValue(Files.readAllBytes(Paths.get("***.json")), PenetrationTesting.class);
```

`ObjectMapper`: class in Jackson that lets deserialize a JSON to a java object. It reads from a file and creates an object of the class `MyValue`. For instance, the input `{"name":"testname","age":12}` will create an object of class `MyValue` with the attribute `name` set to `testname` and `age` to `12`.

In short, this allows you to host an infected payload somewhere, and call a Java gadget to do things.

- JSON starting with **{** is JSON object.

- JSON starting with **[** is JSON array.

## Drupal

Drupal is a CMS (a content management system), particularly a web content management system. Something related to Drupal came up in HTB Ready. Recheck that box for more details.

## Snap

Snap is a linux based package manager. First encountered in HTB Time. Some thoughts about snap and whether it is open to exploitation.

- **Why are there two separate snap directories: one in / and the other in /home/user?**

Snap in `/` has a `README` which goes as 

```s
This directory presents installed snap packages.

It has the following structure:

/snap/bin                   - Symlinks to snap applications.
/snap/<snapname>/<revision> - Mountpoint for snap content.
/snap/<snapname>/current    - Symlink to current revision, if enabled.

DISK SPACE USAGE

The disk space consumed by the content under this directory is
minimal as the real snap content never leaves the .snap file.
Snaps are *mounted* rather than unpacked.

For further details please visit
https://forum.snapcraft.io/t/the-snap-directory/2817
```
The snap directory in `/` contains mountpoints for snaps. By the meaning of mountpoints that I understand, snaps are outside the root directory. And `/home/user/snap` contains the configuration file for your snaps.

Snap has a certain vulnerability [dirty-sock](https://0xdf.gitlab.io/2019/02/13/playing-with-dirty-sock.html). Any version above 2.37.1 is patched and beyond us.

## GitLab

- GitLab comes with an interesting CI/CD (continous integration/continuous deployment) that allows one to run tests, checks for things, and do other stuff.

- In `.gitlab-ci.yml`, one can have shell scripts. Upon running the pipeline, the script is run by a `runner` (which can be a local VM or a hosted environment). The idea is that if somehow a runner is configured on the machine to compromise and the pipeline is executed, the commands should run on the given machine and you should be able to get a connection to a remote computer. (?)

- Another exploit for GitLab runners given [here](https://frichetten.com/blog/abusing-gitlab-runners/). Given only the runner token (which is used to register the runner with GitLab), upon pushing to a repo which is configured for the runner, the runner will POST to `/api/v4/jobs/request` and will receive a JSON with information it requires to run the job. The attack is to set up a separate runner to steal the job (pipeline checks when code is pushed) and get the data. A normal runner queries things once every 3 minutes, but we could do it endlessly, thereby almost ensuring we always get the job. Our imposter runner will spit out much data this way. 

## Docker escape

- Read more at the Ready writeup.

- Finding if you are within a container:

	-- Run the `linpeas` script. It tells you.
	-- Check the `cgroup` information of the `init` from `/proc/1/cgroup`. If it is not `/`, it's a container.

- Find if the container is privileged by running a command that requires the docker container to have specified the `--privileged` flag. Like `ip link add dummy0 type dummy`

- Find the rest of the things here: `https://blog.trailofbits.com/2019/07/19/understanding-docker-container-escapes/`. The core problem is that when the cgroup ends, the cgroup executes the command given in its `release_agents` file in the cgroup's hierarchy's root directory.

```s
When the last task in a cgroup leaves (by exiting or attaching to another cgroup), 
a command supplied in the release_agent file is executed. 
The intended use for this is to help prune abandoned cgroups. 
This command, when invoked, is run as a fully privileged root on the host.
```

The reason for this command running as root is very simple: it needs to prune the `cgroup` and end everything. So if this command is overridden in a dummy cgroup and destroy it, the command shall be executed as the root of the highest privilege in the hierarchy.

- There are two things of interest: 

	-- `notify_on_release` which as named notifies when the last task is done. A `1` must be written to this file.

	-- `release_agent` which contains the command to be executed

## HTTP 418 Teapot

- Came up in `Laboratory` writeup

- The response code implies the server's response to the client's request implying that I am a teapot, find a coffee maker.

- In the literal sense, this means I can't handle this request, find another server.

## Wordpress penetration testing

From ippsec's [Apocalyst](https://www.youtube.com/watch?v=TJVghYBByIA)

- The reason you shall not see themes is because wordpress uses absolute URLs to its stylesheets (like>

- `wpscan`

        -- `wpscan --url ... -e vp,tt,u` this also enumerates vulnerable plugins.
        -- Bruteforce usernames and passwords
                --- create a wordlist using cewl

- To get code execution on the website, edit some files. Wordpress allows editing things. So in the ap>

- `readme.html` exposes the wordpress version through its system requirements. `wpscan` also finds it.

## PHP

- [Used in Tenet HTB] The following snippet set $input to the first argument if it is not null, else it sets to the second string.

```php
$string = NULL;
$input = $string ?? 's';
```
- [Used in Tenet HTB] `__destruct()` is called when there are no more references to a particular class. The way this vulnerability arises when used in conjunction with `unserialize` is that user input can be sent to match just the class needed in order to maybe write a new PHP file. 

- Decent serializer can be found [here](https://serialize.onlinephpfunctions.com/)

## Netcat

- There are two versions of netcat. The most common one is one from `nmap.org` website. The other ones are also there that don't have the option `-e` for instance. Took me a look time to realise why Tenet HTB was not replying to my local listener.

- A brilliant way to upgrade a simple shell to tab autocomplete shell.

```sh
get the shell
python3 -c "import pty; pty.spawn('/bin/bash');"
Now Crtl+z to push onto background
stty raw -echo
fg
```
## sudo

- `sudo -l` lists the user's privileges or the commands the user can run.

- `(ALL : ALL) NOPASSWD` means this stuff can be run without requiring a password.

## mktemp (HTB Tenet)

- A special utility that creates a temporary file and returns its name.

- Like `mktemp -u ssh-XXXXXXXX` gives a temprary file as `ssh-0DKS10dj`

## umask (HTB Tenet)

- A special utility to set the permissions mask for the file. 

- `(umask 110; touch file)` will create a file `file` and give permissions `rw_` to each entity. So `110` got masked with permissions `111` and became the same permissions for all entities: root, user, and group.

## TXT resource record (Easy Phish challenge, HTB)

- provide the ability to associate arbitrary text with a host or other name

## SPF TXT record (Easy Phish challenge, HTB)

- Can be seen directly on `https://mxtoolbox.com/`

- SPF or sender policy framework is an email authentication technique protecting against email spoofing attacks

- Setting up an SPF record helps to prevent malicious persons from using your domain to send unauthorized (malicious) emails

- SPF record lists all authorized hostnames / IP addresses that are permitted to send email on behalf of your domain.

- `v=spf1` is the version number: sender policy framework version 1.

- `all` comes in many flavours:

	-- `-all` : servers that aren't listed in the SPF record are not authorized to send email 
	-- `~all` :  If the email is received from a server that isn't listed, the email will be marked as a soft fail (emails will be accepted but marked).
	-- `+all` : any server to send email from your domain.
	-- `?all` : 

- Presence of `a` and `mx` in SPF mean that all the A records and all the A records for the MX records are tested. If the client IP is found, the mechanism matches.

- "v=spf1 mx -all" authorizes any IP that is also a MX for the sending domain.

## DMARC (Easy Phish Challenge, HTB)

- Can be seen directly on `https://mxtoolbox.com/`

- `Domain Message Authentication Reporting and Conformance` involves reporting back regarding failed messages

- The basic idea is if the email received fails the DMARC test, then there shall be a report somewhere. That is exactly what querying the DMARC records can tell someone.

- `v=DMARC1` is the DMARC version

- `v=DMARC1;p=none;` separated by semicolon, p defines the policy to undertake failed emails. Here, `p=none` could be `quarantine` or `reject`.

## Jinja2 (Templated challenge, HTB)

- [Jinja2](https://flask.palletsprojects.com/en/1.1.x/templating/) is a template engine for python's flask.

- All template engines, using this one too, focuses on separating the logic of the application and the content to be displayed (a makeover from the old days when everything had to be inside the same file). This comes very handy if you have something you wish to display based on user input. Rather than making one page for every user, we make a template and let the parameters submitted by the user dictate the rendering pattern of the page.

- A better understanding of the thing can be found [here](https://code.tutsplus.com/tutorials/templating-with-jinja2-in-flask-essentials--cms-25571)

## favicon.ico

- Modern browsers will show an icon to the left of the URL. This known as the 'favicon.ico' and is typically fetched from website.com/favicon.ico. Your browser will automatically request it when browsing to different sites. If your browser receives a valid favicon.ico file, it will display this icon. If it fails, it will not display a special icon.

## Server side template injection (Templated challenge, HTB)

- SSTI information [here](https://portswigger.net/research/server-side-template-injection) From templates, it is clear that user input is processed in some form by the backend to render the template. This is where injection can occur.

- Jinja2 exploitation steps [here](https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee)

```s
{{ config.items() }} <-- notice initial configuration
{{ config.from_object('os') }} <-- add OS things to the configuration
{{ config.items() }} <-- notice OS functions added now
{{ ''.__class__.__mro__[1].__subclasses__()[414:] }} <-- Popen offset
```
- mro is the method resolution order that is used by Python to resolve methods in the face of multiple inheritance. mro aids in displaying the hierarchy of classes wherein the actual class one is looking for can be found.

- `from_object` is a special jinja function that allows the configuration to load stuff from objects. Here, the configuration loads support for all class and functions defined in the `os` package in python.

- This [link](https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/) lists a lot of different payload types that can be used while crafting SSTI payload, even without {{}}.


## LDAP (Lightweight Directory Access Protocol, in HTB web challenge Phonebook)

- mechanism for interacting with directory servers. Organizations typically store information about users and resources in a central directory (such as Active Directory), and applications can access and manipulate this information using LDAP statements.

- It's often used for authentication and storing information about users, groups, and applications, but an LDAP directory server is a fairly general-purpose data storage system.

- Read about LDAP injection [here](https://www.netsparker.com/blog/web-security/ldap-injection-how-to-prevent/). The main thing is that LDAP involves wildcards in its search filters.


# General ports

# General information

- SSL/TLS certificates allow HTTP websites to be served below TLS (HTTPS = HTTP + TLS). The main difference is SSL makes **explicit** connections via a port, while TLS makes **implicit** connections via a protocol. SSL is secure socket layer while TLS is transport layer security. Both of SSL and TLS certs are **X.509** certificates that help to authenticate the server and facilitate the handshake process to create a secure connection. 

- [Brute-force cheatsheet](https://book.hacktricks.xyz/brute-force)

# Information about general ports.

# Port 25

- SMTP (Simple Mail Transfer Protocol) is for **sending** emails.

- Useful commands:

```s
smtp-user-enum -p 25 -t 10.10.10.197 -U emails -M VRFY
```

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
