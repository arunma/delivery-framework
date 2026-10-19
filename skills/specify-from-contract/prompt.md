# Phase 9 · Specifications, UI review and verification

**Back up `specs/` before every round.** Write `docs/delivery/SPEC-BRIEF.md` from
`<framework>/templates/SPEC-BRIEF.md` first.

## 9a · Write a spec (one agent per spec, in parallel)

```
Write specs/<NNN-name>/spec.md (and its checklist and UI review). Follow docs/delivery/SPEC-BRIEF.md
exactly. Use /speckit.specify for the skeleton if the folder does not exist, but do not let it
create or switch branches; then shape it to the house format. Work only in specs/<NNN-name>/ and
design/ui-review/<NNN>.md. Conflicts go in the spec's last section, not in shared files.
```

Brownfield: also tell the agent to fill in *Carried over from today*, with file:line for each row.
Greenfield: tell it to cite `design/research.md` and the decisions in the Overview.

## 9b · Per-spec UI review only (if the spec exists already)

```
Review the screens owned by spec <NNN> (list them with spec_map.spec_of) against
specs/<NNN-name>/spec.md, DECISIONS.md and GLOSSARY.md. Write design/ui-review/<NNN>.md: for each
screen, 1–3 findings (clarity, copy, consistency, accessibility, realism, missing state), each with
a severity (High/Med/Low), the backend tag from backend_map.py, and its resolution: Spec (fixed in
the spec — say which FR), Mockup (say exactly what to change), Spec + mockup, Owner, or None. End
with "Missing screens". No praise. Edit only that file.
```

## 9c · Traceability (brownfield, mandatory)

```
Write TRACEABILITY.md (<framework>/templates/TRACEABILITY.md). Rows come from the current inventory
(every route, screen, sheet, action, setting, flag, gate — with paths; build the inventory first if
it does not exist, from the code, using graphify). Homes come from the specs, read in full. Cite an
FR id only where grep finds it; write "carried" where only the carried-over table covers it. Every
row is Kept / Restyled / Moved / Merged / Replaced / Removed (reason). Table C maps every spec to its
screens, FR count, backend items, sessions and build. Report the counts, and every Removed row
without an owner decision.
```

## 9d · Verification pass (one agent, after all specs)

```
Verify specs/000–<NNN> before planning. Script every check you can (screen ids from
render_parts.load() with spec_of; FR ids from "- **FR-NNN**" definitions; "NNN FR-xxx" references;
session ranges from SESSIONS.md "Spec and range" lines when it exists; Jira keys from
docs/delivery/jira-map.json). Write docs/delivery/SPEC-VERIFICATION.md:
Part A — decisions applied: each decision → where it now lives (spec · FR).
Part B — checks, each with "before fixes" and "after":
  1. Screen coverage: every screen id cited by an FR of its owning spec; cited ids that do not exist.
  2. Cross-references: every NNN FR-xxx resolves; duplicate FR ids; checklist FR counts current.
  3. [OPEN: …] markers still present for answered questions.
  4. Build lines vs backend_map.py (every tagged item named).
  5. Constitution version cited consistently.
  6. Glossary: Not words in copy.
  7. Numbers across specs (windows, limits, thresholds) that must agree.
  8. Session coverage: FRs in no session's range (orphans), once SESSIONS.md exists.
  9. Diagrams: every user story has a flow diagram; every Mermaid block compiles (mmdc).
  10. Overviews tell the same story (the build split, what is later).
Part C — decisions → implementing FR (every decision has one).
For the owner — everything you did not fix, numbered, each with a recommendation.
Fix mechanical findings in place (wrong id, stale count, missing citation) and say so. Never
renumber an FR; never change meaning without the owner. Back up specs/ first.
```
