#!/usr/bin/env bash
# Install the code-understanding and diagram tools the framework uses, then print versions.
#
#   tools/setup-tools.sh [platform ...]     # platforms for the graphify skill; default: claude
#   tools/setup-tools.sh claude codex agents
#
# Installs GLOBALLY (user-level): graphify (uv tool) and its /graphify agent skill for each platform
# (claude = Claude Code, codex = Codex, agents = AGENTS.md-based tools), and the archify agent skill
# (npx skills). Run once per machine. Re-check each README before changing commands:
#   https://github.com/Graphify-Labs/graphify   (PyPI package is "graphifyy", double y)
#   https://github.com/tt-a1i/archify
# Per project afterwards: copy templates/graphifyignore to .graphifyignore, then `graphify update .`
# builds the code graph locally (no AI calls). For graphify's MCP server: uv tool install "graphifyy[mcp]".
set -euo pipefail

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 ($2)" >&2; exit 1; }; }
need uv  "https://docs.astral.sh/uv/"
need npx "Node.js"

echo "== graphify"
uv tool install graphifyy
for platform in "${@:-claude}"; do
  graphify install --platform "$platform"
done

echo "== archify"
npx skills add tt-a1i/archify -g

echo "== versions"
uv tool list | grep -i graphify || true
graphify --version 2>/dev/null || graphify --help | head -1
node --version
echo "archify: installed as an agent skill; its CLI is <skill dir>/bin/archify.mjs (node)."
