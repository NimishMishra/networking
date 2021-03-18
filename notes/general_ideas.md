# General Ideas

## Privesc

- **cron** joins repeat regularly. Can you fit something there?

- Python import hijacking

- **lxd group member** based privilege escalation (using alpine image)

- **snapd** based privilege escalation (**dirty-sock**)

- Linux privilege escalation: [linpeas.sh](https://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh)

- Docker container escape. Read more on the Ready writeup.

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

```
When the last task in a cgroup leaves (by exiting or attaching to another cgroup), a command supplied in the release_agent file is executed. The intended use for this is to help prune abandoned cgroups. This command, when invoked, is run as a fully privileged root on the host.
```

The reason for this command running as root is very simple: it needs to prune the `cgroup` and end everything. So if this command is overridden in a dummy cgroup and destroy it, the command shall be executed as the root of the highest privilege in the hierarchy.
