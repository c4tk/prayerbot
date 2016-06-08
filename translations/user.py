#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import facebook.utils
from flask.ext.babel import force_locale, gettext

def ugettext(user_id, string, **variables):
    locale = utils.get_language(user_id)
    with force_locale(locale):
        gettext(string, variables)
