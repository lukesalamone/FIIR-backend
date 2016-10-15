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
import requests
import smtplib



upload_debug_mode = 0
# upload_debug_mode = 1 displaying picture binary content
# upload_debug_mode = 0 normal uploading mode


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle multiple thread"""

class MyServer(BaseHTTPRequestHandler):
    def json_header(self,status_code=200):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()



    def do_GET(self):
        print(self.headers)

        requestPath = urlparse(self.path).path
        requestList = requestPath.split('/')
        if len(requestList)!=3 or requestList[0]!= '':
            self.json_header(400)
            self.wfile.write(bytes('{"error":"invalid request format"}', "utf-8"))
            return
        query = urlparse(self.path).query
        queryList = dict(parse_qsl(query))
        #print(str(queryList))


        #routing
        if requestList[1]=='pics' and requestList[2]=='created':
            self.listPics(queryList)
        elif requestList[1]=='friends' and requestList[2]=='list':
            self.listFriends(queryList)
        elif requestList[1]=='newest' and requestList[2]=='pics':
            self.listNewPics()


        else:
            self.json_header(400)
            self.wfile.write(bytes('{"error":"illegal GET request"}', "utf-8"))


    def listNewPics(self):


        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "SELECT price,date_added,id FROM PICS  ORDER BY `date_added` DESC LIMIT 20;"
        curMy.execute(query);
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




    def listPics(self,queryList):
        #query format validation
        key = self.headers.get("key")
        user = self.headers.get("user")

        #if 'key' in queryList and 'user' in queryList:
        #    key = queryList['key']
        #    user = queryList['user']
        if key is None or user is None:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing GET query"}', "utf-8"))
            return

        auth_result = self.authenticate(user,key)
        if auth_result == -1:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid key"}', "utf-8"))
            return
        elif auth_result == -2:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid user id"}', "utf-8"))
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

    def authenticate(self,user_id,key):


        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()

        query = "SELECT auth_token,salt FROM USER WHERE id = %s;"
        curMy.execute(query,(user_id,));
        credentials = curMy.fetchone()
        connMy.close()
        if credentials is None:
            return -2
        if credentials[0] == '' or credentials[0] is None or credentials[1] == '' or credentials[1] is None:
            return -3
        auth_token = credentials[0]
        salt = credentials[1]
        hashedKey = str(hashlib.sha256((key+salt).encode()).hexdigest())
        if hashedKey!=auth_token:
            return -1

        return 0


    def listFriends(self,queryList):
        key = self.headers.get("key")
        user = self.headers.get("user")

        #query format validation
        #if 'key' in queryList and 'user' in queryList:
        #    key = queryList['key']
        #    user = queryList['user']
        if key is None or user is None:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing GET query"}', "utf-8"))
            return
        auth_result = self.authenticate(user,key)
        if auth_result == -1:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid key"}', "utf-8"))
            return
        elif auth_result == -2:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid user id"}', "utf-8"))
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
        sys.stdout.flush()
        if self.headers.get_content_maintype()=="multipart":

            if upload_debug_mode == 1:

                self.deal_post_display()
            else:
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
            print("error parsing json object")
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object:%s"}'%(str(e),), "utf-8"))
            return


        #routing: user creation
        if requestList[1]=='users' and requestList[2]=='create':
            self.createUser(postContent)
            return
        if requestList[1]=='users' and requestList[2]=='verify':
            self.verifyUser(postContent)
            return

        #json format validation
        if 'key' in postContent and 'user' in postContent:
            key = postContent['key']
            user = postContent['user']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        auth_result = self.authenticate(user,key)
        if auth_result == -1:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid key"}', "utf-8"))
            return
        elif auth_result == -2:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"invalid user id"}', "utf-8"))
            return
        elif auth_result == -3:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"user not verified"}', "utf-8"))
            return


        #routing: operations that should be authenticated beforehand
        if requestList[1]=='friends' and requestList[2]=='add':
            self.addFriend(postContent)
        elif requestList[1]=='friends' and requestList[2]=='remove':
            self.removeFriend(postContent)
        elif requestList[1]=='settings' and requestList[2]=='update_email':
            self.updateEmail(postContent)
        elif requestList[1]=='settings' and requestList[2]=='update_phone':
            self.updatePhone(postContent)
        elif requestList[1]=='users' and requestList[2]=='setPromo':
            self.setPromocode(postContent)
        elif requestList[1]=='pics' and requestList[2]=='flag':
            self.updatePic(postContent,flagged=True)
        elif requestList[1]=='pics' and requestList[2]=='hide':
            self.updatePic(postContent,hided=True)
        elif requestList[1]=='pics' and requestList[2]=='like':
            self.updatePic(postContent,liked=True)
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"error":"illegal operation"}', "utf-8"))

    def updatePic(self,postContent,flagged=False,hided = False,liked = False):

        #json format validation
        if 'user' in postContent and 'picId' in postContent:
            user = postContent['user']
            picId = postContent['picId']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()

        query = "SELECT COUNT(*) FROM PICS WHERE id = %s;"
        curMy.execute(query,(picId,))
        picExisted = curMy.fetchone()[0]
        if picExisted==0:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"the picture %s does not exist"}'%(picId,), "utf-8"))
            return


        if liked == False:
            query = "SELECT user_id FROM PICS WHERE id = %s;"
            curMy.execute(query,(picId,))
            picOwner = curMy.fetchone()[0]
            if picOwner != user:
                self.json_header(400)
                self.wfile.write(bytes('{"status":"error","msg":"this picture is not owned by %s"}'%(user,), "utf-8"))
                return

        if flagged == True:
            query = "UPDATE PICS SET flagged=1 WHERE id=%s;"
            curMy.execute(query,(picId,));
            connMy.commit();
            connMy.close()
            #send success response
            self.json_header()
            self.wfile.write(bytes('{"status":"success","msg":"picture %s successfully flagged"}' %(picId,), "utf-8"))

        if hided == True:
            query = "UPDATE PICS SET hided=1 WHERE id=%s;"
            curMy.execute(query,(picId,));
            connMy.commit();
            connMy.close()
            #send success response
            self.json_header()
            self.wfile.write(bytes('{"status":"success","msg":"picture %s successfully hided"}' %(picId,), "utf-8"))

        if liked == True:

            query = "SELECT COUNT(*) FROM LIKED WHERE pic_id = %s AND user_id = %s;"
            curMy.execute(query,(picId,user))
            likeExisted = curMy.fetchone()[0]
            if likeExisted!=0:
                self.json_header(400)
                self.wfile.write(bytes('{"status":"error","msg":"the picture %s is already liked by user %s"}'%(picId,user), "utf-8"))
                return


            query = "INSERT INTO LIKED (user_id, pic_id) VALUES (%s,%s);"
            curMy.execute(query,(user,picId));
            connMy.commit();
            connMy.close()
            #send success response
            self.json_header()
            self.wfile.write(bytes('{"status":"success","msg":"picture %s successfully liked"}' %(picId,), "utf-8"))





    
    def setPromocode(self,postContent):


        #json format validation
        if 'user' in postContent and 'promoCode' in postContent:
            user = postContent['user']
            promoCode = postContent['promoCode']

        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"errors parsing json object"}', "utf-8"))
            return

        #update database
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        query = "UPDATE USER SET promo_code=%s WHERE id=%s;"
        curMy.execute(query,(promoCode,user));
        connMy.commit();
        connMy.close()
        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"promoCode successfully updated"}', "utf-8"))



    def updateEmail(self,postContent):


        #json format validation
        if 'user' in postContent and 'email' in postContent:
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

    def sanitizePhone(self,number):
        number=''.join(list(filter(str.isdigit, number)))
        number= number if len(number)<=10 else number[len(number)-10:] 
        return number

    def updatePhone(self,postContent):


        #json format validation
        if 'user' in postContent and 'phone' in postContent:
            user = postContent['user']
            phone = self.sanitizePhone(postContent['phone'])

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
        try:
            multiparser = multipart.MultipartParser(self.rfile,self.headers.get_boundary(),content_length=int(self.headers['content-length']))
        except BaseException as e:
            print("multipart parsing error: "+ str(e))
            return
        key = multiparser.get("key")
        user_id = multiparser.get("user")
        #print("multipart key:"+str(key.value))
        #print("multipart user:"+str(user_id.value))
        if user_id is None or key is None:
            self.json_header(400)
            print("userid or key not well-formatted")
            self.wfile.write(bytes('{"msg":"invalid key field"}', "utf-8"))
            return

        auth_result = self.authenticate(user_id.value,key.value)
        if auth_result == -1:
            self.json_header(400)
            print("auth invalid key")
            self.wfile.write(bytes('{"status":"error","msg":"invalid key"}', "utf-8"))
            return
        elif auth_result == -2:
            self.json_header(400)
            print("invalid user id")
            self.wfile.write(bytes('{"status":"error","msg":"invalid user id"}', "utf-8"))
            return



        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8')
        curMy = connMy.cursor()
        for part in multiparser:
            print(part.name)
        uploadedFile = multiparser.get("uploadedfile")
        if uploadedFile is None:
            self.json_header(400)
            print("invalid uploaded image")
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



        uploadedFile.save_as("/var/www/html/pics/"+randomStr+fileExt)
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
        if 'user' in postContent and 'friend' in postContent:
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
        if 'user' in postContent and 'friend' in postContent:
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

        query = 'SELECT COUNT(*) FROM USER WHERE id = %s'
        curMy.execute(query,(user,));
        nameCount = curMy.fetchone()[0]
        if nameCount==0:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"err","msg":"user %s does not exist"}' %(user,), "utf-8"))
            return
        query = 'SELECT COUNT(*) FROM USER WHERE id = %s'
        curMy.execute(query,(friend,));
        nameCount = curMy.fetchone()[0]
        if nameCount==0:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"err","msg":"friend_id %s does not exist"}' %(friend,), "utf-8"))
            return
        query = 'SELECT COUNT(*) FROM FRIENDS WHERE user_id = %s AND friend_id = %s'
        curMy.execute(query,(user,friend));
        nameCount = curMy.fetchone()[0]
        if nameCount==0:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"err","msg":"%s and %s are not friend yet"}' %(user,friend), "utf-8"))
            return




        query = "DELETE FROM FRIENDS WHERE user_id = %s AND friend_id=%s;"
        curMy.execute(query,(user,friend));
        query = "DELETE FROM FRIENDS WHERE user_id = %s AND friend_id=%s;"
        curMy.execute(query,(friend,user));
        connMy.commit();
        connMy.close()

        #send success response
        self.json_header()
        # -1 server error, 0 user error
        self.wfile.write(bytes('{"status":"ok","msg":"firend %s successfully removed"}' %(friend,), "utf-8"))


    def createUser(self,postContent):

        #json format validation
        if 'phone' in postContent and 'invitedby' in postContent and 'email' in postContent:
            phoneNumber = self.sanitizePhone(postContent['phone'])
            invitedBy = postContent['invitedby']
            email = postContent['email']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"incomplete sign up request"}', "utf-8"))
            return

        if len(phoneNumber)>10:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"bad phone number"}', "utf-8"))
            return
        
        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8') 
        curMy = connMy.cursor()
        query = "INSERT INTO USER (phone_number,invited_by,email_address,salt) VALUES (%s,%s,%s,'');"
        curMy.execute(query,(phoneNumber,invitedBy,email));
        connMy.commit();

        query ="SELECT LAST_INSERT_ID();"
        curMy.execute(query);
        user_id = curMy.fetchone()[0]


        res = requests.get("http://apilayer.net/api/validate?access_key=afe1b8406a16a12087107bcaa5c483eb&number=%s&country_code=US&format=1"%(phoneNumber,))
        telInfo = None
        try:
            telInfo = json.loads(res.text)
        except BaseException as e:
            print("error: " + str(e))



        if telInfo is not None and 'line_type' in telInfo and 'carrier' in telInfo and 'location' in telInfo:



            query = "UPDATE USER SET tel_carrier = %s, tel_location = %s, tel_line_type = %s WHERE id = %s;"
            curMy.execute(query,(telInfo['carrier'],telInfo['location'],telInfo['line_type'],user_id));
            connMy.commit();
        
        if telInfo is not None and 'carrier' in telInfo:

            activationCode = ''.join(random.SystemRandom().choice(string.digits) for _ in range(6))

            res = self.sendToNumber(phoneNumber,telInfo['carrier'],activationCode)
            if res == -1:
                self.json_header(400)
                self.wfile.write(bytes('{"status":"error","msg":"unrecognized carrier"}', "utf-8"))
                return


            query = "UPDATE USER SET activation_code = %s WHERE id = %s;"
            curMy.execute(query,(activationCode,user_id));
            connMy.commit();
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"phone number invalid, no carrier detected"}', "utf-8"))
            return


        connMy.close()

        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"user successfully created","user_id":"%s"}'%(user_id,), "utf-8"))

    def verifyUser(self, postContent):



        #json format validation
        if 'user' in postContent and 'verification' in postContent:
            verification = postContent['verification']
            user = postContent['user']
        else:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"incomplete verify request"}', "utf-8"))
            return



        conf = Config()     #load configuration
        connMy = MySQLdb.connect(host=conf.host, user=conf.username,passwd=conf.password,db='fiir',charset='utf8') 
        curMy = connMy.cursor()


        query = 'SELECT activation_code FROM USER WHERE id = %s '
        curMy.execute(query,(user,));
        activation_code = curMy.fetchone()[0]

        if activation_code is None or activation_code =='':
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"user not verifiable"}', "utf-8"))
            return

        if activation_code != verification:
            self.json_header(400)
            self.wfile.write(bytes('{"status":"error","msg":"wrong activation code"}', "utf-8"))
            return



        salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))
        password =  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        hashedKey = str(hashlib.sha256((password+salt).encode()).hexdigest())


        query = "UPDATE USER SET auth_token = %s ,salt = %s, activation_code='' WHERE id =%s;"
        curMy.execute(query,(hashedKey,salt,user));
        connMy.commit();






        connMy.close()

        #send success response
        self.json_header()
        self.wfile.write(bytes('{"status":"user successfully verified","auth_token":"%s"}'%(password,), "utf-8"))


    def deal_post_display(self):
        remainbytes = int(self.headers['content-length'])
        while remainbytes>0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            print(line)
        return (True,"success")

    def sendToNumber(self,phoneNumber,carrier,msgToSend):
        if carrier == 'AT&T Mobility LLC':
            toaddrs = phoneNumber + '@txt.att.net'
        elif carrier =='Sprint Corp.':
            toaddrs = phoneNumber + '@messaging.sprintpcs.com'
        else:
            print("unrecognized carrier:"+carrier)
            return -1
        print("send to number:"+phoneNumber)
        fromaddr = 'fiirappmain@gmail.com'
        msg =  str(msgToSend)
        print(msg)
        server = smtplib.SMTP("smtp.gmail.com:587")

        server.starttls()

        server.login("fiirappmain","1234qwerZ")

        server.sendmail(fromaddr, toaddrs, msg)

        # Send the message via our own SMTP server.
        server.quit()
        return 0

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



