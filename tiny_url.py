"""
Tiny url service: Uses a third party service to shorten url.
So we don't need the expand the url before hitting the service("tinyurl.com" will do the job for us)
Also caches the tiny url for some time so as to avoid frequent calculation of tiny url for same url
"""

import logging
import pyshorteners
import mem_cache
import utils



class Initialize:
    __instance = None
    __cache = None

    @staticmethod
    def get_shorten_object():
        """ Static access method. """
        if Initialize.__instance is None:
            Initialize.__instance = lambda m: pyshorteners.Shortener()
        return Initialize.__instance

    @staticmethod
    def get_shorten_cache():
        """ Static access method. """
        if Initialize.__cache is None:
            Initialize.__cache = lambda m: mem_cache.Memc()
        return Initialize.__cache

    def __init__(self):
        raise Exception("This class is a singleton!")


def get_short_url(url):
    url_hash = utils.get_hash(url)
    tiny_cache = Initialize.get_shorten_cache()
    cached_url = tiny_cache.get_mem_cache(url_hash)
    if cached_url:
        logging.info("Serving tiny url from cache for %s", url)
        tiny_url = cached_url
    else:
        logging.info("tiny url not found in cache for %s. Calling tiny url service to get the short url...", url)
        tiny_object = Initialize.get_shorten_object()
        tiny_url = tiny_object.tinyurl.short(url)
        tiny_cache.set_mem_cache(url_hash, tiny_url, utils.CACHE_TIME)
        logging.info("putting the tiny url in cache for %s", url)
    return tiny_url


def get_expanded_url(url):
    logging.info("decoding the tiny url...", url)
    tiny_object = Initialize.get_shorten_object()
    tiny_url = tiny_object.tinyurl.expand(url)
    logging.info("putting the short url in cache for %s", url)
    return tiny_url