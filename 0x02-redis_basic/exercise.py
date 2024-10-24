#!/usr/bin/env python3
"""Exercise Module"""
import redis
from typing import Union, Optional, Callable, Any
from uuid import uuid4
from functools import wraps

r = redis.Redis()


def count_calls(func: Callable) -> Callable:
    """
    A decorator that counts the number of times a function is called and stores the count in Redis.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self.__class__.__qualname__ + '.' + func.__name__  # Create a unique key
        r.incr(key)  # Increment the call count in Redis
        return func(self, *args, **kwargs)  # Call the original method

    return wrapper


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

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Create a get method that take a key string argument and an optional
        Callable argument named fn. This callable will be used to convert
        the data back to the desired format.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Return str conversion"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Return int conversion"""
        return self.get(key, int)
