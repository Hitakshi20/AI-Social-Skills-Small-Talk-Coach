def tip_from_scores(s):
    # Pick the lowest score dimension and suggest a concrete action
    dims = sorted(s.items(), key=lambda kv: kv[1])
    lowest, val = dims[0]
    if lowest == "confidence":
        return "Add one more sentence and remove a filler word. Try starting with a clear headline about yourself."
    if lowest == "engagement":
        return "Ask one follow-up question to keep the conversation going (e.g., 'What projects does your team enjoy most?')."
    if lowest == "friendliness":
        return "Add a warm tone marker like 'Thanks for asking' or 'I appreciate your time'."
    if lowest == "specificity":
        return "Include one concrete detail: a project name, tool, number, or outcome."
    return "Nice balance! Keep answers specific and end with a friendly follow-up question."
