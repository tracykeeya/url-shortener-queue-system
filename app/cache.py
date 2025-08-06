import redis
import os

# Connect to Redis (localhost, default port)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Cache functions
def get_cached_url(code: str):
    return redis_client.get(code)

def set_cached_url(code: str, url: str):
    redis_client.set(code, url, ex=3600)  # Cache for 1 hour (3600s)
