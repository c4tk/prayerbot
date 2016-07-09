#-*- encoding: utf-8 -*-

import json
import mock
import unittest

from events import UserEvent
from prayer import PrayerWebhook


class MessengerBotTestSuite(unittest.TestCase):

    @mock.patch('facebook.user_utils.locale')
    def test_help_message(self, mock_locale):
        mock_locale.return_value = 'en_GB'

        sender_id = '11'
        message = {'text': u"Help"}
        response = handle_message(sender_id, message)
        assert_response(response, sender_id, {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': u"Please choose what do you need?",
                    'buttons': [
                        {
                            'type': 'postback',
                            'title': u"Please pray for me",
                            'payload': '{\"user_event\": ' + str(UserEvent.PRAY_FOR_ME.value) + '}'
                        },
                        {
                            'type': 'postback',
                            'title': u"I want to pray",
                            'payload': '{\"user_event\": ' + str(UserEvent.WANT_TO_PRAY.value) + '}'
                        },
                        ########################################
                        # this block shouldn't be present here #
                        # when there are no commited prayers   #
                        ########################################
                        {
                            'type': 'postback',
                            'title': u"Who do I pray for?",
                            'payload': '{\"user_event\": ' + str(UserEvent.MY_PRAYERS.value) + '}'
                        },
                        #########################################
                    ]
                }
            }
        })

    @mock.patch('facebook.user_utils.locale')
    def test_pray_message(self, mock_locale):
        mock_locale.return_value = 'en_GB'

        sender_id = '12'
        message = {'text': u"How can I pray?"}
        response = handle_message(sender_id, message)
        assert_response(response, sender_id, {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': u"Please choose what do you need?",
                    'buttons': [
                        {
                            'type': 'postback',
                            'title': u"Please pray for me",
                            'payload': '{\"user_event\": ' + str(UserEvent.PRAY_FOR_ME.value) + '}'
                        },
                        {
                            'type': 'postback',
                            'title': u"I want to pray",
                            'payload': '{\"user_event\": ' + str(UserEvent.WANT_TO_PRAY.value) + '}'
                        },
                        {
                            'type': 'postback',
                            'title': u"Who do I pray for?",
                            'payload': '{\"user_event\": ' + str(UserEvent.MY_PRAYERS.value) + '}'
                        },
                    ]
                }
            }
        })

    @mock.patch('facebook.user_utils.locale')
    def test_unknown_message(self, mock_locale):
        mock_locale.return_value = 'en_GB'

        sender_id = '13'
        message = {'text': u"What is this?"}
        response = handle_message(sender_id, message)
        assert_response(response, sender_id, {
            'text': u"Sorry but I don't understand you.\nType 'help' to get additional information."
        })

# Helper functions
def handle_message(sender_id, message):
    response = PrayerWebhook.handle_message(sender_id, message)
    return json.loads(response)

def assert_response(response, recipient_id, data):
    assert response['recipient']['id'] == recipient_id
    assert json.loads(response['message']) == data