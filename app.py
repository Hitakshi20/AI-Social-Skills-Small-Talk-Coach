import os, sys, json
from pathlib import Path
from functools import lru_cache
import yaml
import streamlit as st

# ---------- setup ----------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.analyzer import analyze_text
from core.scorer import score_response
from core.tips import tip_from_scores

SCENARIOS_DIR = Path("knowledge/scenarios")
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ---------- page setup ----------
st.set_page_config(page_title="IceBreakr", page_icon="🧊", layout="wide")

# ---------- session state ----------
if "view" not in st.session_state:
    st.session_state.view = "home"
if "scenario_path" not in st.session_state:
    st.session_state.scenario_path = ""
if "scores" not in st.session_state:
    st.session_state.scores = {}

# ---------- CSS ----------
st.markdown("""
<style>
.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 5rem;
}
.hero {
    background: linear-gradient(180deg, #fafaff 0%, #ffffff 100%);
    border: 1px solid #ececf3;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 18px;
    text-align: center;
}
.hero h1 {margin: 0 0 6px 0;}
.hero p {margin: 0; color: #6b7280;}
.preview {color:#6b7280; font-size: 13px;}
.chips {display:flex; gap:8px; flex-wrap:wrap; margin:8px 0 0 0;}
.chip  {font-size:12px; padding:4px 8px; border-radius:999px; background:#f3f4f6; color:#374151;}
/* Buttons */
div.stButton > button {
    background-color: #f5f5f5;
    color: #333;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 0.4em 1em;
    font-size: 0.9em;
    transition: all 0.2s ease;
}
div.stButton > button:hover {
    background-color: #e8e8e8;
}
textarea {
    border-radius: 10px !important;
    background-color: #f8f9fb !important;
    font-size: 0.95em !important;
}
[data-testid="stHorizontalBlock"] {
    align-items: flex-start;
}
</style>
""", unsafe_allow_html=True)

# ---------- helpers ----------
@lru_cache(maxsize=64)
def load_yaml(path_str: str):
    p = Path(path_str)
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def list_scenarios():
    files = sorted(SCENARIOS_DIR.glob("*.yaml"))
    items = []
    for p in files:
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
            title = data.get("scenario", p.stem.replace("_", " ").title())
        except Exception:
            title = p.stem
        items.append((title, str(p)))
    return items

def reset_session_for_new_scenario(path_str: str):
    st.session_state.scenario_path = path_str
    st.session_state.turn = 0
    st.session_state.log = []
    st.session_state.scores = {}
# --- action helpers (put near list_scenarios/reset_session_for_new_scenario) ---

def start_selected_scenario(path_str: str):
    """Initialize state for a selected scenario and show first bot turn."""
    reset_session_for_new_scenario(path_str)
    scenario = load_yaml(path_str)
    dialogue = scenario.get("dialogue", [])
    first_bot = dialogue[0]["bot"] if dialogue else "Hi there!"
    st.session_state.bot_message = first_bot
    st.session_state.scenario_title = scenario.get("scenario", Path(path_str).stem)
    st.session_state.scenario_description = scenario.get("description", "")

def restart_current_scenario():
    """Replay the currently selected scenario from the beginning."""
    path = st.session_state.get("scenario_path")
    if not path:
        return
    start_selected_scenario(path)
    # clear any typed text
    st.session_state.pop("user_reply", None)
    st.session_state.view = "chat"

def handle_user_reply(reply):
    """Handles user message, scoring, and advancing dialogue."""
    scenario = load_yaml(st.session_state.scenario_path)
    dialogue = scenario.get("dialogue", [])
    turn = st.session_state.turn

    # --- scoring ---
    analysis = analyze_text(reply)
    scores = score_response(analysis)
    st.session_state.scores = scores

    # --- next turn ---
    st.session_state.turn += 1
    if st.session_state.turn < len(dialogue):
        st.session_state.bot_message = dialogue[st.session_state.turn].get("bot", "Thanks for your response!")
    else:
        st.session_state.bot_message = "✅ Conversation complete! You can restart or change the scenario."

