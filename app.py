# app.py
from flask import Flask, request, jsonify
from request_features import RequestFeatures
from model import score_request

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    features = RequestFeatures(data)
    decision = score_request(features)
    return jsonify({"decision": decision})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)