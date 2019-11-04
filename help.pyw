import keyboard
import requests
import configparser
import os

path = "settings.ini"
section = 'Settings'

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section(section)
    config.set(section, "get", "")
    config.set(section, "key", "end")
    config.set(section, "url", "http://localhost:8080/")

    with open(path, "w") as config_file:
        config.write(config_file)


if os.path.exists(path) == False:
    createConfig(path)
config = configparser.ConfigParser()
config.read(path)

while True:
    keyboard.wait(config.get(section, "key"))
    r = requests.get(config.get(section, "url")+config.get(section, "get"))
