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



headers = {'Content-Type': 'text/xml'}
quest = '<delete><query>(type:1)AND(episode_id:)</query></delete>' 
r = requests.post("http://localhost:9096/solr/update", data=quest, headers=headers)
