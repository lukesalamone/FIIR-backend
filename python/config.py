import sys
import xml
import xml.etree.ElementTree as ET
import os



class Config(object):


    def __init__(self):
        tree = ET.parse(os.path.dirname(os.path.realpath(__file__)) + '/config/config.xml')
        root = tree.getroot()
        self.host = root.find('database').find('host').text
        self.databasename = root.find('database').find('databasename').text
        self.username = root.find('database').find('user').text
        self.password = root.find('database').find('password').text
