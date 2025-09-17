import json
from pathlib import Path
import streamlit as st
import yaml
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.analyzer import analyze_text
from core.scorer import score_response
from core.tips import tip_from_scores

st.set_page_config(page_title="ConvoCoach", page_icon="🤝", layout="wide")

# --- Load scenario ---
SCENARIO_PATH = Path("knowledge/scenarios/recruiter.yaml")
scenario = yaml.safe_load(SCENARIO_PATH.read_text(encoding="utf-8"))

st.title("🤝 ConvoCoach (MVP)")
st.caption("Practice networking & workplace small talk. MVP build in progress.")

# Session state
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "log" not in st.session_state:
    st.session_state.log = []  # list of dicts: {bot, user, scores}

bot_turns = [d for d in scenario["dialogue"] if "bot" in d]

# Left: chat
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.subheader(scenario["scenario"])
    # Render previous turns
    for turn in st.session_state.log:
        st.markdown(f"**Recruiter:** {turn['bot']}")
        st.markdown(f"**You:** {turn['user']}")
        st.markdown(
            f"Scores → Confidence: {turn['scores']['confidence']}/10 | "
            f"Engagement: {turn['scores']['engagement']}/10 | "
            f"Friendliness: {turn['scores']['friendliness']}/10 | "
            f"Specificity: {turn['scores']['specificity']}/10"
        )
        st.markdown(f"_Tip:_ {turn['tip']}")
        st.divider()

    # Current prompt
    if st.session_state.turn < len(bot_turns):
        current_bot = bot_turns[st.session_state.turn]["bot"]
        st.markdown(f"**Recruiter:** {current_bot}")
        user_input = st.text_area("Your reply", key=f"reply_{st.session_state.turn}", height=100)

        if st.button("Submit reply"):
            feats = analyze_text(user_input)
            scores = score_response(feats)
            tip = tip_from_scores(scores)
            st.session_state.log.append({
                "bot": current_bot,
                "user": user_input,
                "scores": scores,
                "tip": tip
            })
            st.session_state.turn += 1
            st.rerun()
    else:
        st.success("End of scenario. Nice work! 🎉")
        st.write(scenario.get("end_note", ""))

with col2:
    st.subheader("Session Summary")
    if st.session_state.log:
        # Simple averages
        avg = {"confidence":0,"engagement":0,"friendliness":0,"specificity":0}
        for t in st.session_state.log:
            for k in avg:
                avg[k] += t["scores"][k]
        for k in avg:
            avg[k] = round(avg[k] / len(st.session_state.log), 1)
        st.metric("Confidence", avg["confidence"])
        st.metric("Engagement", avg["engagement"])
        st.metric("Friendliness", avg["friendliness"])
        st.metric("Specificity", avg["specificity"])

    # Reset / Save
    if st.button("Restart scenario"):
        st.session_state.turn = 0
        st.session_state.log = []
        st.rerun()

    if st.button("Save session"):
        Path("data").mkdir(exist_ok=True, parents=True)
        out = Path("data/sessions.json")
        previous = []
        if out.exists():
            previous = json.loads(out.read_text(encoding="utf-8"))
        previous.append(st.session_state.log)
        out.write_text(json.dumps(previous, ensure_ascii=False, indent=2), encoding="utf-8")
        st.toast("Saved to data/sessions.json")
