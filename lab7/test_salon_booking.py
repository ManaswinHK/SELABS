"""Lab 7 - Hypothesis fuzz tests for salon_booking.py.

Contract checked by these tests (every function):
  * it never raises, whatever it is given (str, None, garbage)
  * invalid input returns None
  * valid input returns a correct, finite, non-negative result

Run:
    python -m pytest test_salon_booking.py
"""
import math

from hypothesis import given, settings, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill

settings.register_profile("lab7", max_examples=300, deadline=None)
settings.load_profile("lab7")

# Text biased towards the characters the parsers care about, so the fuzzer
# hits separators, signs, decimals and special float words ("nan", "inf").
TRICKY = st.text(alphabet="0123456789:|,.-+e naifNAIF\t") | st.sampled_from([
    "", ":", "|", ",", "a:", ":5", "a:b:c", "1,,3", "1|2|3",
    "haircut:nan", "haircut:inf", "haircut:-30", "spa:0",
    "nan|0", "inf|inf", "800|-100", "-800|100", "1e308|0",
    "30,-45", "0,0", "99999999,1",
])
ANY_INPUT = st.text() | st.none() | TRICKY


# ---------------------------------------------------------------- no crash

@given(ANY_INPUT)
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed on {s!r} with: {e!r}"


@given(ANY_INPUT)
def test_duration_average_no_crash(s):
    try:
        duration_average(s)
    except Exception as e:
        assert False, f"duration_average crashed on {s!r} with: {e!r}"


@given(ANY_INPUT)
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed on {s!r} with: {e!r}"


# ------------------------------------------------- output sanity on any input

def _safe(fn, s):
    try:
        return fn(s)
    except Exception:
        return None  # crashes are reported by the no-crash tests above


@given(ANY_INPUT)
def test_parse_booking_output_is_valid(s):
    result = _safe(parse_booking, s)
    if result is not None:
        service, minutes = result
        assert service != "", f"empty service accepted for {s!r}"
        assert math.isfinite(minutes), f"non-finite duration {minutes} for {s!r}"
        assert minutes > 0, f"non-positive duration {minutes} for {s!r}"


@given(ANY_INPUT)
def test_duration_average_output_is_valid(s):
    result = _safe(duration_average, s)
    if result is not None:
        assert math.isfinite(result) and result > 0, f"bad average {result} for {s!r}"


@given(ANY_INPUT)
def test_payable_bill_output_is_valid(s):
    result = _safe(payable_bill, s)
    if result is not None:
        assert math.isfinite(result), f"non-finite bill {result} for {s!r}"
        assert result >= 0, f"negative bill {result} for {s!r}"


# ------------------------------------------------- correctness on valid input

SERVICE = st.text(alphabet=st.characters(categories=["Ll", "Lu"]),
                  min_size=1, max_size=15)
MINUTES = st.integers(min_value=1, max_value=1440)


@given(SERVICE, MINUTES)
def test_parse_booking_valid_roundtrip(service, minutes):
    assert _safe(parse_booking, f"  {service} : {minutes} ") == (service.title(), float(minutes))


@given(st.lists(MINUTES, min_size=1, max_size=20))
def test_duration_average_is_true_mean(durations):
    result = _safe(duration_average, ",".join(map(str, durations)))
    assert result is not None
    assert min(durations) <= result <= max(durations)
    assert math.isclose(result, sum(durations) / len(durations), abs_tol=0.01), \
        f"average of {durations} should be {sum(durations) / len(durations)}, got {result}"


AMOUNT = st.decimals(min_value=0, max_value=100000, places=2)


@given(AMOUNT, AMOUNT)
def test_payable_bill_valid(bill, discount):
    result = _safe(payable_bill, f"{bill}|{discount}")
    expected = max(float(bill) * 1.18 - float(discount), 0)
    assert result is not None
    assert math.isclose(result, expected, abs_tol=0.01)


@given(AMOUNT, st.decimals(min_value="-100000", max_value="-0.01", places=2))
def test_payable_bill_rejects_negative_discount(bill, discount):
    # a negative discount would silently increase the bill
    assert _safe(payable_bill, f"{bill}|{discount}") is None
