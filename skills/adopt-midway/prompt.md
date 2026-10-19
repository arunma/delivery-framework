# Bootstrap — adopt midway (specs or docs already exist)

For a project that is partway through, with specs, mockups, plans or session notes already written.
It adopts the framework without redoing work: it inventories what exists, maps it onto the phases,
and lists the gaps. Paste into a fresh session at the repo root.

```
You are adopting the delivery framework on a project already in progress: <PROJECT>. The framework
is at <path to delivery-framework>; read README.md, FRAMEWORK.md and CHECKLIST.md first. You change
no product code and no existing document in this session. You commit nothing.

## Step 0 — Back up
Copy every untracked or modified document (specs/, design/, docs/, *.md) to <backup dir>/<date>/ and
print the path.

## Step 1 — Inventory
With subagents, list every existing artefact: instructions files, constitution or principles,
decision records, open questions, glossaries, mockups and their source, specs (count, format, FR
numbering, whether they cite screens), plans, task lists, session prompts, tracker tickets, E2E
flows, screenshots, architecture docs, backend notes. For each, give the path, the date it was last
changed, and a one-line verdict: current, stale, or contradicted (with evidence).

## Step 2 — Map onto phases
A table: Phase (0–14) | What exists | Gate items met (from CHECKLIST.md) | Gap | Effort (S/M/L).
Treat existing artefacts as inputs, not as things to redo. Examples: existing mockups become the
screen map by rebuilding them in the kit (phase 4) without redesigning; existing specs go straight to the
verification pass (phase 9) rather than being rewritten; existing decisions move into DECISIONS.md
with their original dates.

## Step 3 — Fill the cheap gaps; propose the rest
Without asking, you may create from the framework's templates any file that does not exist yet and
contradicts nothing: GLOSSARY.md, DISCREPANCIES.md, BACKLOG.md, OPEN-QUESTIONS.md. Fill them from
what you found. Contradictions between existing documents go to DISCREPANCIES.md. Do not edit
existing specs, mockups or decisions. Propose those changes instead.

## Step 4 — The track for what remains
Say whether the rest runs as brownfield (there is a codebase: capture the before if it has not been
done, write TRACEABILITY.md, audit the backend) or greenfield.

## Gate — stop here and report (≤ 40 lines)
1. Backup path.
2. The phase map table.
3. Files created (Step 3), and discrepancies raised (ids).
4. The proposed order for closing the gaps, with the first three skills to run.
5. Questions for the owner.
Commit nothing, and ask.
```