# ---------- views ----------
def render_home():
    options = list_scenarios()
    if not options:
        st.error("No scenarios found in `knowledge/scenarios/`.")
        st.stop()

    # Hero banner
    st.markdown("""
    <div class="hero">
        <h1>🧊 IceBreakr</h1>
        <p style="font-size:18px; color:#555;">
            Break the ice. Build your confidence.<br>
            Practice real conversations — before they happen.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Choose a scenario")

    # Card container style
    st.markdown("""
        <style>
        .scenario-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 18px;
            background-color: #fff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        }
        .scenario-card:hover {
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: 0.2s ease-in-out;
        }
        .start-btn {
            display: inline-block;
            background-color: #2563eb;
            color: white;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 14px;
            text-decoration: none;
            transition: all 0.2s ease-in-out;
        }
        .start-btn:hover {
            background-color: #1d4ed8;
        }
        </style>
    """, unsafe_allow_html=True)

    for title, path in options:
        data = load_yaml(path) or {}
        desc = data.get("description", "Practice a realistic conversation.")
        preview_lines = [d["bot"] for d in data.get("dialogue", []) if "bot" in d][:2]
        preview = " · ".join([f"“{p}”" for p in preview_lines]) if preview_lines else ""

        # Render scenario card
        st.markdown(f"""
        <div class="scenario-card">
            <div style="font-size:13px; color:#6b7280;">Scenario</div>
            <h3 style="margin-top:4px;">{title}</h3>
            <p style="margin:6px 0 8px 0; color:#444;">{desc}</p>
            <div style="color:#6b7280; font-size:13px; margin-bottom:8px;">
                <b>Preview:</b> {preview}
            </div>
        """, unsafe_allow_html=True)

        # tags (chips)
        chips = []
        low = title.lower()
        if "recruit" in low: chips += ["Recruiting", "Casual"]
        if "coffee" in low: chips += ["Casual"]
        if "new" in low: chips += ["New-Joiner"]
        if "standup" in low: chips += ["Team"]
        if chips:
            st.markdown(
                "<div style='display:flex; gap:6px; margin-bottom:10px;'>"
                + "".join([f"<div style='background:#f3f4f6; color:#374151; font-size:12px; padding:4px 8px; border-radius:999px;'>{c}</div>" for c in chips])
                + "</div>",
                unsafe_allow_html=True,
            )

        # Start button (smaller & aligned right)
        col1, col2, col3 = st.columns([6, 1, 1])
        with col3:
            if st.button("Start", key=f"start_{path}", use_container_width=True):
                start_selected_scenario(path)
                st.session_state.view = "chat"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)



def render_chat():
    # guard: if no scenario, go home
    if not st.session_state.get("scenario_path"):
        st.session_state.view = "home"
        st.rerun()

    scenario = load_yaml(st.session_state.scenario_path)
    dialogue = scenario.get("dialogue", [])
    total_turns = len(dialogue)

    st.markdown("### 💬 Live Conversation")
    st.caption(st.session_state.get("scenario_title", ""))
    st.write(st.session_state.get("scenario_description", ""))

    chat_col, summary_col = st.columns([2.5, 1.2], gap="large")

    # ----- CHAT -----
    with chat_col:
        # Conversation complete?
        done = st.session_state.get("turn", 0) >= total_turns

        st.markdown("#### Recruiter")
        if done:
            st.success("✅ Conversation complete! You can restart or change the scenario.")
        st.markdown(st.session_state.get("bot_message", "Hi there! Let's start chatting."))

        # Clear callback (avoids StreamlitAPIException)
        def _clear_reply():
            st.session_state["user_reply"] = ""

        # Reply input (render AFTER defining callback)
        user_input = st.text_area("Your reply", key="user_reply", placeholder="Type your response…")

        # Actions
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Submit reply", use_container_width=True, disabled=done):
                if not (user_input or "").strip():
                    st.warning("Please type a reply before submitting.")
                else:
                    # score + advance
                    analysis = analyze_text(user_input)
                    st.session_state.scores = score_response(analysis)

                    # advance to next bot line
                    st.session_state.turn += 1
                    if st.session_state.turn < total_turns:
                        st.session_state.bot_message = dialogue[st.session_state.turn]["bot"]
                    else:
                        st.session_state.bot_message = "✅ Conversation complete! You can restart or change the scenario."
                    st.rerun()
        with c2:
            st.button("Clear", use_container_width=True, on_click=_clear_reply)

        # Back to scenarios
        if st.button("⬅ Back to Scenarios"):
            st.session_state.view = "home"
            # optional: clear the input when going back
            st.session_state.pop("user_reply", None)
            st.rerun()

    # ----- SUMMARY -----
    with summary_col:
        st.markdown("### 🧾 Session Summary")
        st.markdown(
            f"""
            <div style="padding: 10px 16px; border: 1px solid #ddd; border-radius: 10px; background-color: #fafafa;">
              <p><b>Confidence:</b> {st.session_state.get('scores', {}).get('confidence', 0)}</p>
              <p><b>Engagement:</b> {st.session_state.get('scores', {}).get('engagement', 0)}</p>
              <p><b>Friendliness:</b> {st.session_state.get('scores', {}).get('friendliness', 0)}</p>
              <p><b>Specificity:</b> {st.session_state.get('scores', {}).get('specificity', 0)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("")
        # Working restart
        st.button("Restart scenario", use_container_width=True, on_click=restart_current_scenario)
        # Removed: Save session

# ---------- router ----------
if st.session_state.view == "home":
    render_home()
else:
    if not st.session_state.scenario_path:
        st.session_state.view = "home"
        st.rerun()
    render_chat()
