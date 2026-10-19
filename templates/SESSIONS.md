# Session prompts — <PRODUCT> <initiative>

<!-- Guidance: the build sequence. One fenced block per session; each block is pasted ALONE into a
fresh agent session, so it must carry every guard and the whole Definition of done in short.
Headings are parsed by tools/sessionize.py and tools/create_tickets.py:
`### <step>. <name> — <summary> · <JIRA_KEY>-NN` (no ` · <key>` before tickets exist) then, on the next line,
`*Depends on: <name>, <name>. Branch: `wave/...`. Epic: <EPIC>.*`. A name is kebab-case
`<area>-<what>`; a wave's close is `close-<wave-name>`; the step is the order across the whole build.
Text outside the fences is for the engineer. Never rename a session once it has a ticket. Remove
these comments when filled in. -->

Run one block at a time in a **fresh agent session opened at the repo root**, on the wave's branch
(`/delivery:session <name>`, or paste the block), let it run to completion, then move to the next.
The exact commands are in `docs/delivery/RUN-SHEET.md`; how the sessions were cut is in
`docs/delivery/SESSIONS-EXPLAINED.md`. A session never commits: it ends with the work staged, a report,
and a question to the owner. Long sessions lose the thread, so every block also says how to stop
cleanly and hand over.

**Before the first session**, open `design/atlas/this-build.html` (what this build ships) and
`design/atlas/index.html` (every screen), read `docs/delivery/DECISIONS.md` and work through
*Owner tasks* below. `ARCHITECTURE.md` says how the pieces fit; `TRACEABILITY.md` maps old to new;
`design/BACKEND-SPLIT.md` says which screens ship reduced and why.

Each block is self-contained. It opens with the guard text every session needs, then says what is
specific to its slice of a spec, and ends with the Definition of done in short. Each block carries
its Jira key (`docs/delivery/JIRA.md`); the session moves its own ticket with `tools/jira.py`.

**Order and why.** Foundation first: the flag, the harnesses and the parity tooling, the design
system, the data layer every screen reads, and the shell every screen sits in. Then the engines
that have no screen of their own, so later screens are not retro-fitted. Then the screens, wave by
wave, in the order their dependencies allow; sign-in and first run last because they hand over to
everything else. The old UI stays the default behind `<flag>` until the closing session, so the main
branch ships at every step.

Large specs span several sessions (one context window each). A part-1 session plans the whole spec
and implements its range; later parts continue from `HANDOFF.md` without re-planning. Each part is
its own story and closes itself: the Definition of done over its own diff, its own ticket to Done,
without waiting for the next part. Engine
sessions ship no screen; their E2E flows are written by the session that first gives them one, and
the block names it.

| Wave | Sessions | Specs | Branch |
| --- | --- | --- | --- |
| Foundation | foundation-flag, …, then close-foundation | `000`, `001`, … | `wave/<JIRA_KEY>-NN-foundation` |
| 1 — <theme> | widgets-domain, widgets-screens, then close-wave-1 | `00N`, … | `wave/<JIRA_KEY>-NN-wave-1` |
| Close | remove-flag | removes `<flag>` | `wave/<JIRA_KEY>-NN-remove-flag` |

Within a wave, run the sessions in the order listed: each names what it depends on. **One branch per
wave**, named after the ticket of the session that closes it. Every session of the wave works on it
and ends staged; the owner commits each one (one commit per session, its key in the subject) and,
after the close session passes, pushes the branch once and opens one PR for the wave.

---

## Definition of done (every implementation session)

Constitution VI and XIII. **Non-negotiable, and in this order.** Every block repeats it in short;
this is the full text.

<!-- Guidance: steps 2 and 3 below are written for a UI (E2E with captures, then screenshot parity).
Take them from .delivery/profile.json for each surface the project has, keep the step numbers, and
delete the rows that do not apply. The sessionize skill does this. -->

| Surface | Step 2 (E2E / integration) | Step 3 (verification round) |
| --- | --- | --- |
| UI | Device or browser flows on staging, captures by screen id | Screenshot parity → `design/parity/NNN.md` |
| API / service | API tests against an ephemeral or staging environment | Contract tests, consumer-driven tests, contract diff → `verification/NNN.md` |
| Data / pipeline | Pipeline run on the golden dataset (synthetic) | Output equals the answer key; quality checks; a reproducible second run → `verification/NNN.md` |
| CLI / library | Golden CLI runs | Doctests, golden output diff, semver check → `verification/NNN.md` |
| Infra | Plan against a sandbox (never apply in a pilot) | Plan diff and policy checks → `verification/NNN.md` |
| ML / model | Eval harness on the benchmark hardware | Scores against the decision rule → `verification/NNN.md` |

