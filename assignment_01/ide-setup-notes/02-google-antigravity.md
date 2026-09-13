# 02 — Google Antigravity

**Type:** Standalone Agentic IDE (VS Code fork) · **Developer:** Google DeepMind

## Install (Arch/CachyOS)
```bash
# Free download from the official site (needs a Google account, no paid plan):
#   https://antigravity.google
wget -O antigravity.AppImage "https://antigravity.google/download/linux"
chmod +x antigravity.AppImage && ./antigravity.AppImage
```
On this machine: **not installed** (download + Google login required); benchmark scored as
SIMULATED with a verified reference implementation (`implementations/antigravity/`).

## Key facts (published, Sep 2026)
- Gemini 3 powered; dual-surface Editor + Manager ("mission control") architecture
- Free tier ~20 agent requests/day; AI Pro $20/mo for more; reported 76.2% SWE-bench Verified
- MCP support; multi-model (Gemini 3.1 Pro, Claude Sonnet/Opus, GPT-OSS-120B per guides)

## Notes from our review
- Strengths: async multi-agent runs without locking the editor; verifiable artifacts
- Weaknesses: dual-surface paradigm takes adjustment; higher memory footprint