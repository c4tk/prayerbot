#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import sqlite3
from labels import label_id

data = [
    {label_id: 12, "user_id": "1099770976753951", "description": "Potrzebuję modlitwy w intencji mojej mamy", "ts": 1412412331, "said": "no", "commiter_id": "1099770976753951", },
    {label_id: 13, "user_id": "1099770976753951", "description": "O powrót do zdrowia", "ts": 121312313, "said": "no", "commiter_id": "", },
    {label_id: 15, "user_id": "1209178385783730", "description": "O rozeznanie drogi", "ts": 121312312, "said": "no", "commiter_id": None, },
    {label_id: 16, "user_id": "10208414992228182", "description": "O Światowe Dni Młodzieży", "ts": 121312313, "said": "no", "commiter_id": "1209178385783730", },
    {label_id: 17, "user_id": "10208414992228182", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "no", "commiter_id": "1099770976753951", },
    {label_id: 18, "user_id": "215380638847054", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "yes", "commiter_id": None, },
]

cmd_create = """\
CREATE TABLE IF NOT EXISTS t_intent(
user_id text,
description text,
ts integer,
said text,
commiter_id text
)
"""

cmd_select = """\
SELECT %s, * FROM t_intent
""" % label_id

cmd_insert = """\
INSERT INTO t_intent(
%(label_name)s,
user_id,
description,
ts,
said,
commiter_id
)
VALUES
(
%(label_value)d,
'%(user_id)s',
'%(description)s',
%(ts)d,
'%(said)s',
'%(commiter_id)s'
)
"""

db_file = 'intent.db'

def is_db_file():
    return os.path.isfile(db_file)

def fetch_from_db():
    if is_db_file():
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        data = c.execute(cmd_select)
    return data.fetchall()

if not is_db_file():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(cmd_create)
    if not fetch_from_db():
        for data_line in data:
            data_line['label_name'] = label_id
            data_line['label_value'] = data_line[label_id]
            cmd = cmd_insert % data_line
            c.execute(cmd)
    conn.commit()

def fetch_history():
    data = fetch_from_db()
    return data
