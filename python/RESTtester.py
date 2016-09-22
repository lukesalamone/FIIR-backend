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



headers = {'Content-Type': 'application/json'}
quest = '{"phone":"1234567890", "invitedby":"1", "email":"test@gmail.com"}' 
r = requests.post("http://localhost:9096/users/create", data=quest, headers=headers)
print(str(r))


