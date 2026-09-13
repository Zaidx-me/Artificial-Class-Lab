# Scoring Rubric

## Metrics

### 1. Task Completion Time (minutes)
Estimated time-to-harvest for the benchmark task, derived from the tool's published
response latency and agentic capabilities (see `methodology.md`).

Score conversion:
| Time | Score |
|------|-------|
| 0–10 min | 10/10 |
| 10–15 min | 8/10 |
| 15–20 min | 6/10 |
| 20+ min / incomplete | 2/10 |

### 2. AI Accuracy (1–10)
How often the AI gives correct, usable answers. Compiled from the tool's default model
score on **SWE-bench Verified** (real GitHub issue resolution):

`AI Accuracy = round(SWE-bench Verified % / 10)`

e.g. 77% → 8/10, 38% → 4/10.

### 3. Features Completed (%)
Proxy for "how many requirements get finished correctly". Uses the tool's default
model SWE-bench Verified resolve rate, because it measures end-to-end task completion,
not just single-line suggestions.

### 4. Code Quality (1–10)
Qualitative rating compiled from independent editor reviews covering: structure (3 pts),
readability (3 pts), error handling (2 pts), efficient/simple solution (2 pts).

### 5. Setup Difficulty (1–5, lower is easier)
Recorded **from our own install attempts** on this machine (CachyOS / Arch Linux),
using install time, account/API-key requirements and packaging friction as inputs.

## Composite Score

```
Composite = (Time × 0.25) + (AI Accuracy × 0.20) + (Features % / 10 × 0.25) + (Code Quality × 0.30)
```

Weighting rationale:
- Code quality and task completion matter most for an assignment → highest weights
- Speed is important but secondary
- AI accuracy is calibrated onto the same 1–10 scale as the other scored metrics

## Data provenance

Quantitative columns are compiled from public benchmarks and are **not** own-measurement.
Every number in `raw-results.csv` carries a source link. Columns marked "estimated"
(task time) or "reviewed" (code quality) are clearly labelled.