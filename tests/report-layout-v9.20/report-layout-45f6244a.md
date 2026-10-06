# Report Layout

> **Scope:** the page layout for the PDF reader report, and the folder index that links every
> delivered file. The agent body's *Deliver the analysis as a file* steps, and the persona skill,
> extract the template and the index script below by awk; nothing here is read by the model for
> its content. The Markdown reader report needs no layout file — it is plain
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

Every delivered file links to its neighbours, and the two formats never mix: a Markdown file
links only to Markdown files, and a PDF links only to PDFs. The working file has no PDF, so it is
linked from the Markdown files only. Each PDF render rewrites a link to a sibling that has a PDF
to point at that PDF, and turns any remaining link to a `.md` file into plain text:

- the reports carry a `Read with:` line under the date, linking the reading guide, the working
  file and the folder index;
- the reading guide's delivered copy ends with a link to the folder index;
- each persona memo's Basis field links its analysis, its report and the folder index;
- **`INDEX.md`** and **`INDEX.pdf`** list every analysis in the folder, newest first, with links
  to its report and each persona memo. Working files are not listed. `INDEX.md` links only the
  Markdown outputs and `INDEX.pdf` only the PDF outputs; an output with no PDF is left out of
  `INDEX.pdf`. The index is rewritten whenever an
  analysis is delivered and whenever a persona memo is written. The report is written before
  any memo exists, so this rewritten index is how the report reaches the memos.

Every tool on the PDF path is free software: pandoc (GPL-2.0-or-later), typst (Apache-2.0), and
the fonts above (SIL OFL-1.1). If pandoc or typst is not installed, the Markdown report is still
written and the PDF is skipped.

## Template

The block below is a pandoc template for the `typst` writer with professional features including
a cover page and auto-generated table of contents. `$title$` and `$date$` are pandoc template
variables, filled from the `-M title=` and `-M date=` arguments; `$body$` is the report content.

```typst
// First-principles report: professional business layout for pandoc's typst writer.
// Features: cover page, table of contents, business typography, professional styling.
#let navy = rgb("#1f3864")
#let slate = rgb("#4a5568")
#let rule-gray = rgb("#c9ced6")
#let band = rgb("#f2f4f7")
#let light-navy = rgb("#e8ecf1")

// typst 0.15 ships a built-in `divider()` function; pandoc's typst writer emits `#divider()`
// for a Markdown thematic break (`---`). Binding `divider` to a function (not a content value)
// here keeps that call working while giving the rule the report's own gray stroke.
#let divider() = line(length: 100%, stroke: 0.5pt + rule-gray)

#set document(title: [$title$], author: [First-Principles Analysis])

// Configure pages with different settings for cover page and content pages
#let cover-page = page(
  paper: "us-letter",
  margin: (x: 0.75in, y: 0.75in),
  header: none,
  footer: none,
  {
    set align(center + horizon)
    text(size: 48pt, weight: "bold", fill: navy, [$title$])
    v(2em)
    text(size: 16pt, fill: slate, [First-Principles Analysis])
    v(4em)
    text(size: 14pt, fill: slate, [$date$])
    v(1em)
    text(size: 11pt, fill: rule-gray, [Professional Strategic Analysis])
  }
)

#let content-page = page(
  paper: "us-letter",
  margin: (x: 0.9in, top: 0.95in, bottom: 0.9in),
  header: context {
    if here().page() > 2 {
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

#set page(content-page)

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

// Professional cover page
#cover-page

// Table of contents
#pagebreak()
#heading(level: 1, outlined: false, [Contents])
#outline(title: none, indent: 1em)

#pagebreak()

$body$
```

## Folder index

The block below is a POSIX `sh` script. Its first argument is the folder that holds the delivered
files. Its second argument is the path of this file, which it reads for the template above. It
rewrites `INDEX.md` and, if pandoc renders it, `INDEX.pdf`, and prints the path of each file it
writes. It only writes `INDEX.*` files. Each memo's display name comes from the memo's own title
line. In the PDF pass, `t` prints nothing for an output with no PDF, so that line is skipped.

```sh
D="$1"; L="$2"; cd "$D" || exit 1
emit() {
  ext="$1"
  t() { if [ "$ext" = pdf ]; then [ -s "${1%.md}.pdf" ] && printf '%s' "${1%.md}.pdf"; else printf '%s' "$1"; fi; }
  printf '# First-Principles Analyses\n\n'
  printf '*Every analysis in this folder, newest first, with its reader reports and memos.*\n\n'
  G=""; [ -s HOW-TO-READ.md ] && G=$(t HOW-TO-READ.md)
  [ -n "$G" ] && printf 'New to these reports? Start with [How to read this analysis]''(%s).\n\n' "$G"
  ls -1 analysis-*.md 2>/dev/null | sort -r | while read -r A; do
    U="${A#analysis-}"; U="${U%.md}"
    case "$U" in [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]Z) ;; *) continue ;; esac
    R="report-$U.md"; T=""
    [ -s "$R" ] && T=$(sed -n '1s/^# //p' "$R")
    [ -n "$T" ] || T="Analysis $U"
    printf '## %s\n\n' "$T"
    printf '*%s-%s-%s %s:%s UTC*\n\n' "$(echo "$U" | cut -c1-4)" "$(echo "$U" | cut -c5-6)" \
      "$(echo "$U" | cut -c7-8)" "$(echo "$U" | cut -c10-11)" "$(echo "$U" | cut -c12-13)"
    K=""; [ -s "$R" ] && K=$(t "$R")
    [ -n "$K" ] && printf -- '- [Report]''(%s)\n' "$K"
    ls -1 persona-*-"$U".md 2>/dev/null | while read -r P; do
      N=$(sed -n '1s/^# \(.*\) memo — .*$/\1/p' "$P"); K=$(t "$P")
      [ -n "$N" ] && [ -n "$K" ] && printf -- '- [%s memo]''(%s)\n' "$N" "$K"
    done
    printf '\n'
  done
}
emit md > INDEX.md.tmp && [ -s INDEX.md.tmp ] && mv INDEX.md.tmp INDEX.md && echo "$D/INDEX.md"
rm -f INDEX.md.tmp
if [ -s INDEX.md ] && [ -s "$L" ] && command -v pandoc >/dev/null 2>&1; then
  awk '/^```typst$/ { f = 1; next } f && /^```$/ { exit } f' "$L" > INDEX.layout.typ
  if emit pdf | pandoc -f commonmark_x --template=INDEX.layout.typ --pdf-engine=typst \
      -M title="First-Principles Analyses" -M date="$(date -u '+%-d %B %Y')" -o INDEX.pdf 2>/dev/null \
      && [ -s INDEX.pdf ]; then echo "$D/INDEX.pdf"; else rm -f INDEX.pdf; fi
  rm -f INDEX.layout.typ
fi
```
