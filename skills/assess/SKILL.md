---
name: assess
description: Classify a project before any delivery work - its surface (UI, API/service, data/pipeline, CLI/library, infra, ML/model), track (brownfield, greenfield, adopt-midway), tier (S, M, L) and risk flags - and write .delivery/profile.json and PROFILE.md listing which phases are on, off or swapped. Use first on any project, when /delivery:start runs, when .delivery/profile.json is missing, or when the project changes shape (a new surface, a new backend).
argument-hint: "[repo path] [--tier S|M|L]"
---

# Assess the project

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` §3 (guards).
Arguments: `$ARGUMENTS`.

The framework's phases assume a UI by default. Most projects are not only UI. This step decides,
from evidence, which contract artefact plays the atlas's role and which verification gate plays
parity's role, so no later skill draws screens for a data pipeline.

## Steps

1. **Detect.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/tools/assess.py <repo> --stdout` (repo defaults to
   the project root). It scans file names and dependency manifests and prints a draft profile with
   its evidence. It writes nothing with `--stdout`.
2. **Greenfield or an empty repo:** detection finds nothing. Interview the owner instead: what the
   product is, who uses it, which surfaces it has (a UI? an API others call? a pipeline? a CLI or a
   library? infrastructure? a model?), and the risks below.
3. **Confirm with the owner.** Show the draft as a short table: surfaces with their evidence, track,
   risk flags. Ask about anything detection cannot know: regulated domain, sensitive data, other
   repos involved, backend dependencies of a UI. Do not guess a surface the evidence does not show.
4. **Tier.** Run the `tiering` skill (or take the tier the owner already gave) to choose S, M or L
   for the work at hand.
5. **Write.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/tools/assess.py <repo> --tier <T>` with the owner's
   corrections as `--surface …`, `--track …`, `--flag …`. It writes `.delivery/profile.json` and
   `.delivery/PROFILE.md`.
6. **Hooks.** If `.delivery/guards.json` is missing, copy `${CLAUDE_PLUGIN_ROOT}/templates/guards.json`
   there and tell the owner the guards are now active in this project (commit and secrets guards on,
   production guard off until patterns are set). Suggest adding `.delivery/APPROVED` to `.gitignore`.
7. **Report** in at most 12 lines: surfaces and their contract artefacts, the verification gate per
   surface, track, tier, risk flags, the phases that are off or swapped and why, and the next skill to
   run (the track's bootstrap for tier L, `specify-from-atlas` for M, `run-session` for S).

## Surface decision table

| Surface | Contract artefact (atlas role) | Verification gate (parity role) | E2E |
| --- | --- | --- | --- |
| UI | Mockup atlas | Screenshot parity, independent reviewer | Device or browser E2E on staging |
| API/service | OpenAPI/AsyncAPI/protobuf + sequence diagrams | Contract and consumer-driven tests, contract diff | API tests, ephemeral or staging env |
| Data/pipeline | Data contract: schemas, dictionary, lineage, SLAs | Output equals the answer key; quality checks; reproducible | Run on the golden dataset |
| CLI/library | Public API surface + usage examples | Doctests, golden CLI output, semver check | Golden CLI runs |
| Infra | Architecture diagram + IaC plan | Plan diff and policy checks (plan only in a pilot) | Plan against a sandbox |
| ML/model | Eval set + answer key + decision rule | Scores meet the rule on named hardware | Eval harness |

A mixed project gets every row that applies; its sessions run every gate that applies.
