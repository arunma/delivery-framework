---
name: sessionize
description: Phase 11 - generate SESSIONS.md, the self-contained session prompts (one per agent context, named <area>-<what>, in dependency order), from the session phases of every tasks.md and plan.md session mapping, with the Definition of done chosen from the profile's verification gate, wave-close blocks and owner tasks; size and split sessions to one context; write the run sheet and the sessions explainer; then validate. Use after plans exist at tier L, or when someone asks to (re)build, resize, rename or check SESSIONS.md.
argument-hint: "[generate | validate]"
---

# Sessionize

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `sessions`). Mode: `$ARGUMENTS` (default: generate, then validate).

1. Start `SESSIONS.md` from `${CLAUDE_PLUGIN_ROOT}/templates/SESSIONS.md` (prompt:
   [prompt.md](prompt.md)). Keep its top sections: how to use it, order and
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
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py generate specs/<the wave's specs>/tasks.md --wave <wave-name> --close-key <closing ticket key> --first-step <n> --set "<JIRA_KEY>=<KEY>" --out SESSIONS.draft.md`
   One run per wave: it numbers the blocks from `--first-step`, names the wave's branch in every
   block and ends with the wave's `close-<wave-name>` block. It fills the id, spec, FR range, stories, contract ids (plan.md's "Screens shipped" column),
   flows, task ids, dependencies and known ticket keys. Paste each block under its wave, then fill
   the placeholders it reports (read-first lists, watch-fors from DISCREPANCIES and OPEN-QUESTIONS).
   Order: foundation first, engines with no surface of their own next, then features wave by wave.
4. Fill each wave-close block, `close-<wave-name>`, with the seams specific to that
   wave. Every block of a wave names one branch, `wave/<closing ticket key>-<wave-name>` (the key of
   its close session): one branch, one commit per session and one PR per wave.
5. Validate: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py validate SESSIONS.md --strict` and
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/create_tickets.py --dry-run --sessions SESSIONS.md --project <KEY>`.
   Every block must pass alone: guards, Jira start/done, GAPS IN, HANDOFF, all five DoD steps, report.
6. Session coverage: list every FR not in any session's range; there must be none, or each is
   "not built in this build" with its reason.

7. **Run sheet**: `docs/delivery/RUN-SHEET.md` from `${CLAUDE_PLUGIN_ROOT}/templates/RUN-SHEET.md`,
   the short form: each wave's one `/delivery:wave <wave>` command, then one
   `#### <step>. <name> — <summary> · <KEY>` heading per session with its *After* line. Check it:
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/runsheet.py docs/delivery/RUN-SHEET.md --sessions SESSIONS.md`
   (every session exactly once, each after what it depends on).
8. **Explainer**: `docs/delivery/SESSIONS-EXPLAINED.md` from
   `${CLAUDE_PLUGIN_ROOT}/templates/SESSIONS-EXPLAINED.md`, with the table of every session
   regenerated from SESSIONS.md. Refresh both whenever SESSIONS.md changes.

## Names

A session id is a readable kebab-case name, `<area>-<what>` (`labels-domain`, `search-results`); a
wave's close is `close-<wave-name>` (`close-foundation`, `close-wave-2`). Headings carry a step number for the order across the whole build:
`### 7. labels-domain — <summary> · <KEY>` in SESSIONS.md, `## Phase 3 — labels-domain · <KEY>: …`
in tasks.md. The step is not part of the name. Names never change once
tickets exist. When renaming an existing plan from codes, keep an old → new table in the explainer
and in each renamed ticket's description, so old notes and commits still resolve.

## Size: one session, one context

A session must finish inside one context window, closing review included. Measure it by tasks,
files and screens or outputs. Starting rule of thumb, to tune from the pilot log: split when a
session has more than about 25 tasks, touches more than about 15 files, or ships more than about 6
screens (or contract ids). Count the files from the plan, not from a guess.

Split at a seam (domain and store, engine and screen) into **named parts**, each its own block and
tracker story:
- Each part closes itself: its own tests, E2E and verification for what it ships, its own closing
  review and lint, a HANDOFF for the next part, and its own ticket to Done, without waiting.
- Each part's screens or outputs must be complete enough to verify on their own. If a story in the
  next part draws on a screen this part ships, move that story into this part.

**Coarse or fine.** When engineers want fewer, simpler units, keep the size splits and make the
names readable instead. Do not merge to one unit per spec when a spec is larger than one context, or
when two specs depend on each other in both directions: the merged unit cannot finish or cannot be
ordered.

Gate (CHECKLIST.md §11). Report sessions per wave, splits, FR orphans (0), validator, run-sheet check
and dry-run output; stage, ask.
