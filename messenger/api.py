#!/usr/bin/env python

import httplib
import os
import requests
import sys

GRAPH_API = "https://graph.facebook.com"
GRAPH_API_URL = "/v2.6"

class MessengerApi:
    def __init__(self):
        self.access_token = os.environ.get('ACCESS_TOKEN')
        if self.access_token == None:
            print("Environment variable ACCESS_TOKEN is not set")
            sys.exit(2)

    def post(self, path, body = None):
        print("* HTTP request: POST " + path)
        if body != None:
            headers = { 'content-type': 'application/json' }
            print("  body: " + body)
        else:
            headers = {}
        response = requests.post(GRAPH_API + GRAPH_API_URL + path, params = { 'access_token': self.access_token }, headers = headers, data = body)
        print("* HTTP response: " + str(response.status_code))
        if response.text != '':
            print("  body: " + response.text)
        return response
