#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from facebook import user_utils
from flask_babel import force_locale, gettext

def user_gettext(user_id, string, **variables):
    # TODO: user's locale should be saved in DB
    locale = user_utils.locale(user_id)
    with force_locale(locale):
        return gettext(string, **variables)
