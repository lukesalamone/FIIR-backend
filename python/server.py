#!/usr/bin/env python3
import json
import warnings
import os.path
import os
import time
import datetime
from urllib import request
from urllib import error
from urllib.parse import urlparse
from urllib.parse import parse_qsl
import xml.etree.ElementTree as ET
import hashlib
import MySQLdb
import sys
import _mysql_exceptions
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from socketserver import ThreadingMixIn
from config import Config
import cgi
import re
from io import StringIO
import shutil
import multipart
import random
import string



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle multiple thread"""

class MyServer(BaseHTTPRequestHandler):
    def json_header(self,status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()



    def do_GET(self):

        requestPath = urlparse(self.path).path
        requestList = requestPath.split('/')
        if len(requestList)!=3 or requestList[0]!= '':
            self.json_header(400)
            self.wfile.write(bytes('{"error":"invalid request format"}', "utf-8"))

        query = urlparse(self.path).query
        queryList = dict(parse_qsl(query))
        #print(str(queryList))

        #routing
        if requestList[1]=='pics' and requestList[2]=='created':
            self.listPics(queryList)
        elif requestList[1]=='friends' and requestList[2]=='list':
            self.listFriends(queryList)
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"error":"illegal GET request"}', "utf-8"))
    def listPics(self,queryList):
        #query format validation
        if 'key' in queryList and 'user' in queryList:
            key = queryList['key']
            user = queryList['user']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing GET query"}', "utf-8"))
            return

        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "SELECT price,date_added,id FROM PICS WHERE user_id=%s;"
        curMy.execute(query,(user,));
        result = curMy.fetchall()
        connMy.close()

        
        pictures = "["
        for row in result:
            price = row[0]
            date_added = row[1]
            pid = row[2]
            pictures +='{"id":%s,"price":%s,"date_added":"%s"}'%(pid,price,date_added)
        pictures +="]"

        #send back picture list
        self.json_header()
        self.wfile.write(bytes('{"status":"success","num_pic":%s,"pictures":%s}'%(len(result),pictures), "utf-8"))

    def listFriends(self,queryList):
        #query format validation
        if 'key' in queryList and 'user' in queryList:
            key = queryList['key']
            user = queryList['user']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing GET query"}', "utf-8"))
            return

        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "SELECT u.id,u.phone_number,u.email_address,u.name,f.date_added FROM FRIENDS AS f, USER AS u WHERE f.friend_id=u.id AND f.user_id=%s;"
        curMy.execute(query,(user,));
        result = curMy.fetchall()
        connMy.close()


        friends = "["
        for row in result:
            uid = row[0]
            phone_number = row[1]
            email_address = row[2]
            name = row[3]
            friendSince = row[4]
            if len(friends)!=1:
                friends +=','
            friends +='{"uid":%s,"phone_number":"%s","email_address":"%s","name":"%s","friend_since":"%s"}'%(uid,phone_number,email_address,name,friendSince)
        friends +="]"

        #send back picture list
        self.json_header()
        self.wfile.write(bytes('{"status":"success","num_friend":%s,"friends":%s}'%(len(result),friends), "utf-8"))
    



    def do_POST(self):
        print(self.headers)
        print('*' * 60)
        if self.headers.get_content_maintype()=="multipart":
            #self.deal_post_display()
            self.createPic()
            return


        requestPath = self.path
        requestList = requestPath.split('/')
        if len(requestList)!=3 or requestList[0]!= '':
            self.json_header(400)
            self.wfile.write(bytes('{"error":"invalid request format"}', "utf-8"))


        #read in request content
        varLen = int(self.headers['Content-Length'])
        postVars = self.rfile.read(varLen)
        postContent = None
        print(postVars)
        try:
            postContent = json.loads(postVars.decode('utf-8'))
        except BaseException as e:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object:%s"}'%(str(e),), "utf-8"))
            return


        #routing
        if requestList[1]=='users' and requestList[2]=='create':
            self.createUser(postContent)
        elif requestList[1]=='friends' and requestList[2]=='add':
            self.addFriend(postContent)
        elif requestList[1]=='friends' and requestList[2]=='remove':
            self.removeFriend(postContent)
        elif requestList[1]=='settings' and requestList[2]=='update_email':
            self.updateEmail(postContent)
        elif requestList[1]=='settings' and requestList[2]=='update_phone':
            self.updatePhone(postContent)
            
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"error":"illegal operation"}', "utf-8"))
    def updateEmail(self,postContent):


        #json format validation
        if 'key' in postContent and 'user' in postContent and 'email' in postContent:
            key = postContent['key']
            user = postContent['user']
            email = postContent['email']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "UPDATE USER SET email_address=%s WHERE id=%s;"
        curMy.execute(query,(email,user));
        connMy.commit();
        connMy.close()
        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"email successfully updated"}', "utf-8"))

    def updatePhone(self,postContent):


        #json format validation
        if 'key' in postContent and 'user' in postContent and 'phone' in postContent:
            key = postContent['key']
            user = postContent['user']
            phone = postContent['phone']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "UPDATE USER SET phone_number=%s WHERE id=%s;"
        curMy.execute(query,(phone,user));
        connMy.commit();
        connMy.close()
        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"phone number successfully updated"}', "utf-8"))



    def createPic(self):
        multiparser = multipart.MultipartParser(self.rfile,self.headers.get_boundary(),content_length=int(self.headers['content-length']))
        key = multiparser.get("key")
        user_id = multiparser.get("user")
        if key is None or user_id is None:
            self.json_header(400)
            self.wfile.write(bytes('{"msg":"invalid key field"}', "utf-8"))
            return

        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()


        uploadedFile = multiparser.get("fileToUpload")
        if uploadedFile is None:
            self.json_header(400)
            self.wfile.write(bytes('{"msg":"invalid uploaded image"}', "utf-8"))
            return
        fileExt = os.path.splitext(uploadedFile.filename)[1]
        fileNameIsValid = False
        while fileNameIsValid is False:
            randomStr = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
            query = 'SELECT COUNT(*) FROM `PICS` WHERE `filename` = %s'
            curMy.execute(query,(randomStr+fileExt,));
            nameCount = curMy.fetchone()[0]
            if nameCount>0:
                fileNameIsValid = False
            else:
                fileNameIsValid = True



        uploadedFile.save_as("/var/www/fiir/img/"+randomStr+fileExt)
        #r, info = self.deal_post_data()
        #print( "%s,%s,%s,%s"%(r, info, "by: ", self.client_address))


        

        #update database
        query = "INSERT INTO PICS (user_id,filename) VALUES (%s,%s);"
        curMy.execute(query,(user_id.value,randomStr+fileExt));
        connMy.commit();
        connMy.close()
        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"picture successfully created"}', "utf-8"))

    def addFriend(self,postContent):


        #json format validation
        if 'key' in postContent and 'user' in postContent and 'friend' in postContent:
            key = postContent['key']
            user = postContent['user']
            friend = postContent['friend']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "INSERT INTO FRIENDS (user_id,friend_id) VALUES (%s,%s),(%s,%s);"
        curMy.execute(query,(user,friend,friend,user));
        connMy.commit();
        connMy.close()
        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"friend successfully added"}', "utf-8"))

    def removeFriend(self,postContent):


        #json format validation
        if 'key' in postContent and 'user' in postContent and 'friend' in postContent:
            key = postContent['key']
            user = postContent['user']
            friend = postContent['friend']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "DELETE FROM FRIENDS WHERE user_id = %s AND friend_id=%s;"
        curMy.execute(query,(user,friend));
        query = "DELETE FROM FRIENDS WHERE user_id = %s AND friend_id=%s;"
        curMy.execute(query,(friend,user));
        connMy.commit();
        connMy.close()

        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"friend successfully removed"}', "utf-8"))


    def createUser(self,postContent):

        #json format validation
        if 'phone' in postContent and 'invitedby' in postContent and 'email' in postContent:
            phoneNumber = postContent['phone']
            invitedBy = postContent['invitedby']
            email = postContent['email']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8') 
        curMy = connMy.cursor()
        query = "INSERT INTO USER (phone_number,invited_by,email_address) VALUES (%s,%s,%s);"
        curMy.execute(query,(phoneNumber,invitedBy,email));
        connMy.commit();
        connMy.close()

        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"user successfully created"}', "utf-8"))

    def do_POST2(self):
        """Serve a POST request."""
        if self.headers.is_multipart():
            r, info = self.deal_post_data()
            print( "%s,%s,%s,%s"%(r, info, "by: ", self.client_address))
        
            self.json_header()
            self.wfile.write(bytes('{"success":"invalid request format"}', "utf-8"))

    def deal_post_display(self):
        remainbytes = int(self.headers['content-length'])
        while remainbytes>0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            print(line)
        return (True,"success")

    def deal_post_data(self):
        #print(self.headers)
        #print(type(self.headers))
        #print(self.headers.get_boundary())
        boundary = self.headers.get_boundary()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        print(type(line))
        if not str.encode(boundary) in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        print(line)
        fn = re.findall(str.encode('Content-Disposition.*name="file"; filename="(.*)"'), line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        print(str(path))
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
                
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path







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



