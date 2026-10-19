# Phase 10 · Plans and tasks

Write `docs/delivery/PLAN-BRIEF.md` from `<framework>/templates/PLAN-BRIEF.md` first. **Back up
`specs/`.** Have a draft of `SESSIONS.md`'s wave table, so plans know which sessions build each spec.

## 10a · Plan one spec (one agent per spec, in parallel)

```
Plan specs/<NNN-name>. Follow docs/delivery/PLAN-BRIEF.md exactly, the parallel-safety rules first:
write only inside specs/<NNN-name>/ (plan.md, research.md, data-model.md, contracts/,
quickstart.md, tasks.md, plan-discrepancies.md); edit no shared file and not spec.md; run no
spec-kit script that creates or switches branches or writes .specify/feature.json — follow the
/speckit.plan, /speckit.tasks and /speckit.analyze templates and write the files directly; change
no code and run no state-changing git command. Ground every claim about today's code in path:line
(run `graphify update .` first if the graph is stale; use graphify query/explain/path before
reading files, and list `graphify affected "<symbol>"` for every existing symbol the plan changes,
confirmed with grep or the language server). The sessions that build this spec are
<session ids and order>. Return the brief's ≤10-line summary.
```

Launch these as parallel agents (one per spec) in a single message. When all have finished:

## 10b · Merge (one main session)

```
Merge the planning round. For every specs/*/plan-discrepancies.md, append each entry to
docs/delivery/DISCREPANCIES.md under "From <NNN> planning" (keep the ids), and mark the source file
"merged <date>". Check each plan: the Constitution Check passes the non-negotiables; the UI plans
cite screen ids; FR → task coverage is complete; session mapping matches SESSIONS.md's draft. List
mismatches between plans (one spec's plan assumes a module another does not provide; two plans
build the same thing). Report: discrepancies merged (count, ids), plan gaps, overlaps, CRITICAL
analysis findings.
```

## 10c · Analyze (per spec, read-only, optional second pass)

```
Run a /speckit.analyze-style pass over specs/<NNN-name>/spec.md, plan.md and tasks.md against the
constitution. Read-only: write findings into plan.md's "Analysis pass" table and spec problems into
plan-discrepancies.md; touch nothing else. Categories: constitution, coverage, inconsistency,
ambiguity, ordering, underspecification. Report CRITICAL and HIGH findings.
```
