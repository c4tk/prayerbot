#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import random
import storage

def fetch_history(attributes, limit = None):
    filtered_data = storage.fetch_history()
    random.shuffle(filtered_data)
    if limit:
        filtered_data = filtered_data[:limit]
    return filtered_data
