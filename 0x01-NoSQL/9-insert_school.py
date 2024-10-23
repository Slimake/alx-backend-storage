#!/usr/bin/env python3
"""9-insert_school Module"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    """
    result = mongo_collection.insert(kwargs)
    return result
