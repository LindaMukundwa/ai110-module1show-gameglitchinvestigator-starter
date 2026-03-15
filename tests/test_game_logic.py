from logic_utils import (
    check_guess,
    get_attempt_limit_for_difficulty,
    get_hint_message,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

def test_winning_guess():
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_parse_guess_none_is_invalid():
    ok, guess, err = parse_guess(None)
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_guess_blank_string_is_invalid():
    ok, guess, err = parse_guess("   ")
    assert ok is False
    assert guess is None
    assert err == "Enter a guess."


def test_parse_guess_non_numeric_is_invalid():
    ok, guess, err = parse_guess("abc")
    assert ok is False
    assert guess is None
    assert err == "That is not a number."


def test_parse_guess_integer_is_valid():
    ok, guess, err = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert err is None


def test_get_range_for_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_get_range_for_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_get_range_for_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_get_attempt_limit_for_easy():
    assert get_attempt_limit_for_difficulty("Easy") == 10


def test_get_attempt_limit_for_normal():
    assert get_attempt_limit_for_difficulty("Normal") == 7


def test_get_attempt_limit_for_hard():
    assert get_attempt_limit_for_difficulty("Hard") == 5


def test_get_hint_message_for_too_high():
    assert get_hint_message("Too High") == "📉 Go LOWER!"


def test_get_hint_message_for_too_low():
    assert get_hint_message("Too Low") == "📈 Go HIGHER!"


def test_update_score_win_early_attempt_awards_more_points():
    result = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert result == 80


def test_update_score_win_has_minimum_points_floor():
    result = update_score(current_score=0, outcome="Win", attempt_number=99)
    assert result == 10


def test_update_score_too_high_even_attempt_adds_points():
    result = update_score(current_score=10, outcome="Too High", attempt_number=2)
    assert result == 15


def test_update_score_too_high_odd_attempt_subtracts_points():
    result = update_score(current_score=10, outcome="Too High", attempt_number=3)
    assert result == 5


def test_update_score_too_low_subtracts_points():
    result = update_score(current_score=10, outcome="Too Low", attempt_number=2)
    assert result == 5
