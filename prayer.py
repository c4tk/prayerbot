#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import random

from dbms.rdb import db
from dbms.models import Intent, BibleVerse
from events import *
from facebook import user_utils, utils
from translations.user import user_gettext

displayed_prayers_limit = 5

class PrayerWebhook(object):
    @staticmethod
    def handle_message(sender_id, message):
        response_message = None
        text = message['text']
        lower_text = unicode(text.lower())

        initialized_prayers = Intent.query.filter_by(user_id = sender_id, description = '').all()
        if initialized_prayers != []:
            prayer = initialized_prayers[0]
            response_message = utils.response_buttons(
                user_gettext(sender_id, u"You requested a prayer for: %(value)s?", value=text),
                [
                    {
                        'title': user_gettext(sender_id, u"Yes"),
                        'payload': UserEvent.payload(UserEvent.UPDATE_PRAYER, {'prayer_id': prayer.id, 'description': text})
                    },
                    {
                        'title': user_gettext(sender_id, u"No"),
                        'payload': UserEvent.payload(UserEvent.DELETE_PRAYER, {'prayer_id': prayer.id})
                    },
                ]
            )
        elif lower_text in user_gettext(sender_id, 'help') or user_gettext(sender_id, 'pray') in lower_text:
            commited_prayers = Intent.query.filter_by(commiter_id = sender_id)
            options = [
                {
                    'title': user_gettext(sender_id, u"Please pray for me"),
                    'payload': UserEvent.payload(UserEvent.PRAY_FOR_ME)
                },
                {
                    'title': user_gettext(sender_id, u"I want to pray"),
                    'payload': UserEvent.payload(UserEvent.WANT_TO_PRAY)
                },
            ]
            if commited_prayers != []:
                options.append({
                    'title': user_gettext(sender_id, u"Who do I pray for?"),
                    'payload': UserEvent.payload(UserEvent.MY_PRAYERS)
                })
            response_message = utils.response_buttons(
                user_gettext(sender_id, u"Please choose what do you need?"),
                options
            )
        elif lower_text in user_gettext(sender_id, u"bible"):
            # bibleVerses = BibleVerse.query.all()
            # verse = random.choice(bibleVerses)
            # if (verse == None):
            verse = BibleVerse(u"Bóg jest światłością, a nie ma w Nim żadnej ciemności.", "1J5b")
            response_message =  utils.response_text("\"" + verse.text + "\" " + verse.address)
        else:
            response_message = utils.response_text(user_gettext(sender_id, u"Sorry but I don't understand you.\nType 'help' to get additional information."))

        response = json.dumps({
            'recipient': { 'id' : sender_id },
            'message': response_message
        })
        return response

    @staticmethod
    def handle_postback(sender_id, postback):
        payload = json.loads(postback['payload'])

        if 'user_event' in payload:
            event_key = payload['user_event']
            event = UserEvent(event_key)
            callbacks = PrayerWebhook.handle_user_event(sender_id, event, payload)
        elif 'prayer_event' in payload:
            event_key = payload['prayer_event']
            event = PrayerEvent(event_key)
            user_id = payload['user_id']
            prayer_id = payload['prayer_id']
            callbacks = PrayerWebhook.handle_prayer_event(sender_id, user_id, prayer_id, event, payload)
        # commit DB changes
        db.session.commit()
        response_callbacks = map(map_callback, callbacks.items())
        return response_callbacks

    @staticmethod
    def handle_user_event(sender_id, event, payload):
        if event == UserEvent.UPDATE_PRAYER:
            prayer_id = payload['prayer_id']
            description_value = payload['description']
            intent = Intent.query.filter_by(id = prayer_id).first()
            intent.description = description_value
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"You'll be notified when somebody wants to pray for you")),
            }
        elif event == UserEvent.DELETE_PRAYER:
            prayer_id = payload['prayer_id']
            intent = Intent.query.filter_by(id = prayer_id).first()
            db.session.delete(intent)
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"I've deleted a prayer request")),
            }
        elif event == UserEvent.PRAY_FOR_ME:
            intent = Intent(sender_id, '')
            intent.ts = 1234
            db.session.add(intent)
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"What is your prayer request?")),
            }
        elif event == UserEvent.WANT_TO_PRAY:
            prayers = Intent.query.filter(Intent.commiter_id == '').filter(Intent.user_id != sender_id).limit(displayed_prayers_limit).all()
            #print('Fetched prayers: ' + json.dumps(prayers))
            prayer_elements = map(map_prayer, prayers)
            if prayer_elements == []:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"There're no prayer requests")),
                }
            else:
                return {
                    sender_id : utils.response_elements(prayer_elements),
                }
        elif event == UserEvent.MY_PRAYERS:
            commited_prayers = Intent.query.filter_by(commiter_id = sender_id)
            prayer_elements = map(map_said_prayer, commited_prayers)
            if prayer_elements == []:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"There're no prayer requests")),
                }
            else:
                return {
                    sender_id : utils.response_elements(prayer_elements),
                }

    @staticmethod
    def handle_prayer_event(sender_id, user_id, prayer_id, event, payload):
        sender_name = user_utils.user_name(sender_id)
        user_name = user_utils.user_name(user_id)
        intent = Intent.query.filter_by(id = prayer_id).one_or_none()
        intent_description = intent.description.encode('utf-8')

        if event == PrayerEvent.I_PRAY:
            intent.commiter_id = sender_id
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"You're subscribed for the prayer request from user %(name)s", name=user_name)),
                user_id : utils.response_text(user_gettext(user_id, u"User %(name)s will be praying in your following request: %(desc)s", name=sender_name, desc=intent_description)),
            }
        elif event == PrayerEvent.DID_PRAY:
            db.session.delete(intent)
            return {
                user_id : utils.response_text(user_gettext(user_id, u"User %(name)s has prayed in your request: %(desc)s", name=sender_name, desc=intent_description)),
                sender_id : utils.response_text(user_gettext(sender_id, u"User %(name)s has been notified that you've prayed for him/her. Thank you", name=user_name)),
            }
        elif event == PrayerEvent.SEND_MESSAGE:
            return {
                user_id : utils.response_text(user_gettext(user_id, u"User %(name)s wants to ensure you about his prayer in the following request: %(desc)s", name=sender_name, desc=intent_description)),
                sender_id : utils.response_text(user_gettext(sender_id, u"User %(name)s has been ensured that you pray for him", name=user_name)),
            }
        elif event == PrayerEvent.GIVE_UP:
            intent.commiter_id = ''
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"Thank you for your will of praying. User %(name)s won't be notified about you giving up.", name=user_name)),
            }

