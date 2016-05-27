#!/usr/bin/env python2

import os
from flask import Flask, request
from messenger.api import MessengerApi
from prayer import PrayerWebhook as webhook
from raygun4py.middleware import flask

app = Flask(__name__)
api = MessengerApi()
flask.Provider(app, os.environ.get('RAYGUN_APIKEY')).attach()

###
# Routing for your application.
###

def setup():
    api.post("/me/subscribed_apps")

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
            response_body = webhook.handle_message(event['sender'], event['message'])
            if response_body:
                api.post("/me/messages", response_body)
        elif 'postback' in event:
            response_callbacks = webhook.handle_postback(event['sender'], event['postback'])
            for response_callback in response_callbacks:
                api.post("/me/messages", response_callback)
    return "OK"

setup()

if __name__ == '__main__':
    app.run(debug=True)
