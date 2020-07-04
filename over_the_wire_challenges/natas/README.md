# Natas walkthrough

### For serverside web security.

Initial: 

Username: natas0
Password: natas0
URL: http://natas0.natas.labs.overthewire.org

# Level 0

URL: http://natas0.natas.labs.overthewire.org/

A simple view page source gave the password.

Password: gtVrDuiDfck831PqWsLEZy5gyDz1clto

# Level 1

URL: http://natas1.natas.labs.overthewire.org/

Even though rightclicking was blocked, F12 gave away the result.

Password: ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi

# Level 2

URL: http://natas2.natas.labs.overthewire.org/

There is nothing in the page, except one pixel wide image. Not of much interest. But the link of that image is `files/image.png`. Firing a URL to view this `files` directory comes up with more code, with somewhere a `users.txt`. The contents are as below.

```s
#### username:password
alice:BYNdCesZqW
bob:jw2ueICLvT
charlie:G5vCxkVV3m
natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
eve:zo4mJWyNj2
mallory:9urtcpzBmH
```

# Level 3

URL: http://natas3.natas.labs.overthewire.org/

Viewing the page source gave a hint: not even Google will find this time. What prevents Google from finding anything? robots.txt. Firing in `http://natas3.natas.labs.overthewire.org/robots.txt` gave the:

```s
User-agent: *
Disallow: /s3cr3t/
```
Firing `http://natas3.natas.labs.overthewire.org/robots.txts3cr3t/` gave the directory's index with a txt file.

natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

# Level 4

URL: http://natas4.natas.labs.overthewire.org/

The page on being visited says something on the lines you are coming from xyz, access granted to only `http://natas5.natas.labs.overthewire.org/`.

Quite evidently, accessing this page as if it was being accessed from `http://natas5.natas.labs.overthewire.org/` does the trick. When thinking about such, refer to `HTTP headers`. The useful header to use is the `HTTP referer URL`, that spoofs the source to be something else.

Simply fire from terminal: 

```s
wget http://natas4.natas.labs.overthewire.org/ --http-user=natas4 --http-password=Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ --referer=http://natas5.natas.labs.overthewire.org/
```

where `--http-user` and `--http-password` serve to authenticate the page. This downloads a file `index.html`. Open that and you shall get the password.

Password: iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq

#### (This level may also be solved using a Burp proxy).