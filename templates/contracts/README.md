# Contract templates, one per surface

The contract artefact is the source of truth for a surface (constitution principle XI). `tools/assess.py`
names the artefact for each surface in `.delivery/profile.json`; the `contract` skill (or `atlas` for
UI) creates it from these templates. Specs cite its ids; the verification gate checks built output
against it.

| Surface | Contract artefact | Template | Ids that specs cite | Verification gate | E2E / integration |
| --- | --- | --- | --- | --- | --- |
| UI | Mockup atlas, `design/atlas/` | `tools/atlas-starter/` | screen ids | Screenshot parity, independent reviewer | Maestro, XCUITest, Espresso, Playwright on staging |
| API / service | `contracts/api/openapi.yaml` (or AsyncAPI, protobuf) + Mermaid sequences | [API-CONTRACT.md](API-CONTRACT.md) | operation ids, message names | Contract tests, consumer-driven tests, contract diff | API tests on an ephemeral or staging environment |
| Data / pipeline | `contracts/data/` schemas, dictionary, lineage, SLAs | [DATA-CONTRACT.md](DATA-CONTRACT.md), [GOLDEN-DATASET.md](GOLDEN-DATASET.md) | dataset and column names | Output equals the committed answer key; quality checks; reproducible run | Pipeline run on the golden dataset |
| CLI / library | `contracts/surface/API-SURFACE.md` + usage examples | (a list of commands, flags, exit codes and public symbols; examples run as tests) | command and symbol names | Doctests, golden CLI output, semver check | Golden CLI runs |
| Infra | Architecture diagram + IaC plan, `contracts/infra/` | (Mermaid deployment diagram; the plan output committed as text) | resource addresses | Plan diff holds only intended changes; policy checks | Plan only, sandbox account, never apply in the pilot |
| ML / model | Eval set + answer key + decision rule, `contracts/eval/` | [GOLDEN-DATASET.md](GOLDEN-DATASET.md) used as the eval set README | eval case ids | Scores meet the decision rule on named hardware | Eval harness on benchmark devices |

A mixed project keeps one artefact per surface; a UI app with its own backend has the atlas and the
API contract, and its sessions run both gates.
