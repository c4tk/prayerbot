#!/usr/bin/env python2

import os
from flask import Flask, request
from flask.views import MethodView
from facebook.api import FacebookApi
from prayer import PrayerWebhook as webhook
from dbms.rdb import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///intent.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

###
# Routing for your application.
###

class WebhookAPI(MethodView):

    @property
    def api(self):
        if not hasattr(self, '_api'):
            self._api = FacebookApi()
        return self._api

    def get(self, user_id=None):
        """Facebook's API webhook challenge."""

        if request.args.get('hub.verify_token') == 'challenge_me':
            challenge = request.args.get('hub.challenge')
            if challenge:
                return challenge
            else:
                return "Challenge not found", 400
        else:
            return "Wrong validation token", 400

    def post(self):
        """Facebook's API webhook."""
        print("Webhook request data: " + request.data)
        data = request.get_json()
        entry = data['entry'][0]
        messaging_events = entry['messaging']
        for event in messaging_events:
            if 'message' in event:
                response_body = webhook.handle_message(event['sender'], event['message'])
                if response_body:
                    self.api.post("/me/messages", response_body)
            elif 'postback' in event:
                response_callbacks = webhook.handle_postback(event['sender'], event['postback'])
                for response_callback in response_callbacks:
                    self.api.post("/me/messages", response_callback)
        return "OK"

app = create_app()
app.app_context().push()
app.add_url_rule('/webhook', view_func=WebhookAPI.as_view('webhook'))

if __name__ == '__main__':
    app.run(debug=True)
