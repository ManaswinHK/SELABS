# Lab 7: Fuzzing for Input Validation Bugs - Salon Booking

**Name:** H K Manaswin  **SRN:** PES1UG24AM108

Using Hypothesis to fuzz a salon booking module that parses bookings, averages service durations and works out the payable bill after a discount, then fixing the input validation bugs it finds.

Assigned repo: [SETAPESU26/L6_L7_42_salon_booking](https://github.com/SETAPESU26/L6_L7_42_salon_booking) (`Lab 7` folder). In this repo the handout's `processor.py` is `salon_booking.py` and `test_processor.py` is `test_salon_booking.py`.

## Contents

```
lab7/
├── salon_booking.py        # deliverable: fixed application script
├── test_salon_booking.py   # deliverable: completed Hypothesis tests
├── screenshots/
│   ├── step2_buggy_app_run.png     # python salon_booking.py (original)
│   ├── step4_tests_failing.png     # pytest test_salon_booking.py (original): 8 failed, 2 passed
│   ├── step5_fixed_app_run.png     # python salon_booking.py (fixed)
│   └── step6_tests_passing.png     # pytest test_salon_booking.py (fixed): 10 passed
├── Lab7_FuzzTesting_Report_PES1UG24AM108.pdf   # deliverable: PDF with the screenshots
└── README.md
```

The original buggy script is in commit "Lab 7: add original salon_booking and Hypothesis fuzz tests".

## Bugs found and fixed

| Function | Example input | Bug | Fix |
|----------|---------------|-----|-----|
| `parse_booking` | `None`, `''`, `':'`, `'a:b:c'` | Crash (AttributeError, unpack ValueError, `float('')`) | Type check, exactly one `:`, safe number parsing, return `None` |
| `parse_booking` | `'spa:nan'`, `'a:-30'`, `':45'` | nan, negative/zero minutes and empty service accepted | Non-empty service and finite `0 < minutes <= 1440` |
| `duration_average` | `None`, `''`, `'1,,3'` | Crash on `int('')` and on `None` | Every item must be a whole number, else `None` |
| `duration_average` | `'1,2'` gives `1` | Floor division (`//`) cut off the average; zero/negative durations accepted | True mean (`/`) to 2 places; each value 1..1440 |
| `payable_bill` | `None`, `''`, `'1\|2\|3'` | Unpack and `float` crashes | Type check, exactly one `\|`, safe number parsing |
| `payable_bill` | `'NAN\|0'`, `'inf\|inf'`, `'1e308\|0'` | nan/inf got through `max(total, 0)`; overflow | Reject non-finite parts and totals |
| `payable_bill` | `'0.00\|-0.01'` | Negative discount raised the bill | Reject negative bill or discount |

Invalid input now returns `None`, and `main()` prints `Invalid input` instead of crashing.

## Tests

For each function, `test_salon_booking.py` has:

- a no-crash test on `st.text() | st.none()`, plus text biased towards `:`, `|`, `,`, signs, digits and `nan`/`inf`
- an output check: the result is `None`, or finite and in range
- correctness checks on valid generated input: parsing round-trips, the average is the true mean, and the bill is `max(bill * 1.18 - discount, 0)`

Each test runs 300 examples.

## How to run

```bash
pip install hypothesis pytest
python salon_booking.py
pytest test_salon_booking.py
```
