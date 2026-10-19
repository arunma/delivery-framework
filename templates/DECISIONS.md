# Owner decisions

<!-- Guidance: the owner's word, dated. This file WINS over every other document (constitution,
specs, briefs, screen map) until those are amended to match. Agents write answers here the same day
they are given; never leave a decision only in chat. Group by theme; number every item so specs
can cite it (D1.2, R3.4 …). Never renumber; strike through and add a dated note instead. -->

**Status**: decided. These supersede anything in the constitution, the briefs or the specs that
disagrees. The screen map (`design/screen-map/`) is rebuilt from these, and the specs and sessions are written
from these and the screen map.

## D1 · <Theme, e.g. Brand, look and feel> (<YYYY-MM-DD>)
1. <Decision, one or two sentences. Name the screen ids or specs it touches.>
2. <Decision.> *(Changed <date>: <old> → <new>, because <reason>.)*

## D2 · <Theme, e.g. Backend for this build>
1. This build changes <scope>. Every screen that needs backend work ships reduced with a client
   fallback or is deferred.
2. Deferred out of this build: <spec / area>, because <no fallback>.
3. Critical items: <none | list with reason>.

## D3 · Screen map approval
1. Screen map approved on <date> at <commit or backup path>, <N> screens. Later changes go through the
   screen map source and are listed here.

## R<n> · <Round, e.g. plans> recommendations accepted (<YYYY-MM-DD>)
1. The owner accepted every recommendation in the round's list: <ids>. Exceptions: <id: the answer
   instead | none>. Until an item is answered, sessions build its recommendation.

## Answers to open questions (<date>)

| Question | Answer | Applied in |
| --- | --- | --- |
| Q1 | <answer, or "as recommended"> | <screen map part / spec FR / constitution version> |
