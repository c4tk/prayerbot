#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
from enum import Enum

class PrayerEvent(Enum):
    I_PRAY = 1
    DID_PRAY = 2
    SEND_MESSAGE = 3
    GIVE_UP = 4

    @staticmethod
    def payload(key, prayer_id, user_id):
        return json.dumps({"prayer_event": key.value, "prayer_id": prayer_id, "user_id": user_id})

class UserEvent(Enum):
    UPDATE_PRAYER = 1
    DELETE_PRAYER = 2
    PRAY_FOR_ME = 3
    WANT_TO_PRAY = 4
    MY_PRAYERS = 5

    @staticmethod
    def payload(key, args = {}):
        event_payload = {"user_event": key.value}
        event_payload.update(args)
        return json.dumps(event_payload)