# Phase 8 · Architecture

Brownfield: run `graphify update .` first if the graph is stale (local, no AI calls), and keep
`graphify-out/GRAPH_REPORT.md` open.

```
Write ARCHITECTURE.md for <PRODUCT> from <framework>/templates/ARCHITECTURE.md. Read CLAUDE.md, the
constitution, docs/delivery/DECISIONS.md, the screen map, design/BACKEND-SPLIT.md,
docs/delivery/BACKEND-AUDIT.md and the specs that exist.
Brownfield: use graphify-out/GRAPH_REPORT.md for the module map, dependencies and hot spots; use
graphify path / explain / affected to trace each key flow before reading files. Call edges can be
incomplete for some languages (e.g. widget construction in Dart): confirm with grep or the language
server before marking a claim [V]. Every claim about what exists
is [V] with path:line (at commit <sha>), or [?]. What this initiative adds is [P].
Greenfield: a target design; everything is [P].
Diagrams: Mermaid inline for the system context, containers/modules, every key flow (sequence),
every state machine, the data flow and the deployment. Compile each with `mmdc`. For the
architecture overview and the two or three key workflows, also produce archify diagrams: ask the
archify skill to convert the Mermaid source to its JSON IR, save it as docs/diagrams/<name>.json,
render the HTML and PNG beside it, and run
`node <archify skill dir>/bin/archify.mjs validate <type> docs/diagrams/<name>.json --quality showcase --json`
until it passes.
§12 lists every conflict found while writing; copy each to docs/delivery/DISCREPANCIES.md.
Report: sections, the [V]/[P]/[?] counts, the diagrams with their validation results, the conflicts
(ids).
```
