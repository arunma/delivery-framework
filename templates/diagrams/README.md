# Diagrams

<!-- Guidance: copy to docs/diagrams/README.md. The rule: a diagram's SOURCE is committed, never
only an image. -->

Two kinds, one rule: **commit the source**.

| Kind | Tool | Where | For |
| --- | --- | --- | --- |
| Inline, canonical | Mermaid in markdown | `ARCHITECTURE.md`, `specs/*/spec.md`, `plan.md` | Every user flow per story, state machines, sequence diagrams (sync, auth, crypto handshakes), context, containers, data flow, deployment |
| Polished, interactive | archify (agent skill) | `docs/diagrams/<name>.json` (IR source) + `<name>.html` / `<name>.png` beside it | The architecture overview, key workflows and lifecycles for reviews and stakeholders |

GitHub and claude.ai artifacts render Mermaid natively. Keep Mermaid as the simple canonical form;
when a richer view is needed, ask the archify skill to convert the Mermaid source into its JSON IR,
then commit the JSON.

## Mermaid

- Compile before calling a doc done: `mmdc -i diagram.mmd -o /tmp/check.svg` (mermaid-cli), or the
  project's doc check.
- One diagram per flow; label edges with the action the person takes.
- Name nodes by screen id where a flow crosses screens (`07-item-actions`), so a diagram can be
  checked against the atlas.

## archify

Install once per machine: `tools/setup-tools.sh` (runs `npx skills add tt-a1i/archify -g`).

```bash
# ask the agent: "use archify to draw the <name> workflow from docs/diagrams/<name>.mmd"
# then validate (schema, layout, overlaps, every edge/route resolves):
node <archify skill dir>/bin/archify.mjs validate workflow docs/diagrams/<name>.json --quality showcase --json
```

Diagram types include architecture, workflow, sequence, data flow, lifecycle, ERD, class, tree,
timeline and waterfall; outputs are self-contained HTML plus PNG/WebP/JPG exports. Other
subcommands (`preview`, `deliver`, `guide`, `compare`, `doctor`) are described in archify's README.

`validate` runs in CI or the pre-PR checklist for every `docs/diagrams/*.json`. A session that
changes a flow updates its diagrams in the same session (Definition of done).

## graphify (code understanding, not diagrams)

`graphify-out/graph.html` is an interactive graph of the codebase. It is evidence, not
documentation: cite it in `ARCHITECTURE.md`, never replace a Mermaid diagram with it. Build it with
`graphify update .` (local, no AI calls). `graphify-out/` is gitignored; only `GRAPH_REPORT.md` is
committed.
