#!/usr/bin/python

import httplib, urllib
import json

params = json.dumps( {"username": "ich", "password": "pw123"} )
print params

headers = {"Content-type": "application/json", "Accept": "*/*"}
conn = httplib.HTTPConnection("localhost:5000")
conn.request("POST", "/create_user", params, headers)

response = conn.getresponse()
print response.status, response.reason
