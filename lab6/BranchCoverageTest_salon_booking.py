"""Lab 6 - Branch coverage tests for salon_booking.py.

Goal: make every decision (if / elif / else) evaluate to both True and False,
including boundary values on each comparison.
Run:
    coverage run --branch -m pytest BranchCoverageTest_salon_booking.py
    coverage report -m
"""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------------- extra_time_charge ----------------
# Decisions:
#   D1 service not in INCLUDED_MIN     D2 duration_min < 0
#   D3 is_member and service != "spa"  D4 extra <= 0
#   D5 stylist_level == "junior"       D6 extra > 60
#   D7 stylist_level == "senior" (inside D6)

def test_d1_true_unknown_service():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("manicure", 30, "junior", False)


def test_d2_true_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -1, "junior", False)


def test_d2_false_zero_duration_boundary():
    # 0 is the smallest valid duration
    assert extra_time_charge("haircut", 0, "junior", False) == 0


def test_d3_true_member_non_spa_gets_bonus():
    # haircut 30 + 15 = 45 included -> 45 min used is free
    assert extra_time_charge("haircut", 45, "junior", True) == 0
    # one minute more is charged
    assert extra_time_charge("haircut", 46, "junior", True) == 10


def test_d3_false_member_spa_no_bonus():
    # spa members get no bonus: 100 - 90 = 10 extra at junior rate
    assert extra_time_charge("spa", 100, "junior", True) == 100


def test_d3_false_non_member():
    assert extra_time_charge("colour", 70, "junior", False) == 100


def test_d4_true_exactly_included_boundary():
    assert extra_time_charge("colour", 60, "senior", False) == 0


def test_d4_false_one_minute_over():
    assert extra_time_charge("colour", 61, "senior", False) == 18


@pytest.mark.parametrize("level, expected", [
    ("junior", 20 * 10),   # D5 true
    ("regular", 20 * 18),  # D5 false
    ("senior", 20 * 18),   # D5 false, D6 false so no senior surcharge
])
def test_d5_rate_by_level_short_overrun(level, expected):
    assert extra_time_charge("haircut", 50, level, False) == expected


def test_d6_false_exactly_60_extra_boundary():
    # extra == 60 is NOT > 60, base rate only
    assert extra_time_charge("haircut", 90, "junior", False) == 60 * 10


def test_d6_true_d7_false_junior_long_overrun():
    # extra 61, junior rate 10 + 8
    assert extra_time_charge("haircut", 91, "junior", False) == 61 * 18


def test_d6_true_d7_false_regular_long_overrun():
    # extra 61, regular rate 18 + 8, no senior surcharge (branch 21->23)
    assert extra_time_charge("haircut", 91, "regular", False) == 61 * 26


def test_d6_true_d7_true_senior_long_overrun():
    # extra 110, senior rate 18 + 8 + 4
    assert extra_time_charge("spa", 200, "senior", False) == 110 * 30


# ---------------- can_book ----------------
# Decisions: E1 is_walk_in, E2 party_size > 4, E3 services <= 2

@pytest.mark.parametrize("party, expected", [(2, True), (3, False)])
def test_e1_true_walk_in_party_limit(party, expected):
    assert can_book(party, 5, True) is expected


def test_e2_true_party_over_four():
    assert can_book(5, 1, False) is False


@pytest.mark.parametrize("services, expected", [(2, True), (3, False)])
def test_e2_false_e3_service_limit(services, expected):
    # party of 4 is the largest allowed booking
    assert can_book(4, services, False) is expected


# ---------------- arrival_status ----------------
# Decisions: F1 is_colour, F2 is_weekend,
#            F3 minutes_early >= cutoff, F4 minutes_early >= cutoff - 15

@pytest.mark.parametrize("is_colour, is_weekend, cutoff", [
    (False, False, 5),
    (False, True, 15),
    (True, False, 10),
    (True, True, 20),
])
def test_f1_f2_cutoff_combinations(is_colour, is_weekend, cutoff):
    # F3 true at the boundary
    assert arrival_status(cutoff, is_colour, is_weekend) == "open"
    # F3 false, F4 true just below cutoff
    assert arrival_status(cutoff - 1, is_colour, is_weekend) == "late"
    # F4 true at the lower boundary of the late window
    assert arrival_status(cutoff - 15, is_colour, is_weekend) == "late"
    # F4 false just outside the late window
    assert arrival_status(cutoff - 16, is_colour, is_weekend) == "closed"
