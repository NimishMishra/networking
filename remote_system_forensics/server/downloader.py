import subprocess
import time

loaded_files = []

def run_command(command):

    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output



def fetch_directory_list():
    global loaded_files
    COMMAND = "curl http://192.168.43.38:9000"
    output = run_command(COMMAND)
    try:
        output = output.decode('utf-8')
    except:
        pass
    output_split = output.split("\n")

    try: 
        for line in output_split:
            if(line not in loaded_files):
                loaded_files.append(line)
    except:
        pass


def download_fetched_files():
    global loaded_files

    for file in loaded_files:
        path = "http://192.168.43.38:9000/" + file
        command = "curl -o " + file + " " + path + " --silent"
        run_command(command)


while True:
    fetch_directory_list()  
    download_fetched_files()
    time.sleep(10)