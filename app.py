# app.py
from flask import Flask, request, jsonify
from request_features import RequestFeatures
from fusion_engine import fused_decision
import logging
import json

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    features = RequestFeatures(data)

    rule, model, final = fused_decision(features)

    # 结构化日志记录
    log_entry = {
        "features": data,
        "rule_decision": rule,
        "model_decision": model,
        "final_decision": final
    }
    logging.info(json.dumps(log_entry))  # 可直接写入文件、ES、Kafka 等

    return jsonify({"decision": final})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)