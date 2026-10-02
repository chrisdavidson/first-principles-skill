# Visual Inspection: Report Figures

> Every `.png` written by `scripts/check-report-figures.py --render` was opened with the Read
> tool, one by one, in full -- no sampling. This record is the complement to the FIG-GATE
> self-test's mechanical `overflow == 0` assertion: the gate proves labels fit their boxes; this
> record proves the figure reads as a human-facing image.

- **Date:** 2026-10-02
- **Commit:** `b559977d`
- **typst version:** `typst 0.15.1 (9dfd3a08)`
- **Render command:** `python3 scripts/check-report-figures.py --render <scratch dir>`
- **PNGs produced:** 32 (16 fixtures x 2 figures), exit 0
- **Images opened with Read:** 32 (one per PNG; the real-analysis `trace` figure was additionally
  inspected via three higher-resolution (400 ppi) crops -- GT column, chain-column/C8 lane
  convergence, and conclusion -- to judge the 7-arc C8 case closely per the plan's instruction;
  those three crops are not separate rows, they informed the one `analysis-...json | trace` row
  below)

## Judging criteria applied to every image

1. Every node/cell label fully inside its box; none clipped or overlapping a neighbour.
2. Text legible at rendered size (8pt at 144 ppi), sans-serif (a serif face would mean the font
   fallback failed -- prototype lesson 1).
3. Nothing cut at the image edge; legend fully present.
4. Trace only -- read-at-source GTs solid navy, unverified dashed with ` ?`; amber dashed edges
   from `?` inputs; chain-to-chain edges distinguishable from GT-to-chain edges; every edge into
   the conclusion present (GT-18 on the real fixture connects to the conclusion directly, not an
   orphan); any genuine orphan GT still drawn; chain/conclusion fills match their confidence; each
   chain-to-chain arc in its own lane, distinct and traceable, no arc crossing a node or a label,
   no lane touching the conclusion node.
5. Verdicts only -- cell numbers sum to the fixture's assumption count; `untyped (legacy)` row
   appears exactly on fixtures with null-typed assumptions; an empty-assumptions example renders
   an all-zero grid rather than breaking.

## Verdicts

| Fixture | Figure | Verdict | Notes |
| --- | --- | --- | --- |
| tests/report-figures-v9.17/analysis-20261001T204943Z.json | trace | OK | 18 GTs (GT-1..12 solid navy, GT-13..18 dashed navy with ` ?`), 8 chains, legend present. C8's 7 chain-to-chain arcs (C1..C7 -> C8) each render in their own nested lavender lane right of the chain column, confirmed at 400 ppi: ports are stacked but distinct and stay within C8's node-height band, no lane crosses a node or a label, no lane reaches past the chain column into the conclusion's side. GT-18's dashed amber edge runs directly to the conclusion (visible crossing the chain column diagonally, distinct from the lavender lanes), confirming it is not an orphan. Green/gold solid+dashed edges into Recommendation are all present and distinguishable from the C-to-C lanes. |
| tests/report-figures-v9.17/analysis-20261001T204943Z.json | verdicts | OK | 4x3 typed grid, no untyped row (none in this fixture), cell numbers legible, shading scales with count, grid sums to 17. |
| tests/report-figures-v9.17/worst-case-labels.json | trace | OK | Widest schema-allowed labels (`GT-82..99`, `C92..99 . MEDIUM`) all fit their node width with margin; no clipping; legend present. |
| tests/report-figures-v9.17/worst-case-labels.json | verdicts | OK | Same widest-label grid as the real fixture (shares assumption data); labels fit, shading legible. |
| shared/examples/composed-inversion-second-order.md | trace | OK | 5 GTs (GT-5 unverified, dashed amber edge into C1), 1 chain, conclusion node drawn with zero edges (legacy example, `conclusion.rests_on` null -- matches the documented fallback, not a defect). |
| shared/examples/composed-inversion-second-order.md | verdicts | OK | `untyped (legacy)` row present (1 Accept, 1 Challenge) -- this is one of the two fixtures with null-typed assumptions named in the CONTEXT; totals correct. |
| shared/examples/decompose-irreducibility.md | trace | OK | 8 GTs, 1 chain, conclusion drawn with zero edges (legacy, no Pre-check line). |
| shared/examples/decompose-irreducibility.md | verdicts | OK | All-zero 4x3 grid -- the empty-assumptions case renders cleanly rather than breaking, per spec. |
| shared/examples/estimate-fermi.md | trace | OK | 5 GTs (GT-7 unverified), 1 chain with a solid gold edge straight to the conclusion -- conclusion edge present and legible. |
| shared/examples/estimate-fermi.md | verdicts | OK | All-zero 4x3 grid, renders cleanly. |
| shared/examples/ishikawa-fishbone.md | trace | OK | 5 GTs (GT-5 unverified, dashed amber into C3), 3 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/ishikawa-fishbone.md | verdicts | OK | Typed grid only (no untyped row), totals correct, shading legible. |
| shared/examples/personal-general-2.md | trace | OK | 6 GTs (GT-3 unverified, two dashed amber edges into C1/C2), 3 chains by confidence (LOW/LOW/MEDIUM), conclusion LOW with zero edges (legacy). |
| shared/examples/personal-general-2.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/personal-general.md | trace | OK | 5 GTs, 2 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/personal-general.md | verdicts | OK | `untyped (legacy)` row present (0/1/0) -- second of the two null-typed fixtures named in the CONTEXT; totals correct. |
| shared/examples/product-business-2.md | trace | OK | 5 GTs (GT-5 unverified), 3 chains, solid gold/green edges into the conclusion from C1 and C3, legible and distinct. |
| shared/examples/product-business-2.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/product-business.md | trace | OK | 4 GTs (GT-4 unverified, dashed amber edges), 3 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/product-business.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/science-engineering-2.md | trace | OK | 7 GTs (GT-2 and GT-7 unverified), 2 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/science-engineering-2.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/science-engineering.md | trace | OK | 5 GTs (GT-5 unverified, dashed amber edges into both chains), 2 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/science-engineering.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/self-application.md | trace | OK | 9 GTs (GT-9 unverified), 3 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/self-application.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/software-systems-2.md | trace | OK | 7 GTs (GT-7 unverified), 3 chains, conclusion drawn with zero edges (legacy). |
| shared/examples/software-systems-2.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/software-systems.md | trace | OK | 5 GTs, 3 chains all HIGH, conclusion drawn with zero edges (legacy). |
| shared/examples/software-systems.md | verdicts | OK | Typed grid only, legible. |
| shared/examples/theoretical-limit-carnot.md | trace | OK | 4 GTs, 1 chain, conclusion drawn with zero edges (legacy). |
| shared/examples/theoretical-limit-carnot.md | verdicts | OK | Typed grid only, legible. |

## Defects found and fixed

None. All 32 rendered images passed inspection against the five judging criteria above on the
first render -- no library change was needed. The one case most likely to show a defect (C8's
7-converging chain-to-chain arcs in the real-analysis fixture, singled out by the user as the
hardest case after commit `b559977d` gave each arc its own lane) was inspected at 400 ppi
specifically to verify the lanes stay distinct, stay off the node labels, and stay off the
conclusion node, and no overlap or crossing was observed.
