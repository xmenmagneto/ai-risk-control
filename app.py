# app.py
from flask import Flask, request, jsonify

import llm_infer
import logging
import json
import pandas as pd

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    try:
        # 将 dict 包装成 2D DataFrame
        input_df = pd.DataFrame([{
            'ip': data.get('ip'),
            'userAgent': data.get('userAgent'),
            'requestCountLastMinute': data.get('requestCountLastMinute'),
            'userId': data.get('userId'),
            'productId': data.get('productId'),
            'timestamp': data.get('timestamp')
        }])

        # 推理
        decisions, probs = llm_infer.predict(input_df)
        decision = decisions[0]  # 例如 "BLOCK"
        prob_block = probs[0]  # 例如 1.0

        # 如果想记录概率，你需要改 predict 函数返回概率或同时返回概率
        # 如果只要决策，直接用decision即可

        logging.info(json.dumps({
            "input": data,
            "decision": decision
        }))

        return jsonify({"decision": decision})

    except Exception as e:
        logging.exception("LLM 推理异常：")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)