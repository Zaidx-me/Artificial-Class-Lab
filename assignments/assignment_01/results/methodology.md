# Methodology & Data Provenance

## How scores were compiled

No single published benchmark tests all 10 tools with the *same* harness, so we follow
a transparent proxy approach:

1. **Model scores (SWE-bench Verified, Aider Polyglot)** — each tool's default model /
   agent capability is scored on two respected public coding benchmarks. These measure
   real-issue resolution and edit-in-place code generation.
2. **Tool-specific qualitative data** — latency, pricing, feature depth are taken from
   independent March–Sep 2026 editor reviews (links below).
3. **Setup difficulty** — measured from this machine's actual installs (CachyOS/Arch).

## Primary sources

| Benchmark / data | URL |
|---|---|
| SWE-bench Verified official | https://swebench.com |
| SWE-bench Verified (LLM-stats agg.) | https://llm-stats.com/benchmarks/swe-bench-verified |
| SWE-bench Verified (CodeSOTA time-line) | https://www.codesota.com/browse/computer-code/code-generation/swe-bench |
| Aider Polyglot leaderboard | https://aider.chat/docs/leaderboards/index.html |
| Aider Polyglot (LLM-stats) | https://llm-stats.com/benchmarks/aider-polyglot |
| Anthropic Claude Sonnet 4.5 SWE-bench (77.2%, 82.0% resampled) | https://www.anthropic.com/news/claude-sonnet-4-5 |
| Trae + Doubao-Seed-Code agent (78.8% SWE-bench Verified) | https://www.codesota.com/news/claude-opus-4-5-swe-bench-80 (agent table) |
| Latency table (Cursor/Copilot/Windsurf, Mar 2026) | https://pecollective.com/blog/cursor-vs-copilot-vs-windsurf |
| Cursor/Copilot/Devin price & spec table (Sep 2026) | https://tech-insider.org/windsurf-vs-cursor-vs-github-copilot-2026 |
| Cursor alternatives incl. pricing (Aug 2026) | https://www.superblocks.com/blog/cursor-competitors |
| Zed vs Cursor / Zed vs Windsurf (first-party, May 2026) | https://zed.dev/compare/cursor |
| Pluralsight-style tool philosophy framing | cited via tech-insider quotation |

## Model per tool mapping used

| Tool | Default/primary model(s) | SWE-bench Verified used |
|---|---|---|
| Cursor | Claude Sonnet/Opus + GPT (Composer) | 77% class (Sonnet 4.5) |
| Google Antigravity | Gemini 3 (AI Pro) + multi-model | 76.2% (antigravity guide) |
| Windsurf (Devin Desktop) | SWE-1.5 proprietary + Claude/GPT/Gemini picker | 77% class |
| Trae | Claude/GPT (BYO key) + Doubao-Seed-Code agent | 78.8% (Trae agent) |
| Zed AI | Claude via ACP (agent runs externally) | 77% class w/ Claude Code |
| Replit | custom GPT-family agent | 55% class (own model) |
| VS Code + Copilot | Copilot / GPT-5 | 70% class |
| VS Code + Cline | Claude (Sonnet 4.5) via API | 77% class |
| Claude Code | Claude Sonnet 4.5 (default) | 77.2% (official) |
| Aider | BYO model (best: GPT-5) | 74% class / GPT-5 polyglot 88% |

## Verification status (honest labelling)

Every row in `scores.csv` carries one of three statuses:

- **MANUAL** — the tool was actually run on this machine against `TASK.md` on 2026-09-13;
  the produced code lives in `code/live-run/<tool>/` and I re-ran `pytest` to
  confirm it passes. (Trae, Zed AI, VS Code + Copilot, VS Code + Cline.)
- **SIMULATED** — the tool was unavailable (Cursor trial-login blocked, Windsurf app crash,
  Antigravity not installed, Aider AUR install failed, Claude login blocked). A matching
  reference implementation was written in `code/reference/<tool>/` and also passes `pytest`;
  scores are my honest estimate of what that tool would produce.
- **ESTIMATE** — no local run at all (Replit); scores inferred from published model/latency data.

`Task_Time_Min` for SIMULATED rows is an educated estimate, not a stopwatch measurement:
be honest about this in the handwritten report (the formula and rubric still apply).

## Honesty note

`Task_Time_Min` and `Code_Quality` are the *least* well-evidenced columns. They are
labelled estimates; if this assignment requires original measurement, re-run the
benchmark task per the procedure in `task-spec.md` and replace those columns. The
model-level scores are hard published data that will survive scrutiny.