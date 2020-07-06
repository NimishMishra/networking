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
    COMMAND = "curl http://192.168.43.38:8080 --silent | grep href"
    output = run_command(COMMAND)
    output = output.decode('utf-8')
    output_split = output.split("\n")

    try: 
        for line in output_split:
            start_index = line.index("href=")
            line = line[start_index + 6: ]
            end_index = line.index(">")
            line = line[0: end_index - 1]
            if(line not in loaded_files):
                loaded_files.append(line)
    except:
        pass


def download_fetched_files():
    global loaded_files

    for file in loaded_files:
        path = "http://192.168.43.38:8080/" + file
        command = "curl -o " + file + " " + path + " --silent"
        run_command(command)


while True:
    fetch_directory_list()  
    download_fetched_files()
    time.sleep(10)