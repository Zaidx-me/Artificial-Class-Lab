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

| # | Folder | IDE | Type | Status |
|---|--------|-----|------|--------|
| 1 | `01-cursor` | Cursor | Standalone AI IDE (VS Code fork) | SIMULATED (trial-login blocked) |
| 2 | `03-windsurf` | Windsurf (now Devin Desktop) | Standalone AI IDE (VS Code fork) | SIMULATED (app error) |
| 3 | `04-trae` | Trae (ByteDance) | Standalone AI IDE (VS Code fork) | **MANUAL — live run** |
| 4 | `05-zed` | Zed AI | Native Rust GUI IDE | **MANUAL — live run** |
| 5 | `06-replit` | Replit | Cloud / browser IDE | ESTIMATE |
| 6 | `07-vscode-copilot` | VS Code + GitHub Copilot | Editor + Extension | **MANUAL — live run** |
| 7 | `08-vscode-cline` | VS Code + Cline | Editor + Autonomous Agent | **MANUAL — live run** |
| 8 | `09-claude-code` | Claude Code | CLI Agent | SIMULATED (login blocked) |
| 9 | `10-aider` | Aider | Terminal Agent | SIMULATED (install failed) |
| 10 | `02-google-antigravity` | Google Antigravity | Standalone Agentic IDE | SIMULATED (not installed) |

> Note: Codeium was dropped from the final report (its autocomplete-only product is no longer
> competitive with agent tools and has been folded into the Windsurf/Devin family); Google
> Antigravity took its place as tool #2 per the written report. Folder numbering follows the
> written report order (see `ide-setup-notes/`).

## Repository layout

```
assignment_01/
├── README.md                      <- this file
├── task-spec.md                   <- the benchmark task (same for every IDE)
├── benchmark-data/
│   ├── raw-results.csv            <- all scores, with sources + MANUAL/SIMULATED/ESTIMATE
│   ├── methodology.md             <- how scores were derived & honest-labelled
│   ├── ranking-table.md           <- final ranked table
│   └── analysis.md                <- pros/cons, findings, recommendation
├── ide-setup-notes/               <- setup notes + install commands per tool
├── implementations/               <- verified reference code per tool (SIMULATED set)
└── benchmark-runs/                <- live run folders + manual benchmark kit
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
- LLM-stats / CodeSOTA aggregations — links in `methodology.md`
- Google Antigravity SWE-bench (76.2%) — antigravity.im guide (cited in `raw-results.csv`)