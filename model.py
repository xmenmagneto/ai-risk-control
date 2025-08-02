# model.py

def score_request(features):
    """
    模拟风控评分逻辑（可替换成 ML 模型）
    """  # 简单规则：一分钟请求次数大于 10，或 UA 嫌疑（如 curl/python），就拦截
    suspicious_ua_keywords = ["python", "curl", "bot", "scrapy", "java"]

    if features.request_count_last_minute > 10:
        return "BLOCK"

    ua = features.user_agent.lower() if features.user_agent else ""
    if any(keyword in ua for keyword in suspicious_ua_keywords):
        return "BLOCK"

    return "ALLOW"