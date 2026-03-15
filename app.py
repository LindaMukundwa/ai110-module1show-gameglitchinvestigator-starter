import random
import streamlit as st
#FIX: app.py now consumes reusable logic helpers instead of embedding game rules directly.
from logic_utils import (
    check_guess,
    get_attempt_limit_for_difficulty,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.markdown(
    """
    <style>
    .stApp {
        background: #020024;
        background: linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 35%, rgba(0, 212, 255, 1) 100%);
    }
    [data-testid="stSidebar"] {
        background: #020024;
        background: linear-gradient(90deg, rgba(2, 0, 36, 1) 0%, rgba(9, 9, 121, 1) 35%, rgba(0, 212, 255, 1) 100%);
    }
    .hint-card {
        border: 1px solid #f6b3d2;
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        background: #fff9fd;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .summary-title {
        color: #ad1457;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = get_attempt_limit_for_difficulty(difficulty)

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    #FIX: Start attempts at 0 so players do not lose a turn before their first guess.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "feedback_history" not in st.session_state:
    st.session_state.feedback_history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    #FIX: Reset all game state on New Game so the app never appears stuck after win/loss.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.feedback_history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        message = get_hint_message(outcome)

        distance = abs(st.session_state.secret - guess_int)
        if distance == 0:
            temp_text = "🎯 Perfect hit"
        elif distance <= 2:
            temp_text = "🔥 Very hot"
        elif distance <= 5:
            temp_text = "🌡️ Warm"
        elif distance <= 10:
            temp_text = "🧊 Cool"
        else:
            temp_text = "❄️ Cold"

        st.session_state.feedback_history.append(
            {
                "Attempt": st.session_state.attempts,
                "Guess": guess_int,
                "Outcome": outcome,
                "Heat": temp_text,
            }
        )

        if show_hint:
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(message)
            else:
                st.info(message)
            st.markdown(
                f"<div class='hint-card'><strong>Temperature:</strong> {temp_text}</div>",
                unsafe_allow_html=True,
            )

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.markdown("<div class='summary-title'>📊 Session Summary</div>", unsafe_allow_html=True)
summary_data = [
    {
        "Difficulty": difficulty,
        "Range": f"{low} - {high}",
        "Attempts Used": st.session_state.attempts,
        "Attempts Allowed": attempt_limit,
        "Score": st.session_state.score,
        "Status": st.session_state.status,
    }
]
st.table(summary_data)

if st.session_state.feedback_history:
    st.caption("Recent guess feedback")
    st.table(st.session_state.feedback_history[-5:])

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
