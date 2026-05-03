from flask import Blueprint, request, jsonify
from services.groq_client import generate_text
from services.chroma_client import query_documents

query_bp = Blueprint("query", __name__)

@query_bp.route("/query", methods=["POST"])
def query():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Missing 'question' field"}), 400

    user_question = data["question"]

    # Step 1: Retrieve top 3 similar docs
    results = query_documents(user_question, n_results=3)
    docs = results.get("documents", [[]])[0]

    # Step 2: Build context
    context = "\n".join(docs)

    # Step 3: Prompt
    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{user_question}

Answer clearly and concisely.
"""

    # Step 4: Call Groq
    answer = generate_text(prompt)

    return jsonify({
        "answer": answer,
        "sources": docs
    })