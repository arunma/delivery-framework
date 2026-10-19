---
name: parity-review
description: The verification round that closes every session - an independent reviewer that never wrote the code checks built output against the contract and writes the findings file. UI - app captures beside screen map PNGs into design/parity/NNN.md; API - contract tests, consumer tests and the contract diff; data - output against the committed answer key plus quality checks; CLI - golden output and doctests; infra - plan diff; ML - eval against the decision rule. Use at DoD step 3, at wave close, or when someone asks whether a built feature matches its mockups or contract.
argument-hint: "<spec NNN>"
---

# Verification round (parity)

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.
Spec: `$ARGUMENTS`. Read `.delivery/profile.json` for the surfaces this spec touches.

The reviewer must be independent: launch the `parity-reviewer` agent with only what the prompt below
names. Never give it the diff, the session's notes or HANDOFF.md.

## UI surface

1. Run the project's screen-map-compare command for the spec (it writes `design/parity/NNN/index.html`,
   pairing each capture with its screen map PNG). If the project has none yet, list the pairs:
   `design/app/<screen-id>.png` beside the screen map PNG of the same id.
2. Launch `parity-reviewer` with: the spec number, `specs/NNN-*/spec.md`, `design/parity/NNN/`
   (or the pair list), `design/BACKEND-SPLIT.md` §3 and `design/seed.md`. It writes
   `design/parity/NNN.md`, one row per difference, resolution Open, and the count of Open rows.

## Other surfaces

1. Run the gate commands yourself and save their raw output under `verification/NNN/`:
   API → contract tests, consumer-driven tests, contract diff; data → the run on the golden dataset,
   the answer-key diff, quality checks, a second run's diff; CLI → doctests, golden output diff,
   semver check; infra → plan and policy check output; ML → scores per case group and the rule.
2. Launch `parity-reviewer` with the spec, the contract artefact and `verification/NNN/` only. It
   writes `verification/NNN.md`: one row per contract id with its result (pass, difference, NOT RUN),
   and every difference Open.

## Resolve

Each Open row becomes **Fixed in code** (fix, re-run, re-review that row) or **The contract was
wrong** (change the contract source first, rebuild or re-validate, record in DISCREPANCIES; if it is
a product decision rather than a drawing or typing error, stop and ask the owner). Reduced UI screens
compare with their stand-in or are recorded *Reduced — <item>*; regions owned by an unbuilt spec are
*Partial — owned by NNN*. Done when no row is Open.
