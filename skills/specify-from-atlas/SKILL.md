---
name: specify-from-atlas
description: Phase 9 - write one spec per feature from the contract artefact (the atlas's screen ids for UI; operation ids, dataset and column names, command names or eval case ids for other surfaces), in the house format with a Build line, Jira line, prioritised Given/When/Then stories citing contract ids, numbered FRs with backend tags, a three-layer test plan and Mermaid flows, plus a per-spec review. Use when specifying features at tier M or L, after the contract is approved.
argument-hint: "[NNN-name or feature description]"
---

# Specify from the contract

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `specs`; its `with` names the contract). Feature: `$ARGUMENTS`.

1. **Back up `specs/`** before any agent writes to it.
2. Write `docs/delivery/SPEC-BRIEF.md` from `${CLAUDE_PLUGIN_ROOT}/templates/SPEC-BRIEF.md` once per
   project; the spec prompts are in `${CLAUDE_PLUGIN_ROOT}/prompts/09-specs.md`.
3. One spec per feature in `specs/NNN-name/spec.md` (spec-kit `/speckit.specify`, then shaped to the
   house format), with `checklists/requirements.md` including *Contract and build coverage*: every
   contract id this spec owns → its FRs. For UI, the owner spec comes from `spec_map.py`.
4. Every story and UI FR names the contract id it implements: `Screen: <id>` for UI,
   `Operation: <operationId>` for an API, `Dataset: <name>.<column>` for data, `Command: <name>` for a
   CLI, `Resource: <address>` for infra, `Eval case: <id>` for ML. Backend FRs carry
   **[Backend: ITEM]** or **[Backend, critical: ITEM]**.
5. The test plan names the three layers for this surface, from the profile's `contracts.e2e`.
6. Mermaid: a flow per story, a state diagram per stateful entity, a sequence per server or device
   exchange (API: per operation that crosses a boundary; data: the lineage slice the spec touches).
7. Per-spec review: UI → `design/ui-review/NNN.md` by the `design-reviewer` agent; other surfaces →
   the same agent reviews the spec against the contract into `docs/delivery/reviews/NNN.md`.
8. Brownfield: the Overview cites current code (`path:line`, found with graphify), a *Carried over
   from today* table, and `TRACEABILITY.md` maps every current capability.

Specs run in parallel as one agent per spec. Never renumber an FR; withdraw it and leave the gap.
Then run `verify-specs`. Gate (CHECKLIST.md §9). Report, stage, ask.