def map_callback(callback):
    sender_id = callback[0]
    response_message = callback[1]
    return json.dumps({
        'recipient': { 'id' : sender_id },
        'message': response_message
    })

def map_prayer(prayer):
    user_id = prayer.user_id
    return {
        'title': user_utils.user_name(user_id),
        'subtitle': prayer.description,
        'buttons': [
            {
                'title': user_gettext(user_id, u"I am praying"),
                'payload': PrayerEvent.payload(PrayerEvent.I_PRAY, prayer.id, user_id)
            }
        ],
        'image_url': user_utils.img_url(user_id)
    }

def map_said_prayer(prayer):
    user_id = prayer.user_id
    return {
        'title': user_utils.user_name(user_id),
        'subtitle': prayer.description,
        'buttons': [
            {
                'title': user_gettext(user_id, u"I've prayed"),
                'payload': PrayerEvent.payload(PrayerEvent.DID_PRAY, prayer.id, user_id)
            },
            {
                'title': user_gettext(user_id, u"Ensure about your prayer"),
                'payload': PrayerEvent.payload(PrayerEvent.SEND_MESSAGE, prayer.id, user_id)
            },
            {
                'title': user_gettext(user_id, u"Stop your prayer"),
                'payload': PrayerEvent.payload(PrayerEvent.GIVE_UP, prayer.id, user_id)
            },
        ],
        'image_url': user_utils.img_url(user_id)
    }
