# 06 — VS Code + GitHub Copilot

**Type:** Editor + Extension · **Developer:** Microsoft / GitHub

## Install
VS Code (OSS build on this machine) is at `/usr/bin/code`. Install the extension:
```bash
code --install-extension GitHub.copilot
```

> Note: the OSS `code` build points at the Open VSX gallery by default, which does NOT
> host the official Copilot extension. We re-pointed `/usr/lib/code/product.json` to the
> Microsoft marketplace (`https://marketplace.visualstudio.com/_apis/public/gallery`) and
> used `Codeium.codeium`, `saoudrizwan.claude-dev` and `GitHub.copilot` from there.

## Setup
- Sign in with GitHub account (free with GitHub Student Developer Pack)
- Plans: free 50 requests/mo; Pro $10/mo; Business $19/user/mo

## Notes
- Works in 7 editors (VS Code, JetBrains, Neovim, Xcode…). Completion-only if you don't
  use Agent mode / Copilot Workspace.