from flask import Blueprint, request, jsonify
from threading import Thread
import uuid
import time

report_bp = Blueprint("report", __name__)

# Store job results
jobs = {}


def generate_report_job(job_id, text):
    # simulate AI processing
    time.sleep(5)

    report = f"AI Generated Report for: {text}"

    jobs[job_id] = {
        "status": "completed",
        "report": report
    }


@report_bp.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    text = data["text"]

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "processing"
    }

    thread = Thread(
        target=generate_report_job,
        args=(job_id, text)
    )

    thread.start()

    return jsonify({
        "job_id": job_id,
        "status": "processing"
    })


@report_bp.route("/report-status/<job_id>", methods=["GET"])
def report_status(job_id):

    if job_id not in jobs:
        return jsonify({"error": "Invalid job_id"}), 404

    return jsonify(jobs[job_id])