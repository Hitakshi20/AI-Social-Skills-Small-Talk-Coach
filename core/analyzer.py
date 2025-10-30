import re
from typing import Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_sid = SentimentIntensityAnalyzer()

# Simple patterns (tweak as you like)
FILLERS_RE = re.compile(r"\b(um+|uh+|erm|like|you know|kinda|sorta)\b", re.I)
THANKS_RE  = re.compile(r"\b(thanks|thank you|appreciate)\b", re.I)
NUM_RE     = re.compile(r"\d")
QUESTION_RE= re.compile(r"\?")
DOMAINS_RE = re.compile(
    r"\b(python|java|figma|design|api|dataset|pipeline|kafka|pytorch|react|sql|ml|data)\b", re.I
)

def _sentences(text: str):
    # naive sentence split: '.', '!', '?'
    return [s for s in re.split(r"[.!?]+", text) if s.strip()]

def _tokens(text: str):
    # naive tokens: split by whitespace
    return [t for t in re.split(r"\s+", text.strip()) if t]

def _capitalized_chunks(text: str):
    # cheap "specificity" proxy: Capitalized words that aren't at sentence start
    return re.findall(r"\b[A-Z][a-zA-Z0-9_-]{2,}\b", text)

def analyze_text(text: str) -> Dict[str, float]:
    text = (text or "").strip()

    toks = _tokens(text)
    sents = _sentences(text)

    features = {
        "tokens": len(toks),
        "sentences": len(sents),
        "fillers": len(FILLERS_RE.findall(text)),
        "has_question": bool(QUESTION_RE.search(text)),
        "sentiment": _sid.polarity_scores(text)["compound"],
        "has_thanks": bool(THANKS_RE.search(text)),
        "has_numbers": bool(NUM_RE.search(text)),
        "has_domain_terms": bool(DOMAINS_RE.search(text)),
        "caps_chunks": len(_capitalized_chunks(text)),
        "ends_trail": text.endswith("..."),
    }
    return features
