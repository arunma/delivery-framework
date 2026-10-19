---
name: atlas
description: Phases 3 and 4 for a UI surface - research and review the current UI, then scaffold the mockup atlas generator into design/atlas-src from the bundled starter kit, build the kit and parts, render every screen, build the atlas with strict checks, and run design-review rounds until the owner approves. Use when the profile's contract phase names the mockup atlas, or when someone asks to draw, render or rebuild screens or the atlas.
argument-hint: "[part name to render, or 'scaffold' | 'build' | 'review']"
---

# Mockup atlas (the UI contract)

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile: run only if `ui` is in `surfaces` and the `contract` phase is on or swapped with
"Mockup atlas". Argument: `$ARGUMENTS`.

## Research and review first (phase 3, tier L)

Run `${CLAUDE_PLUGIN_ROOT}/prompts/03-research-and-review.md`: `design/research.md` (every claim
sourced or marked unverified), `design/review.md` for brownfield, and at least one independent
design review by the `design-reviewer` agent, which did not draw the screens.

## Scaffold (once)

1. If `design/atlas-src/` does not exist, copy `${CLAUDE_PLUGIN_ROOT}/tools/atlas-starter/` there,
   leaving out `.venv/`, `out/` and `__pycache__/`.
2. Point the output paths at the top of its scripts to `design/atlas/`, `design/png/` and
   `design/BACKEND-SPLIT.md`.
3. In `design/atlas-src/`: `uv sync`, then `uv run playwright install chromium` once per machine.

## Every change

1. `uv run backup.py` first. Always.
2. `kit.py` is the only styling source and holds the one seed facts block; one agent owns it. Part
   authors each own one `parts/pN_*.py` (brief in `${CLAUDE_PLUGIN_ROOT}/prompts/04-atlas.md`).
3. `uv run render_parts.py [part]`, then open every PNG and look at it.
4. `uv run build_atlas.py --strict`: 0 duplicate ids, 0 ambiguous prefixes, 0 unowned screens, and
   0 unresolved links or a reason for each.
5. A design-review round by the `design-reviewer` agent, then a fix round. Repeat until the owner
   approves in writing (a dated line in `docs/delivery/DECISIONS.md`).

Gate: CHECKLIST.md §3 and §4. Report the build output, the review findings and their fixes, stage, ask.
