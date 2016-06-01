#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
import os
import psycopg2

class PostgresStorage:
    def __init__(self):
        if 'VCAP_SERVICES' in os.environ:
            vcap_services = json.loads(os.environ['VCAP_SERVICES'])
            print("VCAP_SERVICES: " + str(vcap_services))
            pgsql_srv = vcap_services['elephantsql'][0]
            pgsql_credentials = pgsql_srv['credentials']
            self.conn = psycopg2.connect(pgsql_credentials['uri'])

    def test(self):
        cur = self.conn.cursor()
        print("Begin DB test")
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        cur.execute("SELECT * FROM test;")
        print("DB result: " + str(cur.fetchone()))
        cur.close()
