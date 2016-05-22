#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import random
from labels import label_id

import storage

def fetch_history(attributes, limit=None):
    data = storage.fetch_history()
    filtered_data = []
    for prayer in data:
        match_all = True
        for attr_key,attr_value in attributes.items():
            if prayer[attr_key] != attr_value:
                match_all = False
        if match_all:
            filtered_data.append(prayer)
    random.shuffle(filtered_data)
    if limit:
        filtered_data = filtered_data[:limit]
    return filtered_data

def fetch(id_value):
    result_ls = storage.fetch_from_db(id_value=id_value)
    if result_ls:
        one_record = result_ls[0]
    else:
        one_record = None
    return one_record

def insert_row(data_line, conn=None):
    storage.insert_row(data_line, conn=conn)

def delete_from_db(id_value):
    storage.delete_from_db(id_value)

def update_description(id_value, description_value):
    storage.update_description(id_value, description_value)