1. **Unit and widget/component + golden tests green.** Unit tests for every pure function the
   session wrote, from hand-built inputs including the spec's edge cases. Widget and golden tests for
   every state the spec names (empty, loading, populated, error, offline): light and dark, normal and
   largest text size, <two device sizes>, golden files named by atlas screen id. `<test command>`
   with coverage ≥ <80>% overall and for every new module. A bug fix adds the test that would have
   caught it, shown failing first. Paste the output.
2. **E2E flows written and green on <STAGING>.** One flow in `<e2e dir>/` for every user story and
   every atlas screen the session implemented — at every priority — named `NNN_<story-slug>`,
   targeting accessibility identifiers only. Each flow captures every atlas screen it passes through
   the shot helper, which writes `design/app/<screen-id>.png`. Build with `<capture build command>`
   (it sets `<CAPTURE_SWITCH>`); run with `tools/maestro/e2e.sh <flow>` (credentials passed with
   `-e`). Synthetic account only; the seeded one (`design/seed.md`) for screenshots. A flow that
   changes data restores the seed, or runs on a second synthetic account and takes no parity
   screenshot. Paste the output. A flow that cannot run here is reported **NOT RUN** with the reason
   and covered by a widget test; it is never reported as passing.
3. **Parity round.** `<atlas-compare command> --spec NNN` writes `design/parity/NNN/index.html`,
   pairing each capture with the atlas PNG. A **fresh reviewer agent that did not write the code**
   (prompt below) compares them and writes `design/parity/NNN.md`. Every difference is resolved as
   one of two things:
   - **Fixed in code**, then re-capture and re-review that screen; or
   - **The atlas was wrong**: change `design/atlas-src` first, rebuild the atlas, and record it in
     `docs/delivery/DISCREPANCIES.md`. If it is a product decision rather than a drawing error, stop
     and ask the owner.

   Reduced screens: where `backend_map.REDUCED` names a stand-in, compare with the stand-in. On a
   reduced screen with no stand-in, a difference that is exactly the stated fallback is recorded as
   *Reduced — <item>*. On a screen whose region belongs to a spec not yet built, the row is
   *Partial — region owned by NNN, re-run in <session>*. Done when `<parity-check command> NNN`
   passes (no *Open* row).
4. **Closing review: is there a simpler way?** Check the diff against the session's
   `graphify affected` list: every affected caller is either unchanged in behaviour or tested. Run a
   code review over the session's diff and act on it. Then ask whether the same result needs fewer components, providers or states. Do the small
   ones; put the rest in `docs/delivery/BACKLOG.md` with the reason.
5. **`<full lint command>`** and `<analyzer>`, both clean, and **diagrams current**: if the session
   changed a flow, its Mermaid diagram in the spec or `ARCHITECTURE.md` is updated, and every
   changed `docs/diagrams/*.json` passes `archify validate`. Paste the output.

Then stage, report and ask. "It works, I ran it" is not evidence; pasted output and a passed parity
file are.

### The parity reviewer

Step 3's reviewer is started fresh (a new agent, or a person), so it has not seen the code. Give it
this, with `NNN` filled in, and nothing else — not the diff, not the session's notes:

```
You are the parity reviewer for spec NNN of <PRODUCT>. You did not write this code; do not read
its diff or its HANDOFF. Read design/parity/README.md, specs/NNN-*/spec.md (the screens and states
it names, and its Build line for reduced forms) and design/BACKEND-SPLIT.md §3. Open
design/parity/NNN/index.html. For every screen, compare the app capture with the atlas PNG:
  - layout and order of every element;
  - copy, word for word — titles, rows, buttons, empty states, snackbars;
  - tokens and type: palette, fonts, the type scale, spacing rules;
  - glyphs and icons;
  - the one primary button;
  - every state the spec names for that screen, and whether each was captured.
Values that differ only because of the seed mapping in design/seed.md are not differences. Where
backend_map.REDUCED names a stand-in, compare with the stand-in. On a reduced screen with no
stand-in, a difference that is exactly the stated fallback is "Reduced — <item>"; anything beyond
it is a difference. Write design/parity/NNN.md in the format below: one row per difference, with
the aspect, what the atlas shows and what the app shows, resolution "Open". Do not fix anything.
End with the count of Open differences.
```

Parity file format (`design/parity/NNN.md`):

