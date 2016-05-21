#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import db.storage as storage
from messenger.utils import MessengerUtils as utils

class PrayerWebhook(object):

    @staticmethod
    def handle_message(sender, message):
        text = message['text']
        if text in ['modlitwa', 'm']:
            response_message = utils.response_buttons(
                "Witaj user " + sender['id'] + "... Czego potrzebujesz?",
                [
                    {
                        "type":"postback",
                        "title":"Potrzebuję modlitwy",
                        "payload": json.dumps({"event": "pray_for_me"})
                    },
                    {
                        "type":"postback",
                        "title":"Chcę się pomodlić",
                        "payload": json.dumps({"event": "want_to_pray"})
                    },
                ]
            )
        else:
            response_message = utils.response_text("Bot echo: " + text)

        response = json.dumps({
            'recipient': { 'id' : sender['id'] },
            'message': response_message
        })
        return response

    @staticmethod
    def handle_postback(sender, postback):
        payload = json.loads(postback['payload'])
        event_type = payload['event']
        if event_type == 'pray_for_me':
            response_message = utils.response_text('Jaka jest Twoja intencja?')
        elif event_type == 'want_to_pray':
            intentions = storage.fetch_history()
            print("Fetched intentions: " + json.dumps(intentions))
            intention_elements = map(transform_intention, intentions)
            print(json.dumps(intention_elements))
            response_message = utils.response_elements(intention_elements)
        elif event_type == 'i_pray':
            response_message = utils.response_text('Zostałeś zapisany na modlitwę w intencji użytkownika ' + str(payload['user_id']))

        response = json.dumps({
            'recipient': { 'id' : sender['id'] },
            'message': response_message
        })
        return response

def transform_intention(intention):
    user_id = intention['user_id']
    return {
        "title": user_id,
        "subtitle": intention['description'],
        "buttons": [
            {
                "type": "postback",
                "title": "Modlę się",
                "payload": json.dumps({"event": "i_pray", "user_id": user_id})
            }
        ]
    }
        
