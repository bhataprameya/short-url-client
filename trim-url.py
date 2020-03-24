"""
calculates teh short url by a logic internally and does not hit any external server to get the short url
So we need to expand the usr internally before hitting the url else the url will be invalid)
Also caches the short url for some time so as to avoid frequent calculation of short url for same url
"""
import logging
import short_url
import mem_cache
import utils


class Initialize:
    __cache = None
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
    cache = Initialize.get_shorten_cache()
    cached_url = cache.get_mem_cache(url_hash)
    if cached_url:
        logging.info("Serving short url from cache for %s", url)
        small_url = cached_url
    else:
        logging.info("short url not found in cache for %s. calculating short url...", url)
        small_url = short_url.encode_url(url)
        cache.set_mem_cache(url_hash, small_url, utils.CACHE_TIME)
        logging.info("putting the short url in cache for %s", url)
    return small_url

def get_expanded_url(url):
    logging.info("decoding the short url...", url)
    long_url = short_url.decode_url(url)
    logging.info("putting the short url in cache for %s", url)
    return long_url
