# General Ideas

# Privesc

- **cron** joins repeat regularly. Can you fit something there?

- Python import hijacking

- **lxd group member** based privilege escalation (using alpine image)

- **snapd** based privilege escalation (**dirty-sock**)

- Linux privilege escalation: [linpeas.sh](https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh)

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

