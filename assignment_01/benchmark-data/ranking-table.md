# Final Ranking

Composite = (Time × 0.25) + (AI Accuracy × 0.20) + (Features % / 10 × 0.25) + (Code Quality × 0.30)

Weights & score scales: see `scoring-rubric.md`. Data provenance: see `methodology.md`.

| Rank | IDE | Type | Composite | Time (min) | AI Accuracy | Features % | Code Quality | Setup (1–5) | Price |
|------|-----|------|-----------|------------|-------------|------------|--------------|--------------|-------|
| 1 | **Claude Code** | CLI Agent | **8.43** | 11 | 9 | 77 | 9 | 2 | Free tier / Pro |
| 2 | **Cursor** | Standalone Fork | **8.23** | 12 | 8 | 77 | 9 | 1 | $20/mo |
| 3 | **Windsurf (Devin Desktop)** | Standalone Fork | **7.88** | 13 | 8 | 75 | 8 | 3 | Free tier / $15–20 |
| 4 | **Aider** | Terminal Agent | **7.85** | 14 | 8 | 74 | 8 | 2 | Free OSS |
| 5 | **Trae** | Standalone Fork | **7.65** | 14 | 8 | 78 | 7 | 3 | Free (preview) |
| 6 | **Zed AI** | Native GUI IDE | **7.10** | 16 | 7 | 72 | 8 | 2 | Free OSS / $20 AI |
| 7 | **VS Code + Cline** | Editor + Agent | **7.05** | 16 | 8 | 74 | 7 | 3 | Free OSS + API |
| 8 | **VS Code + Copilot** | Editor + Extension | **7.05** | 17 | 7 | 70 | 8 | 2 | $10/mo / student free |
| 9 | **Replit** | Cloud Browser | **5.88** | 19 | 6 | 55 | 6 | 1 | Free / $25 |
| 10 | **Codeium** | Editor + Extension | **4.43** | 20+ | 5 | 45 | 6 | 2 | Free / $15 |

Rows 7–8 are a statistical tie (7.05); Cline ranks ahead by AI accuracy since it runs
frontier models (Claude) rather than Copilot's default model.

## Quick takeaways

- **Best overall:** Claude Code (best model + agent depth) and Cursor (best editor UX).
- **Best free / open source:** Aider, then Cline and Zed.
- **Best value for a student:** Copilot (free student tier) → Cursor free tier → Windsurf free tier.
- **Autocomplete-only tools (Codeium) can't build a project on their own** — that's the
  biggest differentiator between "assistant" and "agent".