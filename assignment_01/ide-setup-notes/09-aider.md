# 09 — Aider

**Type:** Terminal Agent (BYO model) · **Developer:** Aider-AI (open source)

## Install (Arch/CachyOS)
```bash
paru -S --noconfirm aider-chat     # AUR package (0.86.2)
# or Python:  pip install aider-chat  (needs --break-system-packages on Arch,
#             written by AUR/Arch's PEP-668 policy)
```
Then set your model key, e.g. `export OPENAI_API_KEY=...` or `ANTHROPIC_API_KEY=...`

## Setup
- `aider --version`
- Run `aider` inside a git repo → AI edits become commits automatically
- 40+ slash commands; code / architect / ask / help chat modes

## Notes
- Free, Apache-2.0, 45K+ stars. Publishes the Aider Polyglot leaderboard; with GPT-5 its
  best result is **88%** — the top code-editing score we used.