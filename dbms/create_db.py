# -*- coding: utf-8 -*-
from rdb import db
from models import Intent

# create the database and the db tables
db.create_all()

# insert
db.session.add(Intent(1099770976753951, u"Potrzebuje modlitwy w intencji mojej mamy"))
db.session.add(Intent(1099770976753951, u"O powrot do zdrowia"))
db.session.add(Intent(1209178385783730, u"O rozeznanie drogi"))
db.session.add(Intent(10208414992228182, u"O Swiatowe Dni Mlodziezy"))
db.session.add(Intent(10208414992228182, u"W intencji Bogu wiadomej"))
db.session.add(Intent(215380638847054, u"W intencji Bogu wiadomej"))

# commit the changes
db.session.commit()
