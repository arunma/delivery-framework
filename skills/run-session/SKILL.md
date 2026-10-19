---
name: run-session
description: Phase 13 execution loop for one session or one tier-S ticket - Jira start, GAPS IN, code-graph refresh and blast radius, tasks test-first, three test layers, E2E or integration runs, the independent verification round against the contract (screenshot parity for UI, contract diff for APIs, answer key for data), simpler-way review, lint, evidence comment, done, then stage and ask before any commit. Use when someone runs a SESSIONS.md block, says "run session S03", or picks up a ticket to implement.
argument-hint: "<SESSION-ID | TICKET-KEY> [--ci]"
---

# Run one session

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.
Target: `$ARGUMENTS`. Prompts: `${CLAUDE_PLUGIN_ROOT}/prompts/13-execution.md`.

## 0. Load the session

- A session id: find its block in `SESSIONS.md` (`### <ID> · …`). The fenced block is the prompt;
  follow it exactly. It carries the guards, the spec range, contract ids, flows and the DoD.
- A ticket key at tier S: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/jira.py show <KEY>`; the ticket's
  acceptance criteria are the spec. If it changes the contract or needs more than one session, stop
  and run `tiering`.
- `specs/<NNN>/HANDOFF.md` exists for this session: continue from it (re-entry, prompt 13c); do not
  re-plan or redo finished tasks.
- Read `.delivery/profile.json` for the verification gate and E2E layer of each surface touched.

## The loop, in order

1. **Start the ticket:** `python3 ${CLAUDE_PLUGIN_ROOT}/tools/jira.py start <KEY>` (or the project's
   `tools/jira.py`). In `--ci` mode with no Jira credentials, record NOT RUN and continue.
2. **GAPS IN, the first output:** every item in DISCREPANCIES.md, BACKLOG.md, OPEN-QUESTIONS.md and
   each dependency's HANDOFF.md and verification file that touches this session, one line each, or
   "none". Close what can be closed here.
3. **Graph:** `graphify update .` if stale; `graphify affected "<symbol>"` for every symbol the session
   changes; confirm callers with grep or the language server; list them in the plan.
4. **Tasks test-first:** this session's phase of `tasks.md`. Write the test, watch it fail, paste
   the failure, then write the code. A bug fix adds the test that would have caught it.
5. **Three layers green** with coverage at the constitution's floor: unit; component and golden (or
   the surface's equivalent: contract-level tests for an API, data-quality tests for a pipeline);
   E2E or integration from the profile. Paste the output.
6. **E2E / integration on staging or an ephemeral environment**, synthetic data only. UI: flows by
   story and screen, captures as `design/app/<screen-id>.png`, via
   `${CLAUDE_PLUGIN_ROOT}/tools/maestro/e2e.sh` or the project's wrapper. API: tests against the
   running service. Data: the pipeline on the golden dataset. Anything that cannot run here is
   **NOT RUN** with the reason, never passing.
7. **Verification round:** run the `parity-review` skill for this spec. It uses an independent
   reviewer that did not write this code. Resolve every finding: fixed in code, or the contract was
   wrong (contract source changed first, rebuilt, recorded in DISCREPANCIES).
8. **Simpler-way review:** check the diff against the affected list; run a code review over the diff;
   ask whether fewer components, providers, states, endpoints or stages would do. Do the small ones;
   the rest goes to BACKLOG.md with the reason.
9. **Lint and analysis** (the project's full commands), clean, pasted. Diagrams updated if a flow
   changed; archify validate for changed `docs/diagrams/*.json`.
10. **Evidence and done:** `jira.py done <KEY> "<evidence>"` only when every step above holds;
    otherwise `jira.py comment <KEY> "<what is left>"` and leave it In Progress. Write HANDOFF.md if
    work remains.
11. **Stage, then ask.** Show `git status` and the staged files, propose the subject
    `<KEY>: <summary>`, and stop. Never commit or push; the owner does (the git guard blocks it).
    In `--ci` mode, stop after staging and print the report: the workflow commits to the ticket's
    branch and opens a pull request, which is the owner's review.

## Report

Three layers with counts from pasted output; success criteria mapped to tests by number; every E2E
or integration run passed or NOT RUN with the reason; the verification file and its result; the
simpler-way answer; what was skipped; contradictions found; the staged files and proposed subject.
Gate: CHECKLIST.md §13 "Each session".
