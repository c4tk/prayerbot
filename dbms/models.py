# -*- coding: utf-8 -*-
from rdb import db

class Intent(db.Model):
    """ Intent """

    __tablename__ = 't_intent'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    description = db.Column(db.String)
    ts = db.Column(db.Integer)
    commiter_id = db.Column(db.Integer)

    def __init__(self, user_id, description):
        self.user_id = user_id
        self.description = description

    def __repr__(self):
        return u"<Intent id:{}, user_id: {}, desc:{}>".format(self.id, self.user_id, self.description)
