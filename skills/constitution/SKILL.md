---
name: constitution
description: Phase 7 - draft or amend the project constitution at .specify/memory/constitution.md from the bundled template and DECISIONS.md, with the contract principle naming this project's contract artefacts from the profile, versioned with a Sync Impact Report. Use at tier L after decisions, when the owner wants principles every plan is checked against, or when a decision requires an amendment.
---

# Constitution

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `constitution`).

1. Read `${CLAUDE_PLUGIN_ROOT}/prompts/07-constitution.md` and
   `${CLAUDE_PLUGIN_ROOT}/templates/constitution.md`.
2. Product principles first (what the product promises its users), then the framework floor.
3. **XI. The contract artefact is the source of truth:** name every artefact from the profile's
   `contracts`; delete the rows for surfaces this project does not have.
   **XIII. Built output matches the contract:** keep the gate for each surface in the profile.
   Principle VI (three layers): name the E2E layer per surface (device E2E, API tests, a pipeline
   run on the golden dataset, golden CLI runs).
4. The owner chooses the non-negotiables. Never pick them by default.
5. Versioning and the Sync Impact Report at the top. After an amendment, search for the old version
   string in `CLAUDE.md` §1, the specs' checklists and `SESSIONS.md`, and update every one.

Gate (CHECKLIST.md §7). Report the principles and which are non-negotiable, stage, ask.
