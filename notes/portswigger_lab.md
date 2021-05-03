# PortSwigger Labs

## Basic password reset poisoning

[Link](https://portswigger.net/web-security/host-header/exploiting/password-reset-poisoning/lab-host-header-basic-password-reset-poisoning)

The user carlos will carelessly click on any links in emails that he receives. You can access your own account with the following credentials: wiener:peter. Any emails sent to this account can be read via the email client on the exploit server.

## HTTP host header attacks

[Main link](https://portswigger.net/web-security/host-header/exploiting)

- Modify the host header and see if you can still reach the application. If yes, host header can be used to probe the application.

- Flawed validation: Host headers can be validated in a number of ways. The only way to have a path ahead is to fuzz requests and understand how validation works. Then payload can be crafted.

- Ambiguous requests: The code that is validating the host and the code that is running the application will most often be very different from one another. In such a case, the two places may disagree on the kind of processing they want to do with the request. Advantage of such discrepancies can be taken of. Ambiguous requests can involve duplicate host headers or supplying absolute URLs or adding line wrapping.

- Override: Use X-Forwarded-Host. Sometimes, the servers are accessed by intermediary systems rather than the client itself, so the original host is rather written into the X-Forwarded-For header, which is actually referred to by the server. Other variants are X-Host, X-Forwarded-Server, X-HTTP-Host-Override, and Forwarded.

### Lab: web cache poisoning via the host header

- Host header is used without HTML encoding. Client side vulnerabilities are not usually not exploitable.


