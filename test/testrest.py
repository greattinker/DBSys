#!/usr/bin/python

import httplib, urllib
import json

params = json.dumps( {"username": "user_0"} )
print params

headers = {"Content-type": "application/json", "Accept": "*/*"}
conn = httplib.HTTPConnection("localhost:5000")
conn.request("POST", "/tweets", params, headers)

response = conn.getresponse()
print response.status, response.reason, response
