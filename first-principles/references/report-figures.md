<!-- GENERATED — DO NOT EDIT. Source: shared/spine/references/report-figures.md. Regenerate via: scripts/sync-content.py --write. -->

# Report Figures

> **Scope:** the typst figure library for the PDF reader report. Two figures: an evidence
> trace (ground truths to derivation chains to conclusion) and an assumption verdict matrix
> (taxonomy type by verdict). The agent body's step 7 under *Deliver the analysis as a file*
> compiles both figures from here; nothing in this file is read by the model for its content.
> A risk heat map and trade-off score bars were prototyped alongside these two and are
> deliberately not shipped -- their source data needs its own schema field and milestone.

## What each figure draws

**Evidence trace** reads `ground_truths[]`, `chains[]` and `conclusion` from the structured
summary (`shared/spine/references/summary-schema.json`). Three columns: every ground truth, every
derivation chain, and the conclusion. An edge is drawn for every entry in a chain's `rests_on`
array (ground-truth to chain or chain to chain) and for every entry in `conclusion.rests_on`
(chain to conclusion, or ground truth to conclusion directly) -- one edge per citation, not one
edge per node pair, so a chain cited twice by different `rests_on` entries draws twice. A ground
truth with no incoming or outgoing edge is still drawn: an orphaned ground truth is a real,
visible signal, never hidden. `conclusion.rests_on` is Phase 80's add-only field; it is `null` on
a legacy worked example whose section 6 carries no `**Pre-check:**` line, in which case the
conclusion node draws with zero edges rather than failing.

**Assumption verdict matrix** reads `assumptions[]`. Rows are the four schema taxonomy types
(`physical law`, `current constraint`, `convention`, `untested belief`), columns are the three
verdicts (`Accept`, `Challenge`, `Discard`); each cell counts the assumptions matching that
type/verdict pair. `type` is nullable only on legacy worked examples that predate the taxonomy
(`shared/spine/references/assumption-taxonomy.md` says these are never backfilled); when any such
null-typed assumption exists, the matrix draws one additional `untyped (legacy)` row so that the
drawn total always equals `assumptions.len()` -- the typed grid itself keeps its fixed 4x3 = 12
cells regardless.

## Visual encoding

Palette: navy `#1f3864`, slate `#4a5568`, rule-gray `#c9ced6` -- the same constants
`report-layout.md`'s PDF template uses. Chain and conclusion fill by confidence band: HIGH
`#2f6f4f`, MEDIUM `#b7791f`, LOW `#9b2c2c`. A ground-truth node is solid navy with white text when
`read_at_source` is true; white with a dashed navy border and a trailing ` ?` when false. An edge
whose citation carries a `?` suffix (an unverified ground truth) is dashed amber; every other
GT-to-chain edge is gray. Chain-to-chain edges are drawn in a lighter navy as rounded brackets to
the right of the chain column, each in its own vertical lane: shorter spans take the inner lanes so
longer ones nest around them rather than cross, edges whose spans do not overlap share a lane, and
every edge attaches at its own port on each node, so several edges into one chain (a chain resting
on many prior chains) stay visually distinct instead of overlapping. Both figures carry their legend
as part of the figure itself, not as separate report prose: one line under the trace, two short
lines under the matrix, set inside the matrix's own width so they cannot widen its canvas.

## Compiling and reading a figure

The block below is extracted the same way `report-layout.md`'s pandoc template is -- the awk
one-liner the agent body already runs:

```sh
awk '/^```typst$/ { f = 1; next } f && /^```$/ { exit } f' report-figures.md > figures.typ
```

Compile the extracted file directly (it is a standalone typst document, not a module to
`#import`), selecting a figure by the `figure` input and passing the structured-summary JSON
as the `summary` input:

```sh
typst compile --format svg --input figure=trace \
  --input summary="$(cat block.json)" figures.typ out.svg
```

