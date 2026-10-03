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

The block below is a professional pandoc template for the `latex` writer featuring a custom
cover page, table of contents, and professional business styling. It is adapted from the
Eisvogel template by Wandmalfarbe (https://github.com/Wandmalfarbe/pandoc-latex-template).
`$title$` and `$date$` are pandoc template variables filled from the `-M title=` and
`-M date=` arguments; `$body$` is the report content.

```latex
\documentclass[11pt,a4paper]{article}
\usepackage[utf-8]{inputenc}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{tocloft}

% Color definitions for professional appearance
\definecolor{navy}{RGB}{31,56,100}
\definecolor{slate}{RGB}{74,85,104}

% Configure links with navy color
\hypersetup{
  colorlinks=true,
  linkcolor=navy,
  urlcolor=navy,
  citecolor=navy,
  filecolor=navy
}

% Professional cover page with title and date
\makeatletter
\renewcommand{\maketitle}{
  \begin{titlepage}
    \centering
    \vspace*{60pt}
    {\fontsize{42}{50}\bfseries\textcolor{navy}$title$\par}
    \vspace{40pt}
    {\Large\textcolor{slate}First-Principles Analysis\par}
    \vspace*{\fill}
    {\Large\textcolor{slate}$date$\par}
    \vspace{20pt}
    {\normalsize\textcolor{slate}Professional Strategic Analysis\par}
    \vspace{20pt}
  \end{titlepage}
  \clearpage
}
\makeatother

% Professional table of contents styling
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\renewcommand{\cftsecfont}{\color{navy}\bfseries}
\renewcommand{\cftsubsecfont}{\color{slate}}
\setcounter{tocdepth}{2}

% Header and footer styling
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}
\lhead{\small\textcolor{slate}$title$}
\rhead{\small\textcolor{slate}First-principles analysis}
\cfoot{\small\textcolor{slate}Page \thepage\ of \pageref{LastPage}}
\fancypagestyle{plain}{\fancyhf{}\cfoot{\small\textcolor{slate}Page \thepage\ of \pageref{LastPage}}}

% Professional section heading styling
\usepackage{sectsty}
\sectionfont{\color{navy}\Large\bfseries}
\subsectionfont{\color{slate}\large}

% Title and author metadata
\title{$title$}
\date{$date$}
\author{}

\begin{document}

% Cover page
\maketitle

% Table of contents
\clearpage
\tableofcontents
\clearpage

% Document body
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
