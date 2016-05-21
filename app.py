#!/usr/bin/env python2

import json
import os
import sys
from flask import Flask, request
from messenger.api import MessengerApi
from messenger.utils import MessengerUtils as utils

app = Flask(__name__)
api = MessengerApi()

###
# Routing for your application.
###

def setup():
    api.request("/subscribed_apps")

@app.route('/webhook')
def challenge_webhook():
    """Facebook's API webhook challenge."""
    if request.args.get('hub.verify_token') == 'challenge_me':
        challenge = request.args.get('hub.challenge')
        if challenge:
            return challenge
        else:
            return "Challenge not found", 400
    else:
        return "Wrong validation token", 400

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Facebook's API webhook."""
    print("Webhook request data: " + request.data)
    data = request.get_json()
    entry = data['entry'][0]
    messaging_events = entry['messaging']
    for event in messaging_events:
        if 'message' in event:
            response_body = handle_webhook_message(event['sender'], event['message'])
            api.request("/messages", response_body)
        elif 'postback' in event:
            response_body = handle_webhook_postback(event['sender'], event['postback'])
            api.request("/messages", response_body)
    return "OK"

def handle_webhook_message(sender, message):
    text = message['text']
    if text == 'modlitwa':
        response_message = utils.response_buttons(
            "Witaj user " + sender['id'] + "... Czego potrzebujesz?",
            [
                {
                    "type":"postback",
                    "title":"Potrzebuje modlitwy",
                    "payload":"pomodl_sie_za_mnie"
                },
                {
                    "type":"postback",
                    "title":"Chce sie pomodlic",
                    "payload":"chce_sie_pomodlic"
                }
            ]
        )
    else:
        response_message = utils.response_text("Bot echo: " + text)

    response = json.dumps({
        'recipient': { 'id' : sender['id'] },
        'message': response_message
    })
    return response
    
def handle_webhook_postback(sender, postback):
    payload = postback['payload']
    if payload == 'pomodl_sie_za_mnie':
        response_message = utils.response_text('Jaka jest Twoja intencja?')
    elif payload == 'chce_sie_pomodlic':
        response_message = utils.response_text('TODO')
        
    response = json.dumps({
        'recipient': { 'id' : sender['id'] },
        'message': response_message
    })
    return response

setup()

if __name__ == '__main__':
    app.run(debug=True)
