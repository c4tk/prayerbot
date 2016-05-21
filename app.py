#!/usr/bin/env python2

from flask import Flask, request
from messenger.api import MessengerApi
from prayer import PrayerWebhook as webhook

app = Flask(__name__)
api = MessengerApi()

###
# Routing for your application.
###

def setup():
    api.request("/me/subscribed_apps")

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
            api.request("/me/messages", response_body)
        elif 'postback' in event:
            response_body = webhook.handle_postback(event['sender'], event['postback'])
            api.request("/me/messages", response_body)
    return "OK"

setup()

if __name__ == '__main__':
    app.run(debug=True)
