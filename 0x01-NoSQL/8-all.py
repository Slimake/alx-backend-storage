#!/usr/bin/env python3
"""8-all Module"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    """
    return mongo_collection.find() if mongo_collection else []
