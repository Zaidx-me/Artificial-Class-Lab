# Analysis — Pros, Cons, Findings

All quantitative claims source from `methodology.md`. Scores: composite (1–10).

---

## 1. Claude Code — CLI Agent — 8.43

**Pros**
- Best-in-class agent: 77.2% SWE-bench Verified (official Anthropic result) on its default model
- Works inside any editor or plain terminal; no editor lock-in
- Long-horizon focus (30+ hour autonomous tasks reported by Anthropic)
- Free for Claude Pro subscribers; git-native workflow

**Cons**
- Requires Claude account/API — subscription cost for unlimited use
- Terminal-only, no GUI; steep learning curve for beginners
- Runs up token bills fast on big codebases

## 2. Cursor — Standalone Fork — 8.23

**Pros**
- Best editor UX: tab completion ~200 ms, fastest inline edits in independent measures
- Full VS Code extension ecosystem works out of the box
- Composer handles multi-file edits natively and reliably
- Deepest code-understanding (project-wide indexing + language server)

**Cons**
- $20/mo Pro; heavy usage pushed into a $200/mo tier
- Closed source; opaque about data/context handling
- Electron-based — can lag on huge files ("vibe coding" latency trade-off)

## 3. Windsurf (Devin Desktop) — Standalone Fork — 7.88

**Pros**
- Cascade agent does multi-file reasoning; fastest multi-file ops in review tests (~6 s)
- Free tier with real agent features (rare); Arena Mode to compare models
- Model picker: Claude / GPT / Gemini per task; proprietary SWE-1.5 "13× faster"
- VS Code extension ecosystem

**Cons**
- Rebranded twice (Codeium → Windsurf → Devin Desktop) — docs/tutorials lag behind
- Higher latency on tab completions (~300 ms) than Cursor
- Free credits are capped (25/mo); more supervised agent than fully hands-off

## 4. Aider — Terminal Agent — 7.85

**Pros**
- Free and open source (Apache 2.0); model-agnostic (BYO key)
- 45K+ GitHub stars, huge community; publishes its own benchmark (Aider Polyglot)
- GPT-5 scores 88% on Aider Polyglot — strongest code *editing* numbers on the board
- Git-native; every change is a commit — perfect for tracked projects

**Cons**
- CLI only; no visual UI/diff browsing built-in
- Needs API keys and token budget management
- Quality depends entirely on which model you bring

## 5. Trae — Standalone Fork — 7.65

**Pros**
- Free during preview; ByteDance's VS Code fork with Claude/GPT and BYO-key options
- Its agent (Doubao-Seed-Code) scored 78.8% on SWE-bench Verified — top of our table
- Competitive multi-file + agent features at zero cost

**Cons**
- Young product; fewer reviews and less community polish
- AUR package out of date at install time on our machine
- ByteDance data-policy concerns for some users
- Reduced per-feature polish vs Cursor

## 6. Zed AI — Native GUI IDE — 7.10

**Pros**
- Native Rust — sub-50 ms feel; handles large files without crashing
- Fully open source; agentic editing with editable diff review ("follow mode")
- Real-time multiplayer collaboration built-in
- ACP support = plug Claude Code / Codex agents into the editor

**Cons**
- Plug-in ecosystem much smaller than VS Code's
- AI features less polished than Cursor; tab completion "noticeably less magical"
- Best agents run *externally* (via ACP), not natively

## 7. VS Code + Cline — Editor + Agent — 7.05

**Pros**
- Free, open-source, autonomous agent inside VS Code (6M+ downloads)
- Bring-your-own-model → frontier models (Claude) at API prices
- Transparent permissioned steps; good for learning what agents do

**Cons**
- You must manage API keys + token spend yourself
- Slower than native agent IDEs (our latency estimate ~400 ms class)
- Performance depends on model choice & key limits

## 8. VS Code + Copilot — Editor + Extension — 7.05

**Pros**
- Cheapest mainstream option ($10/mo, free 50 req/mo, free for students)
- Works in 7 editors (VS Code, JetBrains, Neovim, Xcode…) — no editor lock-in
- Deep GitHub integration: PR reviews, Copilot Workspace → CI runs tests
- Low setup difficulty (2/5) — a plugin, not a new tool

**Cons**
- Agent mode is "shallower" than Cursor on multi-file work
- Chat/dev-flow feels bolted-on vs Cursor's native inline UX
- Completion latency ~250 ms — behind Cursor

## 9. Replit — Cloud Browser IDE — 5.88

**Pros**
- Zero setup — everything in the browser; works on any device
- All-in-one: editor + hosting + DB → fastest path from idea to deployed link
- Free tier exists; great for quick prototypes and collaboration

**Cons**
- Its default models trail the frontier (SWE-bench ~55% class)
- Browser latency (~1 s+); less responsive than local editors
- $25/mo for real agent usage; limited deterministic editor tooling

## 10. Codeium — Editor + Extension — 4.43

**Pros**
- Free autocomplete, no credit card, unlimited
- Very light and fast (~40 ms completions)
- Great as a *completion* upgrade to existing VS Code

**Cons**
- Autocomplete-only — cannot autonomously build the benchmark task
- No agent mode; features now largely folded into Windsurf/Devin
- Doesn't compete with agent-class tools on any measured metric

---

## Cross-cutting findings

1. **Agents beat assistants.** Every tool with a real multi-file *agent* (1–7) beat every
   autocomplete/chat-only tool (9–10). The differentiator is autonomy, not model size.
2. **The model does most of the work.** Cline and Aider score high purely because they
   can run frontier models. The IDE is a wrapper; the model is the engine.
3. **Free ≠ bad.** Aider, Cline, Zed and Windsurf free tiers are genuinely usable —
   better than some paid plans a year ago.
4. **Latency matters.** Cursor's ~200 ms completions vs Replit's ~1 s is the difference
   between "flow" and "waiting".
5. **Ecosystem is a moat.** VS Code forks inherit thousands of extensions; Zed's native
   speed can't replace that yet.

## Recommendation for a 5th-semester student

- **Try first:** Copilot (free students) or Cursor free tier — lowest friction, biggest
  learning value.
- **Want the best code:** Claude Code or Aider with GPT-5/Claude — frontier output.
- **Worth your money:** Cursor $20/mo if the free tier feels too small.
- **Avoid for projects:** Codeium (completion only) and Replit (frontier gap) unless
  you specifically need browser deployment.