| Screen | Aspect | Atlas shows | App shows | Resolution |
| --- | --- | --- | --- | --- |
| `<screen-id>` | copy | *<atlas text>* | *<app text>* | Open → Fixed in code (re-captured <date>) / Atlas was wrong (D-NNN-n) / Reduced — <item> / Partial — region owned by NNN, re-run in <session> / Not captured — <reason> |

---

## Owner tasks

<!-- Guidance: what only the owner can do; each names the session it blocks. -->

These are the owner's, not a session's. Each names the session it blocks.

**O1 — Staging test data.** A seeded synthetic account (`design/seed.md`); a second synthetic account
for flows that change data; <other fixtures>. **Blocks foundation-flag.**

**O2 — Jira.** Tickets created with `tools/create_tickets.py` (index: `docs/delivery/JIRA.md`). Keep
`JIRA_SITE`, `JIRA_USER` and `JIRA_TOKEN` in `.env`. **Blocks foundation-flag.**

**O3 — Decisions still open** (`docs/delivery/OPEN-QUESTIONS.md`). A session that reaches one builds
the recommendation and says so.

| Question | Blocks | What the specs build until answered |
| --- | --- | --- |
| Q<n> | <session> | <recommendation> |

**O4 — Devices.** <Physical devices for the performance budgets; SDKs on the build machine.>

**O5 — Triage `docs/delivery/DISCREPANCIES.md` before foundation-flag.**

**O6 — Commits.** Every session ends staged. The owner commits it on the wave branch after reading
the report, and pushes and merges once per wave.

---

## Foundation — before any screen

These are the ground every screen stands on, and **skipping them is the main way this goes wrong**: a
screen built before the data layer is retro-fitted into it, and a screen built before the parity
tooling has no way to prove it matches the atlas.

### 1. foundation-flag — The flag, identifiers, the E2E wrapper, goldens and parity tooling (`000-foundation`) · <JIRA_KEY>-NN

*Depends on: none. Branch: `wave/<JIRA_KEY>-NN-foundation`. Epic: <EPIC>.*

<!-- Guidance: F-sessions build what every DoD step uses: the feature flag, the accessibility
identifier convention, the E2E wrapper and capture build, the shot helper, the golden matrix,
<atlas-compare> and <parity-check>, the coverage gate. Same block shape as widgets-domain below. -->

```
<Same block shape as widgets-domain below, with Spec and range 000 FR-001–FR-0xx.>
```

---

## Wave 1 — <theme>

### 2. widgets-domain — <What a person can do when this session is done> (`00N-<name>`, part 1) · <JIRA_KEY>-NN

*Depends on: foundation-flag. Branch: `wave/<JIRA_KEY>-NN-wave-1`. Epic: <EPIC>.*

<One or two lines for the engineer: what this session is for, anything to set up first.>

