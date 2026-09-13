# Assignment 01 — Benchmarking 10 Modern AI Coding IDEs

**Name:** Muhammad Zaid  
**Course:** Artificial Intelligence — 5th Semester, IT  
**University:** University of the Punjab, Lahore  
**GitHub:** https://github.com/zaidx-me/artificial-class-lab (folder: `assignment_01`)

---

## What is this?

A comparative study of 10 modern AI coding IDEs / assistants. Each tool was set up
locally (where applicable) and evaluated against the same benchmark task. Scores are
compiled from **published, cited benchmark data** (SWE-bench Verified, Aider Polyglot,
independent latency/pricing reviews) plus setup observations made while installing each
tool on this machine.

## The 10 tools

| # | Folder | IDE | Type |
|---|--------|-----|------|
| 1 | `01-cursor` | Cursor | Standalone AI IDE (VS Code fork) |
| 2 | `02-windsurf` | Windsurf (now Devin Desktop) | Standalone AI IDE (VS Code fork) |
| 3 | `03-trae` | Trae (ByteDance) | Standalone AI IDE (VS Code fork) |
| 4 | `04-zed` | Zed AI | Native Rust GUI IDE |
| 5 | `05-replit` | Replit | Cloud / browser IDE |
| 6 | `06-vscode-copilot` | VS Code + GitHub Copilot | Editor + Extension |
| 7 | `07-vscode-cline` | VS Code + Cline | Editor + Autonomous Agent |
| 8 | `08-claude-code` | Claude Code | CLI Agent |
| 9 | `09-aider` | Aider | Terminal Agent |
| 10 | `10-codeium` | Codeium | Editor + Extension |

## Repository layout

```
assignment_01/
├── README.md                      <- this file
├── task-spec.md                   <- the benchmark task (same for every IDE)
├── benchmark-data/
│   ├── raw-results.csv            <- all scores, with sources
│   ├── methodology.md             <- how scores were derived
│   ├── ranking-table.md           <- final ranked table
│   └── analysis.md                <- pros/cons, findings, recommendation
├── ide-setup-notes/               <- setup notes + install commands per tool
└── implementations/               <- reserved: code produced per tool
```

## Headline finding

Frontier standalone editors (Claude Code, Cursor, Windsurf) currently outperform both
autocomplete-only extensions (Codeium) and generic chat assistants (Replit) on real
coding benchmarks. **Best value for a student: Cursor free tier or Copilot's free tier /
Student Pack; most capable free/open tool: Aider.**

## Sources

All quantitative scores reference public leaderboards (links inside each file):
- SWE-bench Verified official leaderboard — https://swebench.com
- Aider Polyglot leaderboard — https://aider.chat/docs/leaderboards
- LLM-stats / CodeSOTA aggregations — links in `methodology.md`