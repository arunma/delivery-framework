---
name: sessionize
description: Phase 11 - generate SESSIONS.md, the self-contained session prompts (one per agent context, in dependency order), from the session phases of every tasks.md and plan.md session mapping, with the Definition of done chosen from the profile's verification gate, wave-close blocks and owner tasks, then validate every block. Use after plans exist at tier L, or when someone asks to (re)build or check SESSIONS.md.
argument-hint: "[generate | validate]"
---

# Sessionize

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `sessions`). Mode: `$ARGUMENTS` (default: generate, then validate).

1. Start `SESSIONS.md` from `${CLAUDE_PLUGIN_ROOT}/templates/SESSIONS.md` (prompt:
   `${CLAUDE_PLUGIN_ROOT}/prompts/11-sessions.md`). Keep its top sections: how to use it, order and
   why, the wave table, the full Definition of done, the reviewer prompt, owner tasks, and "How to
   tell a session actually finished".
2. **Pick the Definition of done for the profile.** Steps 2 and 3 come from `.delivery/profile.json`
   `contracts`: UI → E2E flows with captures by screen id, then the parity round; API → API and
   integration tests on an ephemeral or staging environment, then contract tests, consumer-driven
   tests and the contract diff; data → the pipeline run on the golden dataset, then the answer-key
   diff, quality checks and a reproducibility run; CLI/library → golden CLI runs, then doctests and
   the semver check; infra → plan only, then plan diff and policy checks; ML → the eval harness, then
   the decision rule. A mixed project lists each. Keep the step numbers and headings ("1. Tests",
   "2. E2E", "3. <gate>", "4. Closing review", "5. … lint") so the validator can find them.
3. Generate the blocks:
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py generate specs/*/tasks.md --set "<JIRA_KEY>=<KEY>" --out SESSIONS.draft.md`
   It fills the id, spec, FR range, stories, contract ids (plan.md's "Screens shipped" column),
   flows, task ids, dependencies and known ticket keys. Paste each block under its wave, then fill
   the placeholders it reports (read-first lists, watch-fors from DISCREPANCIES and OPEN-QUESTIONS).
   Order: foundation first, engines with no surface of their own next, then features wave by wave.
4. Add a wave-close block after every wave with the seams specific to that wave.
5. Validate: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py validate SESSIONS.md --strict` and
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/create_tickets.py --dry-run --sessions SESSIONS.md --project <KEY>`.
   Every block must pass alone: guards, Jira start/done, GAPS IN, HANDOFF, all five DoD steps, report.
6. Session coverage: list every FR not in any session's range; there must be none, or each is
   "not built in this build" with its reason.

Gate (CHECKLIST.md §11). Report sessions per wave, FR orphans (0), validator and dry-run output; stage, ask.
