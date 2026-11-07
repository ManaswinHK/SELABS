"""Salon booking helpers, hardened after Hypothesis fuzz testing (Lab 7).

Every function returns None for invalid input instead of raising.

Bugs found by fuzzing and fixed:
  parse_booking    - crashed on None, missing ':' or extra ':' (unpack error),
                     non-numeric minutes; accepted "nan"/"inf", zero/negative
                     minutes and an empty service name.
  duration_average - crashed on None, "" and non-integer items ("1,,3");
                     used floor division (30,45 -> 37 instead of 37.5);
                     accepted zero/negative durations.
  payable_bill     - crashed on None, missing/extra '|', non-numeric parts;
                     "nan" / "inf" leaked through max() as nan/inf;
                     negative bill or negative discount accepted (a negative
                     discount silently increased the bill); overflow to inf.
"""
import math

MAX_MINUTES = 1440   # a booking cannot last longer than a day
GST_RATE = 1.18


def _to_finite_float(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def parse_booking(text):
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    service, minutes = text.split(':')
    service = service.strip()
    minutes = _to_finite_float(minutes)
    if not service or minutes is None or not 0 < minutes <= MAX_MINUTES:
        return None
    return service.title(), minutes


def duration_average(durations_csv):
    if not isinstance(durations_csv, str):
        return None
    values = []
    for item in durations_csv.split(','):
        item = item.strip()
        if not item.isdecimal() or len(item) > 4:
            return None
        value = int(item)
        if not 0 < value <= MAX_MINUTES:
            return None
        values.append(value)
    return round(sum(values) / len(values), 2)


def payable_bill(text):
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    bill, discount = (_to_finite_float(part) for part in text.split('|'))
    if bill is None or discount is None or bill < 0 or discount < 0:
        return None
    total = bill * GST_RATE - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0.0), 2)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result if result is not None else "Invalid input")

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result if result is not None else "Invalid input")

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
