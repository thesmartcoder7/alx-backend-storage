#!/usr/bin/env python3
""" implement get_page function """
import requests
import redis
import functools
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """
    this is a Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"count:{args[0]}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Web:
    """
    this is a Web class for getting HTML content of a URL and caching it.

    Attributes:
        _redis (Redis): Instance of the Redis client.
    """

    def __init__(self):
        """
        Web class constructor.
        """
        self._redis = redis.Redis()

    @count_calls
    def get_page(self, url: str) -> str:
        """
        Get the HTML content of a URL and cache it.

        Args:
            url (str): The URL to get the HTML content from.

        Returns:
            str: The HTML content of the URL.
        """
        response = self._redis.get(url)
        if response is None:
            response = requests.get(url).text
            self._redis.setex(url, 10, response)
        return response
