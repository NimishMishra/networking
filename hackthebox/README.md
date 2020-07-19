# Hack The Box

## Entry

The task is to find the an interesting script. It goes as `view-source:https://www.hackthebox.eu/js/inviteapi.min.js`.

```js
eval(function(p,a,c,k,e,r){e=function(c){return c.toString(a)};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('0 3(){$.4({5:"6",7:"8",9:\'/b/c/d/e/f\',g:0(a){1.2(a)},h:0(a){1.2(a)}})}',18,18,'function|console|log|makeInviteCode|ajax|type|POST|dataType|json|url||api|invite|how|to|generate|success|error'.split('|'),0,{}))
```

This looks like packed code. Unpack the code to get:

```js
function makeInviteCode() {
	$.ajax({
		type: "POST",
		dataType: "json",
		url: '/api/invite/how/to/generate',
		success: function (a) {
			console.log(a)
		},
		error: function (a) {
			console.log(a)
		}
	})
}
```

Go on to the console and run the function `makeInviteCode()`. The following is received:

```s
SW4gb3JkZXIgdG8gZ2VuZXJhdGUgdGhlIGludml0ZSBjb2RlLCBtYWtlIGEgUE9TVCByZXF1ZXN0IHRvIC9hcGkvaW52aXRlL2dlbmVyYXRl

Encoding: Base 64
```

Simply put a `echo ... | base64 -d` to get `In order to generate the invite code, make a POST request to /api/invite/generate`. Now `curl -X POST 'https://www.hackthebox.eu/api/invite/generate'` to get another base64 encoded `Sk5ZSVAtQlNMQU0tSkJCUlAtQ0dQTkstRU5IQlY=`. Perform another `base64 -d` to get the invite code.

(Unpacker)[https://www.strictly-software.com/unpacker/]


# Cheatsheet

## Exploit database

1. Exploit-db

2. Rapid 7

## Scanning

First step is to enumerate the machine. Some tried and tested combinations.

1. Do not go for `T1`. It's too fast, and 

```s
nmap -A -T4 -p- <ip-address>
```

Host scripts results from `nmap`:

1. `Message signing disabled` (or `enabled but not required`) is a dangerous thing allowing an attacker to access a reverse shell.

## Port

1. 139: SMB (`man smbclient`)

## Metasploit

Opening: `msfconsole`

Access: `/usr/share/metasploit-framework/modules`

HTTP scanners: [link](https://www.offensive-security.com/metasploit-unleashed/scanner-http-auxiliary-modules/)

### Staged and unstaged payloads

Whether the exploit delivers the payload at once or in stages. Forward slashes in the payload implies staged payload.

### SMB enumeration

1. `search smb_version` gives an auxiliary smb scanner (`auxiliary/scanner/smb/smb_version`).

2. To use that, `use auxiliary/scanner/smb/smb_version`

3. `set rhosts` to set the remote hosts.

4. `exploit` to carry out the exploit/scanner.

5. Search for other exploits on some database, like `exploit/windows/smb/ms08_067_netapi` and use it like `use exploit/windows/smb/ms08_067_netapi` from within the auxiliary scanner already set up.

6. [MS17-010](https://docs.microsoft.com/en-us/security-updates/securitybulletins/2017/ms17-010): a very critical SMB vulnerability. And [EternalBlue](https://research.checkpoint.com/2017/eternalblue-everything-know/) exploit.

#### Searching for Eternal Blue

This might be crash the machine, so heads up.

1. `msfconsole`

2. `search ms17-010`

3. `use auxiliary/scanner/smb/smb_ms17_010`

# Meterpreter

Reverse shell

### Postexploitation enumeration

1. getuid

2. sysinfo

3. hashdump: Dump the SAM table and thus the user passwords.

4. shell
