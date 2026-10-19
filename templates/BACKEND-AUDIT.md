# Backend audit — <scope>

<!-- Guidance: read-only. Brownfield: what the backend ALREADY does, with repo/path:line evidence
at named commits, then the work list. Greenfield: use the same shape as a target inventory
(status "to build"). Never claim "exists" without a citation. Local checkouts only: say what was
not fetched. -->

**Date**: <YYYY-MM-DD> · **Asked for by**: <DECISIONS id> · **Target**: <specs / screens>

**Method.** Read-only. Citations are `repo/path:line` at these commits. A remote branch newer than
these commits is not covered.

| Repo | Commit (date) | What it is | Relevant to |
|---|---|---|---|
| <repo> | `<sha>` (<date>) | <one line> | Core / supporting / unrelated |

## 1. Summary

<Five lines: what exists, what is missing, what is critical, what the client can do alone.>

## 2. What exists already (no change needed)

| Need | Already there | Where |
|---|---|---|
| <capability a screen needs> | <endpoint / table / job> | `<repo/path:line>` |

**Client-side bugs found while reading** (client fixes, no backend work):
- <What the client sends vs what the server reads, with both file:lines.>

## 3. Backend work, item by item

### B1 — <title>
- **Needed by**: <screen ids, spec FRs>
- **Today**: <what exists, file:line>
- **Change**: <minimal change; schema, endpoint, job>
- **Client fallback**: <what ships without it> | none (why)
- **Classification**: ships reduced | deferred | critical (reason)
- **Risks / prerequisites**: <…>

## 4. Prerequisites and gaps found by this audit

<Items not on any list before the audit: bugs, missing cascades, security gaps. Each becomes a
ticket.>

## 5. Sequencing

<Which item unblocks which, and which sessions build each fallback.>

## 6. Open questions

<Each with a recommendation; copied to OPEN-QUESTIONS.md.>
