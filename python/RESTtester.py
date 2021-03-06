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

    def createUser(phone="1234567890",invitedBy = 2, email = "123@gmail.com", carrier = None):
        print("create user")
        headers = {'Content-Type': 'application/json'}
        if carrier is None:
            quest = '{"phone2":"%s", "invitedby":%s, "email":"%s"}' %(phone,invitedBy,email)
        else:
            quest = '{"phone2":"%s", "invitedby":%s, "email":"%s", "carrier":"%s"}' %(phone,invitedBy,email,carrier)
        r = requests.post("http://fiirapp.ddns.net:9096/users/create", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))
    def verifyUser(user_id = 10, verification = '893021'):
        print("verify user")
        headers = {'Content-Type': 'application/json'}
        quest = '{"user":%s, "verification":"%s"}' %(user_id,verification)
        r = requests.post("http://fiirapp.ddns.net:9096/users/verify", data=quest, headers=headers)
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
        headers = {'key': key,'user':user_id }
        r = requests.get("http://fiirapp.ddns.net:9096/friends/list", headers = headers)
        print(str(r))
        print(str(r.text))

    def listNewPics():
        print("list newest pictures")
        r = requests.get("http://fiirapp.ddns.net:9096/newest/pics")
        print(str(r))
        print(str(r.text))

    def listPictures(key="123",user_id=1):
        print("list pictures")
        headers = {'key': key,'user':user_id }
        r = requests.get("http://fiirapp.ddns.net:9096/pics/created%s&user=%s"%(key,user_id))
        print(str(r))
        print(str(r.text))

    def uploadPicture(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS'):
        print("upload picture")
        files = {"user":user,"key":key,'uploadedfile': open('/home/app/test.png', 'rb')}
        r = requests.post("http://fiirapp.ddns.net:9096/pics/create",files=files)
        print(str(r))
        print(str(r.text))

    def uploadPicture2():
        print("upload picture")
        files = {"name":"uploadedFile",'file': open('/home/app/backend/python/test.png', 'rb')}
        r = requests.post("http://localhost:8000/pics/create",files=files)
        print(str(r))
        print(str(r.text))

    def flagPic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '18'):
        print("flag picture")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "picId":"%s"}'%(key,user,picId)
        r = requests.post("http://fiirapp.ddns.net:9096/pics/flag", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def hidePic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '18'):
        print("hide picture")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "picId":"%s"}'%(key,user,picId)
        r = requests.post("http://fiirapp.ddns.net:9096/pics/hide", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))
    def likePic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '18'):
        print("like picture")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"%s", "user":%s, "picId":"%s"}'%(key,user,picId)
        r = requests.post("http://fiirapp.ddns.net:9096/pics/like", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))




def main():
    tester = fiirRestTester
    tester.createUser(phone="16083207727",invitedBy = 1, email = "123@gmail.com",carrier = "verizon")
    #tester.verifyUser(user_id = 20, verification = '343435')
    #tester.createPic(key="secret",tag1="travel",user_id=1,price=12,token="YUJN58HJI8UJ5R")
    #tester.updatePhone(key="secret",user_id=3,phone="1234567890")
    #tester.updateEmail(user_id = 1, email = "newemail@gmail.com")
    #tester.addFriend(user_id=1,friend_id=3)
    #tester.removeFriend(key="DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS",user_id=1,friend_id=5)
    #tester.listFriends(key="DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS",user_id=1)
    #listPictures(key="123",user_id=1)
    #tester.uploadPicture()
    #tester.listNewPics()
    #tester.updatePromo(user_id = 1,key="DX0SRYUYZQ4ZQXYSRNWOGZZCPCMIWQS", promoCode = "ZMK")
    #tester.flagPic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '18')
    #tester.hidePic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '17')
    #tester.likePic(user='1',key='DX0SRPYUYZQ4ZQXYSRNWOGZZCPCMIWQS',picId = '17')


if __name__ == '__main__':
    main()
