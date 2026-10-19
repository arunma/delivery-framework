# Case study: a mobile document vault, brownfield

A cross-platform mobile app for storing sensitive personal documents, brownfield. It is
end-to-end encrypted and runs on iOS and Android from one codebase. The initiative redesigned the
whole app on top of an existing backend that was to change as little as possible. The framework was
distilled from this project over about a week. Names, paths and identifiers from the project are
left out; what follows is the shape of the work, its counts and its lessons.

## Where each phase's artefacts lived

| Phase | Artefacts |
| --- | --- |
| 1 Setup | `CLAUDE.md` (§0 traps, §1 non-negotiables), `AGENTS.md`, a longer `docs/AGENTS.md`, `tools/jira.py`, `.env` |
| 2 Before | The seed record, a synthetic-document generator, a Maestro capture flow, the before screenshots |
| 3 Research, review | The review prompt, `research.md`, `review.md`, two design-review rounds |
| 4 Atlas | The atlas source (`kit.py`, ten parts, `spec_map.py`, `backend_map.py`, `render_parts.py`, `build_atlas.py`, a part brief and a fix brief), output `index.html` and `this-build.html` |
| 5 Decisions | A decisions file (wins over everything), a second decisions file for the model and later-build questions, `OPEN-QUESTIONS.md`, `GLOSSARY.md`, `DISCREPANCIES.md` |
| 6 Backend | A backend change list, a separate audit of the later-build backend, the generated backend split |
| 7 Constitution | `.specify/memory/constitution.md` (13 principles, 5 non-negotiable) |
| 8 Architecture | `ARCHITECTURE.md` (with [V]/[P] markers and a conflicts section) |
| 9 Specs | 19 spec folders, the spec brief, one UI review per spec, the verification report, `TRACEABILITY.md`, and one feature-level review |
| 10 Plans | Per spec: `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`, `plan-discrepancies.md` |
| 11 Sessions | `SESSIONS.md` (Definition of done, the parity reviewer, owner tasks, one block per session, a wave-close block per wave) |
| 12 Jira | A PM-facing ticket index and the id → key map |
| 13 Execution | A script that reverts one fix, runs its regression tests to watch them fail, then restores the tree |

## Counts

- **Atlas:** 235 screens in 10 parts, 164 of them in this build. Of the 235, 149 are client-only,
  33 ship reduced with a client fallback, and 53 wait for a later build (41 for a later backend
  build, 8 for a new sign-in method, 4 that need an on-device model). 0 unresolved links.
- **Specs:** 19, about 1,220 functional requirements (1,221 at the verification pass), and 17
  per-spec UI reviews. The combined review found 387 findings, 49 of them High.
- **Sessions:** 54 blocks: a foundation, 5 waves with a close each, a closing session, an
  on-device model follow-up (7 sessions), and the later builds.
- **Jira:** 97 tickets under 4 epics, all carrying the initiative label. They are: a story per
  session, a task per backend item, the audit's prerequisites as bugs, the open decisions for the
  later build, and security findings outside the initiative's scope.
- **Open questions answered:** 54, in four groups, in one owner round.
- **Backend:** no critical item for this build. The largest later-build area was deferred whole,
  because its screens had no client fallback.

## Lessons (each is now a rule in the framework)

1. **Screen protection hid the accessibility tree.** Once any protected screen mounted, a
   screen-capture protection widget hid the whole accessibility tree from UI automation. The E2E
   tool then failed with selector errors that looked like wrong ids. The fix was a staging-only
   build flag that allows capture, is a no-op in production and is pinned by a test. The protection
   itself was never weakened. → Phase 2 pitfall, `CLAUDE.md` template §0.1.
2. **The E2E tool needed `-e`.** Maestro 2.x ignores plainly exported shell variables, so the flow
   typed `undefined` into the email field. The fix was to source the env file and pass `-e`.
   → `tools/maestro/e2e.sh`, `CLAUDE.md` template §0.2.
3. **Untracked specs were overwritten with no backup.** An agent rewrote the original specs in
   place. They were untracked, so they had to be recovered from session transcripts. → Back up
   before every change: `backup.py`, Step 0 of every bootstrap, and phase 9's "back up `specs/`".
4. **Parallel agents and shared files.** Agents planning specs in parallel wanted to write
   `DISCREPANCIES.md`. spec-kit's setup scripts also switch branches and write
   `.specify/feature.json`, which would have stepped on each other. → Each agent writes only its own
   folder and its own `plan-discrepancies.md`, and runs no setup script. One main session merges
   (`PLAN-BRIEF.md`).
5. **Gadget configuration through the API failed.** Filters and the dashboard could be created
   through the REST API, but pointing gadgets at filters did not work reliably. It is done once by
   hand. → `jira_dashboard.py` prints the filter ids for that step.
6. **Ids colliding in the atlas.** Links resolve by prefix (`S-28` → `S-28-due-date-editor`). Two
   screens sharing a prefix can send a link to the wrong one with no error, so duplicate ids had to
   be asserted in the build. Some cited ids also did not exist, or were ambiguous prefixes.
   → `build_atlas.py` fails on duplicate ids, ambiguous prefixes and unowned screens, and the
   verification pass checks every cited id.
7. **Keeping copy consistent through shared seed facts.** Early parts invented their own dates,
   counts and names. The same document expired on different days on different screens. The seed's
   folder names also collided with the new grouping names. → One facts block in `kit.py`, which
   every screen reads (the fix-round brief, item 1), and a seed ↔ atlas mapping in `seed.md`.

Also learned:
- A verification pass before planning raised screen coverage from 194 to 235 of 235.
- An agent "approved to push a branch" is not approved to commit. That is now an explicit rule.
- Jira's issueLink payload is inverted: the blocker goes in `inwardIssue`. The first run got all
  117 "Blocks" links backwards; check one pair in the UI after creating links.
