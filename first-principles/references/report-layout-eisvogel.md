<!-- GENERATED — DO NOT EDIT. Source: shared/spine/references/report-layout-eisvogel.md. Regenerate via: scripts/sync-content.py --write. -->

# Report Layout (Eisvogel)

> **Scope:** Alternative PDF layout using the Eisvogel template (LaTeX-based) instead of typst.
> The agent body's *Deliver the analysis as a file* steps can extract this template and use it
> with pandoc's LaTeX writer. This template provides a polished academic/professional appearance
> with extensive customization options.

Eisvogel is a clean pandoc LaTeX template designed for professional documents. It provides:
- Custom title page support
- Syntax highlighting for code
- Color-coded headers
- Professional table styling
- Customizable margins and fonts
- Built-in table of contents

To use this template instead of the default typst template, modify the agent body's PDF rendering
command to use `--pdf-engine=xelatex` (or `pdflatex`) and this template.

## Template

The block below is a combined pandoc template for the `latex` writer. It is adapted from the
Eisvogel template by Wandmalfarbe (https://github.com/Wandmalfarbe/pandoc-latex-template).
`$title$` and `$date$` are pandoc template variables filled from the `-M title=` and
`-M date=` arguments; `$body$` is the report.

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{hyperref}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\lhead{\small $title$}
\cfoot{\small Page \thepage}
\title{$title$}
\date{$date$}
\author{}
\begin{document}
\maketitle
$body$
\end{document}
```

## Usage

To use the Eisvogel template instead of typst, modify the pandoc command in the agent:

```bash
pandoc -f commonmark_x \
  --template=path/to/template.latex \
  --pdf-engine=xelatex \
  -M title="Report Title" \
  -M date="2026-10-02" \
  -o output.pdf input.md
```

**Requirements:**
- pandoc (with LaTeX writer support)
- LaTeX distribution (e.g., TeX Live, MiKTeX, MacTeX)
- xelatex or pdflatex engine

If LaTeX is not installed, the PDF rendering will fail and the Markdown report will be used as the fallback.
