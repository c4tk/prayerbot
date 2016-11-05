#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from facebook import user_utils
from flask_babel import force_locale, gettext
from dbms.models import User
from dbms.rdb import db

def user_gettext(user_id, string, **variables):
    user_pref = User.query.filter_by(user_id=user_id).first()
    if user_pref:
        locale = user_pref.locale
    else:
        locale = user_utils.locale(user_id)
        user_pref = User(user_id, locale)
        db.session.add(user_pref)
        db.session.commit()
        db.session.flush()

    with force_locale(locale):
        return gettext(string, **variables)
