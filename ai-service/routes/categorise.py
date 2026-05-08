from flask import Blueprint, request, jsonify
from services.groq_client import generate_text, MODEL_NAME
import json
from extensions import limiter

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
@limiter.limit("5 per minute")
def categorise():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_input = data["text"]

    # Cache control
    use_cache = data.get("use_cache", True)

    # Prompt
    prompt = f"""
You are an expert risk classification system.

Classify the input STRICTLY into one of:

1. Operational Risk → system failures, downtime, technical issues, hardware/software problems
2. Financial Risk → fraud, monetary loss, financial transactions
3. Compliance Risk → legal violations, regulations, policies, insider trading, money laundering
4. Strategic Risk → business decisions, pricing strategy, market strategy, planning mistakes

Rules:
- Choose ONLY one category
- Be accurate and consistent
- Confidence must be between 0 and 1
- Do not guess randomly

Return ONLY valid JSON:
{{
  "category": "...",
  "confidence": 0.0,
  "reasoning": "..."
}}

Input: {user_input}
"""

    # Generate AI response
    response = generate_text(prompt, use_cache=use_cache)

    ai_output = response["text"]
    response_time = response["response_time_ms"]
    cached = response["cached"]
    is_fallback = response["is_fallback"]

    try:

        # Parse AI JSON
        result = json.loads(ai_output)

        # Safety fix
        result["confidence"] = max(
            0.0,
            min(1.0, result.get("confidence", 0))
        )

        # Final response
        return jsonify({
            "data": result,
            "meta": {
                "confidence": result.get("confidence", 0),
                "model_used": MODEL_NAME,
                "tokens_used": len(ai_output.split()),
                "response_time_ms": round(response_time, 2),
                "cached": cached,
                "is_fallback": is_fallback
            }
        })

    except Exception:

        return jsonify({
            "data": {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": "Failed to parse AI response"
            },
            "meta": {
                "model_used": MODEL_NAME,
                "cached": cached,
                "is_fallback": is_fallback
            },
            "raw_output": ai_output
        }), 500