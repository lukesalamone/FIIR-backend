#!/usr/bin/env python3
import json
import warnings
import os.path
import time
import datetime
from urllib import request
from urllib import error
import xml.etree.ElementTree as ET
import hashlib
import MySQLdb
import sys
import _mysql_exceptions
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from socketserver import ThreadingMixIn




class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle multiple thread"""

class MyServer(BaseHTTPRequestHandler):


    def json_header(self,status_code=200):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        print("do_get")
        self.json_header()
        self.wfile.write(bytes('{"status":"GET still in progress"}', "utf-8"))





    def do_POST(self):
        print("do_post")
        self.json_header()
        self.wfile.write(bytes('{"status":"GET still in progress"}', "utf-8"))


def main():

    hostName = "localhost"
    hostPort = 9096
    myServer = ThreadedHTTPServer((hostName, hostPort), MyServer)
    print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))


if __name__ == '__main__':
    main()



