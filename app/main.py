"""
Service Monitoring Dashboard - Main Flask Application
"""

import time
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="../templates")

# In-memory list to store services
services = []


def check_service(url):
    """Check if a service URL is UP or DOWN and return response time in ms."""
    try:
        start = time.time()
        response = requests.get(url, timeout=5)
        elapsed = round((time.time() - start) * 1000, 2)
        status = "UP" if response.status_code == 200 else "DOWN"
    except Exception:
        elapsed = 0
        status = "DOWN"
    return status, elapsed


@app.route("/", methods=["GET", "POST"])
def index():
    """Main dashboard page. Allows adding services and displays their status."""
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            status, response_time = check_service(url)
            services.append({"url": url, "status": status, "response_time": response_time})
    return render_template("index.html", services=services)


@app.route("/check", methods=["POST"])
def check():
    """API endpoint to check a service URL."""
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "url is required"}), 400
    url = data["url"]
    status, response_time = check_service(url)
    return jsonify({"status": status, "response_time": response_time})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
