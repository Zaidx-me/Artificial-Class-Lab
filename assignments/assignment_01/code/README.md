# code/ — The produced code

All 10 tools solved the same benchmark task (`task-spec.md`). Each folder holds that
tool's solution: `grades.py`, `students.txt`, `test_grades.py` (all pass `python3 -m pytest`).

Two groups — the honest status split is also recorded per-row in `../results/scores.csv`:

| Group | Tool folders | Meaning |
|-------|-------------|---------|
| **Live-run** | `trae`, `zed`, `vscode-copilot`, `vscode-cline` | Real timed runs on this machine; `RESULTS.md` holds the actual metrics |
| **Reference** | `aider`, `claude-code`, `cursor`, `google-antigravity`, `replit`, `windsurf` | Tools that couldn't run here (login/install/app limits); a verified reference implementation is supplied instead |

## Run any solution

```bash
cd code/<tool>          # e.g. cd code/trae
python3 -m pytest       # 3 tests, all pass
python3 grades.py       # prints the class table + statistics
```