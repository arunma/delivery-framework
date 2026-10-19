# Brief for writing (or rewriting) a specification

<!-- Guidance: lives at docs/delivery/SPEC-BRIEF.md. Every spec agent gets this plus a task line
naming its spec(s): "Write specs/NNN-name. Follow docs/delivery/SPEC-BRIEF.md." Agents run in
parallel, so each writes ONLY the files named in its task. Back up specs/ before the round. -->

You are writing one or more specs in `specs/NNN-name/spec.md` so they describe **exactly what the
screen map shows**, and reviewing those screens. Work only in the files named in your task. Do not edit
shared files (`DISCREPANCIES.md`, `OPEN-QUESTIONS.md`, `SESSIONS.md`, the constitution, the screen map).
Put conflicts in your spec's last section; the main session merges them.

## Read first
1. `CLAUDE.md`, `.specify/memory/constitution.md`. Where it disagrees with `DECISIONS.md`, the
   decisions win; say so in the spec's last section.
2. `docs/delivery/DECISIONS.md` (authoritative), `OPEN-QUESTIONS.md`, `GLOSSARY.md`.
3. The current spec text, if any, and the house format (below). Reference style:
   `specs/<an approved spec>/spec.md`.
4. **The screen map — source of truth for the UI.** List your screens:
   `cd design/screen-map-src && uv run python -c "from render_parts import load; from spec_map import spec_of; [print(s.sid, '|', s.title, '|', s.purpose) for s in load() if spec_of(s.sid)=='NNN']"`.
   Open every one of your PNGs and read their `reached_from` / `goes_to` in `parts/*.py`. Facts,
   names and copy come from those screens and the kit's facts block.
5. Backend: `design/BACKEND-SPLIT.md`, `backend_map.py` (`BACKEND[screen]`, `ITEMS[item]` with
   fallback), `docs/delivery/BACKEND-AUDIT.md`.
6. **Evidence.** Brownfield: the current code the spec replaces. Cite file:line in the Overview. Use
   `graphify query` / `graphify path` / `graphify explain` before broad file reads. Greenfield:
   `design/research.md` and the decisions. Cite them instead.

## House format
Feature Branch · Created · Status · **Build** · **Jira** · Input · Overview (with evidence) ·
prioritised user stories (Why this priority, Independent Test, Given/When/Then) · Edge cases ·
numbered FRs · Key entities · *Carried over from today* (brownfield) · Success criteria · Assumptions ·
Dependencies · Out of scope · Test plan · Changes needed elsewhere / Decisions applied.

## Rules
- Cite screen ids in stories and FRs ("Screen: `07-item-actions`"). Every screen you own is
  covered by at least one FR, and every FR that shows UI names its screen.
- A **Build** line under Status: `This build` (client-only), `This build, reduced — <fallback>`, or
  `Later build (backend)`. FRs that need backend are tagged **[Backend: ITEM]** with the client
  fallback stated. FRs with no fallback are tagged **[Backend, critical: ITEM]** with the reason the
  build cannot ship without it. Prefer the fallback.
- A **Jira** line: sessions and backend items this spec touches (keys once they exist).
- FRs are `- **FR-001**: …` with MUST/SHOULD. **Never renumber**: withdraw with *Withdrawn — reason*
  and add new ones at the end or as `FR-0xxa`.
- **Diagrams (Mermaid, inline):** one flow diagram per user story (nodes named by screen id, edges by
  the action), a state diagram for every entity with states, and a sequence diagram for every
  exchange with a server or another device. Compile each with `mmdc`.
- Copy matches the screens and the glossary (no *Not* words). Tokens and type reference the design
  system spec; do not redefine them.
- Test plan at three layers, with an accessibility identifier per interactive element per screen.
- Keep what is still right; delete what the screen map dropped; add what it added. Unanswered questions are
  cited as `[OPEN: Qn]`, and the spec states the recommendation it builds meanwhile.
- Then write `specs/NNN-name/checklists/requirements.md`: spec-kit's quality items plus *Screen map and
  build coverage* (each owned screen → FRs; Build line; backend tags; copy; tokens; three layers;
  diagrams present).

## UI review (also yours)
Write `design/ui-review/NNN.md`. For each of your screens give 1–3 findings (clarity, copy,
consistency, accessibility, realism, missing state). Each finding has a severity (High/Med/Low), the
backend tag, and whether you fixed it in the spec or it needs a mockup change (say what). End with
*Missing screens*: states the spec requires but the screen map lacks. Be concrete. No praise.

Return a ≤10-line summary: spec(s) written, FR count, screens covered, backend items referenced
(critical ones called out), mockup changes you recommend, conflicts for DISCREPANCIES.
