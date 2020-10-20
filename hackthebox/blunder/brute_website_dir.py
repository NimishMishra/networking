import requests
import time
import os
import sys

# Wordlist obtained: /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
# Status codes obtained: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


wait_time = 5
status_codes = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-authoritative info",
    204: "No Content",
    205: "Reset content",
    206: "Partial content",
    207: "Multi-status",
    208: "Already reported",
    226: "IM used",
    300: "Multiple choices",
    301: "Moved permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",
    307: "Temporary redirect",
    308: "Permanent redirect",
    400: "Bad request",
    401: "Unauthorized",
    402: "Payment required",
    403: "Forbidden",
    404: "Not found",
    405: "Method Not allowed",
    406: "Not acceptable",
    407: "Proxy auth required",
    408: "Request timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length required",
    412: "Precondition failed",
    413: "Payload too large",
    414: "URI too long",
    415: "Unsupported media type",
    416: "Range not satisfiable",
    417: "Expectation failed",
    418: "Teapot",
    421: "Misdirected request",
    422: "Unprocessable entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too early",
    426: "Upgrade required",
    428: "Precondition requried",
    429: "Too many requests",
    431: "Request header fields too large",
    451: "Unavailable for legal reasons",
    500: "Internal server error",
    501: "Not implemented",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
    505: "HTTP version not supported",
    506: "Variant also negotiates",
    507: "Insufficient storage",
    508: "Loop detected",
    510: "Not extended",
    511: "Network auth required"
}



exception_log = ""
exception_words = []
loaded_words = []
statuscode_word_mapper = {}

def write_to_file_handler(signalNumber, frame):
    write_to_file()

def load_checked_words():
    global _output_file_name
    try:
        file_object = open(_output_file_name, "r")
    except Exception as e:
        return
    read_data = file_object.readlines()
    for line in read_data:
        line_split = line.split(" ")
        loaded_words.append(line_split[0].rstrip())
    file_object.close()
    del(read_data)

def brute_force_website():
    global status_codes
    global wait_time
    global loaded_words
    global statuscode_word_mapper
    global exception_log
    global _wordlist_file_name
    global _base_url
    global _extra_append_text
    global exception_words

    base_url = _base_url
    file_object = open(_wordlist_file_name, "r")
    words = file_object.readlines()
    file_object.close()
    i = 0
    for word in words:
        word = word.rstrip()
        if(word in loaded_words):
            continue
        i = i + 1
        if(i % 100 == 0):
            write_to_file()
            statuscode_word_mapper = {}
            exception_log = ""
            exception_words = []
        if(i % 30 == 0 and wait_time > 0):
            wait_time = wait_time - 1
        time.sleep(wait_time)
        url =  base_url + word + _extra_append_text
        try: 
            response = requests.get(url)
        except Exception as e:
            print(str(e))
            exception_log = exception_log + str(e)
            exception_words.append(word)
            wait_time += 5
            if(wait_time > 10):
                wait_time = 10
            continue
        response_status = response.status_code
        try:
            print(word + " " + str(response_status) + " " + status_codes[response_status])
            if(response_status in statuscode_word_mapper.keys()):
                statuscode_word_mapper[response_status] = statuscode_word_mapper[response_status] + word + "\n"
            else:
                statuscode_word_mapper[response_status] =  word + "\n"
        except:
            print(word + " " + str(response_status) + " Unknown status code")
    write_to_file()

def write_to_file():
    global exception_log
    global exception_words
    global status_codes
    global wait_time
    global statuscode_word_mapper
    global _output_file_name
    global _base_url
    global _extra_append_text

    file_object = open(_output_file_name, "a")
    i = 0
    
    keys = statuscode_word_mapper.keys()
    for key in keys:
        file_object.write("\n" + str(key) + " - " + status_codes[key] + " \n" + statuscode_word_mapper[key])
    
    for word in exception_words:
        i = i + 1
        if(i % 100 == 0 and wait_time > 0):
            wait_time = wait_time - 1
        time.sleep(wait_time)
        word = word.rstrip()
        url =  _base_url + word + _extra_append_text
        try: 
            response = requests.get(url)
        except Exception as e:
            file_object.write(word + " - " + str(e) + "\n")
            wait_time += 5
            if(wait_time > 10):
                wait_time = 10
            continue
        response_status = response.status_code
        try:
            file_object.write(word + " " + str(response_status) + " " + status_codes[response_status])
        except:
            file_object.write(word + " " + str(response_status) + " Unknown status code")
    if(exception_log != ""):
        file_object.write(exception_log + "\n\n")
    file_object.close()


_base_url = sys.argv[1]
_wordlist_file_name = sys.argv[2]
_output_file_name = sys.argv[3]
_extra_append_text = ""
try:
    _extra_append_text = sys.argv[4]
except:
    pass

load_checked_words()
brute_force_website()