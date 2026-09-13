# Assignment 01 — Benchmarking 10 Modern AI Coding IDEs

**Name:** Muhammad Zaid  
**Course:** Artificial Intelligence — 5th Semester, IT  
**University:** University of the Punjab (Gujranwala Campus)  
**GitHub:** https://github.com/zaidx-me/artificial-class-lab (folder: `assignment_01`)

---

## What is this?

A comparative study of 10 modern AI coding IDEs / assistants. Each tool was set up
locally (where applicable) and evaluated against the same benchmark task. Four tools were
run **live on this machine** (Trae, Zed AI, VS Code + Copilot, VS Code + Cline — all with
`pytest` 3/3 pass); the rest are honestly-labelled SIMULATED (reference implementation
provided) or ESTIMATE (published data) because of auth/app/install limits on this machine.
Model-level context comes from published, cited benchmarks (SWE-bench Verified, Aider
Polyglot, independent latency/pricing reviews).

## The 10 tools

| # | Tools page | IDE | Type | Status |
|---|-----------|-----|------|--------|
| 1 | `tools/01-cursor.md` | Cursor | Standalone AI IDE (VS Code fork) | SIMULATED (trial-login blocked) |
| 2 | `tools/02-google-antigravity.md` | Google Antigravity | Standalone Agentic IDE | SIMULATED (not installed) |
| 3 | `tools/03-windsurf.md` | Windsurf (now Devin Desktop) | Standalone AI IDE (VS Code fork) | SIMULATED (app error) |
| 4 | `tools/04-trae.md` | Trae (ByteDance) | Standalone AI IDE (VS Code fork) | **MANUAL — live run** |
| 5 | `tools/05-zed.md` | Zed AI | Native Rust GUI IDE | **MANUAL — live run** |
| 6 | `tools/06-replit.md` | Replit | Cloud / browser IDE | ESTIMATE |
| 7 | `tools/07-vscode-copilot.md` | VS Code + GitHub Copilot | Editor + Extension | **MANUAL — live run** |
| 8 | `tools/08-vscode-cline.md` | VS Code + Cline | Editor + Autonomous Agent | **MANUAL — live run** |
| 9 | `tools/09-claude-code.md` | Claude Code | CLI Agent | SIMULATED (login blocked) |
| 10 | `tools/10-aider.md` | Aider | Terminal Agent | SIMULATED (install failed) |

> Note: Codeium was dropped from the final report (its autocomplete-only product is no longer
> competitive with agent tools and has been folded into the Windsurf/Devin family); Google
> Antigravity took its place as tool #2 per the written report. Folder numbering follows the
> written report order (see `tools/`).

## Repository layout

```
assignment_01/
├── README.md                 <- this file (start here)
├── task-spec.md              <- the benchmark task (same for every IDE)
├── results/                  <- all scoring data
│   ├── scores.csv            <- one row per tool, with sources + MANUAL/SIMULATED/ESTIMATE
│   ├── ranking.md            <- final ranked table
│   ├── methodology.md        <- how scores were derived & honest-labelled
│   ├── rubric.md             <- scoring rules + composite formula
│   └── analysis.md           <- pros/cons, findings, recommendation
├── tools/                    <- one page per tool: install + key facts (01–10)
├── code/                     <- the produced code
│   └── <tool>/               <- per-tool output (4 live runs + 6 reference impls), see code/README.md
│
└── report/                   <- docs for the written report
    ├── handwritten-report-outline.md
    └── manual-benchmark-guide.md
```

## Headline finding

On this simple deterministic task, **all 9 evaluated tools pass** (pytest 3/3) — the gap is
minutes, not functionality. **Fastest live finisher: VS Code + Copilot (2.0 min)**; the
strongest agent-only tool remains **Claude Code**, and the best free agent path for a student
is **Trae** or **Cline**.

## Sources

All quantitative scores reference public leaderboards (links inside each file):
- SWE-bench Verified official leaderboard — https://swebench.com
- Aider Polyglot leaderboard — https://aider.chat/docs/leaderboards
- LLM-stats / CodeSOTA aggregations — links in `results/methodology.md`
- Google Antigravity SWE-bench (76.2%) — antigravity.im guide (cited in `results/scores.csv`)