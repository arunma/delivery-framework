# Changelog

All notable changes to the delivery framework plugin. Versions follow [semver](https://semver.org/).

## Unreleased

### Added
- `templates/RUN-SHEET.md`: the exact commands per wave (branch, graph, status, each session with
  its review and commit, the wave close, push and PR), a legend, and what to do when a session
  stops short. `tools/runsheet.py` checks that every session appears once and in dependency order.
- `templates/SESSIONS-EXPLAINED.md`: how sessions are derived (contract → specs → plans → tasks →
  sessions → tracker), the cutting rules, and a table of every session.
- `templates/RESTART-PROMPT.md` (`docs/RESTART.md`): a paste-able block to resume a long planning
  session, refreshed after every major step and shown by the SessionStart hook.
- Decision rounds (`decisions` skill, *round*): the agents' "needs owner" items as one list of
  recommendations; "accept all" recorded as one dated section.

### Changed
- Named sessions: readable kebab-case names, `<area>-<what>`, with a step number for order
  (`### 7. labels-domain — … · KEY-12`, the key absent before tickets exist; tasks.md phases
  `## Phase 1 — labels-domain · KEY-12: …`). Wave closes are `close-<wave-name>`. `sessionize.py`,
  `runsheet.py` and `create_tickets.py` read them, and the old `S01 · …` forms still parse;
  `sessionize.py generate` writes them (`--wave`, `--close-key`, `--first-step`), ending each wave
  with its close block. `/delivery:session <session-name>` with no argument lists the next runnable
  sessions. Templates and samples use names (`widgets-domain`, `widgets-screens`, `close-wave-1`).
  Keep an old → new table when renaming a plan.
- Sessions are sized to one context (tasks, files, screens) and split into named parts, each its own
  story that closes itself, with its screens complete enough to check on their own. When engineers
  want fewer units, names get readable; specs are not merged into one unit each.
- Per-wave branches: one branch per wave, `wave/<closing key>-<wave-name>`, named in every block
  of the wave instead of `feat/…` per session; a session never creates a branch. One commit per
  session by the owner, one push and one PR after the wave's close (constitution template, SESSIONS template, `PILOT.md`,
  `CHECKLIST.md`, `wave-close`). Sessions run by hand; CI-driven runs stay optional. The last
  per-session branch mentions now say the same: the project-setup prompt, `templates/CLAUDE.md`,
  `templates/PLAN-BRIEF.md`, and `tools/atlas-starter/backend_map.py` (session names, not `S03a`
  ids). The example CI workflow (`ci/github-actions/`) runs by hand on the wave branch given as an
  input, commits the session there and opens the wave's draft PR if it has none; it no longer
  creates a branch per session or runs from an issue label.
- Each phase prompt moved from `prompts/` into the folder of the skill that runs it
  (`skills/<name>/prompt.md`; the atlas skill also has `research.md`, and the project-setup prompt
  is `skills/bootstrap-greenfield/project-setup.md`, used by both bootstrap skills). Skills link
  them with relative paths, as supporting files loaded on demand. `prompts/` is gone.
- New traps in the case study, `CHECKLIST.md` and `PILOT.md`: ignored planning folders, the approval
  file's push window, status headings, parallel agents sharing a file, `.env` without a newline.
- Docs rewritten in plain words and cut by about two thirds (README, FRAMEWORK, CHECKLIST, PILOT).
  "Tier S/M/L" is now "small / medium / large project"; "parity" is "check the result matches the
  contract"; "atlas" is "clickable mockups". Two worked examples: an existing web app with an API,
  and a new data pipeline. The CI-driven pilot week is optional. Plugin behaviour is unchanged.

### Removed
- The learning guide (`docs/learning/`) and its link from the README.

### Fixed
- `sessionize.py` reads phase headings without the word "Session" and with a tracker key after the
  id (`## Phase 1a — S03a1 · ABC-148: …`), so `/delivery:status` works on such projects.
- README: `.delivery/APPROVED` allows commit and push for 15 minutes, not one commit.

## 0.1.0

First release as a Claude Code plugin (`delivery`) with its own marketplace (`delivery-framework`).

### Added
- **Step 0, assess.** `tools/assess.py` and the `assess` skill classify a project by surface (UI,
  API/service, data/pipeline, CLI/library, infra, ML/model), track, tier and risk flags, and write
  `.delivery/profile.json` and `PROFILE.md` with every phase on, off or swapped. Every skill reads the
  profile first.
- **Per-surface contracts and gates.** The `contract` skill and templates in `templates/contracts/`
  (API contract, data contract with lineage, golden dataset) for surfaces without a UI; the atlas
  stays the UI contract. The verification round checks built output against the profile's gate.
- **20 skills**, one per phase or job, and **5 commands**: `/delivery:start`, `/delivery:session`,
  `/delivery:parity`, `/delivery:status`, `/delivery:close-wave` (`/delivery:assess` is the skill).
- **5 subagents**: `parity-reviewer`, `design-reviewer`, `spec-verifier`, `backend-auditor`,
  `plan-writer`, with tool allowlists.
- **Hooks**, opt-in per project through `.delivery/`: git guard (no commit or push without the
  owner's approval), secrets guard, production guard (off until configured), session-start context.
- `tools/sessionize.py`: generate SESSIONS.md blocks from tasks.md session phases, validate that every
  block is self-contained, and report task/tracker drift. `templates/tasks.md` fixes the phase format.
- `ci/github-actions/`: an example workflow for ticket-driven sessions through
  `anthropics/claude-code-action`, opening draft PRs.
- `PILOT.md` and `templates/pilot-LOG.md`; `reference/CONVENTIONS.md`; unit tests in `tests/`.

### Changed
- Constitution template: "the atlas is the contract" became "the contract artefact is the source of
  truth", and parity became "built output matches the contract", with a gate per surface.
- `FRAMEWORK.md` and `CHECKLIST.md` name the skill and command for each phase and gate, and start
  with Step 0. `templates/SESSIONS.md` takes Definition of done steps 2 and 3 from the profile.
