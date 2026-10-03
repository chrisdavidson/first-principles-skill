# Eisvogel PDF Template Integration

The first-principles skill now supports rendering PDFs with the **Eisvogel** template, a professional LaTeX-based pandoc template as an alternative to the default typst template.

## Quick Start

### 1. Install Requirements

Eisvogel requires a LaTeX distribution:

```bash
# macOS
brew install basictex

# Ubuntu/Debian  
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra

# Windows
# Download and install MiKTeX or TeX Live from:
# - https://miktex.org/download
# - https://tug.org/texlive/
```

### 2. Use the Eisvogel Template

After running a first-principles analysis, you can re-render PDFs with Eisvogel:

```bash
#!/bin/bash
# Re-render a report with Eisvogel template

REPORT_MD=".first-principles/reports/2026-10-02T111530Z/report.md"
TEMPLATE_PATH="$(find . -path "*/references/report-layout-eisvogel.md" -type f | head -1)"

if [ ! -f "$TEMPLATE_PATH" ]; then
  echo "Error: Could not find Eisvogel template"
  exit 1
fi

# Extract template from markdown
TEMP_TEMPLATE=$(mktemp)
awk '/^```latex$/ { f = 1; next } f && /^```$/ { exit } f' "$TEMPLATE_PATH" > "$TEMP_TEMPLATE"

# Render PDF
OUTPUT_PDF="${REPORT_MD%.md}.eisvogel.pdf"
sed 's/ · \[Working file\][(][^)]*)//; s/](HOW-TO-READ\.md)/](HOW-TO-READ.pdf)/g; s/](INDEX\.md)/](INDEX.pdf)/g; s/\[\([^]]*\)\](\([^)]*\)\.md)/\1/g' "$REPORT_MD" | \
  pandoc -f commonmark_x \
    --template="$TEMP_TEMPLATE" \
    --pdf-engine=xelatex \
    -M title="$(sed -n '1s/^# //p' "$REPORT_MD")" \
    -M date="$(date -u '+%-d %B %Y')" \
    -o "$OUTPUT_PDF" 2>&1

rm -f "$TEMP_TEMPLATE"

if [ -f "$OUTPUT_PDF" ]; then
  echo "✓ PDF rendered: $OUTPUT_PDF"
else
  echo "✗ PDF rendering failed"
  exit 1
fi
```

### 3. Customization

The Eisvogel template supports many customization options via YAML metadata. Add to your Markdown report:

```yaml
---
title: "First-Principles Analysis"
author: "Your Name"
date: "2026-10-02"
margin-left: 2.5cm
margin-right: 2.5cm
margin-top: 2.5cm
margin-bottom: 2.5cm
fontsize: 11pt
papersize: letter
linestretch: 1.2
---
```

### 4. Template Comparison

| Feature | typst (Default) | Eisvogel (LaTeX) |
|---------|-----------------|------------------|
| **Installation** | typst binary | Full LaTeX dist |
| **File Size** | Smaller | Larger |
| **Customization** | Limited | Extensive |
| **Code Highlighting** | Basic | Advanced (with `listings`) |
| **Mathematical Formulas** | Native support | Native support |
| **Title Page** | Simple | Customizable |
| **Margins** | Fixed | Fully configurable |
| **Installation Size** | ~50 MB | ~1-5 GB |
| **Speed** | Fast | Slower |

## Files

- **Template source:** `shared/spine/references/report-layout-eisvogel.md`
- **Generated in plugin:** `first-principles/references/report-layout-eisvogel.md`
- **Helper script:** `scripts/render-with-eisvogel.sh` (create manually or request)

## Troubleshooting

### "xelatex not found"
Install LaTeX: `brew install basictex` (macOS) or equivalent for your OS.

### "Undefined control sequence"
Update LaTeX packages: `tlmgr update --all` (if using TeX Live)

### PDF looks different from typst version
This is expected—Eisvogel uses a different layout engine. Customize via YAML metadata to match your preferences.

## References

- **Eisvogel Repository:** https://github.com/Wandmalfarbe/pandoc-latex-template
- **Pandoc LaTeX Template Variables:** https://pandoc.org/MANUAL.html#latex-variables
- **Eisvogel Documentation:** https://github.com/Wandmalfarbe/pandoc-latex-template/blob/master/README.md
