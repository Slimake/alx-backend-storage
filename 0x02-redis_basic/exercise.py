#!/usr/bin/env python3
"""Exercise Module"""
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """
    Create a Cache class. In the __init__ method, store an instance
    of the Redis client as a private variable named _redis
    (using redis.Redis()) and flush the instance using flushdb.
    """

    def __init__(self) -> None:
        """Initialize"""
        self._redis = redis.Redis()  # Create an instance of Redis class
        self._redis.flushdb()  # Flush database: clear old entries

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
