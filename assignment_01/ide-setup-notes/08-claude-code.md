# 08 — Claude Code

**Type:** CLI Agent · **Developer:** Anthropic

## Install
```bash
npm install -g @anthropic-ai/claude-code
# or the dedicated installer
claude --version
```

## Setup
- Authenticate with a Claude account (subscription) or set `ANTHROPIC_API_KEY`
- Runs in any terminal; git-native workflow

## Notes from our install
- Installed 2.1.270 successfully via npm. npm's default may block the postinstall script;
  if the binary doesn't appear, rerun with `npm install -g --allow-scripts=@anthropic-ai/claude-code`.
- Default model Claude Sonnet 4.5: **77.2% SWE-bench Verified** (82.0% resampled) reported
  by Anthropic — the strongest default agent on our board.