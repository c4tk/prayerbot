#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import sqlite3

data = [
    {"id": 12, "user_id": "1099770976753951", "description": "Potrzebuję modlitwy w intencji mojej mamy", "ts": 1412412331, "said": "no", "commiter_id": "1099770976753951", },
    {"id": 13, "user_id": "1099770976753951", "description": "O powrót do zdrowia", "ts": 121312313, "said": "yes", "commiter_id": "", },
    {"id": 15, "user_id": "215380638847054", "description": "O rozeznanie drogi", "ts": 121312312, "said": "no", "commiter_id": None, },
    {"id": 16, "user_id": "10208414992228182", "description": "O Światowe Dni Młodzieży", "ts": 121312313, "said": "yes", "commiter_id": "1099770976753951", },
    {"id": 17, "user_id": "10208414992228182", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "yes", "commiter_id": "1099770976753951", },
    {"id": 18, "user_id": "215380638847054", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "no", "commiter_id": None, },
]

cmd_create = """\
CREATE TABLE t_intent(
user_id text,
description text,
ts integer,
said text,
commiter_id text
)
"""

cmd_select = """\
SELECT * FROM t_intent
"""

cmd_insert = """\
INSERT INTO t_intent(
user_id,
description,
ts,
said,
commiter_id
)
VALUES
(
'%(user_id)s',
'%(description)s',
%(ts)s,
'%(said)s',
'%(commiter_id)s'
)
"""

db_file = 'intent.db'

def is_db_file():
    return os.path.isfile(db_file)

if not is_db_file():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(cmd_create)
    for data_line in data:
        cmd = cmd_insert % data_line
        print cmd
        c.execute(cmd)
    conn.commit()

def fetch_from_db():
    if is_db_file():
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        data = c.execute(cmd_select)
    return data.fetchall()

def fetch_history():
    data = fetch_from_db()
    return data
