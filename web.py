#!/usr/bin/env python2
import os

from flask import Flask, request
from flask.views import MethodView, View
from flask_admin import Admin
from flask_babel import Babel

from facebook import utils
from facebook.api import FacebookApi
from prayer import PrayerWebhook as webhook
from dbms.rdb import db, register_admin

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
            sender_id = event['sender']['id']
            if 'message' in event:
                response_body = webhook.handle_message(sender_id, event['message'])
                if response_body:
                    self.api.post("/me/messages", response_body)
            elif 'postback' in event:
                response_callbacks = webhook.handle_postback(sender_id, event['postback'])
                for response_callback in response_callbacks:
                    self.api.post("/me/messages", response_callback)
        return "OK"

class PrivacyPolicy(View):

    def dispatch_request(self):
        return "This page does not collect any personal information.\n<BR> " \
               "All prayer intentions collected via Messenger will be deleted after 60 days."

def create_app(sqlite_path='sqlite:///intent.db'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['BASIC_AUTH_USERNAME'] = 'john'
    app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
    babel = Babel(app)
    admin = Admin(app, name='PrayerBot', template_mode='bootstrap3')
    db.init_app(app)
    register_admin(admin, app)
    app.app_context().push()

    app.add_url_rule('/webhook', view_func=WebhookAPI.as_view('webhook'))
    app.add_url_rule('/privacy', view_func=PrivacyPolicy.as_view('privacy'))

    if os.environ.get('ACCESS_TOKEN'):
        utils.send_greeting_text_config()

    db.create_all()
    db.session.commit()
    db.session.autoflush = True
    db.session.autocommit = True

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0")
