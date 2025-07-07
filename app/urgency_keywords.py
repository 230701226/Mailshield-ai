import re

# Common urgency or fear-based phrases in phishing
URGENCY_PHRASES = [
    "urgent", "immediate action", "verify your account", "suspended",
    "limited time", "act now", "click below", "click here",
    "security alert", "unusual activity", "your account is compromised",
    "update your billing", "confirm your identity", "password expired",
    "access restricted", "failure to", "resolve now"
]

def analyze_urgency(text):
    found = []
    for phrase in URGENCY_PHRASES:
        if re.search(rf'\b{re.escape(phrase)}\b', text.lower()):
            found.append(phrase)
    return {
        "urgency_score": len(found),
        "matched_phrases": found
    }
