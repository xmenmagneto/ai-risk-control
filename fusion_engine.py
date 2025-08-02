from config import USE_MODEL, USE_RULE_ENGINE, FUSION_MODE
from rule_engine import rule_decision
from model_engine import model_decision

def fused_decision(features):
    rule = rule_decision(features) if USE_RULE_ENGINE else None
    model = model_decision(features) if USE_MODEL else None

    if FUSION_MODE == "rule_only":
        return rule, model, rule
    elif FUSION_MODE == "model_only":
        return rule, model, model
    elif FUSION_MODE == "vote":
        if rule == "BLOCK" or model == "BLOCK":
            return rule, model, "BLOCK"
        else:
            return rule, model, "ALLOW"