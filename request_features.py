# request_features.py

class RequestFeatures:
    def __init__(self, data):
        self.ip = data.get("ip")
        self.user_agent = data.get("userAgent")
        self.user_id = data.get("userId")
        self.product_id = data.get("productId")
        self.timestamp = data.get("timestamp")
        self.request_count_last_minute = data.get("requestCountLastMinute")