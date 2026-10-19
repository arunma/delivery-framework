# Phase 7 · Constitution

```
Write (or amend) .specify/memory/constitution.md for <PRODUCT>, using /speckit.constitution or
directly, from <framework>/templates/constitution.md and docs/delivery/DECISIONS.md. Keep it short
(200–300 lines).
- Product principles first: what the product promises the person (from the decisions and the
  interview/survey). Each states MUST/MUST NOT and gives a one-line rationale.
- Then the framework principles: nothing fails silently; one concept, one name; tested at three
  layers; accessible by construction; minimal backend (fallback, deferred or critical); measured
  performance only; the atlas is the contract; one visual language; built screens match the atlas
  (parity, independent reviewer).
- Technical constraints, the development workflow (Jira as the progress record; the closing order;
  the simpler-way review; stop on disagreement; never renumber), and governance (non-negotiables,
  waivers with a dated follow-up, MAJOR/MINOR/PATCH, Constitution Check in every plan).
- Mark as NON-NEGOTIABLE only the principles the owner has chosen: <list or "ask">.
- Update the Sync Impact Report. Then update CLAUDE.md §1 to the same version, and search the repo
  for the old version string; list every file that still cites it.
Where DECISIONS.md and the draft disagree, the decisions win; say where. Report: version, the
principles (non-negotiable marked), the files still citing an old version.
```

**Amendment** (later): same prompt, with "Amend for <decision ids>". Bump MAJOR if a principle is
removed or redefined, MINOR if one is added or expanded, PATCH for wording.
