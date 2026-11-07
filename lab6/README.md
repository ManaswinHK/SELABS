# Lab 6: Code and Branch Coverage Analysis - Salon Booking

**Name:** H K Manaswin  **SRN:** PES1UG24AM108

Measuring and improving line and branch coverage of a salon booking module with `coverage` and `pytest`. The module works out extra-time charges by service, stylist level and membership, checks whether a booking can be made and reports client arrival status.

Assigned repo: [SETAPESU26/L6_L7_42_salon_booking](https://github.com/SETAPESU26/L6_L7_42_salon_booking) (`Lab 6` folder).

## Contents

```
lab6/
├── salon_booking.py                      # module under test (unchanged)
├── test_salon_booking.py                 # starter test file from the assigned repo
├── CodeCoverageTest_salon_booking.py     # deliverable: test cases for code coverage
├── BranchCoverageTest_salon_booking.py   # deliverable: test cases for branch coverage
├── screenshots/                          # deliverable: terminal output screenshots
│   ├── code_coverage_test_line_report.png
│   ├── code_coverage_test_branch_report.png
│   ├── branch_coverage_test_line_report.png
│   └── branch_coverage_test_branch_report.png
├── Lab6_Coverage_Report_PES1UG24AM108.pdf  # all screenshots with a short write-up
└── README.md
```

## Results (coverage of `salon_booking.py`)

| Test file | Tests | Line coverage | Branch coverage |
|-----------|-------|---------------|-----------------|
| `test_salon_booking.py` (starter) | 2 | 38% | 32% |
| `CodeCoverageTest_salon_booking.py` | 12 | 100% | 98% (missed `21->23`) |
| `BranchCoverageTest_salon_booking.py` | 24 | 100% | 100% (26/26 branches) |

The code coverage tests run every line but never give a long overrun (more than 60 extra minutes) to a non-senior stylist, so the senior check on line 21 is never False. The branch coverage tests take every `if`/`elif`/`else` both ways and add boundary values: duration 0, extra time of exactly 0 and 60 minutes, walk-in parties of 2 and 3, a party of 4 with 2 and 3 services, and each arrival cutoff at `cutoff`, `cutoff-1`, `cutoff-15` and `cutoff-16` for every colour/weekend combination.

## Commits

| Commit | What it adds |
|--------|--------------|
| Lab 6: add code coverage test cases (100% line coverage) | `CodeCoverageTest_salon_booking.py` and its screenshots |
| Lab 6: add branch coverage test cases (100% branch coverage) | `BranchCoverageTest_salon_booking.py` and its screenshots |

## How to run

```bash
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_salon_booking.py
coverage report -m
coverage run --branch -m pytest BranchCoverageTest_salon_booking.py
coverage report -m
```
