---
name: adopt-midway
description: Adopt the delivery framework on a project that already has specs, docs or mockups - inventory every artefact, map it onto the framework's phases, list the gaps, and re-verify what exists rather than redoing it. Use when a repo already has specs/, a .specify folder, SESSIONS.md, design docs or mockups and the team wants to continue under the framework.
---

# Adopt the framework midway

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.

1. Back up every untracked document before reading anything else.
2. Read [prompt.md](prompt.md) and run it as written.
3. Map each existing artefact onto a phase and onto the profile: existing mockups become the atlas
   (rebuilt in the kit, `atlas` skill); an existing OpenAPI file, schema set or eval set becomes the
   contract artefact (`contract` skill) as it is, after re-validation.
4. List the gaps as phases with their skill: for example "no verification pass on the specs →
   `verify-specs`", "no data-quality checks → `contract`".
5. Re-verify; do not regenerate. Existing specs go through `verify-specs`, existing plans through
   `plan-and-tasks` step 10c (analyze), existing session lists through
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py validate SESSIONS.md`.

Gate (CHECKLIST.md §0, adopt midway): the inventory maps every artefact to a phase, and the owner has
agreed the gap list. Report, stage, ask.
