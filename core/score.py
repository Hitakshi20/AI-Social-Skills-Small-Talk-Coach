def _clip(x, lo=0, hi=10): return max(lo, min(hi, x))

def score_response(f):
    # Confidence
    conf = 0
    conf += 6 if f["tokens"] >= 18 else (3 if f["tokens"] >= 10 else 1)
    conf += 2 if f["sentences"] >= 2 else 0
    conf -= max(0, (f["fillers"] - 1)) * 2
    conf -= 2 if f["ends_trail"] else 0
    confidence = _clip(conf)

    # Engagement
    eng = 0
    eng += 4 if f["has_question"] else 0
    eng += 2 if f["sentences"] >= 2 else 0
    eng -= 2 if f["tokens"] < 8 else 0
    engagement = _clip(eng)

    # Friendliness (VADER -1..1 -> 0..8)
    fr = int((f["sentiment"] + 1) * 4)  # 0..8
    fr += 2 if f["has_thanks"] else 0
    friendliness = _clip(fr)

    # Specificity
    spec = 0
    spec += min(4, f["entities"])
    spec += 2 if f["has_numbers"] else 0
    spec += 2 if f["has_domain_terms"] else 0
    specificity = _clip(spec)

    return {
        "confidence": confidence,
        "engagement": engagement,
        "friendliness": friendliness,
        "specificity": specificity
    }
