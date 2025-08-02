# app.py
from flask import Flask, request, jsonify
from request_features import RequestFeatures
from model import score_request
import logging
import joblib

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = Flask(__name__)
model = joblib.load('model.pkl')  # 加载训练好的模型

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    features = RequestFeatures(data)

    # 用训练好的模型进行预测
    # 这里以 userAgent 作为输入，和训练时保持一致
    user_agent = features.user_agent or ""

    pred = model.predict([user_agent])[0]  # 预测结果是0或1

    decision = "BLOCK" if pred == 1 else "ALLOW"

    # ✅ 记录风控决策与请求特征
    logging.info("Risk decision: %s | Features: %s", decision, data)

    return jsonify({"decision": decision})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)