`summary` travels as one shell argument -- Linux's per-argument `MAX_ARG_STRLEN` ceiling is
128 KiB, and a real analysis's structured-summary block runs a few KB (the tracked real-analysis
fixture under `tests/report-figures-v9.17/` is about 6.3 KB pretty-printed), so this is not a
practical limit today but is worth stating for a future much larger analysis. `figure` must be
`trace` or `verdicts`; a missing or unrecognized value fails the compile with a message naming
both allowed values, rather than silently drawing nothing.

Each figure stamps its drawn counts into a typst `#metadata` value, readable after compiling
without re-parsing the SVG. `typst query` is deprecated as of 0.15 (it still runs, with a
warning); use `typst eval` instead:

```sh
typst eval 'query(<fig-trace>).first().value' --in figures.typ \
  --input summary="$(cat block.json)" --input figure=trace
```

## Metadata fields

`<fig-trace>`: `gts` (drawn ground-truth nodes), `chains` (drawn chain nodes), `edges` (drawn
ground-truth-to-chain and chain-to-chain edges), `conclusion_edges` (drawn edges into the
conclusion, `0` when `conclusion.rests_on` is null or absent), `overflow` (count of labels whose
measured width exceeds the node or legend width they are drawn into -- zero on every fixture this
library ships with), `width` (the figure's own drawn width in points, `458`; the compiled SVG is
this plus the 6pt page margin on each side).

`<fig-verdicts>`: `cells` (always `12` -- the fixed 4x3 typed grid), `total` (every drawn count,
typed grid plus the `untyped (legacy)` row when it is drawn -- always equal to
`assumptions.len()`), `untyped` (drawn count in the `untyped (legacy)` row, `0` when it is not
drawn), `grid` (the twelve typed cell counts, row-major by type then verdict), `overflow` (same
meaning as above, over the matrix's type labels, header cells, and each legend line measured
against the matrix's own width), `width` (the matrix's drawn width in points: the label column plus
three verdict columns, `260`).

## Stated bounds

