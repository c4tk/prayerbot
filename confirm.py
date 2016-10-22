#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import json
from web import db
from dbms.models import Intent
from facebook import utils
from translations.user import user_gettext
from facebook.api import FacebookApi
from events import PrayerEvent

def confirm_praying_for_intention():

    query_prayers = Intent.query.filter( Intent.commiter_id > 0, Intent.confirmed == 0 ).all();

    for prayer in query_prayers:
        if prayer.commiter_id == None or prayer.commiter_id == "":
            print "NULL"
            print prayer.commiter_id
            print prayer.description
        else:
            print prayer.commiter_id
            print prayer.description
            options = [ {
                        'title': user_gettext( prayer.commiter_id, u"Yes" ),
                        'payload': PrayerEvent.payload( PrayerEvent.CONFIRM, prayer.id, prayer.user_id )
                        },
                        {
                        'title': user_gettext( prayer.commiter_id, u"No" ),
                        'payload': PrayerEvent.payload( PrayerEvent.DONT_CONFIRM, prayer.id, prayer.user_id )
                    } ]

            response_message = utils.response_buttons(
                user_gettext( prayer.commiter_id, u"Did You pray in below request ?\n%(value)s", value=prayer.description ),
                options
                )

            response = json.dumps({
                        'recipient': { 'id' : prayer.commiter_id },
                                        'message': response_message
                                })

            api = FacebookApi();
            api.post("/me/messages", response);

        print "\n";

if __name__ == '__main__':
    confirm_praying_for_intention()


