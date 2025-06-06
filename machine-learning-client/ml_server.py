"""
ml_server.py gets request ID from web app and analyses it then returns the results.
"""

from flask import Flask, request, jsonify
from ml_client import run_analysis

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    POST endpoint to run analysis on web app request.
    """
    data = request.get_json()
    reqID = data.get("id")
    result = run_analysis(reqID)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
