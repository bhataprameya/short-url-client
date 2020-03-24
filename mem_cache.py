"""
Caching layer
"""
import memcache


class Memc:

    def __init__(self, hostname="127.0.0.1", port="11211"):

        self.hostname = "%s:%s" % (hostname, port)
        self.server = memcache.Client([self.hostname])

    def set_mem_cache(self, key, value, ttl=20):
        """
        This method is used to set a new value
        in the memcache server.
        """
        self.server.set(key, value, ttl)

    def get_mem_cache(self, key):
        """
        This method is used to retrieve a value
        from the memcache server
        """
        # return "%s"%key
        return self.server.get(key)

    def delete_mem_cache(self, key):
        """
        This method is used to delete a value from the
        memcached server. Lazy delete
        """
        self.server.delete(key)
