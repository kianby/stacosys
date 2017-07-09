import time
from sanic import Sanic

app = Sanic()
cache = {}
cache_time = 0

def get_cached(key):
    global cache
    global cache_time
    value = cache.get(key,None)
    if (time.time() - cache_time) > 120:
        cache = {}
        cache_time = time.time()
    return value

def set_cached(key, value):
    global cache
    cache[key] = value
