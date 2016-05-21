#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import db.utils as db
import tools.systools as systools
import messenger.utils as utils

displayed_prayers_limit = 5

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

            response = json.dumps({
                'recipient': { 'id' : sender['id'] },
                'message': response_message
            })
            return response
        elif text in ['intencje', 'i']:
            response_message = utils.response_buttons(
                "Twoje intencje",
                [
                    {
                        "type":"postback",
                        "title":"Intencje",
                        "payload": json.dumps({"event": "intentions"})
                    },
                ]
            )
            response = json.dumps({
                'recipient': { 'id' : sender['id'] },
                'message': response_message
            })
            return response
        elif text == 'info':
            resp_text = systools.system_info()
            response_message = utils.response_text("Version: " + resp_text)
        else:
            return None

    @staticmethod
    def handle_postback(sender, postback):
        payload = json.loads(postback['payload'])
        event_type = payload['event']
        sender_id = sender['id']
        if event_type == 'pray_for_me':
            response_message = utils.response_text('Jaka jest Twoja intencja?')
        elif event_type == 'want_to_pray':
            intentions = db.fetch_history({"said": "no"}, displayed_prayers_limit)
            print("Fetched intentions: " + json.dumps(intentions))
            intention_elements = map(map_intention, intentions)
            print(json.dumps(intention_elements))
            response_message = utils.response_elements(intention_elements)
        elif event_type == 'intentions':
            intentions = db.fetch_history({"commiter_id": sender_id})
            intention_elements = map(map_said_intention, intentions)
            print(json.dumps(intention_elements))
            response_message = utils.response_elements(intention_elements)
        elif event_type == 'i_pray':
            response_message = utils.response_text('Zostałeś zapisany na modlitwę w intencji użytkownika ' + user_name(payload['user_id']))
        elif event_type == 'did_pray':
            response_message = utils.response_text('Użytkownik ' + user_name(payload['user_id']) + ' został powiadomiony o tym że pomodliłeś się za niego. Dziękujemy')
        elif event_type == 'send_message':
            response_message = utils.response_text('Użytkownik ' + user_name(payload['user_id']) + ' został powiadomiony o tym że pamiętasz o nim w modlitwie')
        elif event_type == 'give_up':
            response_message = utils.response_text('Dziękujemy za chęć modlitwy. Użytkownik ' + user_name(payload['user_id']) + ' nie zostanie powiadomiony o Twojej rezygnacji')


        response = json.dumps({
            'recipient': { 'id' : sender_id },
            'message': response_message
        })
        return response

def map_intention(intention):
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
        ],
        "image_url": utils.get_img_url(user_id)
    }

def map_said_intention(intention):
    user_id = intention['user_id']
    return {
        "title": user_id,
        "subtitle": intention['description'],
        "buttons": [
            {
                "type": "postback",
                "title": "Pomodliłem się",
                "payload": json.dumps({"event": "did_pray", "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Zapewnij o modlitwie",
                "payload": json.dumps({"event": "send_message", "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Rezygnuję z modlitwy",
                "payload": json.dumps({"event": "give_up", "user_id": user_id})
            },
        ],
        "image_url": utils.get_img_url(user_id)
    }