Labels are proven to fit at two-digit schema ids (`GT-99`, `C99 . MEDIUM` -- the widest id and
confidence-band label the schema's `GT-[1-9][0-9]*` / `C[1-9][0-9]*` patterns allow) with zero
measured overflow; see `tests/report-figures-v9.17/worst-case-labels.json`. Total figure width is
at most 470pt, including the page margin, and each SVG is exactly its figure's declared `width`
plus that margin -- the US Letter text column `report-layout.md`'s PDF
template lays out (0.9in side margins on an 8.5in page) is about 482pt wide. Fonts are Noto Sans
with Liberation Sans as fallback, both SIL Open Font License.

## Library

```typst
#set page(width: auto, height: auto, margin: 6pt)
// First-principles report figures: evidence trace + assumption verdict matrix.
#let navy = rgb("#1f3864")
#let slate = rgb("#4a5568")
#let rule-gray = rgb("#c9ced6")
#let conf-fill(c) = if c == "HIGH" { rgb("#2f6f4f") } else if c == "MEDIUM" { rgb("#b7791f") } else { rgb("#9b2c2c") }

#let S = json(bytes(sys.inputs.at("summary")))
#let which = sys.inputs.at("figure", default: none)

#let evidence-trace(S) = {
  set text(font: ("Noto Sans", "Liberation Sans"), size: 8pt)
  let gts = S.ground_truths
  let chains = S.chains
  let concl = S.conclusion

  let row-h = 16pt
  let node-h = 13pt
  let node-inset = 4pt
  let col-x = (0pt, 170pt, 364pt)
  // Sized from the widest schema-allowed label: bold "C99 · MEDIUM" measures ~55pt at
  // 8pt in Noto Sans/Liberation Sans (measured live); this leaves a comfortable margin.
  let node-w = 84pt
  let concl-w = 84pt
  let concl-h = 34pt

  let gt-index = (:)
  for (i, g) in gts.enumerate() { gt-index.insert(g.id, i) }
  let ch-index = (:)
  for (i, c) in chains.enumerate() { ch-index.insert(c.id, i) }

  let gt-gap = row-h
  let H = calc.max(gts.len() * gt-gap, node-h + 10pt)
  let gt-y(i) = i * gt-gap
  let ch-gap = if chains.len() > 0 { H / chains.len() } else { H }
  let ch-y(i) = i * ch-gap + (ch-gap - node-h) / 2
  let concl-y = H / 2 - concl-h / 2

  // Chain-to-chain arcs: each gets its own vertical lane right of the chain column. Shorter
  // spans take inner lanes, so longer arcs nest around them instead of crossing; arcs whose
  // spans do not overlap share a lane. Each arc also gets its own attachment port on both nodes.
  let cc = ()
  for (j, c) in chains.enumerate() {
    for (k, ref) in c.rests_on.enumerate() {
      if ref in ch-index { cc.push((i: ch-index.at(ref), j: j, k: k)) }
    }
  }
  let order = range(cc.len()).sorted(key: n => calc.abs(cc.at(n).i - cc.at(n).j))
  let lane-of = (:)
  let lanes = ()
  for n in order {
    let lo = calc.min(cc.at(n).i, cc.at(n).j)
    let hi = calc.max(cc.at(n).i, cc.at(n).j)
    let placed = false
    for (l, spans) in lanes.enumerate() {
      if not placed and spans.all(s => hi < s.at(0) or lo > s.at(1)) {
        lanes.at(l).push((lo, hi)); lane-of.insert(str(n), l); placed = true
      }
    }
    if not placed { lanes.push(((lo, hi),)); lane-of.insert(str(n), lanes.len() - 1) }
  }
  let lane-room = col-x.at(2) - (col-x.at(1) + node-w) - 24pt
  let lane-step = if lanes.len() > 0 { calc.min(9pt, lane-room / lanes.len()) } else { 0pt }
  let port-count = (:)
  for e in cc {
    for x in (e.i, e.j) { port-count.insert(str(x), port-count.at(str(x), default: 0) + 1) }
  }
  let port-used = (:)
  let port-y = (:)
  for (n, e) in cc.enumerate() {
    for (side, x) in (("a", e.i), ("b", e.j)) {
      let used = port-used.at(str(x), default: 0)
      let total = port-count.at(str(x))
      port-y.insert(str(n) + side, ch-y(x) + 2pt + (node-h - 4pt) * (used + 1) / (total + 1))
      port-used.insert(str(x), used + 1)
    }
  }
  let cc-at = (:)
  for (n, e) in cc.enumerate() { cc-at.insert(str(e.j) + "-" + str(e.k), n) }

  let edges = ()
  for (j, c) in chains.enumerate() {
    for (k, ref) in c.rests_on.enumerate() {
      let unverified = ref.ends-with("?")
      let id = if unverified { ref.slice(0, -1) } else { ref }
      if id in gt-index {
        let i = gt-index.at(id)
        edges.push(place(curve(
          stroke: (paint: if unverified { rgb("#b7791f") } else { rule-gray.darken(20%) },
                   thickness: 0.7pt, dash: if unverified { "dashed" } else { none }),
          curve.move((col-x.at(0) + node-w, gt-y(i) + node-h / 2)),
          curve.cubic(
            (col-x.at(0) + node-w + 50pt, gt-y(i) + node-h / 2),
            (col-x.at(1) - 50pt, ch-y(j) + node-h / 2),
            (col-x.at(1), ch-y(j) + node-h / 2)))))
      } else if id in ch-index {
        let n = cc-at.at(str(j) + "-" + str(k))
        let x0 = col-x.at(1) + node-w
        let xl = x0 + 8pt + lane-step * (lane-of.at(str(n)) + 1)
        let ya = port-y.at(str(n) + "a")
        let yb = port-y.at(str(n) + "b")
        let r = calc.min(4pt, calc.abs(yb - ya) / 2)
        let dir = if yb > ya { 1 } else { -1 }
        edges.push(place(curve(
          stroke: (paint: navy.lighten(45%), thickness: 0.6pt),
          curve.move((x0, ya)),
          curve.line((xl - r, ya)),
          curve.quad((xl, ya), (xl, ya + dir * r)),
          curve.line((xl, yb - dir * r)),
          curve.quad((xl, yb), (xl - r, yb)),
          curve.line((x0, yb)))))
      }
    }
  }
  let drawn-edges = edges

  let concl-refs = if concl.at("rests_on", default: none) != none { concl.rests_on } else { () }
  let concl-edges = ()
  for ref in concl-refs {
    let unverified = ref.ends-with("?")
    let id = if unverified { ref.slice(0, -1) } else { ref }
    if id in ch-index {
      let j = ch-index.at(id)
      concl-edges.push(place(curve(
        stroke: (paint: conf-fill(chains.at(j).confidence), thickness: 1pt),
        curve.move((col-x.at(1) + node-w, ch-y(j) + node-h / 2)),
        curve.line((col-x.at(2), concl-y + concl-h / 2)))))
    } else if id in gt-index {
      let i = gt-index.at(id)
      concl-edges.push(place(curve(
        stroke: (paint: rgb("#b7791f"), thickness: 1pt, dash: "dashed"),
        curve.move((col-x.at(0) + node-w, gt-y(i) + node-h / 2)),
        curve.line((col-x.at(2), concl-y + concl-h / 2)))))
    }
  }

  let legend-str = "Solid = read at source · dashed = not read at source (?) · fill = confidence · amber dashed = unverified input"

  box(width: 458pt, height: H + 40pt, {
    place(dx: col-x.at(0), dy: 0pt, text(weight: "bold", fill: navy)[Ground truths])
    place(dx: col-x.at(1), dy: 0pt, text(weight: "bold", fill: navy)[Derivation chains])
    place(dx: col-x.at(2), dy: 0pt, text(weight: "bold", fill: navy)[Conclusion])
    place(dy: 16pt, box({
      for e in drawn-edges { e }
      for e in concl-edges { e }
      for (i, g) in gts.enumerate() {
        place(dx: col-x.at(0), dy: gt-y(i), rect(width: node-w, height: node-h, radius: 2pt, inset: node-inset,
          fill: if g.read_at_source { navy } else { white },
          stroke: if g.read_at_source { none } else { (paint: navy, dash: "dashed", thickness: 0.7pt) },
          align(center + horizon, text(size: 7pt, fill: if g.read_at_source { white } else { navy },
            g.id + if g.read_at_source { "" } else { " ?" }))))
      }
      for (j, c) in chains.enumerate() {
        place(dx: col-x.at(1), dy: ch-y(j), rect(width: node-w, height: node-h, radius: 2pt, inset: node-inset,
          fill: conf-fill(c.confidence),
          align(center + horizon, text(size: 7pt, fill: white, weight: "bold", c.id + " · " + c.confidence))))
      }
      place(dx: col-x.at(2), dy: concl-y, rect(width: concl-w, height: concl-h, radius: 3pt, inset: node-inset,
        fill: conf-fill(concl.confidence),
        align(center + horizon, text(size: 7pt, fill: white, weight: "bold")[Recommendation \ #concl.confidence])))
    }))
    place(dy: H + 28pt, text(size: 6.5pt, fill: slate, legend-str))
  })

  context {
    let checks = ()
    for g in gts {
      checks.push((text(size: 7pt, g.id + if g.read_at_source { "" } else { " ?" }), node-w - 2 * node-inset))
    }
    for c in chains {
      checks.push((text(size: 7pt, weight: "bold", c.id + " · " + c.confidence), node-w - 2 * node-inset))
    }
    checks.push((text(size: 7pt, weight: "bold", "Recommendation"), concl-w - 2 * node-inset))
    checks.push((text(size: 7pt, weight: "bold", concl.confidence), concl-w - 2 * node-inset))
    checks.push((text(size: 6.5pt, legend-str), 458pt))
    let overflow = checks.filter(pair => measure(pair.at(0)).width > pair.at(1)).len()
    [#metadata((gts: gts.len(), chains: chains.len(), edges: drawn-edges.len(), conclusion_edges: concl-edges.len(), overflow: overflow, width: 458)) <fig-trace>]
  }
}

#let verdict-matrix(S) = {
  set text(font: ("Noto Sans", "Liberation Sans"), size: 8pt)
  let types = ("physical law", "current constraint", "convention", "untested belief")
  let verdicts = ("Accept", "Challenge", "Discard")
  let cell-count(t, v) = S.assumptions.filter(a => a.type == t and a.verdict == v).len()
  let untyped-count(v) = S.assumptions.filter(a => a.type == none and a.verdict == v).len()
  let has-untyped = S.assumptions.filter(a => a.type == none).len() > 0

  let col-w = 50pt
  let label-w = 110pt
  let fig-w = label-w + col-w * 3

  let grid = ()
  let body-rows = ()
  for t in types {
    let row-cells = ()
    for v in verdicts {
      let n = cell-count(t, v)
      grid.push(n)
      row-cells.push(table.cell(fill: if n == 0 { none } else { navy.transparentize(100% - calc.min(n * 14%, 90%)) },
        text(fill: if n >= 4 { white } else { black }, str(n))))
    }
    body-rows.push((table.cell(align: left, t),) + row-cells)
  }

  let untyped-cells = ()
  for v in verdicts {
    let n = untyped-count(v)
    untyped-cells.push(table.cell(fill: if n == 0 { none } else { navy.transparentize(100% - calc.min(n * 14%, 90%)) },
      text(fill: if n >= 4 { white } else { black }, str(n))))
  }
  let untyped-row = (table.cell(align: left, text(style: "italic", "untyped (legacy)")),) + untyped-cells

  let legend-lines = ("Shading darkens with count.", "An untyped (legacy) row appears only for assumptions with no type.")

  let all-rows = body-rows.flatten() + (if has-untyped { untyped-row } else { () })

  box(width: fig-w, {
    table(columns: (label-w,) + (col-w,) * 3, align: center + horizon, inset: 4pt, stroke: 0.5pt + rule-gray,
      table.header(text(weight: "bold", "Type"), ..verdicts.map(v => text(weight: "bold", v))),
      ..all-rows)
    v(4pt)
    for line in legend-lines { block(above: 2pt, below: 0pt, text(size: 6.5pt, fill: slate, line)) }
  })

  context {
    let checks = (
      (text(weight: "bold", "Type"), label-w - 8pt),
    )
    for v in verdicts {
      checks.push((text(weight: "bold", v), col-w - 8pt))
    }
    for t in types {
      checks.push((text(t), label-w - 8pt))
    }
    if has-untyped {
      checks.push((text(style: "italic", "untyped (legacy)"), label-w - 8pt))
    }
    for line in legend-lines { checks.push((text(size: 6.5pt, line), fig-w)) }
    let overflow = checks.filter(pair => measure(pair.at(0)).width > pair.at(1)).len()
    let untyped-total = verdicts.map(v => untyped-count(v)).sum()
    let total = grid.sum() + untyped-total
    [#metadata((cells: 12, total: total, untyped: untyped-total, grid: grid, overflow: overflow, width: int(fig-w / 1pt))) <fig-verdicts>]
  }
}

#if which == "trace" {
  evidence-trace(S)
} else if which == "verdicts" {
  verdict-matrix(S)
} else {
  panic("unknown figure input " + repr(which) + "; expected one of: trace, verdicts")
}
```
