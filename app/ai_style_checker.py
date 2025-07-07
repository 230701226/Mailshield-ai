import textstat
import re

def get_repetition_score(text):
    # High repetition of phrases or short sentence patterns
    words = text.lower().split()
    unique_words = set(words)
    if not words:
        return 0
    repetition_ratio = 1 - len(unique_words) / len(words)
    return round(repetition_ratio, 3)

def detect_ai_style(text):
    text = re.sub(r'\s+', ' ', text.strip())
    stats = {
        "flesch_score": textstat.flesch_reading_ease(text),
        "sentence_complexity": textstat.smog_index(text),
        "repetition_score": get_repetition_score(text)
    }

    # Heuristic scoring
    ai_like = 0
    if stats["flesch_score"] > 70: ai_like += 1       # too easy = robotic
    if stats["sentence_complexity"] < 6: ai_like += 1 # low complexity
    if stats["repetition_score"] > 0.25: ai_like += 1 # high repetition

    result = {
        "ai_style_score": ai_like,
        "details": stats
    }
    return result
