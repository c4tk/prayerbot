#-*- encoding: utf-8 -*-
import json
import mock
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
        response = self.client.get(url_for('webhook')+'?hub.verify_token=challenge_me&hub.challenge=123')
        assert response.status_code == 200

    def test_fail_verify_token(self):
        response = self.client.get(url_for('webhook')+'?hub.verify_token=dunno&hub.challenge=123')
        assert response.status_code == 400
        assert response.data == 'Wrong validation token'

    def test_fail_verify_challenge(self):
        response = self.client.get(url_for('webhook')+'?hub.verify_token=challenge_me')
        assert response.status_code == 400
        assert response.data == 'Challenge not found'


@pytest.mark.usefixtures('client_class')
class PostWebhookTestSuite(unittest.TestCase, JSONFlaskMixin):

    @mock.patch('prayer.PrayerWebhook.handle_message')
    @mock.patch('facebook.api.FacebookApi.post')
    def test_post_message(self, mock_post, mock_handle_message):
        webhook_response = "{\"message\": \"...\", \"recipient\": {\"id\": \"10208414992228182\"}}"
        mock_handle_message.return_value = webhook_response
        mock_post.return_value = None

        page_id = "17424537847389"
        sender_id = "1533251252189"
        message_event = {
            "mid": "mid.1457764197618:41d102a3e1ae206a38",
            "seq": 73,
            "text": "hello, world!"
        }
        facebook_message = {
            "object": "page",
            "entry": [
                {
                    "id": page_id,
                    "time": 1457764198246,
                    "messaging": [
                        {
                            "sender": {
                                "id": sender_id
                            },
                            "recipient": {
                                "id": page_id
                            },
                            "timestamp": 1457764197627,
                            "message": message_event
                        }
                    ]
                }
            ]
        }
        response = self.json_post(url_for('webhook'), facebook_message)
        assert mock_handle_message.call_args_list == [((sender_id, message_event),)]
        assert mock_post.call_args_list == [(('/me/messages', webhook_response),)]
        assert response.status_code == 200

    @mock.patch('prayer.PrayerWebhook.handle_postback')
    @mock.patch('facebook.api.FacebookApi.post')
    def test_post_postback(self, mock_post, mock_handle_postback):
        webhook_response_callback1 = "{\"message\": \"{\\\"text\\\": \\\"Message to user1\\\"}\", \"recipient\": {\"id\": \"30208415992228182\"}}"
        webhook_response_callback2 = "{\"message\": \"{\\\"text\\\": \\\"Message to user2\\\"}\", \"recipient\": {\"id\": \"1538063784705478\"}}"
        webhook_response = [webhook_response_callback1, webhook_response_callback2]
        mock_handle_postback.return_value = webhook_response
        mock_post.return_value = None

        page_id = "15380637847054"
        sender_id = "1533251252189"
        postback_event = {
            "payload": "{\"user_event\": \"cancel\"}"
        }
        facebook_message = {
            "object": "page",
            "entry": [
                {
                    "id": page_id,
                    "time": 1457764198247,
                    "messaging": [
                        {
                            "sender": {
                                "id": sender_id
                            },
                            "recipient": {
                                "id": page_id
                            },
                            "timestamp": 1457764197627,
                            "postback": postback_event
                        }
                    ]
                }
            ]
        }
        response = self.json_post(url_for('webhook'), facebook_message)
        assert mock_handle_postback.call_args_list == [((sender_id, postback_event),)]
        assert mock_post.call_args_list == [
                (('/me/messages', webhook_response_callback1),),
                (('/me/messages', webhook_response_callback2),)
        ]
        assert response.status_code == 200
