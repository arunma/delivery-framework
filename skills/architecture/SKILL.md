---
name: architecture
description: Phase 8 - write ARCHITECTURE.md from the code graph (graphify) with [V]erified file:line, [P]roposed and [?]unverified markers, Mermaid diagrams for context, modules, key flows, state machines, data flow and deployment, and archify diagrams for the overview and key workflows. Use at tier L, when someone asks how the pieces fit, or when the architecture doc is stale against the code.
---

# Architecture

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `architecture`).

1. Read [prompt.md](prompt.md) and
   `${CLAUDE_PLUGIN_ROOT}/templates/ARCHITECTURE.md`.
2. Graph first: `graphify update .` if stale; `graphify-out/GRAPH_REPORT.md` for the module map,
   dependencies and hot spots; `graphify path`, `explain` and `affected` to trace each flow; confirm
   with grep or the language server where call edges may be missing. Cite only extracted edges as
   evidence.
3. Per surface, the sections the profile needs: UI screens and navigation; API operations and their
   sequences (link the contract); pipeline lineage and schedules (link the data contract); CLI
   command tree; infra deployment; model serving and the eval loop.
4. Mermaid inline for every diagram; compile with `mmdc`. archify versions of the overview and two or
   three key workflows in `docs/diagrams/<name>.json` with rendered HTML and PNG, validated with
   `node <archify skill dir>/bin/archify.mjs validate <type> docs/diagrams/<name>.json --quality showcase --json`.
   If mmdc or archify is missing, report it as NOT RUN with the install step
   (`${CLAUDE_PLUGIN_ROOT}/tools/setup-tools.sh`).
5. Copy every conflict between docs and code into `docs/delivery/DISCREPANCIES.md`.

Gate (CHECKLIST.md §8). Report, stage, ask.
