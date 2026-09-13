# Manual GUI Benchmark — How to Run & Record

The task spec lives at the repo root (`../task-spec.md`). Each tool runs entirely in a
fresh folder of its own; only the code it produces is kept (see `../code/live-run/`).

## Procedure (same for every tool)

1. Open the tool (log in where needed).
2. Create/open a fresh empty folder for the run (e.g. `../code/live-run/<tool>/`).
3. Paste the spec from `../task-spec.md` into the tool's chat. Use ONLY the tool's AI
   features (Chat / Agent / Copilot chat). Do not manually type the solution.
4. Note your **start time**, then prompt the AI with: **"Read TASK.md and implement it."**
5. Keep working until either the tool finishes **and `pytest test_grades.py` passes**, or
   20 minutes pass (hard stop).
6. Note your **end time** and fill in `RESULTS.md`.

```bash
date +%s.%N        # start time (run before prompting)
date +%s.%N        # end time (run when done)
```

## Record sheet fields

| Field | Meaning |
|---|---|
| `Task_Time_Min` | (end − start) → minutes, 1 decimal |
| `Attempts_To_Pass` | number of agent attempts until pytest passed |
| `Pytest_Result` | PASS / FAIL (run `pytest test_grades.py` yourself to confirm) |
| `Files_Created` | which files the tool produced (e.g. `grades.py students.txt test_grades.py`) |
| `Manual_Interventions` | count of times you had to re-prompt / fix / copy-paste |
| `AI_Accuracy_1_10` | 10 = correct first try, 7 = needed 2-3 fixes, 4 = kept building wrong things |
| `Code_Quality_1_10` | PEP 8, type hints, modularity, error handling |
| `Features_Completed_Pct` | # of the 6 task-spec requirements met, as % |
| `Notes` | anything striking (wrong model, token limits, UX snags) |

## Scoring (from `../results/rubric.md`)

- Task Time: ≤8 min = 10 · ≤13 min = 8 · ≤18 min = 6 · ≤20 min = 4 · >20 min = 2
- Composite = (Time × 0.25) + (AI Accuracy × 0.20) + (Features %/10 × 0.25) + (Code Quality × 0.30)

## After each run

Copy the numbers into `../results/scores.csv` (replace the estimate columns), then
regenerate `../results/ranking.md`.

## Login notes for manual tools

- **Cursor, Windsurf, Trae, Zed, Copilot, Cline, Replit**: free account sign-up is enough.
  No paid plan required.
- **Claude Code**: free tier works (limited messages/day) — run `claude`, then `/login`.
  No Pro plan needed. Once logged in, Claude's run can be driven headlessly from the CLI.
- **Antigravity**: free download from antigravity.google; sign in with any Google account.