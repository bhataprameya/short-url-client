import hashlib

# short url cache time
CACHE_TIME = 3600


def get_hash(key):
    key = key.encode('utf-8')
    return hashlib.sha256(key).hexdigest()