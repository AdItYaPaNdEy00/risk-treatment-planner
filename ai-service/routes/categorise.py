from flask import Blueprint, request, jsonify
from services.groq_client import generate_text
import json

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_input = data["text"]

    # ✅ cache control (inside function)
    use_cache = data.get("use_cache", True)

    # FINAL IMPROVED PROMPT
    prompt = f"""
You are an expert risk classification system.

Classify the input STRICTLY into one of:

1. Operational Risk → system failures, downtime, technical issues, hardware/software problems
2. Financial Risk → fraud, monetary loss, financial transactions
3. Compliance Risk → legal violations, regulations, policies, insider trading
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

    # ✅ cache-aware call
    response = generate_text(prompt, use_cache=use_cache)

    try:
        result = json.loads(response)

        # Safety fix
        result["confidence"] = max(0.0, min(1.0, result.get("confidence", 0)))

        return jsonify(result)

    except Exception:
        return jsonify({
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": "Failed to parse AI response",
            "raw_output": response
        }), 500