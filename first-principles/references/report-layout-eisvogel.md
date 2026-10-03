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
%%
% Copyright (c) 2017 - 2026, Pascal Wagler;
% Copyright (c) 2014 - 2026, John MacFarlane
%
% All rights reserved.
%
% Redistribution and use in source and binary forms, with or without modification,
% are permitted provided that the following conditions are met:
%
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
% AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
% IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
% DISCLAIMED.
%%
%
% This is the Eisvogel pandoc LaTeX template.
% For usage information and examples visit: https://github.com/Wandmalfarbe/pandoc-latex-template
%
\documentclass[$if(book)$twoside$endif$$if(fontsize)$, $fontsize$$endif$$if(papersize)$, $papersize$$endif$]{$if(book)$book$else$article$endif$}
\usepackage{geometry}
$if(geometry)$
\geometry{$geometry$}
$else$
\geometry{margin=2cm, marginparwidth=1.5cm, marginparsep=1.4cm}
$endif$
\usepackage[T1]{fontenc}
\usepackage[utf-8]{inputenc}
\usepackage{float}
\usepackage{graphicx}
\usepackage{grffile}
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\def\maxheight{\ifdim\Gin@nat@height>\textheight\textheight\else\Gin@nat@height\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth, height=\maxheight, keepaspectratio}
\usepackage{url}
\usepackage[unicode=true]{hyperref}
\hypersetup{$for(hypersetup)$$hypersetup$$sep$,$endfor$}
\usepackage[normalem]{ulem}
\usepackage{color}
\usepackage{fancyvrb}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\}}
\usepackage{listings}
$if(listings)$
\lstset{
  basicstyle=\ttfamily,
  columns=fullflexible,
  showstringspaces=false,
  commentstyle=\color{gray},
  keywordstyle=\bfseries\color{blue},
  stringstyle=\color{red},
  breaklines=true
}
$endif$
\usepackage{xcolor}
\definecolor{default-linkcolor}{HTML}{1f3864}
\definecolor{default-filecolor}{HTML}{1f3864}
\definecolor{default-citecolor}{HTML}{1f3864}
\definecolor{default-urlcolor}{HTML}{1f3864}
\hypersetup{
  colorlinks=true,
  linkcolor=default-linkcolor,
  filecolor=default-filecolor,
  citecolor=default-citecolor,
  urlcolor=default-urlcolor
}
\usepackage{amsmath,amssymb}
$if(fontfamily)$
\usepackage[$for(fontfamilyoptions)$$fontfamilyoptions$$sep$,$endfor$]{$fontfamily$}
$else$
\usepackage[default]{sourcesanspro}
$endif$
$if(csl-refs)$
\newlength{\cslhangindent}
\setlength{\cslhangindent}{1.5em}
\newlength{\csllabelsep}
\setlength{\csllabelsep}{0.6em}
\newenvironment{CSLReferences}[3]{
  \setlength{\parindent}{0pt}
  \everypar{\setlength{\hangindent}{\cslhangindent}\hspace{\csllabelsep}}
  \leavevmode}
{\par}
$endif$
\usepackage{geometry}
\usepackage{setspace}
$if(linestretch)$
\setstretch{$linestretch$}
$endif$
\geometry{margin=2.5cm, includehead=true, includefoot=true}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead{}
\fancyfoot{}
\lhead{$title$}
\rhead{First-principles analysis}
\cfoot{Page \thepage\ of \pageref*{LastPage}}
\usepackage{lastpage}
\author{$author$}
\date{$date$}
\title{$title$}
\begin{document}
$if(title)$
\maketitle
$endif$
$if(abstract)$
\begin{abstract}
$abstract$
\end{abstract}
$endif$
$table-of-contents$
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
