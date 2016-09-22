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
from config import Config



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
        requestPath = self.path
        requestList = requestPath.split('/')
        if len(requestList)!=3 or requestList[0]!= '':
            self.json_header(400)
            self.wfile.write(bytes('{"error":"invalid request format"}', "utf-8"))
        print("do_post")

        if requestList[1]=='users' and requestList[2]=='create':
            self.user_create()

    def user_create(self):

        #read in content
        varLen = int(self.headers['Content-Length'])
        postVars = self.rfile.read(varLen)
        postContent = None
        try:
            postContent = json.loads(postVars.decode('utf-8'))
        except BaseException as e:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object:%s"}'%(str(e),), "utf-8"))
            return

        #json format validation
        if 'phone' in postContent and 'invitedby' in postContent and 'email' in postContent:
            phoneNumber = postContent['phone']
            invitedBy = postContent['invitedby']
            email = postContent['email']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object:%s"}'%(str(e),), "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8') 
        curMy = connMy.cursor()
        query = "INSERT INTO USER (phone_number,invited_by,email_address) VALUES (%s,%s,%s);"
        curMy.execute(query,(phoneNumber,invitedBy,email));
        connMy.commit();

        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"user successfully created"}', "utf-8"))



def main():

    hostName = "0.0.0.0"
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



