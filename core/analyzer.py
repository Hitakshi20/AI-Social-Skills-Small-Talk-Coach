import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

# Load once
_nlp = None
_sid = SentimentIntensityAnalyzer()

def _ensure_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If the model isn't downloaded yet, guide the user:
            raise RuntimeError("Run: python -m spacy download en_core_web_sm")

FILLERS = re.compile(r"\b(um+|uh+|erm|like|you know)\b", re.IGNORECASE)

def analyze_text(text: str):
    _ensure_nlp()
    doc = _nlp(text or "")
    tokens = len([t for t in doc if not t.is_space])
    sentences = len(list(doc.sents))
    entities = len(doc.ents)
    has_question = "?" in text
    fillers = len(re.findall(FILLERS, text))
    sentiment = _sid.polarity_scores(text)["compound"]
    has_thanks = bool(re.search(r"\b(thanks|thank you|appreciate)\b", text, re.I))
    has_numbers = bool(re.search(r"\d", text))
    has_domain_terms = bool(re.search(r"\b(project|internship|pipeline|dataset|api|design|figma|pytorch|kafka)\b", text, re.I))
    ends_trail = text.strip().endswith("...")

    return {
        "tokens": tokens,
        "sentences": sentences,
        "entities": entities,
        "has_question": has_question,
        "fillers": fillers,
        "sentiment": sentiment,
        "has_thanks": has_thanks,
        "has_numbers": has_numbers,
        "has_domain_terms": has_domain_terms,
        "ends_trail": ends_trail
    }
