# Golden dataset — <NAME>

<!-- Guidance: lives at contracts/data/golden/README.md (data) or contracts/eval/README.md (ML).
A golden dataset is small, synthetic, committed, and has an answer key: the exact output the
pipeline (or the model, within the decision rule) must produce. It plays the role the atlas's seed
plays for UI. Never real people, customers or production extracts. Remove these comments once
filled in. -->

**Inputs:** `contracts/data/golden/input/` · **Answer key:** `contracts/data/golden/expected/` ·
**Generator:** `<script that regenerates the inputs deterministically, with its seed>`

## Why each case is here

| Case id | Input file(s) | What it exercises | Expected output (in the answer key) |
| --- | --- | --- | --- |
| `G-01-basic` | `orders_basic.csv` | the ordinary path | `daily_orders_basic.csv` |
| `G-02-empty-day` | `orders_gap.csv` | a day with no orders | a row with `orders = 0`, not a missing row |
| `G-03-late-arrival` | `orders_late.csv` | a record arriving after its day closed | <rule from the data contract> |

Every edge case in the specs has a case here, named by id; specs and tests cite the id.

## Rules

- **Synthetic only.** Generated, stamped as specimen data, no real names, ids, addresses or amounts.
- **Deterministic.** The generator takes a fixed seed; regenerating produces identical files.
- **The answer key changes only with the contract.** A changed expected file is reviewed like a
  contract change: why, which spec, which DECISIONS id. Never regenerate it to make a test pass.
- **ML eval sets:** add the decision rule (for example "ship when accuracy ≥ <x> on every case group
  and latency ≤ <y> ms p95 on <named device>"), the benchmark hardware, and the scoring command.
