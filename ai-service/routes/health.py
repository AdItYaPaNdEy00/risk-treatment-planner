from flask import Blueprint, jsonify
import time
from services.groq_client import response_times, start_time, MODEL_NAME
from services.chroma_client import get_doc_count
from services.redis_client import cache_hits, cache_misses

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    avg_time = 0

    if response_times:
        avg_time = sum(response_times) / len(response_times)

    uptime = time.time() - start_time

    return jsonify({
        "status": "ok",
        "model": MODEL_NAME,
        "avg_response_time_ms": round(avg_time, 2),
        "chroma_doc_count": get_doc_count(),
        "uptime_sec": int(uptime),
        "cache": {
            "hits": cache_hits,
            "misses": cache_misses
        }
    })