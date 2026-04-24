from flask import Blueprint, request, jsonify
from services.groq_client import generate_text

categorise_bp = Blueprint("categorise", __name__)

@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    user_input = data["text"]

    # FIXED PROMPT (f-string)
    prompt = f"""
You are a strict JSON generator.

Classify the input into one of:
Operational Risk, Financial Risk, Compliance Risk, Strategic Risk.

Return ONLY valid JSON. No extra text.

Format:
{{
  "category": "string",
  "confidence": 0.0,
  "reasoning": "string"
}}

Input: {user_input}
"""

    response = generate_text(prompt)

    try:
        import json
        result = json.loads(response)

        # safety fix
        result["confidence"] = max(0.0, min(1.0, result.get("confidence", 0)))

        return jsonify(result)

    except Exception:
        return jsonify({
            "category": "Unknown",
            "confidence": 0.0,
            "reasoning": "Failed to parse AI response",
            "raw_output": response
        }), 500