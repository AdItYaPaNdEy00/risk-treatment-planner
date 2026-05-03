import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

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


def generate_text(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            start = time.time()

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            end = time.time()

            # Track response time
            response_times.append((end - start) * 1000)

            # Keep only last 10 entries
            if len(response_times) > 10:
                response_times.pop(0)

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {str(e)}")

            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return "Error"