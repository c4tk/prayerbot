#!/usr/bin/env python

import os
import sys

import requests

GRAPH_API = "https://graph.facebook.com/"

class FacebookApi:
    def __init__(self, version = "v2.8"):
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.version = version
        self.base_url = GRAPH_API + self.version
        if self.access_token == None:
            print("Environment variable ACCESS_TOKEN is not set")
            sys.exit(2)

    def get(self, path):
        print("* HTTP request: GET " + path)
        response = requests.get(self.base_url + path, params = { 'access_token': self.access_token })
        print("* HTTP response: " + str(response.status_code))
        if response.text != '':
            print("  body: " + response.text)
        return response

    def post(self, path, body = None):
        print("* HTTP request: POST " + path)
        if body != None:
            headers = { 'content-type': 'application/json' }
            print("  body: " + body)
        else:
            headers = {}
        response = requests.post(self.base_url + path, params = { 'access_token': self.access_token }, headers = headers, data = body)
        print("* HTTP response: " + str(response.status_code))
        if response.text != '':
            print("  body: " + response.text)
        return response