#-*- encoding: utf-8 -*-
import json
import pytest
import unittest
from flask import url_for

class JSONFlaskMixin(object):
    def json_post(self, url, data):
        headers = [('Content-Type', 'application/json')]
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))
        return self.client.post(url, headers=headers, data=json_data)

@pytest.mark.usefixtures('client_class')
class ChallengeWebhookTestSuite(unittest.TestCase):

    def test_verify(self):
        assert self.client.get(url_for('webhook')+'?hub.verify_token=challenge_me&hub.challenge=123').status_code == 200

    def test_fail_verify_token(self):
        assert self.client.get(url_for('webhook')+'?hub.verify_token=dunno&hub.challenge=123').status_code == 400

    def test_fail_verify_challenge(self):
        assert self.client.get(url_for('webhook')+'?hub.verify_token=challenge_me').status_code == 400

@pytest.mark.usefixtures('client_class')
class PostWebhookTestSuite(unittest.TestCase, JSONFlaskMixin):

    def test_post_message(self):
        facebook_message = {
            "object": "page",
            "entry": [
                {
                    "id": 1122,
                    "time": 1457764198246,
                    "messaging": [
                        {
                            "sender": {
                                "id": "USER_ID"
                            },
                            "recipient": {
                                "id": "PAGE_ID"
                            },
                            "timestamp": 1457764197627,
                            "message": {
                                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                                "seq": 73,
                                "text": "hello, world!"
                            }
                        }
                    ]
                }
            ]
        }
        assert self.json_post(url_for('webhook'), facebook_message).status_code == 200
