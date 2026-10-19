---
name: bootstrap-greenfield
description: Phases 0 and 1 for a new repo - interview the owner, record the stack decision with options and tradeoffs, scaffold, write CLAUDE.md, AGENTS.md and a target ARCHITECTURE.md, and set up the tracker and harnesses. Use when starting the delivery framework on an empty or new repository at tier L.
---

# Bootstrap a greenfield project

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `bootstrap`). With no code, the profile's surfaces came from the owner's
interview in `assess`; re-check them before choosing a stack.

1. Read `${CLAUDE_PLUGIN_ROOT}/prompts/00-bootstrap-greenfield.md` and run it as written.
2. Present at least two stack options with tradeoffs before choosing; the owner decides. Record the
   decision in `docs/delivery/DECISIONS.md` (template `${CLAUDE_PLUGIN_ROOT}/templates/DECISIONS.md`).
3. Scaffold the harness each surface's gate needs, from `.delivery/profile.json` `contracts`: a UI
   gets the E2E runner and capture build; an API gets a contract file and a contract-test runner; a
   pipeline gets the golden dataset folder and the data-quality check runner; a CLI or library gets
   doctest or golden-output tests.
4. Phase 1 (`${CLAUDE_PLUGIN_ROOT}/prompts/01-project-setup.md`): `CLAUDE.md`, `AGENTS.md`,
   `.env.example`, tracker conventions. `ARCHITECTURE.md` from the template, every section **[P]**.

Gate (CHECKLIST.md §0 and §1). End with the report, the staged files, and ask before any commit.
