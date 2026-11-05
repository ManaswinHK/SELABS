# Lab 5: Issues Found and Fixed

File: `student_grade_system.py`. Line numbers refer to the original file.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.51/10 | 10.00/10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 8 issues | 0 issues |

Reports are in `reports/before/` and `reports/after/`.

## Issues reported by the tools

Highest severity first. Some issues were reported by more than one tool, so they have one row each.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from input | Security, High (Bandit B605) | 60 | `os.system("echo ... " + filename)` passes `filename` to a shell, so a crafted filename runs commands. | Removed the shell call and used `print()`. |
| Weak hash | Security, High (Bandit B324) | 49 | MD5 is broken and should not be used for identifiers that need to be trusted. | Switched to `hashlib.sha256`. |
| Use of `eval` | Security, Medium (Bandit B307, Pylint W0123) | 44 | `eval(gpa_expr)` runs any Python string given by the caller. | Replaced the string with a numeric `scale_divisor=20.0` parameter. The GPA result is unchanged. |
| Insecure random PIN | Security, Low (Bandit B311) | 53 | `random` is predictable, so PINs could be guessed. | Used `1000 + secrets.randbelow(9000)`, which keeps the same range. |
| Hardcoded token | Security, Low (Bandit B105) | 64 | The portal token was stored in the source code. | Read it from the `GRADE_PORTAL_TOKEN` environment variable. |
| Swallowed errors | Bug, Low (Bandit B110, Pylint W0702, Flake8 E722) | 26-27 | A bare `except: pass` hid every error, so a failed update looked like a success. | Check the student exists and return `True` or `False`. |
| Mutable default argument | Bug (Pylint W0102) | 15 | `grade_list=[]` is one list shared across all calls. | Default to `None` and create the list inside the function. |
| Unused `grace_marks` | Bug (Pylint W0612, Flake8 F841) | 31 | Grace marks were defined but never used in the pass check. | Applied them: `avg + grace_marks >= pass_threshold`. |
| File not safely closed | Bug (Pylint R1732, W1514) | 57-59 | If `write` fails the file stays open, and the encoding depends on the platform. | Used `with open(..., encoding="utf-8")`. |
| Comparison to `None` | Style (Pylint C0121, Flake8 E711) | 32 | `== None` should be `is None`. | Used `is None`, later moved into `average_mark`. |
| Unused import | Style (Pylint W0611, Flake8 F401) | 6 | `json` was never used. | Removed the import. |
| Unused variable | Style (Pylint W0612, Flake8 F841) | 43 | `avg_score` was only used inside the `eval` string. | Now used directly after removing `eval`. |
| Function naming | Style (Pylint C0103) | 15 | `addGrade` is not snake_case. | Renamed to `add_grade` and updated the caller. |
| Missing docstrings | Style (Pylint C0116) | 15, 23, 30, 41, 48, 52, 56, 63 | Functions had no docstrings. | Added a one-line docstring to each function. |
| Old string formatting | Style (Pylint C0209) | 19 | `%` formatting used where an f-string is clearer. | Used an f-string. This also stopped `%d` cutting 85.5 down to 85 in the log. |
| Redundant if/else | Style (Pylint R1703, R1705) | 35-38 | `if x: return True else: return False`. | Return the condition directly. |
| Long lines | Style (Flake8 E501) | 19, 34 | Lines over 79 characters. | Wrapped or shortened them. |
| No final newline | Style (Pylint C0304, Flake8 W292) | 75 | The file did not end with a newline. | Added one. |

## Issues no tool reported

Found by reading the code and the program output.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Token printed to the console | Security | 72 | The program printed the secret token in plain text. Bandit flagged the assignment but not this leak. | Print only whether a token is set (`True` or `False`). |
| `main()` runs on import | Bug | 75 | Importing the module ran the demo and wrote a file. | Added an `if __name__ == "__main__":` guard. |
| No upper limit on marks | Bug | 16 | Only `mark < 0` was rejected, so a mark of 150 was accepted. | Require `0 <= mark <= 100`. |
| Negative attendance | Bug | 25 | A negative `present_days` reduced attendance. | Reject negative values. |
| Crash with no marks | Bug | 34, 43 | Dividing by `len(marks)` raises `ZeroDivisionError` for a student with no marks. | Added `average_mark`, which returns `None`. Callers handle that case. |
| Crash on unknown student | Bug | 42 | `compute_weighted_gpa` raised `KeyError`. | Return `None`, handled through `average_mark`. |

## Known limitations

These were left alone because the correct behaviour is not defined by the program.

- `attendance` looks like a percentage, but `record_attendance` adds days to it, so it can go above 100.
- `compute_weighted_gpa` is a plain average with no weights, despite its name.
- `add_grade` discards its log unless the caller passes in a list.
- The old token is still in the git history, so a real system would need to replace it.