```
Before you start: read CLAUDE.md, .specify/memory/constitution.md (v<X.Y.Z>) and
docs/delivery/DECISIONS.md in full. Principles <I, II, IV, VI and XIII> are non-negotiable, and
DECISIONS.md wins over every other document. ARCHITECTURE.md says how the pieces fit; the atlas
(design/atlas/this-build.html) is the UI contract.

Jira key: <JIRA_KEY>-NN. First command: python3 tools/jira.py start <JIRA_KEY>-NN (moves it to In
Progress). At the end: python3 tools/jira.py done <JIRA_KEY>-NN "<evidence>" only when the Definition
of done holds; otherwise python3 tools/jira.py comment <JIRA_KEY>-NN "<what is left>" and leave it
In Progress.
Branch: wave/<JIRA_KEY>-NN-wave-1 (the wave's branch; do not create another)
Put the key in code comments that need one and in the commit subject you propose.

Guards, every one of them:
  - <STAGING> only. Synthetic accounts only (<SYNTHETIC_PATTERN>). Never production, never a real
    account, never real data.
  - No personal data, customer content, credentials, tokens or codes in logs, reports, screenshots,
    fixtures, identifiers, tickets or analytics.
  - No commit and no push. Leave the work staged, show what would go in, and ask the owner.
    Approval of the work is not approval to commit.
  - When a spec, the atlas, the constitution, a decision or the code disagree: STOP, append it to
    docs/delivery/DISCREPANCIES.md and ask. Do not edit the spec you are implementing. The atlas
    changes only through the parity round's "atlas was wrong" path.
  - No backend change. A backend item ships the client fallback design/BACKEND-SPLIT.md §3 names.
    <Sensitive paths> are used through their existing interfaces only. Never weaken <protection>
    to make a test pass.

First output, before any planning: a "GAPS IN" list. Open docs/delivery/DISCREPANCIES.md,
docs/delivery/BACKLOG.md, docs/delivery/OPEN-QUESTIONS.md, and the HANDOFF.md and design/parity/NNN.md
of every spec this one depends on, and list each item that touches this session -> one line, or
"none". Silence is not an answer. Close what you can here, with a test at the layer it was missing.
An open question this session reaches is built as its recommendation and named in the report.

Code graph: if code changed since graphify-out/graph.json was built, run `graphify update .` (local,
no AI calls). Query it before reading files. Before changing an existing symbol, run
`graphify affected "<symbol>"` and list the result in your plan; call edges can be incomplete for
some languages (e.g. widget construction in Dart), so confirm callers with grep or the language
server.

Context discipline: read the spec, its checklist and the files named below — not the whole repo. Use
subagents for wide searches. If the context runs long with work left, stop at a task boundary and
write specs/00N-<name>/HANDOFF.md: what is done (files), what is next (task ids), decisions taken,
anything surprising. The next session starts from it.
---
<What this session builds, in two sentences.>

Spec and range: specs/00N-<name>/spec.md — FR-001–FR-0xx.
User stories: 1, 2 (P1), 3 (P2).
Atlas screens this session ships (design/atlas PNGs by id). If this-build.html no longer matches
this list, the atlas wins — put the difference in GAPS IN:
  - <screen-id>
  - <screen-id> — reduced (<item>): compare with <stand-in id>
Backend: <item> ships its fallback (<fallback>) | none.

Read first, in order:
  1. specs/00N-<name>/checklists/requirements.md, then spec.md FR range and stories
  2. specs/00N-<name>/plan.md, tasks.md (phase for this session), contracts/
  3. <the existing code this replaces, file paths>
  4. the atlas screens above

Then: set .specify/feature.json to {"feature_directory": "specs/00N-<name>"} and run
/speckit-implement for this session's phase of tasks.md, tests first.

Watch for:
  - <A trap specific to this slice, e.g. a rule two specs state differently, with the DISCREPANCIES id.>
  - <A non-obvious requirement that sessions miss.>

E2E flows (<e2e dir>/; captures by atlas id through the shot helper):
  - 00N_<story-slug> (Story 1)
  - 00N_<story-slug> (Story 2)

Definition of done — all five steps, in this order (full text: SESSIONS.md, "Definition of done"):
  1. Tests green. Unit, and widget + golden (light/dark x text scale normal/largest x two devices,
     named by atlas id) for every state the spec names. <test command>: coverage >= <80>% overall
     and for every new module. Paste the output.
  2. E2E green. A flow for every user story and every atlas screen this session implemented, at
     every priority, targeting accessibility identifiers only, capturing every atlas screen by id.
     Build with <capture build command>; run with tools/maestro/e2e.sh <flow> against <STAGING>
     with the synthetic account. Paste the output. A flow that cannot run is NOT RUN with its
     reason — never "passing".
  3. Parity round. Run <atlas-compare command> --spec 00N. Start a fresh reviewer agent that did
     not write this code (prompt in SESSIONS.md, "The parity reviewer"); it writes
     design/parity/00N.md. Resolve every difference: fixed in code, or the atlas was wrong (change
     design/atlas-src first, rebuild, record in docs/delivery/DISCREPANCIES.md). Re-capture and
     re-review until <parity-check command> 00N passes.
  4. Closing review. Every caller in the graphify affected list is unchanged or tested. Review this
     session's diff, then answer "is there a simpler way?" — fewer
     components, providers, states. Act on it, or add it to docs/delivery/BACKLOG.md with the reason.
  5. <full lint command> and <analyzer> clean. Diagrams updated if a flow changed; archify
     validate passes for changed docs/diagrams/*.json. Paste the output.
Then stage the work, report, and ask before any commit.

Report at the end:
  1. Test evidence: the three layers, named, with counts, from pasted output. Not "tests pass".
  2. Success criteria in this session's range, each mapped to the test asserting it, by number.
  3. E2E: each flow, passed or NOT RUN with the reason; the captures it wrote.
  4. Parity: the result per screen from design/parity/00N.md; every atlas change and its
     DISCREPANCIES id.
  5. The simpler-way answer, and what went to BACKLOG.md.
  6. What was not done and why; open questions built as their recommendation; contradictions found.
  7. The staged files and the commit subject you propose ("<JIRA_KEY>-NN: …"). Then ask.
```

### 3. widgets-screens — <What a person can do when this session is done> (`00N-<name>`, part 2) · <JIRA_KEY>-NN

*Depends on: widgets-domain. Branch: `wave/<JIRA_KEY>-NN-wave-1`. Epic: <EPIC>.*

