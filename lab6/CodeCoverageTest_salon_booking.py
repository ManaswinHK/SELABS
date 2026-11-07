"""Lab 6 - Code (line) coverage tests for salon_booking.py.

Goal: execute every statement of salon_booking.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_salon_booking.py
    coverage report -m
"""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------------- extra_time_charge ----------------

def test_within_included_time():
    # haircut includes 30 min, 20 min used -> no charge (covers `return 0`)
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_unknown_service_raises():
    with pytest.raises(ValueError, match="unknown service"):
        extra_time_charge("manicure", 30, "junior", False)


def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        extra_time_charge("haircut", -5, "junior", False)


def test_junior_rate_short_overrun():
    # 50 - 30 = 20 extra min at junior rate 10
    assert extra_time_charge("haircut", 50, "junior", False) == 200


def test_member_gets_bonus_minutes_regular_rate():
    # colour 60 + 15 member bonus = 75 included, 100 - 75 = 25 extra at rate 18
    assert extra_time_charge("colour", 100, "regular", True) == 450


def test_senior_long_overrun_surcharge():
    # spa 90 included, 200 - 90 = 110 extra, rate 18 + 8 + 4 = 30
    assert extra_time_charge("spa", 200, "senior", False) == 3300


# ---------------- can_book ----------------

def test_can_book():
    assert can_book(2, 1, False) is True


def test_walk_in_small_party():
    assert can_book(1, 1, True) is True


def test_large_party_rejected():
    assert can_book(5, 1, False) is False


# ---------------- arrival_status ----------------

def test_colour_weekend_open():
    # cutoff = 10 + 10 = 20
    assert arrival_status(20, True, True) == "open"


def test_regular_weekday_late():
    # cutoff = 5, late window is >= -10
    assert arrival_status(0, False, False) == "late"


def test_regular_weekday_closed():
    assert arrival_status(-20, False, False) == "closed"
