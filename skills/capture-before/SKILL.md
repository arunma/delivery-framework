---
name: capture-before
description: Phase 2 - capture today's behaviour before a redesign so nothing is lost by accident. For UI, screenshots of every current screen on staging with a synthetic seed; for other surfaces, the baseline the profile names (recorded API responses, today's pipeline output on the golden dataset, golden CLI output, the current IaC plan, baseline eval scores). Use on brownfield projects before drawing the contract, or when the profile's capture-before phase is on or swapped.
---

# Capture the before

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `capture-before`; off for greenfield).

Staging only. Synthetic accounts and synthetic data only. The owner provides the staging account
and approves deleting old test data.

## UI (status `on`)

Read [prompt.md](prompt.md) and run it. Use
`${CLAUDE_PLUGIN_ROOT}/templates/seed.md` for `design/seed.md`,
`${CLAUDE_PLUGIN_ROOT}/tools/maestro/capture_before.yaml` as the flow pattern and
`${CLAUDE_PLUGIN_ROOT}/tools/maestro/e2e.sh` as the wrapper (it passes credentials with `-e` and
refuses non-synthetic accounts). If the app blocks screenshots, add a staging-only capture switch
that is a no-op in production, with a test proving it; never weaken the protection. Open every PNG.

## Other surfaces (status `swapped`)

Capture the baseline named in the phase's `with`, with synthetic inputs, and commit it as data:
- **API:** record request/response pairs for every operation in use (`contracts/api/baseline/`),
  secrets and personal data stripped.
- **Data:** run today's pipeline on the golden dataset (`${CLAUDE_PLUGIN_ROOT}/templates/contracts/GOLDEN-DATASET.md`)
  and keep its output as the first answer key, with the run command and versions.
- **CLI/library:** golden output of every command and a listing of the public symbols.
- **Infra:** today's plan output and resource inventory (plan only; never apply).
- **ML:** baseline eval scores on the eval set and the hardware used.

Gate: every capture was opened and checked (no blank, error or wrong-target capture); unreachable
items are listed in `MISSING.md` with the reason; no real data anywhere. Report, stage, ask.
