#!/usr/bin/env python

import httplib
import os
import sys

GRAPH_API = "graph.facebook.com"
GRAPH_API_URL = "/v2.6"

class MessengerApi:
    def __init__(self):
        self.access_token = os.environ.get('ACCESS_TOKEN')
        if self.access_token == None:
            print("Environment variable ACCESS_TOKEN is not set")
            sys.exit(2)
        
    def request(self, path, body = None):
        # TODO: make connection persistent and init in __init__
        conn = httplib.HTTPSConnection(GRAPH_API, 443)
        url = GRAPH_API_URL + path + "?access_token=" + self.access_token
        print("* HTTP request: POST " + GRAPH_API + url)
        conn.request("POST", url, body, {"Content-type": "application/json"})
        response = conn.getresponse()
        print("* HTTP response: " + str(response.status) + " " + response.reason)
        response_data = response.read()
        if response_data != '':
            print("  body: " + response_data)
        conn.close()

