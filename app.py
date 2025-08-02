# app.py
from flask import Flask, request, jsonify
from request_features import RequestFeatures
from model import score_request

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    try:
        data = request.get_json()
        features = RequestFeatures(data)
        result = score_request(features)
        return result, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)