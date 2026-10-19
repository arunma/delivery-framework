---
name: verify-specs
description: Phase 9 verification pass - check every spec against the contract and each other (contract-id coverage, unresolved and duplicate FR references, decisions traced to FRs, contradictions and glossary violations, session coverage, Mermaid compiling) and write docs/delivery/SPEC-VERIFICATION.md. Use after writing or changing specs, before planning, or when someone asks whether the specs are consistent.
---

# Verify the specs

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `verify-specs`).

Delegate to the `spec-verifier` agent (fresh context) with this task, then read its report:

1. **Contract coverage:** every contract id (atlas screen ids from the atlas build; operation ids from
   the API contract; datasets and columns from the data contract; commands; resources; eval cases) is
   cited by an FR of its owning spec, and no spec cites an id that does not exist.
2. **Cross-references:** every `NNN FR-xxx` resolves; no duplicate FR ids; checklist counts current.
3. **Decisions traced:** every DECISIONS.md entry maps to the FR that implements it.
4. **Contradictions:** numbers, copy, rules and field types that differ between specs; glossary
   *Not* words in copy or names.
5. **Session coverage** (once SESSIONS.md exists): every FR in some session's range; run
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py validate SESSIONS.md` too.
6. **Diagrams:** every story has a flow, and every Mermaid block compiles (`mmdc`), or NOT RUN with
   the reason.

Mechanical findings are fixed in place by the verifier; everything else goes to a *For the owner*
list in `docs/delivery/SPEC-VERIFICATION.md`. Gate (CHECKLIST.md §9): full coverage, 0 unresolved
references, 0 duplicate FRs, no `[NEEDS CLARIFICATION]`, and *For the owner* answered or deferred.
