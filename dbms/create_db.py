# -*- coding: utf-8 -*-
from rdb import db
from models import Intent, BibleVerse

# create the database and the db tables
db.create_all()

# insert prayer requests
db.session.add(Intent(1099770976753951, u"Potrzebuje modlitwy w intencji mojej mamy"))
db.session.add(Intent(1099770976753951, u"O powrot do zdrowia"))
db.session.add(Intent(1209178385783730, u"O rozeznanie drogi"))
db.session.add(Intent(10208414992228182, u"O Swiatowe Dni Mlodziezy"))
db.session.add(Intent(10208414992228182, u"W intencji Bogu wiadomej"))
db.session.add(Intent(215380638847054, u"W intencji Bogu wiadomej"))

# insert Bible verses
db.session.add(BibleVerse(u"Lecz ci, co zaufali Panu, odzyskują siły, otrzymują skrzydła jak orły: biegną bez zmęczenia, bez znużenia idą", u"Iz40,31"))
db.session.add(BibleVerse(u"Nie sądźcie, abyście nie byli sądzeni. Bo takim sądem, jakim sądzicie, i was osądzą; i taką miarą jaką wy mierzycie, wam odmierzą", u"Mt7,1"))
db.session.add(BibleVerse(u"Bóg jest światłością, a nie ma w Nim żadnej ciemności.", u"1J5b"))

# commit the changes
db.session.commit()
