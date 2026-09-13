# 03 — Windsurf (now Devin Desktop)

**Type:** Standalone AI IDE (VS Code fork) · **Developer:** Codeium → Cognition AI

## Install (Arch/CachyOS)
The editor formerly named Windsurf is published on AUR as the Devin Desktop package:
```bash
paru -S --noconfirm --skipreview devin-desktop-next
# (next channel = "formerly Windsurf Editor"; stable channel: devin-desktop)
```
Or download from https://windsurf.com / https://devin.ai/desktop

## Setup
- Launch, sign in with account (Google/GitHub)
- Free tier gives 25 credits/mo; Pro $15–20/mo
- Model picker: Claude, GPT, Gemini; proprietary SWE-1.5 model

## Notes from our install
- The `windsurf` / `windsurf-bin` AUR packages do **not** exist anymore — the editor was
  renamed to Devin Desktop (June 2026), so use the AUR `devin-desktop-next` package.
- Signed PKGBUILD clone had one transient network failure before completing.