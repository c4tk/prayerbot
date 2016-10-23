#-*- encoding: utf-8 -*-
import json
import unittest

from prayer import PrayerWebhook

class PrayerBotTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class MessengerBotTestSuite(PrayerBotTest):

    def test_prayer_bot_recipent(self):
        sender_id = '10'
        message = {'text': 'helpppppp'}
        res = json.loads(PrayerWebhook.handle_message(sender_id, message))
        assert res['recipient']['id'] == '10'
        assert json.loads(res['message'])['text'] == u"Unknown, Bóg błogosławi! Wpisz 'modlitwa', aby zobaczyć opcje, albo 'Biblia', aby otrzymać fragment z Pisma!"
