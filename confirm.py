#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import json
from web import app, db
from dbms.models import Intent
from dbms.rdb import db
from facebook import user_utils, utils
from translations.user import user_gettext
from facebook.api import FacebookApi
from events import *


qPrayers = Intent.query.filter( Intent.commiter_id > 0, Intent.confirmed == 0 ).all();

for prayer in qPrayers:
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




