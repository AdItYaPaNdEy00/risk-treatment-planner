import redis

#import redis

try:
    r = redis.Redis(
        host="localhost",
        port=6379,
        decode_responses=True
    )
    r.ping()
    print("✅ Redis Connected")
except Exception:
    print("⚠️ Redis not available, running without cache")
    r = None

# counters
cache_hits = 0
cache_misses = 0