from flask import Flask, request, jsonify
import llm_infer
import logging
import json
import pandas as pd
from rule_engine import RuleEngine
from llm_infer import fuse_decision
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import time

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
rule_engine = RuleEngine()
executor = ThreadPoolExecutor(max_workers=2)  # 模型预测线程池

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    try:
        input_df = pd.DataFrame([{
            'ip': data.get('ip'),
            'userAgent': data.get('userAgent'),
            'requestCountLastMinute': data.get('requestCountLastMinute'),
            'userId': data.get('userId'),
            'productId': data.get('productId'),
            'timestamp': data.get('timestamp')
        }])

        # 1. 规则判定
        rule_decision, rule_hits = rule_engine.evaluate(data)

        logging.info(json.dumps({
            "stage": "rule_engine",
            "rule_decision": rule_decision,
            "rule_hits": rule_hits
        }))

        # 2. 模型预测 + 超时控制
        model_decision = None
        prob_block = None
        model_latency_ms = None
        used_fallback = False

        start_time = time.time()
        future = executor.submit(llm_infer.predict, input_df)

        try:
            model_decisions, probs = future.result(timeout=1.5)
            model_decision = model_decisions[0]
            prob_block = probs[0]
            model_latency_ms = int((time.time() - start_time) * 1000)

            logging.info(json.dumps({
                "stage": "model_infer",
                "model_decision": model_decision,
                "model_probability_block": prob_block,
                "latency_ms": model_latency_ms
            }))

        except TimeoutError:
            used_fallback = True
            logging.warning("[WARN] 模型推理超时，使用规则判定降级")

        except Exception as e:
            used_fallback = True
            logging.exception("[ERROR] 模型推理异常，使用规则判定降级")

        # 3. 决策融合（fallback 时使用规则决策）
        final_decision = fuse_decision(
            rule_decision=rule_decision,
            model_decision=model_decision if not used_fallback else None,
            mode="fuse"
        )

        logging.info(json.dumps({
            "stage": "fusion",
            "final_decision": final_decision,
            "rule_decision": rule_decision,
            "model_decision": model_decision,
            "used_fallback": used_fallback
        }))

        return jsonify({
            "decision": final_decision,
            "rule_hits": rule_hits,
            "model_prob_block": prob_block,
            "model_latency_ms": model_latency_ms,
            "used_fallback": used_fallback
        })

    except Exception as e:
        logging.exception("服务异常：")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)