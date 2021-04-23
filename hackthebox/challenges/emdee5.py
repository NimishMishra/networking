import requests
import re
import hashlib

url='http://138.68.177.159:32040/'
h3_tag = "<h3 align='center'>"
session = requests.Session()
response = session.get(url) # getting the url first time
response_text = response.text
index = response_text.find(h3_tag)
response_text = response_text[index+len(h3_tag):]
index = response_text.find('</h3>')
plain_text = response_text[:index]
hashed = hashlib.md5(plain_text.encode())
data = {'hash' : hashed.hexdigest()}
response = session.post(url, data=data)
print(response.text)
