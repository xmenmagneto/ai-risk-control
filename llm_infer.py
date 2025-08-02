# llm_infer.py
import joblib
import os
import pandas as pd

# 模型路径
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# 加载训练好的模型（包含预处理pipeline + 分类器）
model = joblib.load(MODEL_PATH)


def detect_bot_useragent(ua):
    if ua is None:
        return 0
    ua = ua.lower()
    for bot_keyword in ['curl', 'python', 'bot', 'scrapy', 'java']:
        if bot_keyword in ua:
            return 1
    return 0


def predict(input_df: pd.DataFrame):
    if 'is_bot_ua' not in input_df.columns:
        input_df['is_bot_ua'] = input_df['userAgent'].apply(detect_bot_useragent)

    decisions = []
    probs_list = []

    probs = model.predict_proba(input_df)

    for i, row in input_df.iterrows():
        if row['is_bot_ua'] == 1:
            decisions.append("BLOCK")
            probs_list.append(1.0)  # 机器人概率直接1
        else:
            prob_block = probs[i][1]
            probs_list.append(prob_block)
            decisions.append("BLOCK" if prob_block > 0.5 else "ALLOW")

    # 第一个列表：每条请求的最终决策
    # 第二个列表：对应每条请求被判定为 BLOCK 的概率（硬判机器人时用 1.0）
    # Example:
    #   decisions = ["BLOCK", "ALLOW"]
    #   probs_list = [1.0, 0.3]
    # 第一条是机器人（is_bot_ua=1），硬判决为 "BLOCK"，概率设为1.0
    # 第二条是正常UA，模型预测概率为比如 [0.7, 0.3] (ALLOW 70%，BLOCK 30%)
    return decisions, probs_list