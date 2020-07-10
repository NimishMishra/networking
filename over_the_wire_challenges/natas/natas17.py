import requests
from requests.auth import HTTPBasicAuth


def receive_response(_payload):
    auth_username = 'natas17'
    auth_password = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'
    payload=_payload
    response = requests.post('http://natas17.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data = {'name': payload})
    dissect_response(response)

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

receive_response("")