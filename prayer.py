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
        response = None
        text = message['text']
        sender_id = sender['id']
        if text in ['modlitwa', 'm']:
            response_message = utils.response_buttons(
                "Witaj " + utils.user_name(sender_id) + "... Czego potrzebujesz?",
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
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        elif text in ['intencje', 'i']:
            response_message = utils.response_buttons(
                "Twoje intencje",
                [
                    {
                        "type":"postback",
                        "title":"Intencje",
                        "payload": json.dumps({"event": "prayers"})
                    },
                ]
            )
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        elif text == 'info':
            resp_text = systools.system_info()
            response_message = utils.response_text("Version: " + resp_text)
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        elif text.startswith('poke'):
            fd = open('a.txt', 'wb')
            data_part = text[4:]
            fd.write(data_part)
            fd.close()
            data_len = len(data_part)
            response_message = utils.response_text("Written %d bytes" % data_len)
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        elif text.startswith('peek'):
            fd = open('a.txt', 'rb')
            data_part = fd.read()
            fd.close()
            data_len = len(data_part)
            response_message = utils.response_text("Read %d bytes: %s" % (data_len, data_part))
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        return response

    @staticmethod
    def handle_postback(sender, postback):
        payload = json.loads(postback['payload'])
        event_type = payload['event']
        if 'user_id' in payload:
            user_id = payload['user_id']
        if 'prayer_id' in payload:
            prayer_id = payload['prayer_id']
            prayer = db.fetch(prayer_id)
        sender_id = sender['id']
        if event_type == 'pray_for_me':
            callbacks = {
                sender_id : utils.response_text('Jaka jest Twoja intencja?'),
            }
        elif event_type == 'want_to_pray':
            prayers = db.fetch_history({"said": "no"}, displayed_prayers_limit)
            print("Fetched prayers: " + json.dumps(prayers))
            prayer_elements = map(map_prayer, prayers)
            callbacks = {
                sender_id : utils.response_elements(prayer_elements),
            }
        elif event_type == 'prayers':
            prayers = db.fetch_history({"commiter_id": sender_id})
            prayer_elements = map(map_said_prayer, prayers)
            if prayer_elements == []:
                callbacks = {
                    sender_id : utils.response_text('Brak aktualnych intencji'),
                }
            else:
                callbacks = {
                    sender_id : utils.response_elements(prayer_elements),
                }
        # specific prayer actions
        elif event_type == 'i_pray':
            callbacks = {
                sender_id : utils.response_text('Zostałeś zapisany na modlitwę w intencji użytkownika ' + utils.user_name(user_id)),
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' będzie się modlił w następującej intencji: ' + prayer['description']),
            }
        elif event_type == 'did_pray':
            callbacks = {
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' pomodlił się w Twojej intencji: ' + prayer['description']),
                sender_id : utils.response_text('Użytkownik ' + utils.user_name(user_id) + ' został powiadomiony o tym że pomodliłeś się za niego. Dziękujemy'),
            }
        elif event_type == 'send_message':
            callbacks = {
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' pamięta o Tobie w modlitwie w następującej intencji: ' + prayer['description']),
                sender_id : utils.response_text('Użytkownik ' + utils.user_name(user_id) + ' został powiadomiony o tym że pamiętasz o nim w modlitwie'),
            }
        elif event_type == 'give_up':
            callbacks = {
                sender_id : utils.response_text('Dziękujemy za chęć modlitwy. Użytkownik ' + utils.user_name(user_id) + ' nie zostanie powiadomiony o Twojej rezygnacji'),
            }

        response_callbacks = map(map_callback, callbacks.items())
        return response_callbacks

def map_callback(callback):
    sender_id = callback[0] 
    response_message = callback[1] 
    return json.dumps({
        'recipient': { 'id' : sender_id },
        'message': response_message
    })

def map_prayer(prayer):
    user_id = prayer['user_id']
    return {
        "title": utils.user_name(user_id),
        "subtitle": prayer['description'],
        "buttons": [
            {
                "type": "postback",
                "title": "Modlę się",
                "payload": json.dumps({"event": "i_pray", "prayer_id": prayer['id'], "user_id": user_id})
            }
        ],
        "image_url": utils.get_img_url(user_id)
    }

def map_said_prayer(prayer):
    user_id = prayer['user_id']
    return {
        "title": utils.user_name(user_id),
        "subtitle": prayer['description'],
        "buttons": [
            {
                "type": "postback",
                "title": "Pomodliłem się",
                "payload": json.dumps({"event": "did_pray", "prayer_id": prayer['id'], "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Zapewnij o modlitwie",
                "payload": json.dumps({"event": "send_message", "prayer_id": prayer['id'], "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Rezygnuję z modlitwy",
                "payload": json.dumps({"event": "give_up", "prayer_id": prayer['id'], "user_id": user_id})
            },
        ],
        "image_url": utils.get_img_url(user_id)
    }
