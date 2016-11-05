#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import random
import json

from dbms.rdb import db
from dbms.models import Intent, BibleVerse
from events import PrayerEvent, UserEvent
from facebook import user_utils, utils
from translations.user import user_gettext
import time

displayed_prayers_limit = 5
displayed_intentions_limit = 5
max_intentions = 10
max_prayers = 10

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
                user_gettext(sender_id, u"You requested a prayer for: %(value)s ?", value=text),
                [
                    {
                        'title': user_gettext(sender_id, u"Yes"),
                        'payload': UserEvent.payload(UserEvent.CONFIRM_INTENTION, {'prayer_id': prayer.id, 'description': text})
                    },
                    {
                        'title': user_gettext(sender_id, u"No"),
                        'payload': UserEvent.payload(UserEvent.DELETE_INTENTION, {'prayer_id': prayer.id})
                    },
                ]
            )
            # Quick replies buttons does not work in Web interface
            #response_message = utils.quick_buttons(
            #    user_gettext(sender_id, u"You requested a prayer for: %(value)s ?", value=text),
            #    [
            #       {
            #            'content_type': 'text',
            #            'title': user_gettext(sender_id, u"Yes"),
            #            'payload': UserEvent.payload(UserEvent.CONFIRM_INTENTION, {'prayer_id': prayer.id, 'description': text})
            #        },
            #        {
            #            'content_type': 'text',
            #            'title': user_gettext(sender_id, u"No"),
            #            'payload': UserEvent.payload(UserEvent.DELETE_INTENTION, {'prayer_id': prayer.id})
            #        },
            #    ]
            #)
        elif lower_text in user_gettext(sender_id, 'help') or user_gettext(sender_id, 'prayer') in lower_text or lower_text in 'help':
            # Buttons limited to 3 values
            # So we need to create multiple bubbles in one message

            options1 = [
                {
                    'title': user_gettext(sender_id, u"I want to pray"),
                    'payload': UserEvent.payload(UserEvent.WANT_TO_PRAY)
                }
            ]

            commited_prayers = Intent.query.filter_by(commiter_id = sender_id).first()
            if commited_prayers :
                options1.append({
                    'title': user_gettext(sender_id, u"Who do I pray for ?"),
                    'payload': UserEvent.payload(UserEvent.MY_PRAYERS)
                })

            options2 = [
                {
                    'title': user_gettext(sender_id, u"Please pray for me"),
                    'payload': UserEvent.payload(UserEvent.PRAY_FOR_ME)
                }
            ]

            intentions = Intent.query.filter_by(user_id = sender_id).first()
            if intentions :
                options2.append({
                        'title': user_gettext(sender_id, u"My intentions"),
                        'payload': UserEvent.payload(UserEvent.MY_INTENTIONS)
                    }
                )

            text_list = [ user_gettext(sender_id, u"Maybe you can pray for someone ?") ]
            text_list.append( user_gettext(sender_id, u"Or maybe you need a prayer ?") )

            options_set = [ options1 ]
            options_set.append( options2 )

            response_message = utils.response_multiple_bubbles_buttons( text_list, options_set )

        elif lower_text in user_gettext(sender_id, u"bible"):
            bibleVerses = BibleVerse.query.all()
            verse = random.choice(bibleVerses)
            if (verse == None):
                verse = BibleVerse( user_gettext( u"God is light; in him there is no darkness at all."), "1 J 1,5b")
            response_message =  utils.response_text("\"" + verse.text + "\" " + verse.address)
        else:
            response_message = utils.response_text(user_utils.user_name(sender_id) +
                                     user_gettext(sender_id, u", God bless you!\nType 'prayer' to see prayer options or 'Bible' to get Bible verse for you."))

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
        db.session.flush()
        response_callbacks = map(map_callback, callbacks.items())

        return response_callbacks

    @staticmethod
    def handle_user_event(sender_id, event, payload):
        if event == UserEvent.CONFIRM_INTENTION:
            prayer_id = payload['prayer_id']
            description_value = payload['description']
            intent = Intent.query.filter_by(id = prayer_id).first()
            intent.description = description_value
            return {
                sender_id : utils.response_text(user_gettext(sender_id, u"You'll be notified when somebody wants to pray for you")),
            }
        elif event == UserEvent.DELETE_INTENTION:
            prayer_id = payload['prayer_id']
            intent = Intent.query.filter_by(id = prayer_id).first()
            if intent:
                db.session.delete(intent)
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"I've deleted a prayer request")),
                }
            else:
                return {
                    sender_id: utils.response_text(user_gettext(sender_id, u"There is no such prayer request")),
                }
        elif event == UserEvent.PRAY_FOR_ME:
            # check how many intention user already provided
            int_cnt = Intent.query.filter(Intent.user_id == sender_id).count()

            if int_cnt < max_intentions:
                intent = Intent(sender_id, '')
                intent.ts = int(time.time())
                db.session.add(intent)
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"What is your prayer request ?")),
                }
            else:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"You've reached maximum intentions count. Please come back in few days.")),
                }
        elif event == UserEvent.WANT_TO_PRAY:

            pray_cnt = Intent.query.filter(Intent.commiter_id == sender_id ).count()

            if pray_cnt < max_prayers:
                prayers = Intent.query.filter(Intent.commiter_id == 0 ).filter(Intent.user_id != sender_id).limit(displayed_prayers_limit).all()

                prayer_elements = map(map_prayer, prayers)

                if prayer_elements == []:
                    return {
                        sender_id : utils.response_text(user_gettext(sender_id, u"There're no prayer requests")),
                    }
                else:
                    return {
                        sender_id : utils.response_elements(prayer_elements),
                    }
            else:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"You've reached maximum prayers count. Please pray in your already selected intentions first.")),
                }
        elif event == UserEvent.MY_PRAYERS:

            prayer_elements = map_said_prayer_multiple_bubbles( sender_id )

            if prayer_elements == []:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"There're no prayer requests")),
                }
            else:
                return {
                    sender_id : utils.response_elements(prayer_elements),
                }
        elif event == UserEvent.MY_INTENTIONS:

            all_intentions = []
            options_set = []

            for intention in Intent.query.filter_by(user_id=sender_id)[0:displayed_intentions_limit]:
                buttons = [
                        {
                            'title': user_gettext(sender_id, u"Delete"),
                            'payload': UserEvent.payload(UserEvent.DELETE_INTENTION, {'prayer_id': intention.id})
                        },
                    ]
                if intention.commiter_id > 0:
                    buttons.append( {
                            'title': user_gettext(sender_id, u"Send thank you"),
                            'payload': UserEvent.payload(UserEvent.THANK_FOR_PRAYER, {'prayer_id': intention.id})
                        },
                    )
                if options_set:
                    options_set.append( buttons )
                else:
                    options_set = [ buttons ]

                if all_intentions:
                    all_intentions.append( intention.description )
                else:
                    all_intentions = [ intention.description  ]

                response_message = utils.response_multiple_bubbles_buttons(all_intentions, options_set)

            if all_intentions == []:
                return {
                    sender_id : utils.response_text( user_gettext( sender_id, u"You don't have any intentions" ) ),
                }
            else:
                return {
                    sender_id : response_message
                }

        elif event == UserEvent.THANK_FOR_PRAYER:
            prayer_id = payload['prayer_id']
            intent = Intent.query.filter_by(id = prayer_id).first()
            if intent:
                commiter_id = intent.commiter_id
                prayer_desc = intent.description
                user_name = user_utils.user_name(sender_id)
                commiter_name = user_utils.user_name(commiter_id)
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"User %(name)s will be notified about your thankfulness.", name=commiter_name)),
                    commiter_id : utils.response_text(user_gettext(commiter_id, u"User %(name)s wants to thank you for your prayer in the following request: %(desc)s.", name=user_name, desc=prayer_desc)),
                }
            else:
                return {
                    sender_id: utils.response_text(user_gettext(sender_id, u"There is no such prayer request")),
                }

    @staticmethod
    def handle_prayer_event(sender_id, user_id, prayer_id, event, payload):

        sender_name = user_utils.user_name(sender_id)
        user_name = user_utils.user_name(user_id)

        intent = Intent.query.filter_by(id = prayer_id).one_or_none()

        if intent:
            intent_description = intent.description
            #.encode('utf-8')

            if event == PrayerEvent.I_PRAY:
                intent.commiter_id = sender_id
                return {
                    # This is dictionary - no duplicates allowed
                    # When user_id == sender_id then only second message will be send
                    sender_id : utils.response_text(user_gettext(sender_id, u"You're subscribed for the prayer request from user %(name)s", name=user_name)),
                    user_id : utils.response_text(user_gettext(user_id, u"User %(name)s will be praying in your following request: %(desc)s", name=sender_name, desc=intent_description)),
                }
            elif event == PrayerEvent.DID_PRAY:
                # Should confirmed prayer be deleted or just marked as confirmed and deleted separatelly
                # by scheduled script ?
                # It should be the same way as in CONFIRM_PRAY option
                #db.session.delete(intent)
                intent.confirmed = 1
                return {
                    # This is dictionary - no duplicates allowed
                    # When user_id == sender_id then only second message will be send
                    sender_id : utils.response_text(user_gettext(sender_id, u"User %(name)s has been notified that you've prayed for him/her. Thank you", name=user_name)),
                    user_id : utils.response_text(user_gettext(user_id, u"User %(name)s has prayed in your request: %(desc)s", name=sender_name, desc=intent_description)),
                }
            elif event == PrayerEvent.ENSURE_PRAY:
                # This is dictionary - no duplicates allowed
                # When user_id == sender_id then only second message will be send
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"User %(name)s has been ensured that you pray for him", name=user_name)),
                    user_id : utils.response_text(user_gettext(user_id, u"User %(name)s wants to ensure you about his prayer in the following request: %(desc)s", name=sender_name, desc=intent_description)) ,
                }
            elif event == PrayerEvent.GIVE_UP:
                intent.commiter_id = 0
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"Thank you for your will of praying. User %(name)s won't be notified about you giving up.", name=user_name)),
                }
            elif event == PrayerEvent.DONT_CONFIRM_PRAY:
                return {
                    sender_id : utils.response_text(user_gettext(sender_id, u"Please pray. Someone is counting on you.\nI will ask you again tomorrow.")),
                }
        else:
            return {
                sender_id: utils.response_text(user_gettext(sender_id, u"There is no such prayer request")),
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

def map_said_prayer_multiple_bubbles(sender_id):

    elements = None

    for prayer in Intent.query.filter_by(commiter_id=sender_id).limit(displayed_prayers_limit).all():

        user_id = prayer.user_id
        # some limit for checking images
        # ConnectionError: HTTPSConnectionPool(host='graph.facebook.com', port=443):
        # Max retries exceeded with url: /v2.8/me/thread_settings?access_token=xxx
        # (Caused by NewConnectionError('<requests.packages.urllib3.connection.VerifiedHTTPSConnection object at 0x7fd377cb5350>:
        # Failed to establish a new connection: [Errno -2] Name or service not known',))

        single_bubble_button = {
                    "title": prayer.description,
                    "subtitle": user_utils.user_name(user_id),
                    "image_url": user_utils.img_url(user_id),
                    "buttons": [
                        {
                            'type' : "postback",
                            'title': user_gettext(user_id, u"I've prayed"),
                            'payload': PrayerEvent.payload(PrayerEvent.DID_PRAY, prayer.id, user_id)
                        },
                        {
                            'type': "postback",
                            'title': user_gettext(user_id, u"Ensure about your prayer"),
                            'payload': PrayerEvent.payload(PrayerEvent.ENSURE_PRAY, prayer.id, user_id)
                        },
                        {
                            'type': "postback",
                            'title': user_gettext(user_id, u"Stop your prayer"),
                            'payload': PrayerEvent.payload(PrayerEvent.GIVE_UP, prayer.id, user_id)
                        },
                    ]
                }

        if elements:
            elements.append( single_bubble_button )
        else:
            elements = [ single_bubble_button ]

    return elements


# Facebook API samples
#{
#  "recipient":{
#    "id":"USER_ID"
#  },
#  "message":{
#    "attachment":{
#      "type":"template",
#      "payload":{
#        "template_type":"generic",
#        "elements":[
#          {
#            "title":"Welcome to Peter\'s Hats",
#            "item_url":"https://petersfancybrownhats.com",
#            "image_url":"https://petersfancybrownhats.com/company_image.png",
#            "subtitle":"We\'ve got the right hat for everyone.",
#            "buttons":[
#              {
#                "type":"web_url",
#                "url":"https://petersfancybrownhats.com",
#                "title":"View Website"
#              },
#              {
#                "type":"postback",
#                "title":"Start Chatting",
#                "payload":"DEVELOPER_DEFINED_PAYLOAD"
#              }
#            ]
#          }
#        ]
#      }
#    }
#  }
#}'


#curl -X POST -H "Content-Type: application/json" -d '{
#  "recipient":{
#    "id":"USER_ID"
#  },
#  "message":{
#    "text":"Pick a color:",
#    "quick_replies":[
#      {
#        "content_type":"text",
#        "title":"Red",
#        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
#      },
#      {
#        "content_type":"text",
#        "title":"Green",
#        "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
#      }
#    ]
#  }
#}' "https://graph.facebook.com/v2.6/me/messages?access_token=PAGE_ACCESS_TOKEN"

