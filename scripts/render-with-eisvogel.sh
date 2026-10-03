#!/bin/bash
# Render first-principles analysis reports with Eisvogel template (LaTeX-based)
#
# Usage:
#   ./scripts/render-with-eisvogel.sh <report.md>
#   ./scripts/render-with-eisvogel.sh .first-principles/reports/2026-10-02T111530Z/report.md
#
# Requirements:
#   - pandoc (with LaTeX writer)
#   - xelatex or pdflatex (from LaTeX distribution)
#   - This repository (for access to the template)

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_FILE="$REPO_ROOT/shared/spine/references/report-layout-eisvogel.md"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check inputs
if [ $# -eq 0 ]; then
    echo "Usage: $0 <report.md> [output.pdf]"
    echo ""
    echo "Examples:"
    echo "  $0 .first-principles/reports/2026-10-02T111530Z/report.md"
    echo "  $0 report.md custom-output.pdf"
    exit 1
fi

REPORT_MD="$1"
OUTPUT_PDF="${2:-${REPORT_MD%.md}.eisvogel.pdf}"

# Validate inputs
if [ ! -f "$REPORT_MD" ]; then
    echo -e "${RED}✗ Report not found: $REPORT_MD${NC}"
    exit 1
fi

if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}✗ Eisvogel template not found at: $TEMPLATE_FILE${NC}"
    exit 1
fi

# Check dependencies
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}✗ Required command not found: $1${NC}"
        echo ""
        case "$1" in
            pandoc)
                echo "Install pandoc from: https://pandoc.org/installing.html"
                ;;
            xelatex)
                echo "Install LaTeX distribution:"
                echo "  macOS:    brew install basictex"
                echo "  Ubuntu:   sudo apt-get install texlive-xetex texlive-latex-extra"
                echo "  Windows:  Download from https://miktex.org/ or https://tug.org/texlive/"
                ;;
        esac
        return 1
    fi
}

echo "Checking dependencies..."
check_command pandoc || exit 1
check_command xelatex || {
    echo -e "${YELLOW}⚠ xelatex not found, trying pdflatex...${NC}"
    check_command pdflatex || exit 1
    PDF_ENGINE="pdflatex"
}
PDF_ENGINE="${PDF_ENGINE:-xelatex}"
echo -e "${GREEN}✓ Using PDF engine: $PDF_ENGINE${NC}"

# Extract template from markdown
echo "Extracting Eisvogel template..."
TEMP_TEMPLATE=$(mktemp)
trap "rm -f $TEMP_TEMPLATE" EXIT

if ! awk '/^```latex$/ { f = 1; next } f && /^```$/ { exit } f' "$TEMPLATE_FILE" > "$TEMP_TEMPLATE"; then
    echo -e "${RED}✗ Failed to extract template${NC}"
    exit 1
fi

if [ ! -s "$TEMP_TEMPLATE" ]; then
    echo -e "${RED}✗ Template is empty${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Template extracted ($(wc -c < "$TEMP_TEMPLATE") bytes)${NC}"

# Get title and date from report
REPORT_TITLE=$(sed -n '1s/^# //p' "$REPORT_MD" || echo "Analysis Report")
REPORT_DATE=$(date -u '+%-d %B %Y')

echo "Report title: $REPORT_TITLE"
echo "Report date: $REPORT_DATE"

# Prepare markdown for PDF (convert internal links)
echo "Rendering PDF with Eisvogel template..."
ERROR_FILE=$(mktemp)
trap "rm -f $TEMP_TEMPLATE $ERROR_FILE" EXIT

sed 's/ · \[Working file\][(][^)]*)//; s/](HOW-TO-READ\.md)/](HOW-TO-READ.pdf)/g; s/](INDEX\.md)/](INDEX.pdf)/g; s/\[\([^]]*\)\](\([^)]*\)\.md)/\1/g' "$REPORT_MD" | \
    pandoc -f commonmark_x \
        --template="$TEMP_TEMPLATE" \
        --pdf-engine="$PDF_ENGINE" \
        -M title="$REPORT_TITLE" \
        -M date="$REPORT_DATE" \
        -o "$OUTPUT_PDF" 2>"$ERROR_FILE"

RESULT=$?

if [ $RESULT -eq 0 ] && [ -f "$OUTPUT_PDF" ]; then
    SIZE=$(du -h "$OUTPUT_PDF" | cut -f1)
    echo -e "${GREEN}✓ PDF rendered successfully: $OUTPUT_PDF ($SIZE)${NC}"
    exit 0
else
    echo -e "${RED}✗ PDF rendering failed${NC}"
    if [ -s "$ERROR_FILE" ]; then
        echo "Error details:"
        cat "$ERROR_FILE" | head -20
    fi
    exit 1
fi
