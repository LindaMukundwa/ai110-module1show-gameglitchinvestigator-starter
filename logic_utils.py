#FIX: Refactored core game rules into logic_utils.py using Copilot Agent mode so app.py stays focused on Streamlit UI/state.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def get_attempt_limit_for_difficulty(difficulty: str):
    #FIX: Easy now has more attempts than Normal to match expected difficulty progression.
    """Return max attempts allowed for a given difficulty."""
    if difficulty == "Easy":
        return 10
    if difficulty == "Normal":
        return 7
    if difficulty == "Hard":
        return 5
    return 7


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    #FIX: Standardized guess parsing to prevent invalid/blank inputs from breaking gameplay flow.
    if raw is None:
        return False, None, "Enter a guess."

    cleaned = raw.strip()
    if cleaned == "":
        return False, None, "Enter a guess."

    try:
        value = int(cleaned)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    #FIX: Corrected comparison outcomes so higher/lower hints are accurate and deterministic.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str):
    #FIX: Centralized hint messaging in one function to avoid inverted hint text in the UI layer.
    """Return a display message for a game outcome."""
    message_map = {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }
    return message_map.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
