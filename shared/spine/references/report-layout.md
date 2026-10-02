# Report Layout

> **Scope:** the page layout for the PDF reader report. The agent body's *Deliver the analysis
> as a file* steps extract the template below and pass it to pandoc; nothing here is read by the
> model for its content. The Markdown reader report needs no layout file — it is plain
> CommonMark, readable as text and in any Markdown viewer.

Each analysis produces two reader reports beside the working file
`.first-principles/analysis-<UTC>.md`:

- **`report-<UTC>.md`** — a title, a date line, the Executive Summary (the `## Answer` block,
  renamed), then the six sections. The process-output appendix, its structured summary,
  `**Disclosed:**` paragraphs and `**Pre-check:**` lines are left out: they are audit material
  for the working file, not for the reader. Where typst is installed and the working file's
  structured summary is readable, it also carries the assumption verdict matrix under §2 and the
  evidence trace under §4, drawn with typst from that summary and written beside it as
  `report-<UTC>-fig-verdicts.svg` and `report-<UTC>-fig-trace.svg`; without either, both
  reports are written without figures.
- **`report-<UTC>.pdf`** — the same Markdown typeset by pandoc with the typst PDF engine through
  the template below: US Letter, Noto Sans with Liberation Sans as fallback (both SIL Open Font
  License), a navy heading scheme, banded tables, a running header carrying the title, and a
  `Page N of M` footer.

Every tool on the PDF path is free software: pandoc (GPL-2.0-or-later), typst (Apache-2.0), and
the fonts above (SIL OFL-1.1). If pandoc or typst is not installed, the Markdown report is still
written and the PDF is skipped.

## Template

The block below is a pandoc template for the `typst` writer. `$title$` and `$date$` are pandoc
template variables, filled from the `-M title=` and `-M date=` arguments; `$body$` is the report.

```typst
// First-principles report: business layout for pandoc's typst writer.
#let navy = rgb("#1f3864")
#let slate = rgb("#4a5568")
#let rule-gray = rgb("#c9ced6")
#let band = rgb("#f2f4f7")

// typst 0.15 ships a built-in `divider()` function; pandoc's typst writer emits `#divider()`
// for a Markdown thematic break (`---`). Binding `divider` to a function (not a content value)
// here keeps that call working while giving the rule the report's own gray stroke.
#let divider() = line(length: 100%, stroke: 0.5pt + rule-gray)

#set document(title: [$title$])
#set page(
  paper: "us-letter",
  margin: (x: 0.9in, top: 0.95in, bottom: 0.9in),
  header: context {
    if here().page() > 1 {
      set text(size: 8pt, fill: slate)
      grid(columns: (1fr, auto), [$title$], [First-principles analysis])
      v(-4pt)
      line(length: 100%, stroke: 0.4pt + rule-gray)
    }
  },
  footer: context {
    set text(size: 8pt, fill: slate)
    line(length: 100%, stroke: 0.4pt + rule-gray)
    v(-4pt)
    grid(columns: (1fr, auto), [$date$],
      [Page #counter(page).display() of #counter(page).final().first()])
  },
)
#set text(font: ("Noto Sans", "Liberation Sans"), size: 9.5pt, fill: rgb("#1a202c"), lang: "en", hyphenate: false)
#set par(justify: false, leading: 0.62em, spacing: 0.95em)
#set list(indent: 0.4em, body-indent: 0.5em, spacing: 0.6em)
#set enum(indent: 0.4em, body-indent: 0.5em, spacing: 0.6em)
#set terms(hanging-indent: 1.5em)
#show link: set text(fill: navy)

// Level 1 is the report title; level 2 the numbered sections; level 3 below.
#show heading: set text(fill: navy, hyphenate: false)
#show heading.where(level: 1): it => {
  block(below: 0.6em, text(size: 21pt, weight: "bold", it.body))
}
#show heading.where(level: 2): it => {
  block(above: 1.9em, below: 0.8em, sticky: true, {
    text(size: 13.5pt, weight: "bold", it.body)
    v(-0.45em)
    line(length: 100%, stroke: 1.1pt + navy)
  })
}
#show heading.where(level: 3): it => block(above: 1.4em, below: 0.6em, sticky: true,
  text(size: 11pt, weight: "bold", it.body))
#show heading.where(level: 4): it => block(above: 1.1em, below: 0.5em, sticky: true,
  text(size: 9.5pt, weight: "bold", fill: slate, it.body))

// Tables: navy header row, light banding, horizontal rules only.
#set table(
  inset: (x: 5pt, y: 4.5pt),
  stroke: (x, y) => (bottom: 0.4pt + rule-gray),
  fill: (x, y) => if y == 0 { navy } else if calc.even(y) { band } else { none },
  align: left + top,
)
#show table.cell: set text(size: 8pt)
#show table.cell: set align(left + top)
#show table.cell: set par(leading: 0.5em, justify: false)
#show table.cell.where(y: 0): set text(fill: white, weight: "bold")
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)
#show figure: set block(above: 1em, below: 1.2em)

// Derivation chains and other preformatted text.
#show raw: set text(font: ("DejaVu Sans Mono", "Liberation Mono", "Noto Sans Mono"), size: 8pt)
#show raw.where(block: true): it => block(
  width: 100%, fill: band, inset: 8pt, radius: 2pt, stroke: (left: 2pt + navy), it)
#show raw.where(block: false): it => box(fill: band, inset: (x: 2pt), outset: (y: 2pt), radius: 1.5pt, it)
#show quote: it => block(inset: (left: 10pt, y: 2pt), stroke: (left: 2pt + rule-gray),
  text(fill: slate, it.body))

$body$
```
