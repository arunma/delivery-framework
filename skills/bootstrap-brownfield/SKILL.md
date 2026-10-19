---
name: bootstrap-brownfield
description: Phases 0 and 1 for an existing codebase - back up untracked docs, build the code graph, survey the code, write CLAUDE.md and AGENTS.md with the traps found, draft ARCHITECTURE.md and DISCREPANCIES.md, and list open questions for the owner. Use when starting the delivery framework on a brownfield repo at tier L, or when the profile's bootstrap phase is on and the track is brownfield.
---

# Bootstrap a brownfield project

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `bootstrap`).

1. Read [prompt.md](prompt.md) and run it as written, with these
   paths: templates from `${CLAUDE_PLUGIN_ROOT}/templates/`, tools from `${CLAUDE_PLUGIN_ROOT}/tools/`.
2. Step 0 is the backup of every untracked document. Do it before anything else.
3. The code graph comes first: copy `${CLAUDE_PLUGIN_ROOT}/templates/graphifyignore` to
   `.graphifyignore`, run `graphify update .`, read `graphify-out/GRAPH_REPORT.md`. If graphify is
   missing, tell the owner to run `${CLAUDE_PLUGIN_ROOT}/tools/setup-tools.sh` (it installs globally;
   they should read it first) and continue with grep, marking claims **[?]**.
4. Then phase 1 from [../bootstrap-greenfield/project-setup.md](../bootstrap-greenfield/project-setup.md): `CLAUDE.md` (template
   `templates/CLAUDE.md`, §0 traps with symptom, cause and fix), `AGENTS.md`, `.env.example` (never
   `.env` itself; the owner fills it), conventions for keys in branches and commits.
5. Adapt to the profile: for a non-UI surface, CLAUDE.md §0 and §5 name the contract artefact and the
   verification gate from `.delivery/profile.json`, not the atlas and screenshots.
6. Offer to copy `${CLAUDE_PLUGIN_ROOT}/tools/` into the project's `tools/` so pasted sessions work
   without the plugin.

Gate (CHECKLIST.md §0 and §1): the owner has read the report and answered or deferred every question.
End with the report the prompt asks for, the staged files, and ask before any commit.
