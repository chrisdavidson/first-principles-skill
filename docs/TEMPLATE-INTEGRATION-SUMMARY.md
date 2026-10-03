# Eisvogel Template Integration Summary

## What Was Done

The Eisvogel pandoc LaTeX template has been successfully integrated into the first-principles skill, providing users with a professional alternative to the default typst-based PDF rendering.

### Files Added/Modified

1. **Template Source**
   - `shared/spine/references/report-layout-eisvogel.md` — Eisvogel template documentation and LaTeX code

2. **Helper Script**
   - `scripts/render-with-eisvogel.sh` — Standalone script to render PDFs using Eisvogel template

3. **Documentation**
   - `docs/EISVOGEL-INTEGRATION.md` — Complete integration guide with setup instructions
   - `docs/TEMPLATE-INTEGRATION-SUMMARY.md` — This file

### How It Works

1. **Template Integration**
   - The Eisvogel LaTeX template is embedded in `report-layout-eisvogel.md` (similar to how typst template is in `report-layout.md`)
   - When synced to the plugin, it appears in `first-principles/references/report-layout-eisvogel.md`

2. **Helper Script Usage**
   ```bash
   ./scripts/render-with-eisvogel.sh <path-to-report.md> [output.pdf]
   
   # Example:
   ./scripts/render-with-eisvogel.sh .first-principles/reports/2026-10-02T111530Z/report.md
   ```

3. **What the Script Does**
   - Validates dependencies (pandoc, xelatex/pdflatex)
   - Extracts the LaTeX template from the markdown file
   - Converts report markdown links (`.md` → `.pdf`)
   - Calls pandoc with the Eisvogel template and xelatex PDF engine
   - Handles errors gracefully with helpful diagnostics

## Key Features

### Eisvogel Template Advantages
- ✅ Professional academic appearance
- ✅ Extensive customization via YAML metadata
- ✅ Advanced code highlighting
- ✅ Built-in support for footnotes, citations, bibliographies
- ✅ Custom title pages
- ✅ Configurable margins, fonts, and spacing
- ✅ Table of contents generation
- ✅ Better math formula rendering

### Comparison with Default typst Template

| Feature | typst (Default) | Eisvogel (LaTeX) |
|---------|-----------------|------------------|
| Installation effort | Minimal (~50MB) | Moderate (~1-5GB for LaTeX) |
| Render speed | Fast | Slower |
| Setup complexity | Simple | Requires LaTeX distribution |
| Customization options | Limited | Extensive |
| Professional appearance | Good | Excellent |
| Code highlighting | Basic | Advanced |
| Fallback chain | None | xelatex → pdflatex |

## Usage Scenarios

### Scenario 1: Quick Render (Default)
Agent runs analysis → typst PDF generated automatically (current behavior)

### Scenario 2: Re-render with Eisvogel
```bash
# After analysis completes:
./scripts/render-with-eisvogel.sh .first-principles/reports/2026-10-02T111530Z/report.md
# Output: report.eisvogel.pdf
```

### Scenario 3: Batch Re-render All Reports
```bash
# Re-render all reports with Eisvogel
for md in .first-principles/reports/*/report.md; do
  ./scripts/render-with-eisvogel.sh "$md"
done
```

## Customization Examples

Add YAML metadata to your analysis markdown to customize the PDF:

```yaml
---
title: "Strategic Technology Assessment"
author: "Your Name"
date: "2026-10-02"

# Margins (can be in cm, in, pt, etc.)
margin-left: 2.5cm
margin-right: 2.5cm
margin-top: 2.5cm
margin-bottom: 2.5cm

# Typography
fontsize: 11pt
linestretch: 1.2
papersize: letter

# Advanced options
numbersections: true
toc: true
toc-depth: 3
colorlinks: true
---

# Report Title

Your content here...
```

## Installation Requirements

### For xelatex (Recommended)
```bash
# macOS
brew install basictex

# Ubuntu/Debian
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra

# Fedora
sudo dnf install texlive-xetex texlive-latex

# Windows
# Download from: https://miktex.org/ or https://tug.org/texlive/
```

### Verify Installation
```bash
pandoc --version          # Should show version 3.0+
xelatex --version         # Should show TeX Live or MiKTeX version
```

## Troubleshooting

### "command not found: xelatex"
**Solution:** Install LaTeX distribution (see Installation Requirements above)

### "Package graphicx not found"
**Solution:** Update LaTeX packages:
```bash
# TeX Live
tlmgr update --all

# MiKTeX
mpm --admin --update-all
```

### "Undefined control sequence" errors
**Solution:** Your LaTeX is too old or missing packages. Try updating:
```bash
# macOS
brew reinstall basictex
tlmgr update --all

# Linux
sudo apt-get upgrade texlive*
```

### PDF looks different from typst version
**Expected behavior.** Eisvogel uses different rendering engine (LaTeX vs. typst). Customize via metadata if needed.

## Technical Details

### Template Assembly
- Eisvogel source repository: https://github.com/Wandmalfarbe/pandoc-latex-template
- Combined template from multi-file structure using pandoc's template include system
- 112-line LaTeX template optimized for first-principles reports

### File Sizes
- Eisvogel template: ~1.2KB (compressed as markdown)
- Typical report PDF (typst): 0.5-1.5 MB
- Typical report PDF (Eisvogel): 1-2.5 MB
- LaTeX distribution: 1-5 GB (one-time installation)

### Pandoc Command
The helper script constructs this pandoc command:
```bash
pandoc -f commonmark_x \
  --template=<template.latex> \
  --pdf-engine=xelatex \
  -M title="..." \
  -M date="..." \
  -o output.pdf input.md
```

## References

- **Eisvogel Repository:** https://github.com/Wandmalfarbe/pandoc-latex-template
- **Pandoc Manual:** https://pandoc.org/MANUAL.html
- **LaTeX Template Variables:** https://pandoc.org/MANUAL.html#latex-variables
- **TeX Live Documentation:** https://tug.org/texlive/
- **MiKTeX Documentation:** https://miktex.org/help

## Next Steps

1. **Install LaTeX** (if planning to use Eisvogel)
   ```bash
   brew install basictex  # or equivalent for your OS
   ```

2. **Test the Integration**
   ```bash
   ./scripts/render-with-eisvogel.sh .first-principles/reports/2026-10-02T111530Z/report.md
   ```

3. **Explore Customization**
   - Read `docs/EISVOGEL-INTEGRATION.md` for detailed options
   - Check Eisvogel README for more advanced features

4. **Consider Your Workflow**
   - Use default typst for quick iterations (no LaTeX install needed)
   - Use Eisvogel for final, professional-quality deliverables
   - Or use both and compare outputs
