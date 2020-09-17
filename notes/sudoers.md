# Sudoers

References:

[Sudoers manual](https://www.sudo.ws/man/1.8.13/sudoers.man.html)

## sudo.conf

- sudo consults the sudo.conf(5) file to determine which policy and and I/O logging plugins to load.

It basically sets up the configuration needed for sudo. Examples: path to the sudoers file, ownder of the sudoers, and so on.

## Authentication and logging

- Default behaviour: ask for authentication before anyone can use `sudo` except when

    - invoker is root
    - destination is same as invoker

- A user not listed in the policy when tries to invoke sudo, an automatic mail is sent to the default mail. `sudo -l` or `sudo -v` however does not cause this mail (`sudo -l` is trying to know what can a user run) UNLESS:

    - there is authentication error 
    - either `mail_always` or `mail_badpass` is enabled
    - all attempts to use `sudo` are logged

- `Credential caching`: once someone logs in as `sudo`, a record is logged with user ID, terminal ID, and time stamp (monotonic clock). It remains until the cache is reset (after which the user will need to authenticate again). `timeout` option handles this time of refresh. `Separate record for each tty`.

## Command environment

Controls which environment variables can be inherited by the command.

- `env_reset`: Reset the environment. This causes the commands to be run using a new, minimal environment. There's the file `/etc/environment` using which the environment is initialized. The new environment contains the `TERM`, `PATH`, `HOME`, `MAIL`, `SHELL`, `LOGNAME`, `USER`, `USERNAME` and `SUDO_*` variables in addition to variables from the invoking process permitted by the env_check and env_keep options. This is the whitelist.

- `!env_reset`: Any variables not restricted by `env_delete` and `env_check` are inherited.

- `sudo -i` (initial or first time login): environment variables can be initialized without consideration of value of `env_reset`.

## Sudoers file format

- sudoers file has two specifications:

    - Alias: like `admins = user1, user2`
    - Specs: like `admins` can run what commands

- In case overlapping entries, the last entry for the user is used.

## Tags

- `SETENV` and `NOSETENV`: These tags override the value of the setenv option on a per-command basis. 

-
