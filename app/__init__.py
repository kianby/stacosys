from sanic import Sanic
from aiocache import SimpleMemoryCache

app = Sanic()
cache = SimpleMemoryCache()
