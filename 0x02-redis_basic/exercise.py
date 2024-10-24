#!/usr/bin/env python3
"""Exercise Module"""
import redis
from typing import Union, Optional, Callable, Any
from uuid import uuid4
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs
    for a particular function in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create keys for storing inputs and outputs
        inputs_key = \
            f"{self.__class__.__qualname__}.{method.__name__}:inputs"
        outputs_key = \
            f"{self.__class__.__qualname__}.{method.__name__}:outputs"

        # Store the input parameters in Redis
        self._redis.rpush(inputs_key, str(args))  # Normalize to string

        # Call the original method to get the output
        output = method(self, *args, **kwargs)

        # Store the output in Redis
        self._redis.rpush(outputs_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a
    methodtion is called and stores the count in Redis.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A wrapper method"""
        key = self.__class__.__qualname__ + '.' + method.__name__
        self._redis.incr(key)  # Increment the call count in Redis
        return method(self, *args, **kwargs)  # Call the original method

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
    @call_history
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
