#!/usr/bin/env python3
"""
create a web cach
"""

import requests
import time
from functools import wraps

# Dictionary to store cached results and their access counts
cache = {}


def cache_page_result(func):
    @wraps(func)
    def wrapper(url):
        # Check if the result is in the cache and not expired
        if url in cache and time.time() - cache[url]["timestamp"] < 10:
            # Increment the access count
            cache[url]["count"] += 1
            print(f"Cache hit! Count: {cache[url]['count']}")
            return cache[url]["content"]

        # Cache miss or expired, fetch the page
        content = func(url)

        # Update the cache
        cache[url] = {"content": content, "count": 1, "timestamp": time.time()}

        return content

    return wrapper


@cache_page_result
def get_page(url):
    """ get a page and cach value"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None


# Example usage
# url = "http://slowly.robertmurray.co.uk"
# page_content = get_page(url)
# print(page_content)
