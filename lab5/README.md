# Lab 5: Static Code Analysis - Student Grade System

**Name:** H K Manaswin  **SRN:** PES1UG24AM108

Finding and fixing quality, style and security problems in a student grade manager using Pylint, Flake8 and Bandit. The program logs scores, tracks attendance, computes GPAs, checks passing status and exports a grade sheet.

Assigned repo: [SETAPESU26/L5_42_student_grade_system](https://github.com/SETAPESU26/L5_42_student_grade_system). The commits are on the [`lab5-PES1UG24AM108` branch of my fork](https://github.com/ManaswinHK/L5_42_student_grade_system/tree/lab5-PES1UG24AM108).

## Contents

```
lab5/
├── code/
│   └── student_grade_system.py   # cleaned version
├── reports/
│   ├── before/                   # reports for the original file
│   │   ├── pylint_report.txt
│   │   ├── bandit_report.txt
│   │   └── flake8_report.txt
│   └── after/                    # reports for the final file
│       ├── pylint_report.txt
│       ├── bandit_report.txt
│       └── flake8_report.txt
├── issues.md                     # issue table
├── reflection.md                 # reflection answers
└── README.md
```

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.51/10 | 10.00/10 |
| Bandit | 6 issues (2 High, 1 Medium, 3 Low) | 0 issues |
| Flake8 | 8 issues | 0 issues |

`reports/after/flake8_report.txt` is empty because Flake8 prints nothing when there are no issues.

## Fixes (one commit each)

| Commit | What changed |
|--------|--------------|
| Bandit | Replaced MD5 with SHA-256, removed the `os.system` shell call and `eval`, generated the PIN with `secrets`, moved the token to an environment variable and replaced `try/except/pass` with an explicit check. |
| Flake8 | Removed the unused import, wrapped long lines, used `is None`, applied the unused `grace_marks` and added the final newline. |
| Pylint | Fixed the mutable default argument, renamed `addGrade` to `add_grade`, added docstrings, used an f-string, simplified the pass check and opened the file with `with` and an encoding. |
| Logic bugs | Fixes for problems no tool reported: added a `__main__` guard, rejected marks above 100 and negative attendance, and handled students with no marks and unknown students. |

## How to run

Requires Python 3.10+.

```bash
cd code
python student_grade_system.py
```

Set `GRADE_PORTAL_TOKEN` in the environment to make the portal token line show `True`.

To rerun the analysis:

```bash
pip install pylint bandit flake8
pylint student_grade_system.py
bandit -r student_grade_system.py
flake8 student_grade_system.py
```
