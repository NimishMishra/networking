# PortSwigger Web Security Academy

## HTTP Host Header Attacks

### Multiple domains resolving to same IP

- mandatory request header as of HTTP/1.1 specifying the domain name the client wishes to access

- Example header for `https://portswigger.net/web-security`

```s
GET /web-security HTTP/1.1
Host: portswigger.net
```

- identifies the backend component the client wants communication with. Consider a host with IP 192.168.43.34 on your local network. Historically, this IP would host a single application so no point of ambiguity. But in the modern world, one IP could host a lot of stuff and thus clarity is needed for **routing**. Host headers serve this purpose. Two scenarios:

1. **Virtual Hosts**: Distinct websites (and thus distinct domains) are on the same server. 

2. **Routing traffic via intermediary**: The scenario where the websites are on different servers but all traffic passes through a common system like load balancer, content delivery network (CDN). In this case, although websites are on different servers, their domain names are resolved to the same intermediary system. 

- HTTP Host Headers solve this problem as `portswigger.net` is resolved to the IP of the host and the header `/web-security` determines where exactly the request should be routed to.

- **Insecure websites**: That do not sanitize the host headers of the incoming requests. Attacks that involve injecting a payload directly into the Host header are often known as "Host header injection" attacks.

- If the input is not properly escaped or validated, the Host header is a potential vector for exploiting a range of other vulnerabilities, most notably Web cache poisoning, Business logic flaws in specific functionality, Routing-based SSRF, and Classic server-side vulnerabilities, such as SQL injection.

- In fact, many of these vulnerabilities arise not because of insecure coding but because of insecure configuration of one or more components in the related infrastructure. These configuration issues can occur because websites integrate third-party technologies into their architecture without necessarily understanding the configuration options and their security implications.

- Protect against HTTP Host Header attacks. 

1. The simplest approach is to **avoid** using the Host header altogether in server-side code. Try switching to relative URLs instead. Helps in **web cache poisoining**.

2. **Protect absolute URLs**: If relative URLs are not useful and you are forced to use the absolute URLs, make sure to define the domains in a config file and refer to this. This way you do not rely on host headers for the domain and eliminate the threat of **password reset poisoning**. Like `<a href="https://_SERVER['HOST']/support">Contact support</a>`. In this case, it would have been better to use stuff like `./support`. But should that be not possible, have a config file where you store `_SERVER` and `HOST` and other things to use as placeholders.

3. **Validate the host header**: Compare the host headers against a whitelist. Make sure you know the domain requested by the host header.

4. **Don't support host override headers**: Don't support other headers like *X-Forwarded-Host*.

5. **Whitelist permitted domains**: configure load balancer or reverse proxy to allow only specific whitelisted domains.

6. **Be careful with internal-only virtual hosts**: Avoid hosting internal only websites with content open to the public.

### Identifying vulnerable website (or how's your parser)

The simple way to identify a vulnerable website is to send modified host headers to the website and observe the effect it has on the response.

- **Arbitrary host header**: send an arbitrary domain in the host header. Proxy like Burp Suite actually maintains the difference between the host header and the target IP address. This allows sending arbitrary host header to the intended target. Two things are possible since you are sending an arbitrary and possibly unrecognized host header. One is to land at a default page if that is what you are looking for you are fine. Else you land with an `Invalid Host Header` error.

- **Check for flawed validation**: Receiving `Invalid Host Headers` implies there is some validation going on. Next stop is to test that validation. The point is to try understanding how exactly the websites parse the host headers.

    - **Payload injection via port**: works when you are able to determine the host header parser is ignoring the port as well as being able to inject non-numeric things into the port.

    GET /example HTTP/1.1
    Host: vulnerable-website.com:bad-stuff-here

    - **Matching logic**: in case of matching, you could craft a domain that has the whitelisted domain as a substring. 

- **Send ambiguous requests**: 

    - **Inject duplicate host headers**: Since it is not ideal for browsers to send in double hosts, developers may have not anticipated things. In that case, it is possible that the frontend deals in some way other than how the backend deals with things.

    GET /example HTTP/1.1
    Host: vulnerable-website.com
    Host: bad-stuff-here

    Say if the frontend sees the first host header and the backend sees the last host header, in that case the first host is used to bypass the authentication while the second host is used to exploit the application.

    - **Supply an absolute URL**: Servers are sometimes configured to handle absolute URLs too. It is possible for an implementation *not* to have the request line while routing request. In that case, the domain specifies the absolute URL. Servers also behave different with different protocols as HTTP or HTTPS.

    GET https://vulnerable-website.com/ HTTP/1.1
    Host: bad-stuff-here

    - **Indentation**: Consider the following

    GET /example HTTP/1.1
        Host: bad-stuff-here
    Host: vulnerable-website.com

    As a matter of fact, it is highly server dependent to see how this works or is parsed. Say if the frontend ignores this stuff, then it will be like just another request for the server. Therefore, if the backend prefers the first host in case of duplicates, arbitrary things are gone into the backend.

- **Inject host override headers**: Consider the case of a load balancer. Traffic from your machine reaches the load balancer which then goes on to the target system. The target system or backend will see the host header as containing domain name for the load balancer (because your machine sent the request to the load balancer). In comes the use of **X-Forwarded-Host** in the sense that it contains the original value of the host header from the client. Quite evidently, the backend will see this header.

GET /example HTTP/1.1
Host: vulnerable-website.com
X-Forwarded-Host: bad-stuff-here

Since the load balancer sees the second host, it will route the traffic generally and delivers the malicious payload to the backend. Other kinds of such headers include **X-Host**, **X-Forwarded-Server**, **X-HTTP-Host-Override**, and **Forwarded**. It happens sometimes that such a thing is supported in a third-party application the website is using.

# Password reset poisoning

Password resetting involves generation of special tokens to intended recipients that allow resetting of passwords. Proof of concept:

1. User submits email and requests a password reset request.

2. If the user exists on the website, the website generates a temporary, unique, high-entropy token which it associates with the user's account on the back-end.

3. The website sends a password reset link to the user's mail as `https://normal-website.com/reset?token=0a1b2c3d4e5f6g7h8i9j`

4. When the user visits this link, website uses this high-entropy token to determine the account whose password is being reset. It then gives the user the option to change the password.

How's the attack? Steal that token iff the URL sent to the user is dynamically generated based on controllable input such as Host Header.

1. Obtain the email address to reset the password of. 

2. Submit the password reset form, and intercept the request. Modify the host header to point to a domain you control like `evil-user.net`.

3. The user receives a mail of the form `https://evil-user.net/reset?token=0a1b2c3d4e5f6g7h8i9j`. Note they would receive the token as usual but the domain is changed since we fiddled with the host header. 

4. If the user clicks the link, it will be sent to the attacker's server. The attacker can now visit the real website and supply the token with the real parameters.