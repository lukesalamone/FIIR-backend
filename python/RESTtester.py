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

    def createUser():
        print("create user")
        headers = {'Content-Type': 'application/json'}
        quest = '{"phone":"1234567890", "invitedby":2, "email":"123@gmail.com"}' 
        r = requests.post("http://fiirapp.ddns.net:9096/users/create", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))


    def createPic():
        print("create pic")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret","tag_1":"travel", "user":1, "price":12, "token":"YUJN58HJI8UJ5R"}'
        r = requests.post("http://fiirapp.ddns.net:9096/pics/create", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))


    def addFriend(user,friend):
        print("add friend")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":%s, "friend":%s}'%(user,friend)
        r = requests.post("http://fiirapp.ddns.net:9096/friends/add", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def removeFriend():
        print("remove friend")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":1, "friend":3}'
        r = requests.post("http://fiirapp.ddns.net:9096/friends/remove", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def updateEmail():
        print("update Email")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":1, "email":"newemail@gmail.com"}'
        r = requests.post("http://fiirapp.ddns.net:9096/settings/update_email", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def updatePhone():
        print("update Phone")
        headers = {'Content-Type': 'application/json'}
        quest = '{"key":"secret", "user":3, "phone":"888"}'
        r = requests.post("http://fiirapp.ddns.net:9096/settings/update_phone", data=quest, headers=headers)
        print(str(r))
        print(str(r.text))

    def listFriends(user=1):
        print("list friends")
        r = requests.get("http://fiirapp.ddns.net:9096/friends/list?key=123&user=%s"%(user,))
        print(str(r))
        print(str(r.text))

    def listPictures(user=1):
        print("list friends")
        r = requests.get("http://fiirapp.ddns.net:9096/pics/created?key=123&user=%s"%(user,))
        print(str(r))
        print(str(r.text))

def main():
    tester = fiirRestTester
    #tester.createUser()
    #tester.createPic()
    #tester.updatePhone()
    #tester.updateEmail()
    #tester.addFriend(1,5)
    #tester.removeFriend()
    #tester.listFriends(3)
    tester.listPictures(user=1)

if __name__ == '__main__':
    main()
