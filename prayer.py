#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import db.utils as db
import tools.systools as systools
import messenger.utils as utils
from db.labels import label_id

displayed_prayers_limit = 5

class PrayerWebhook(object):
    @staticmethod
    def handle_message(sender, message):
        response = None
        text = message['text'].encode('utf-8')
        sender_id = sender['id']
        initialized_prayers = db.fetch_history({"user_id": sender_id, "description": ""})
        if initialized_prayers != []:
            prayer = initialized_prayers[0]
            response_message = utils.response_buttons(
                "Czy na pewno chcesz żeby ktoś się pomodlił w następującej intencji: " + text + "?",
                [
                    {
                        "type":"postback",
                        "title":"Tak",
                        "payload": json.dumps({"user_event": "update_prayer", "prayer_id": prayer[label_id], "description": text})
                    },
                    {
                        "type":"postback",
                        "title":"Nie",
                        "payload": json.dumps({"user_event": "delete_prayer", "prayer_id": prayer[label_id]})
                    },
                ]
            )
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        elif text in ['help', 'pomoc']:
            response_message = utils.response_buttons(
                "Witaj " + utils.user_name(sender_id) + "...\nZapraszamy do korzystania ze Skrzynki Modlitewnej. Czego potrzebujesz?",
                [
                    {
                        "type":"postback",
                        "title":"Potrzebuję modlitwy",
                        "payload": json.dumps({"user_event": "pray_for_me"})
                    },
                    {
                        "type":"postback",
                        "title":"Chcę się pomodlić",
                        "payload": json.dumps({"user_event": "want_to_pray"})
                    },
                    {
                        "type":"postback",
                        "title":"Za kogo się modlę?",
                        "payload": json.dumps({"user_event": "prayers"})
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
        else:
            response_message = utils.response_text("Niestety nie rozumiem Twojej prośby.\nWpisz 'pomoc' żeby uzyskać dodatkowe informacje.")
            response = json.dumps({
                'recipient': { 'id' : sender_id },
                'message': response_message
            })
        return response

    @staticmethod
    def handle_postback(sender, postback):
        payload = json.loads(postback['payload'])
        sender_id = sender['id']

        if 'user_event' in payload:
            event_type = payload['user_event']
            callbacks = PrayerWebhook.handle_user_event(sender_id, event_type, payload)
        elif 'prayer_event' in payload:
            event_type = payload['prayer_event']
            callbacks = PrayerWebhook.handle_prayer_event(sender_id, event_type, payload)
        response_callbacks = map(map_callback, callbacks.items())
        return response_callbacks

    @staticmethod
    def handle_user_event(sender_id, event_type, payload):
        if event_type == 'update_prayer':
            # TODO: update prayer in DB
            id_value = payload["prayer_id"]
            description_value = payload["description"]
            db.update_description(id_value, description_value)
            return {
                sender_id : utils.response_text('Zostaniesz poinformowany gdy ktoś będzie chciał się za Ciebie pomodlić'),
            }
        elif event_type == 'delete_prayer':
            # TODO: delete prayer from DB
            id_value = payload["prayer_id"]
            db.delete(id_value)
            return {
                sender_id : utils.response_text('Usunąłem prośbę o modlitwę'),
            }
        elif event_type == 'pray_for_me':
            data_line = dict(
                user_id=sender_id,
                commiter_id="",
                ts=1234,
                description="",
                )
            db.insert_row(data_line)
            return {
                sender_id : utils.response_text('Jaka jest Twoja intencja?'),
            }
        elif event_type == 'want_to_pray':
            prayers = db.fetch_history({"commiter_id": ""}, displayed_prayers_limit)
            print("Fetched prayers: " + json.dumps(prayers))
            prayer_elements = map(map_prayer, prayers)
            return {
                sender_id : utils.response_elements(prayer_elements),
            }
        elif event_type == 'prayers':
            prayers = db.fetch_history({"commiter_id": sender_id})
            prayer_elements = map(map_said_prayer, prayers)
            if prayer_elements == []:
                return {
                    sender_id : utils.response_text('Brak aktualnych intencji'),
                }
            else:
                return {
                    sender_id : utils.response_elements(prayer_elements),
                }

    @staticmethod
    def handle_prayer_event(sender_id, event_type, payload):
        user_id = payload['user_id']
        prayer_id = payload['prayer_id']
        prayer = db.fetch(prayer_id)
        prayer_description = prayer['description'].encode("utf-8")

        if event_type == 'i_pray':
            db.update_commiter(prayer_id, sender_id)
            return {
                sender_id : utils.response_text('Zostałeś zapisany na modlitwę w intencji użytkownika ' + utils.user_name(user_id)),
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' będzie się modlił w następującej intencji: ' + prayer_description),
            }
        elif event_type == 'did_pray':
            db.delete(prayer_id)
            return {
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' pomodlił się w Twojej intencji: ' + prayer_description),
                sender_id : utils.response_text('Użytkownik ' + utils.user_name(user_id) + ' został powiadomiony o tym że pomodliłeś się za niego. Dziękujemy'),
            }
        elif event_type == 'send_message':
            return {
                user_id : utils.response_text('Użytkownik ' + utils.user_name(sender_id) + ' pamięta o Tobie w modlitwie w następującej intencji: ' + prayer_description),
                sender_id : utils.response_text('Użytkownik ' + utils.user_name(user_id) + ' został powiadomiony o tym że pamiętasz o nim w modlitwie'),
            }
        elif event_type == 'give_up':
            db.update_commiter(prayer_id, '')
            return {
                sender_id : utils.response_text('Dziękujemy za chęć modlitwy. Użytkownik ' + utils.user_name(user_id) + ' nie zostanie powiadomiony o Twojej rezygnacji'),
            }

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
                "payload": json.dumps({"prayer_event": "i_pray", "prayer_id": prayer[label_id], "user_id": user_id})
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
                "payload": json.dumps({"prayer_event": "did_pray", "prayer_id": prayer[label_id], "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Zapewnij o modlitwie",
                "payload": json.dumps({"prayer_event": "send_message", "prayer_id": prayer[label_id], "user_id": user_id})
            },
            {
                "type": "postback",
                "title": "Rezygnuję z modlitwy",
                "payload": json.dumps({"prayer_event": "give_up", "prayer_id": prayer[label_id], "user_id": user_id})
            },
        ],
        "image_url": utils.get_img_url(user_id)
    }
