<!--
Sync Impact Report — update on every amendment; remove before committing if the team prefers
=====================================================================
Version change:      <old> → <new> (<MAJOR|MINOR|PATCH>, <date>: <one line why>)
Bump rationale:      <which decision or incident caused it; cite DECISIONS.md ids>
Modified principles: <id "name" — what changed>
Added principles:    <id "name">
Removed principles:  <id "name">
Templates checked:   <.specify/templates/*.md that read this file; what they must now cover>
Follow-up:           <documents still citing the old version: CLAUDE.md §1, spec checklists, SESSIONS.md>
-->

<!-- Guidance: lives at .specify/memory/constitution.md (spec-kit reads it from there). Short:
aim for 200–300 lines. Product-specific principles come first (what the product promises its
users); the framework principles below are the floor. Mark non-negotiables. Every principle gets a
one-line rationale. Rename ids to fit, but keep them stable once specs cite them. -->

# <PRODUCT> Constitution

<Two sentences: what the product is and why these principles exist — the promise to the person
using it.>

## Core Principles

### I. <The product's core promise> (NON-NEGOTIABLE)

<!-- Guidance: e.g. "content never leaves the device unencrypted", "every match carries its
evidence", "money is never a float". Say exactly what MUST and MUST NOT happen. -->

<Rule.>

*Rationale:* <why a deadline cannot waive it>.

### II. <Model or automation proposes; the person disposes> (NON-NEGOTIABLE, if the product uses AI)

No automated output may change stored data until the person accepts it. Unconfirmed values are
visibly marked, show their source, and offer *Confirm* in place. Every model feature has a stated
reduced behaviour with no model. Citations are built by the app, never trusted from model output.

### III. <Local first / data stays where it is> (if applicable)

### IV. Nothing fails silently (NON-NEGOTIABLE)

Every operation the person starts MUST end in a visible outcome: success, a failure with a reason
and a next step, or a pending state that resolves. A dropped async result, an empty `catch`, or an
empty state shown while data is still loading is a defect.

### V. One concept, one name

Each concept has exactly one user-facing name, listed in `docs/delivery/GLOSSARY.md`. A screen that
introduces a synonym, or a concept that needs an explainer to tell it from another, is a design
defect to fix, not to document.

### VI. Tested at three layers (NON-NEGOTIABLE)

A feature is not done until it has:
1. **Unit** tests for every pure function, from hand-built inputs, including the spec's edge cases.
2. **Widget/component and golden** tests for every screen state the spec names (empty, loading,
   populated, error, offline), light and dark, at normal and largest text size.
3. **E2E** flows for every user story and every atlas screen the session builds, at every priority,
   against <STAGING> with a synthetic account, targeting accessibility identifiers. Each flow
   captures every atlas screen it passes, named by screen id, for the parity check (XIII).
   For a surface with no UI, E2E is the integration layer the profile names: API tests against an
   ephemeral or staging environment, a pipeline run on the golden dataset, golden CLI runs.

Coverage MUST stay at or above <80>% overall and for every new module. A bug fix adds the test
that would have caught it, shown failing first. "It works, I ran it" is not evidence; pasted
output is.

### VII. Accessible by construction

Every interactive element has a label and a stable accessibility identifier. Every screen works at
the largest text size and with the screen reader. Colour is never the only signal. Contrast meets
WCAG 2.2 AA in both themes, measured. Touch targets are at least 44×44 pt.

### VIII. Minimal backend

This build changes <what: the app only / app plus named services>. Every server dependency MUST
either have a **client fallback** that ships a stated reduced behaviour, or be **deferred**. A
dependency with no fallback that the build cannot ship without is **critical**, named with its
reason. Dependencies, fallbacks and screens are listed in `design/BACKEND-SPLIT.md` (source
`design/atlas-src/backend_map.py`). Work not listed there MUST NOT introduce a backend change.

### IX. Measured performance only

No performance claim without a measurement on a named device from a committed benchmark. Budgets:
<first frame, search p95, sync time … on named devices>. A measured regression is a defect.

### X. <Security at the screen / privacy> (if applicable)

### XI. The contract artefact is the source of truth

<!-- Guidance: name the artefact(s) from .delivery/profile.json ("contracts"). One per surface:
UI → the mockup atlas; API/service → the API contract (OpenAPI, AsyncAPI or protobuf) plus
sequence diagrams; data/pipeline → the data contract (schemas, dictionary, lineage, SLAs);
CLI/library → the public API surface doc plus usage examples; infra → the architecture diagram
plus the IaC plan; ML/model → the eval set with its answer key and decision rule. A mixed project
lists each. Delete the rows that do not apply. -->

The contract for this project is **<artefact, e.g. the mockup atlas `design/atlas/` (UI) and the
API contract `contracts/api/openapi.yaml` (API)>**. **Every change to a contracted surface starts
in the contract**, is rebuilt or re-validated, and only then is specified and built. Specs cite the
contract ids they implement (screen ids, operation ids, dataset and column names, command names,
resource addresses, eval case ids); an element with no id is not in scope. Where the contract and a
spec disagree, the session stops and records it in `docs/delivery/DISCREPANCIES.md`.

### XII. One visual language

<Fonts, token source, icon set, status as a word plus a dot, one primary button per screen, light
and dark both shipped — whatever the owner decided in DECISIONS.md.>

### XIII. Built output matches the contract, and that is checked (NON-NEGOTIABLE)

<!-- Guidance: keep the gate(s) for this project's surfaces from .delivery/profile.json. -->

Every implementation ends with a **verification round** against the contract, judged by a reviewer
or a check **that did not write the code**:
- **UI — parity:** the app's captures (E2E, <device>, light theme, the seed in `design/seed.md`)
  beside the atlas PNG of the same screen id: layout and order, copy word for word, tokens and
  type, glyphs, the primary button, and every state the spec names. Findings go to
  `design/parity/NNN.md`.
- **API — contract diff:** contract tests and consumer-driven tests pass, and the diff between the
  committed contract and the one the service serves is empty or approved.
- **Data — answer key:** the pipeline run on the golden dataset produces output equal to the
  committed answer key, data-quality checks pass, and a second run reproduces it.
- **CLI/library — golden output:** usage examples run as tests, golden CLI output matches, and the
  semver check agrees with the change.
- **Infra — plan diff:** the IaC plan diff contains only the intended changes and policy checks pass.
- **ML — eval:** the eval set scores meet the decision rule on the named hardware.

Each finding is resolved as **fixed in code** or **the contract was wrong** (contract changed
first, rebuilt, recorded in DISCREPANCIES). A spec is not done until everything it owns has passed.

## Technical Constraints

<!-- Guidance: stack and versions, one token source, data stores, what must not be refactored by
this initiative, flags that hide unfinished work. -->

- <Language / framework at pinned versions; state management; navigation; storage.>
- **One design-token source**; no colour literal or font string outside <theme path>.
- **<Sensitive paths> are not refactored by this initiative**; they are used through their existing
  interfaces.
- **New UI behind a flag** (`<flag>`) until every surface in this build is built; the flag is
  removed in the closing session.

## Development Workflow

- Work is tracked in Jira **<JIRA_KEY>**. Branches, commit subjects and code comments reference a
  key. Scratch TODOs go to <scratch tracker>, never markdown.
- **Jira is the progress record, kept current by the session doing the work.** Every session in
  `SESSIONS.md` and every backend item has a ticket. A session moves its ticket to *In Progress*
  when it starts (`python3 tools/jira.py start <JIRA_KEY>-NN`), comments the evidence when it
  finishes (tests, E2E, verification file, staged files), and moves it to *Done* only when the Definition
  of done holds. A session that stops short leaves it *In Progress* with a comment saying what is
  left. Discrepancies and new work found mid-session become their own linked tickets. Comments
  never contain credentials or personal data.
- **Every implementation session closes in this order**: three test layers green → E2E flows
  green on staging → captures or outputs by contract id → independent verification against the
  contract (the gate the profile names) → differences fixed or recorded → closing review.
- **Every closing review asks whether there is a simpler way** — fewer components, fewer states,
  fewer moving parts. A better way not taken goes into `docs/delivery/BACKLOG.md` with its reason.
- A session that disagrees with a spec, the atlas, a decision or the code STOPS and writes it to
  `docs/delivery/DISCREPANCIES.md`. It does not edit the spec it is implementing.
- **Never renumber a requirement.** Withdraw it and leave the gap.
- Golden images are regenerated only in the session that changes the screen, and the diff is
  reviewed.

## Governance

This constitution supersedes other practice for work under `specs/`. A change that violates a
principle is changed, or the principle is amended explicitly with its reason. Owner decisions in
`docs/delivery/DECISIONS.md` are applied by amending this file; where they conflict before the
amendment, DECISIONS.md wins.

Principles <I, II, IV, VI and XIII> are non-negotiable and cannot be waived for a deadline. The
others may be waived only with a documented justification and a dated follow-up in `BACKLOG.md`.

Every `/speckit.plan` MUST include a Constitution Check naming the principles it engages and how it
satisfies them. A plan that cannot satisfy the non-negotiables does not proceed to tasks, and a UI
plan that cites no atlas screen ids does not proceed either.

Versioning: MAJOR when a principle is removed or redefined; MINOR when one is added or materially
expanded; PATCH for wording. Each amendment updates the Sync Impact Report above, `CLAUDE.md` §1, and
every document that cites the version.

**Version**: 1.0.0 | **Ratified**: <YYYY-MM-DD> | **Last Amended**: <YYYY-MM-DD>
