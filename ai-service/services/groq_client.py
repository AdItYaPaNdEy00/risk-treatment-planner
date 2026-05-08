import os
import time
import logging
import hashlib
from groq import Groq
from dotenv import load_dotenv
from services.redis_client import r, cache_hits, cache_misses

# Metrics
response_times = []
start_time = time.time()
MODEL_NAME = "llama-3.1-8b-instant"

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")

client = Groq(api_key=api_key)


def generate_text(prompt: str, use_cache: bool = True, max_retries: int = 3):
    global cache_hits, cache_misses

    print("CACHE CHECK RUNNING")

    # Create cache key
    cache_key = hashlib.sha256(prompt.encode()).hexdigest()

    # Check Redis cache
    if use_cache:
        cached_response = r.get(cache_key)

        if cached_response:
            print("CACHE HIT")
            cache_hits += 1

            return {
                "text": cached_response,
                "response_time_ms": 0,
                "cached": True
            }

        else:
            print("CACHE MISS")
            cache_misses += 1

    # Retry loop
    for attempt in range(max_retries):
        try:
            start = time.time()

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            end = time.time()

            # Track response time
            response_times.append((end - start) * 1000)

            if len(response_times) > 10:
                response_times.pop(0)

            output = response.choices[0].message.content.strip()

            # Save in Redis (15 min TTL)
            if use_cache:
                r.setex(cache_key, 900, output)

            return {
                "text": output,
                "response_time_ms": (end - start) * 1000,
                "cached": False
            }

        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {str(e)}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

            else:
                return {
                    "text": "Error",
                    "response_time_ms": 0,
                    "cached": False
                }