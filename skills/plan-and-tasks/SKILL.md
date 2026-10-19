---
name: plan-and-tasks
description: Phase 10 - plan each spec against the real code and write tasks.md with one phase per session, in parallel with one plan-writer agent per spec under the parallel-safety rules (write only your own spec folder, edit no shared file, run no branch-switching script, change no code), then merge plan-discrepancies into DISCREPANCIES.md in one main session. Use after specs are verified, at tier M or L.
argument-hint: "[NNN-name ... | merge | analyze NNN-name]"
---

# Plans and tasks

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `plans`). Arguments: `$ARGUMENTS` (default: every spec without a plan).

## Plan (in parallel)

1. Write `docs/delivery/PLAN-BRIEF.md` from `${CLAUDE_PLUGIN_ROOT}/templates/PLAN-BRIEF.md` once, and
   back up `specs/`. Prompts: `${CLAUDE_PLUGIN_ROOT}/prompts/10-plans-and-tasks.md`.
2. Launch one `plan-writer` agent per spec **in a single message** so they run in parallel. Give each
   the spec folder, the session ids that build it and their order, and the brief.
3. **Parallel-safety rules**, repeated to every agent: write only inside `specs/NNN-name/` (plan.md,
   research.md, data-model.md, contracts/, quickstart.md, tasks.md, plan-discrepancies.md); edit no
   shared file (`docs/delivery/*`, SESSIONS.md, TRACEABILITY.md, the constitution,
   `.specify/feature.json`, the contract source, other specs, spec.md); run no setup script that
   creates or switches branches or writes shared state; read code, change none.
   Frontmatter cannot restrict Write to a folder, so check afterwards: `git status --porcelain`
   must show changes only inside the planned spec folders.
4. `tasks.md` follows `${CLAUDE_PLUGIN_ROOT}/templates/tasks.md`: one
   `## Phase n: Session <ID> · <summary>` per session, an optional `**Depends on**:` line, tasks
   `- [ ] T001 [P] [US1] … (FR-001) in <path>`, test-first, the Definition of done in order, and the
   FR → task coverage table. The Close tasks use the verification gate from the profile.

## Merge (one main session)

For every `specs/*/plan-discrepancies.md`, append each entry to `docs/delivery/DISCREPANCIES.md`
under "From NNN planning" (keep ids) and mark the source "merged <date>". Check each plan's
Constitution Check, contract-id citations, FR → task coverage and session mapping. List overlaps
between plans.

Gate (CHECKLIST.md §10). Report coverage, discrepancies merged, overlaps; stage, ask.
