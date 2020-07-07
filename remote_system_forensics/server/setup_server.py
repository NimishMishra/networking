from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time

class ServerHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("Path is: " + self.path)
        
        self._set_response()
        response = ""
        current_directory = os.getcwd()
        if(self.path == "/"):
            for file in os.listdir(current_directory):
                response = response + file + "\n"
        else:
            file_to_open = self.path[1:]
            file_object = open(file_to_open, 'r')
            response = file_object.read()
            file_object.close()

        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        try:
            data_split = data.split("SPLIT")
            file_object = open("../responses" + str(time.time()) +".txt", "a")
            for line in data_split:
                file_object.write(line + "\n")
            file_object.close()
        except:
            pass
        self._set_response()
        self.wfile.write(('POST OK').encode('utf-8'))

def run():
    server_address = ('192.168.43.38', 9000)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

run()