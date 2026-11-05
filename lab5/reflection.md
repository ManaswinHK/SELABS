# Lab 5: Reflection

## 1. Which issues were easiest and hardest to fix?

The easiest were the style issues: the unused import, the final newline, `is None`, long lines, the rename to `add_grade` and the docstrings. Each is a small local change that cannot really break anything.

The hardest was `eval`. Removing it meant changing the function's signature, because the caller was passing code as a string. I had to work out what the string was doing (dividing the average by 20) and replace it with a number while keeping the same GPA of 4.35. The unused `grace_marks` was also hard because it needed a decision, not just a cleanup. Deleting it would have satisfied the tools, but the value was clearly meant to be part of the pass check, so I applied it.

## 2. Did the tools report any false positives, or miss anything?

There were no clear false positives, but some findings depend on context. Bandit's B105 only fired because the variable name contained "token", so a secret stored under an ordinary name might not be caught. B324 on MD5 matters less if the hash is only used as a label and not for security, although SHA-256 costs nothing here.

The tools missed quite a lot. None of them noticed that the token was printed to the console, which I only saw by running the program. They also did not report marks above 100, negative attendance, the divide-by-zero for a student with no marks, or `main()` running on import. A perfect Pylint score therefore does not mean the code is correct. The tools check how code is written, not what it should do.

## 3. How would I integrate static analysis into my workflow?

I would run Flake8 and Pylint in the editor or in a pre-commit hook so problems are caught before a commit. In CI I would run all three tools on every pull request, fail the build on any Bandit High or Medium finding, and set a minimum Pylint score. Any rule that gets disabled should have a written reason. Static analysis would sit alongside unit tests and code review, because the logic bugs here needed a person to find them.

## 4. What improvements did I see in code quality, security and readability?

- **Security:** Bandit went from 6 issues to 0. The code no longer runs arbitrary strings or shell commands, and the token is out of the code and the output.
- **Quality:** Pylint went from 5.51 to 10.00. Failures are now returned instead of hidden, and the shared mutable default is gone. The file is also closed safely.
- **Readability:** Flake8 went from 8 issues to 0. Names are consistent, every function has a docstring, and the average calculation now lives in one helper instead of being repeated.
