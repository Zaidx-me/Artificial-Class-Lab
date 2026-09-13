# vscode-cline — Manual Benchmark Results (fill this in)

| Task_Time_Min | Attempts_to_Pass | Pytest_Result | Files_Created | Manual_Interventions | AI_Accuracy_1_10 | Code_Quality_1_10 | Features_Pct |
|---|---|---|---|---|---|---|---|
| 3.5 | 1 | PASS | grades.py students.txt test_grades.py | 0 | 10 | 9 | 100 |

## Notes
- Single-pass implementation: Cline read `TASK.md` and produced `grades.py`, `students.txt`,
  and `test_grades.py` in one go, no clarifying questions or re-prompts needed.
- `python3 grades.py` output matched the expected table/format in `TASK.md` exactly
  (values, rounding to 2 decimals, column alignment, class stats section).
- `pytest test_grades.py -v` passed all 3 tests on the first run — no fixes required.
- Invalid/malformed lines are skipped with a printed warning (`load_students` +
  `parse_line`), satisfying the graceful-handling requirement.
- Code quality: dataclass-based `Student` model, type hints throughout, docstrings,
  clear separation of parsing/computation/printing concerns, no PEP 8 issues observed.
- Minor deduction on code quality only because there's no `argparse`/CLI-arg handling
  for a custom input filename (defaults to `students.txt`, but `main()` accepts an
  optional `filename` parameter for reuse/testing).

## How to run
See `../MANUAL-BENCHMARK-GUIDE.md`. Open this folder as the project, read `TASK.md`,
prompt: "Read TASK.md and implement it.", time from prompt to passing pytest.
