#!/usr/bin/env python3

import warnings
import os.path
import time
import datetime
from urllib import request
from urllib import error
from urllib import parse
import xml.etree.ElementTree as ET
import hashlib
import MySQLdb
import sys
import _mysql_exceptions
import requests
import json
import email.utils


class fiirRestTester:

    def createUser(phone="1234567890",invitedBy = 2, email = "123@gmail.com"):
        print("create user")
        headers = {'Content-Type': 'application/json'}
        quest = '{"phone":"%s", "invitedby":%s, "email":"%s"}' %(phone,invitedBy,email)
        r = requests.post("http://fiirapp.ddns.net:9096/users/create", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))


    def createPic(key="secret",tag1="travel",user_id=1,price=12,token="YUJN58HJI8UJ5R"):
        print("create pic")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s","tag_1":"%s", "user":%s, "price":%s, "token":"%s"}' % (key,tag1,user_id,price,token)
        r = requests.post("http://fiirapp.ddns.net:9096/pics/create", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))


    def addFriend(user_id=1,friend_id=3):
        print("add friend")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":%s, "friend":%s}'%(user_id,friend_id)
        r = requests.post("http://fiirapp.ddns.net:9096/friends/add", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def removeFriend(key="secret",user_id=1,friend_id=3):
        print("remove friend")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "friend":%s}'%(key,user_id,friend_id)
        r = requests.post("http://fiirapp.ddns.net:9096/friends/remove", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def updatePromo(key = "secret",user_id = 1, promoCode = "XYZ"):
        print("update Email")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "promoCode":"%s"}' %(key,user_id,promoCode)
        r = requests.post("http://fiirapp.ddns.net:9096/users/setPromo", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))



    def updateEmail(user_id = 1, email = "newemail@gmail.com"):
        print("update Email")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":%s, "email":"%s"}' %(user_id,email)
        r = requests.post("http://fiirapp.ddns.net:9096/settings/update_email", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def updatePhone(key="secret",user_id=3,phone="1234567890"):
        print("update Phone")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "phone":"%s"}'%(key,user_id,phone)
        r = requests.post("http://fiirapp.ddns.net:9096/settings/update_phone", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def listFriends(key="123",user_id=1):
        print("list friends")
        r = requests.get("http://fiirapp.ddns.net:9096/friends/list?key=%s&user=%s"%(key,user_id))
        print(str(r))
        print(str(r.text))

    def listPictures(key="123",user_id=1):
        print("list friends")
        r = requests.get("http://fiirapp.ddns.net:9096/pics/created?key=%s&user=%s"%(key,user_id))
        print(str(r))
        print(str(r.text))

    def uploadPicture():
        print("upload picture")
        files = {"user":"5","key":"123",'fileToUpload': open('/home/app/test.png', 'rb')}
        r = requests.post("http://fiirapp.ddns.net:9096/pics/create",files=files)
        print(str(r))
        print(str(r.text))

    def uploadPicture2():
        print("upload picture")
        files = {"name":"uploadedFile",'file': open('/home/app/backend/python/test.png', 'rb')}
        r = requests.post("http://localhost:8000/pics/create",files=files)
        print(str(r))
        print(str(r.text))


def main():
    tester = fiirRestTester
    #tester.createUser(phone="16083207727",invitedBy = 3, email = "123@gmail.com")
    #tester.createPic(key="secret",tag1="travel",user_id=1,price=12,token="YUJN58HJI8UJ5R")
    #tester.updatePhone(key="secret",user_id=3,phone="1234567890")
    #tester.updateEmail(user_id = 1, email = "newemail@gmail.com")
    #tester.addFriend(user_id=1,friend_id=3)
    tester.removeFriend(key="DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS",user_id=1,friend_id=5)
    #tester.listFriends(key="DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS",user_id=1)
    #listPictures(key="123",user_id=1)
    #tester.uploadPicture()
    #tester.updatePromo(user_id = 1,key="DX0SRYUYZQ4ZQXYSRNWOGZZCPCMIWQS", promoCode = "ZMK")

if __name__ == '__main__':
    main()
