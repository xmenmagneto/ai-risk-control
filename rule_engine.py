suspicious_keywords = ["curl", "python", "bot", "scrapy", "java"]

def rule_decision(features):
    if features.request_count_last_minute > 10:
        return "BLOCK"
    ua = features.user_agent.lower() if features.user_agent else ""
    if any(k in ua for k in suspicious_keywords):
        return "BLOCK"
    return "ALLOW"