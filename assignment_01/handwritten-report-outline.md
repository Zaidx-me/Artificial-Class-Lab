# Handwritten Report Outline

STATUS: **written** — full 12-page draft is in the handwritten notebook (title page,
introduction/theoretical framework, 10 tool profiles, task & methodology, results table +
bar chart, pros/cons, decision matrix, key findings + sources). This outline is the source
of truth for the repo files; regenerate pages 7–8 from `benchmark-data/ranking-table.md`
after any re-run.

## Page 1 — Title Page
- Title: **Benchmarking 10 Modern AI Coding IDEs**
- Muhammad Zaid · 5th Semester IT
- University of the Punjab, Lahore
- Course: Artificial Intelligence · Assignment 01

## Pages 2–3 — Introduction
- What are AI coding IDEs? (agents vs autocomplete vs chat)
- Why study them now (2026: models > 80% on SWE-bench Verified)
- Goal of assignment: same task, 10 tools, published-benchmark evidence
- Effort summary: installs + compiled results + recommendations

## Pages 4–5 — The 10 Tools (2 lines each)
1. Cursor – VS Code fork, best-in-class UX
2. Google Antigravity – Google's agent-first Editor + Manager IDE on Gemini 3
3. Windsurf/Devin Desktop – agent-first fork, rebranded 2026
4. Trae – ByteDance fork, free preview, strong agent
5. Zed AI – native Rust, open source, fast
6. Replit – browser IDE, all-in-one
7. VS Code + Copilot – industry-standard extension
8. VS Code + Cline – open-source autonomous agent
9. Claude Code – CLI agent, best default model
10. Aider – terminal BYO-model agent

## Page 6 — Task & Methodology
- Task: Student Grades Manager (grades.py + pytest + students.txt) — `task-spec.md`
- Metrics: time, AI accuracy, features %, code quality, setup difficulty
- Honesty: model scores compiled from SWE-bench Verified & Aider Polyglot (sources cited);
  task-time & code-quality labelled as estimates
- Composite formula (show it)

## Pages 7–8 — Results & Ranking
- Copy `ranking-table.md` table (10 rows)
- Draw a horizontal bar chart of composite scores by hand
- Call out the top/bottom 3

## Pages 9–10 — Pros & Cons (condensed)
- Each tool: 2–3 pros + 2–3 cons (from `analysis.md`)

## Page 11 — Final Ranking & Recommendation
- Top 5 list
- Best for students: Copilot free / Cursor free / Aider
- Best for pros: Claude Code, Cursor
- Best value: Aider, Copilot
- Final verdict: models matter more than the editor; agents beat assistants

## Page 12 — Conclusion
- Key learnings (5 findings from `analysis.md`)
- Reference the repo: `zaidx-me/artificial-class-lab/assignment_01`
- Sources list (SWE-bench, Aider leaderboard, latency/pricing reviews)