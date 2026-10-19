# Changelog

All notable changes to the delivery framework plugin. Versions follow [semver](https://semver.org/).

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
