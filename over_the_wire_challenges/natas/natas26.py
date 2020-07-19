import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random


def receive_response(_payload):
    auth_username = 'natas25'
    auth_password = 'oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T' 
    response = requests.post('http://natas26.natas.labs.overthewire.org/', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
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
    auth_username = 'natas26'
    auth_password = 'oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T'

    _payload = 'x1=1&y1=1&x2=10&y2=10'
    response = sess.get('http://natas26.natas.labs.overthewire.org/?' + _payload, auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response)

    response = sess.get('http://natas26.natas.labs.overthewire.org/', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response)

    for cookie in sess.cookies:
        print(cookie.name + " " + cookie.value)

exploit()