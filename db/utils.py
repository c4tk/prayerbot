#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import random
import storage

def fetch_history(attributes, limit = None):
    data = storage.fetch_history()
    filtered_data = []
    for prayer in data:
        for attr_key,attr_value in attributes.items():
            if prayer[attr_key] == attr_value:
                filtered_data.append(prayer)
    random.shuffle(filtered_data)
    if limit:
        filtered_data = filtered_data[:limit]
    return filtered_data

def fetch(id):
    data = storage.fetch_history()
    for prayer in data:
        if prayer['id'] == id:
            break
    return prayer
