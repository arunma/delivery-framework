# Phase 13 · Execution

The session prompt is the `SESSIONS.md` block itself: paste one block into a fresh session. The
prompts below support it.

## 13a · Parity reviewer (fresh agent; give it nothing else)

Same text as `SESSIONS.md` § The parity reviewer. Fill in `NNN`. Do not give it the diff or the
session's notes.

```
You are the parity reviewer for spec NNN of <PRODUCT>. You did not write this code; do not read
its diff or its HANDOFF. Read design/parity/README.md, specs/NNN-*/spec.md (the screens and states
it names, and its Build line for reduced forms) and design/BACKEND-SPLIT.md §3. Open
design/parity/NNN/index.html. For every screen, compare the app capture with the screen map PNG:
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
the aspect, what the screen map shows and what the app shows, resolution "Open". Do not fix anything.
End with the count of Open differences.
```

## 13b · Session reviewer (optional, after any session, in another fresh session)

```
You are reviewing one session's work on <PRODUCT>. Read CLAUDE.md, .specify/memory/constitution.md,
docs/delivery/DECISIONS.md, the spec and FR range the session implemented, its HANDOFF.md if
present, and design/parity/NNN.md. Then read the staged diff (git diff --staged).
Report, with file:line for each finding:
1. Constitution violations — the non-negotiables first: data leaving where it must not; automated
   output stored without acceptance or shown unmarked; a dropped async result, an empty catch, an
   empty state shown while loading; a story or screen with no E2E flow; a parity row left Open
   or resolved without evidence.
2. Spec drift: requirements built differently from the spec, or not at all, with no DISCREPANCIES
   entry.
3. Screen map drift the parity file missed: compare two or three captures with their screen map PNGs yourself.
4. Copy: user-facing strings not in the spec or the screen map; glossary Not words; the internal name.
5. Tests that assert what the code does rather than what the spec says; goldens regenerated without
   reason; flows reported passing that could not have run.
6. Diagrams: a changed flow with a stale diagram; archify validate not run.
7. Blast radius: run `graphify affected` on each symbol the diff changes (rebuild with
   `graphify update .` if stale; confirm with grep, since call edges can be incomplete); any caller
   whose behaviour changed with no test.
8. Simpler: anything that could be done with fewer components, providers or states.
Do not fix anything. Rank findings Blocker / Should fix / Nit. End with "Mergeable: yes/no".
```

## 13c · Re-entry (a session that stopped part-way)

```
Continue session <ID> (<JIRA_KEY>-NN). Paste-in: the original block from SESSIONS.md follows. Start
from specs/<NNN-name>/HANDOFF.md: do not re-plan, do not redo finished tasks. Rebuild the code graph
if stale (`graphify update .`). First output: GAPS IN
(including anything HANDOFF lists as surprising), then the remaining task ids. The Definition of
done and the report are unchanged.
<the block>
```

## 13d · Wave close

The `SESSIONS.md` wave-close block. Paste it into a fresh session after the wave's last session is
committed.

## 13e · Owner's read of a report (checklist for the engineer)

Accept a session as done only if the report has: three layers with counts from pasted output;
success criteria mapped to tests by number; every flow passed or NOT RUN with a reason; a parity
file that passes, written by a fresh reviewer; what was skipped; contradictions; staged files and a
proposed subject. Otherwise paste 13c with what is missing.
