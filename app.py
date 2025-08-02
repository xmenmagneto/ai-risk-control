# app.py
from flask import Flask, request, jsonify
import llm_infer
import logging
import json
import pandas as pd
from rule_engine import RuleEngine  # 引入规则引擎
from llm_infer import fuse_decision  # 引入融合逻辑函数

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# 初始化规则引擎
rule_engine = RuleEngine()

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    try:
        # 转成 DataFrame
        input_df = pd.DataFrame([{
            'ip': data.get('ip'),
            'userAgent': data.get('userAgent'),
            'requestCountLastMinute': data.get('requestCountLastMinute'),
            'userId': data.get('userId'),
            'productId': data.get('productId'),
            'timestamp': data.get('timestamp')
        }])

        # 1. 获取规则判定
        rule_decision, rule_hits = rule_engine.evaluate(data)  # 返回 "BLOCK"/"ALLOW", ["规则1", "规则2"]
        logging.info(json.dumps({
            "stage": "rule_engine",
            "rule_decision": rule_decision,
            "rule_hits": rule_hits
        }))

        # 2. 获取模型预测
        model_decisions, probs = llm_infer.predict(input_df)
        model_decision = model_decisions[0]
        prob_block = probs[0]
        logging.info(json.dumps({
            "stage": "model_infer",
            "model_decision": model_decision,
            "model_probability_block": prob_block
        }))

        # 3. 融合决策
        final_decision = fuse_decision(rule_decision, model_decision, mode="fuse")
        logging.info(json.dumps({
            "stage": "fusion",
            "final_decision": final_decision,
            "rule_decision": rule_decision,
            "model_decision": model_decision
        }))

        # 4. 日志记录全流程
        logging.info(json.dumps({
            "stage": "fusion",
            "final_decision": final_decision,
            "rule_decision": rule_decision,
            "model_decision": model_decision
        }))

        return jsonify({
            "decision": final_decision,
            "rule_hits": rule_hits,
            "model_prob_block": prob_block
        })

    except Exception as e:
        logging.exception("LLM 推理异常：")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)