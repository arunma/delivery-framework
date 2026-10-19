# Owner decisions

<!-- Guidance: the owner's word, dated. This file WINS over every other document (constitution,
specs, briefs, atlas) until those are amended to match. Agents write answers here the same day
they are given; never leave a decision only in chat. Group by theme; number every item so specs
can cite it (D1.2, R3.4 …). Never renumber; strike through and add a dated note instead. -->

**Status**: decided. These supersede anything in the constitution, the briefs or the specs that
disagrees. The atlas (`design/atlas/`) is rebuilt from these, and the specs and sessions are written
from these and the atlas.

## D1 · <Theme, e.g. Brand, look and feel> (<YYYY-MM-DD>)
1. <Decision, one or two sentences. Name the screen ids or specs it touches.>
2. <Decision.> *(Changed <date>: <old> → <new>, because <reason>.)*

## D2 · <Theme, e.g. Backend for this build>
1. This build changes <scope>. Every screen that needs backend work ships reduced with a client
   fallback or is deferred.
2. Deferred out of this build: <spec / area>, because <no fallback>.
3. Critical items: <none | list with reason>.

## D3 · Atlas approval
1. Atlas approved on <date> at <commit or backup path>, <N> screens. Later changes go through the
   atlas source and are listed here.

## Answers to open questions (<date>)

| Question | Answer | Applied in |
| --- | --- | --- |
| Q1 | <answer, or "as recommended"> | <atlas part / spec FR / constitution version> |
