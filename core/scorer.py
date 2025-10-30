from typing import Dict

def _clip(x, lo=0, hi=10):
    return max(lo, min(hi, int(round(x))))

def score_response(f: Dict[str, float]) -> Dict[str, int]:
    # Hard guard: if there is no content, everything is 0
    if f.get("tokens", 0) == 0:
        return {"confidence": 0, "engagement": 0, "friendliness": 0, "specificity": 0}

    # Confidence (length + structure, punish fillers/trailing ...)
    conf = 0
    conf += 6 if f["tokens"] >= 18 else (3 if f["tokens"] >= 10 else 1)
    conf += 2 if f["sentences"] >= 2 else 0
    conf -= max(0, (f["fillers"] - 1)) * 2
    conf -= 2 if f["ends_trail"] else 0
    confidence = _clip(conf)

    # Engagement (ask back, say more than one short line)
    eng = 0
    eng += 4 if f["has_question"] else 0
    eng += 2 if f["sentences"] >= 2 else 0
    eng -= 2 if f["tokens"] < 8 else 0
    engagement = _clip(eng)

    # Friendliness (VADER + gratitude)
    # If very short (1–2 tokens), cap friendliness so "Hi" doesn't look great by itself.
    fr_base = (f["sentiment"] + 1) * 4
    if f["tokens"] <= 2:
        fr_base = min(fr_base, 2)
    fr = fr_base + (2 if f["has_thanks"] else 0)
    friendliness = _clip(fr)

    # Specificity (numbers, domain terms, capitalized chunks)
    spec = 0
    spec += 2 if f["has_numbers"] else 0
    spec += 2 if f["has_domain_terms"] else 0
    spec += min(6, f["caps_chunks"])
    specificity = _clip(spec)

    return {
        "confidence": confidence,
        "engagement": engagement,
        "friendliness": friendliness,
        "specificity": specificity,
    }
