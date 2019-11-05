from BaseHTTPServer import BaseHTTPRequestHandler
import subprocess
import configparser
import os

path = "server.ini"
section = 'Settings'

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section(section)
    config.set(section, "port", "8080")
    config.set(section, "tv_path", "C:\\Program Files\\TightVNC\\tvnviewer.exe")
    config.set(section, "pass", "vncpass")

    with open(path, "w") as config_file:
        config.write(config_file)


if os.path.exists(path) == False:
    createConfig(path)
config = configparser.ConfigParser()
config.read(path)


class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        qeury = self.path[1:].replace('?', '').split('&')
        if qeury == ['favicon.ico']:
            self.wfile.write('https://www.gravatar.com/avatar/d92ce60d3a4cbe03598e27c2e8dee69d?s=32&d=identicon&r=PG')
        if self.path != '/favicon.ico':
            subprocess.Popen([config.get(section, "tv_path"),'-host='+self.address_string(),
                              '-password='+config.get(section, "pass")], shell=True)
            self.wfile.write(self.address_string() + ' ' + ';'.join(qeury))
            with open("log.txt", "a") as myfile:
                myfile.write(self.address_string() + ' ' + ';'.join(qeury)+'\n')
        return


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', int(config.get(section, "port"))), GetHandler)
    server.serve_forever()
