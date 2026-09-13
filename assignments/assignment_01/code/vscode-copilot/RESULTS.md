# vscode-copilot — Manual Benchmark Results (fill this in)

| Task_Time_Min | Attempts_to_Pass | Pytest_Result | Files_Created | Manual_Interventions | AI_Accuracy_1_10 | Code_Quality_1_10 | Features_Pct |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 3 passed | 3 | 0 | 10 | 9 | 100% |

## Notes
- Implemented `grades.py`, `students.txt`, and `test_grades.py`.
- `python3 grades.py` runs successfully and invalid records are skipped with warnings.
- The specification says B is `>= 70`, so Bilal's average of 70.67 is correctly reported as B; the sample expected output labels him C.
- Editor diagnostics reported no errors.

## How to run
See `../../report/manual-benchmark-guide.md`. Open this folder as the project, read `TASK.md`,
prompt: "Read TASK.md and implement it.", time from prompt to passing pytest.
