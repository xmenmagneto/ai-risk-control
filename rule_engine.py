# rule_engine.py

class RuleEngine:
    def __init__(self):
        self.rules = [
            self.rule_bot_user_agent,
            self.rule_high_freq_access
        ]

    def rule_bot_user_agent(self, row):
        ua = row.get('userAgent', '').lower()
        return any(bot in ua for bot in ['curl', 'bot', 'python', 'java'])

    def rule_high_freq_access(self, row):
        return row.get('requestCountLastMinute', 0) > 20


    def evaluate(self, row: dict):
        hits = []
        for rule in self.rules:
            if rule(row):
                hits.append(rule.__name__)
        decision = "BLOCK" if hits else "ALLOW"
        return decision, hits