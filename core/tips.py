from typing import Dict

def tip_from_scores(s: Dict[str, int]) -> str:
    lowest = min(s, key=lambda k: s[k])

    if lowest == "confidence":
        return "Add one more sentence and remove a filler word. Start with a clear headline about yourself."
    if lowest == "engagement":
        return "Ask a follow-up question to keep the chat going (e.g., 'What projects does your team enjoy most?')."
    if lowest == "friendliness":
        return "Add a warm marker like 'Thanks for asking' or 'I appreciate your time'."
    if lowest == "specificity":
        return "Include one concrete detail: a project name, tool, number, or outcome."
    return "Nice balance—end with a friendly follow-up question."
