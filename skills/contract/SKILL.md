---
name: contract
description: Phases 3 and 4 for a non-UI surface - write the contract artefact that plays the screen map's role and set up the verification gate that plays parity's role - an OpenAPI/AsyncAPI/protobuf contract with sequence diagrams for an API, a data contract with lineage, SLAs, a golden dataset and answer key for a pipeline, a public API surface with runnable examples for a CLI or library, a diagram and IaC plan for infra, an eval set with a decision rule for ML. Use when the profile's contract phase is swapped, or when someone asks to define or change an API, schema, data contract, golden dataset or eval set.
argument-hint: "[surface: api | data | cli | infra | ml]"
---

# Contract artefact for a non-UI surface

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `contract`). Surface: `$ARGUMENTS`, or every non-UI surface in the profile.
For a UI surface use the `screen-map` skill. Templates and the decision table:
`${CLAUDE_PLUGIN_ROOT}/templates/contracts/README.md`.

The rule is the screen map's rule: **every change to the surface starts in the contract**, is validated,
and only then is specified and built. Specs cite the contract's ids.

## Research (tier L)

At most two pages in `docs/delivery/research.md`: comparable APIs, schemas or tools, and 8 to 12
principles, each sourced or marked unverified. Brownfield: start from the baseline that
`capture-before` recorded.

## Per surface

- **API/service:** `contracts/api/openapi.yaml` (or AsyncAPI, `.proto`) plus `contracts/api/README.md`
  from `templates/contracts/API-CONTRACT.md`: consumers, operations with ids, errors, a Mermaid
  sequence per key flow, compatibility rules. Brownfield: generate the contract from the running
  service or code first, then diff it against the docs; every difference goes to DISCREPANCIES.
  Set up the gate: contract tests, consumer-driven tests, and a contract-diff command.
- **Data/pipeline:** `contracts/data/<dataset>.md` from `templates/contracts/DATA-CONTRACT.md`
  (schema, dictionary, Mermaid lineage, SLAs, freshness, quality checks) and the golden dataset from
  `templates/contracts/GOLDEN-DATASET.md`, synthetic and deterministic, with its answer key. Set up
  the gate: run on the golden dataset, diff against the answer key, quality checks, a second run that
  reproduces the output.
- **CLI/library:** `contracts/surface/API-SURFACE.md`: every command, flag, exit code and public
  symbol, each with a usage example that runs as a test (doctest or golden output). Set up a semver
  check against the last release.
- **Infra:** a Mermaid deployment diagram and the committed IaC plan output. Gate: plan diff plus
  policy checks. Plan only in a pilot: never `apply`.
- **ML/model:** the eval set and answer key (GOLDEN-DATASET.md as its README), the benchmark
  hardware, and the decision rule. Gate: the scoring command.

## Review and approval

Ask the `design-reviewer` agent for an independent review of the contract (clarity, consistency,
missing error or edge cases, naming against the glossary). Fix or reject each finding with a reason.
The owner approves the contract in writing (a dated line in `docs/delivery/DECISIONS.md`).

Gate: the contract validates with its own tool (OpenAPI linter, schema check, `terraform validate`,
etc., output pasted); the gate's commands run on today's code (they may fail where work is pending:
say which); every id is unique; the owner approved. Report, stage, ask.