```
<Shortened in this template. A real block repeats widgets-domain's guard text, GAPS IN, context discipline
and the Definition of done in full, then names its own range, screens, read-first list, watch-fors
and flows. It starts from specs/00N-<name>/HANDOFF.md and does not re-plan.>
```

### 4. close-wave-1 — Close Wave 1 · <JIRA_KEY>-NN

*Depends on: widgets-domain, widgets-screens. Branch: `wave/<JIRA_KEY>-NN-wave-1`. Epic: <EPIC>.*

Implements no spec.

```
Before you start: read CLAUDE.md, .specify/memory/constitution.md (v<X.Y.Z>) and
docs/delivery/DECISIONS.md in full. Principles <I, II, IV, VI and XIII> are non-negotiable.

Jira key: <JIRA_KEY>-NN (python3 tools/jira.py start <JIRA_KEY>-NN first; done <JIRA_KEY>-NN
"<evidence>" last). Branch: wave/<JIRA_KEY>-NN-wave-1. After this session is committed,
the owner pushes the branch and opens one PR for the wave.

Guards: <STAGING> only, synthetic accounts only; no personal data, credentials, tokens or codes in
logs, reports or screenshots; no commit and no push — stage and ask; when documents disagree, STOP
and write it to docs/delivery/DISCREPANCIES.md — do not edit a spec; no backend change; never
weaken <protection>.

This session implements no new behaviour. It may add a missing test, flow or parity row, and fix a
defect a test exposes; anything larger goes to BACKLOG.md or DISCREPANCIES.md and to the owner.

First output: a "GAPS IN" list from docs/delivery/DISCREPANCIES.md, BACKLOG.md, OPEN-QUESTIONS.md,
every specs/*/HANDOFF.md and every design/parity/*.md touched by this wave — each item -> one line,
or "none". Anything that blocks the next wave is listed first.
---
1. Run every E2E flow written so far (not only this wave's) on a fresh capture build, <STAGING>,
   synthetic account. Paste the output. A flow that passed in its own session and fails now is a
   regression this wave caused: find which session.
2. <test command> (coverage >= <80>% overall and per module), <analyzer>, <full lint command>.
   Paste the output.
3. Whole-wave parity sweep. Run <atlas-compare command> and <parity-check command> for every spec
   that has a parity file. Then start a fresh reviewer agent (prompt in SESSIONS.md, "The parity
   reviewer") over every screen this wave shipped, looking for drift since its own round. Re-run
   every Partial row whose missing region's spec is now built. Resolve as in the DoD, step 3.
4. Read DISCREPANCIES.md. For each entry from this wave, propose a resolution — amend the spec,
   amend the atlas source, or close it. Apply none without the owner; present them and wait.
5. List what is NOT done, by spec: success criteria with no test, stories with no flow, screens
   with no passed parity row, flows NOT RUN. That list is the wave's real completion state.
6. Test the seams below. They belong to no single spec, which is why nobody has tested them.
7. Closing review: is there a simpler way across what this wave built — a provider two specs both
   made, two components that are one, a state nobody reaches? Act on the small ones; BACKLOG the rest.
8. Learning loop: list every mistake an agent made this wave; propose a rule for AGENTS.md or a §0
   trap for CLAUDE.md for each, or say "no rule needed". Propose pruning. Apply none without the owner.

Seams for this wave:
  - <A number two screens show that must agree.>
  - <A flow that crosses two specs.>

Report: the pasted output of steps 1–2; the parity sweep's results and every change it caused;
step 4's proposals, waiting on the owner; step 5's list; each seam tested and what it found; step
8's proposals; the staged files. Then ask.
```

---

## How to tell a session actually finished

Seven things, in the report:

1. **Three layers, named, with counts**, from pasted output. "Tests pass" is not a report.
2. **Success criteria by number**, each mapped to the test asserting it. A "zero" or "100 %" with no
   test is not done.
3. **E2E: every flow, passed or NOT RUN with the reason**, and the captures by screen id. A story or
   screen with no flow is not done.
4. **A parity file that passes the check**, written by a reviewer who did not write the code, with
   every difference fixed in code or recorded as an atlas change in DISCREPANCIES.
5. **What was skipped**, explicitly. Scope left undone is the owner's to decide about, not the
   session's to drop.
6. **Contradictions found** — the most valuable thing a session produces and the easiest to lose.
7. **Nothing committed**: the staged files and a proposed subject, waiting for the owner.

If a session reports a feature done and cannot produce (1), (3) and (4), it has not finished.

## Review prompt (optional, after any session, in another fresh session)

See `skills/run-session/prompt.md` § Session reviewer in the delivery framework.
