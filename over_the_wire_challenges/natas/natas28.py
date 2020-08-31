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
    
    auth_username = "natas28"
    auth_password = "JWwR438wkgTsNKBbcJoowyysdM82YjeF"
    payload = {
        'query':'i'
    }

    response = requests.post("http://natas28.natas.labs.overthewire.org/", auth=HTTPBasicAuth(auth_username, auth_password), data=payload)
    dissect_response(response)


exploit()