#!/usr/bin/python
import os
import sys
import json

# Turn on debug mode.
import cgitb
cgitb.enable()

STATUS_OK = 'Status: 200 OK'
STATUS_ERROR = 'Status: 500 ERROR'

def sendResponse(status, response):
    print status
    print 'Content-Type: application/json'
    print ''
    print json.dumps(response)


# Print necessary headers.
try:
    post = ''.join([line for line in sys.stdin])
    post = json.loads(post)
except Exception as e:
    sendResponse(STATUS_ERROR, {'Error': str(e)})

sendResponse(STATUS_OK, post)
