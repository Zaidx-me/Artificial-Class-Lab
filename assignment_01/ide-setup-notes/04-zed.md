# 04 — Zed AI

**Type:** Native Rust GUI IDE · **Developer:** Zed Industries

## Install (Arch/CachyOS)
```bash
sudo pacman -S zed               # available in Arch/CachyOS repos
# fallback: paru -S --noconfirm zed-editor
```
Or official installer: `curl -f https://zed.dev/install.sh | sh`

## Setup
- Launch, sign in (Settings → Accounts) to enable Zed AI
- Zed itself is free (open source); Zed AI is $20/mo or bring-your-own-key
- ACP protocol lets it drive external agents (Claude Code, Codex, Gemini CLI)

## Notes from our install
- Native performance (sub-50 ms class). Plug-in ecosystem is smaller than VS Code's —
  a known trade-off vs the forks.