---
phase: 06-final-skill-md-wiring-readme-and-validation
reviewed: 2026-05-18T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - .markdownlint.jsonc
  - dev/check-links.sh
  - README.md
  - first-principles-thinking/SKILL.md
  - first-principles-thinking/references/output-template.md
  - first-principles-thinking/references/validation-rubric.md
  - first-principles-thinking/examples/software-systems.md
findings:
  critical: 0
  warning: 5
  info: 6
  total: 11
status: issues_found
---

# Phase 6: Code Review Report

**Reviewed:** 2026-05-18
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

This phase wires up the final `SKILL.md`, the `README.md`, the markdownlint config, and a
host-side link-resolution check script. The skill files themselves resolve all cross-references
correctly (verified: all 9 internal targets exist; `dev/check-links.sh` reports "All links
resolve OK"). Frontmatter is valid and `name` matches the parent directory.

No BLOCKER issues found. However, the link-checking script — the one piece of executable code
in scope — has multiple correctness gaps that mean it gives a false sense of safety: it silently
ignores anchor links, mishandles the validation it claims to perform when run with a non-bash
shell, and has no protection against link text containing parentheses. There are also several
internal-consistency defects between `SKILL.md`, `output-template.md`, and `validation-rubric.md`
that will mislead the model applying the methodology. None are fatal, but the script is presented
as the project's validation gate and currently under-detects.

## Warnings

### WR-01: Link checker silently drops anchor links — broken `#section` links never detected

**File:** `dev/check-links.sh:14`
**Issue:** The extraction regex is `\[.*?\]\(\K[^)#]+`. The `[^)#]+` character class stops at the
first `#`, so any link of the form `[text](file.md#some-anchor)` is captured only as `file.md`
(the anchor is dropped). For a link that is *purely* an anchor — `[text](#section)` — the match
is empty or the link is skipped entirely. The script therefore cannot detect a broken intra-document
anchor or a broken `file.md#anchor` cross-reference. The script's banner claims it is a
"link-resolution check," but it only resolves the file portion. Today no skill file uses anchor
links (verified), so nothing is currently broken — but the script will continue to report
"All links resolve OK" the moment someone adds a `[...](output-template.md#derivation-chains)`
link that points at a heading that does not exist. A validation gate that cannot fail on a real
defect class is worse than no gate, because it is trusted.
**Fix:** Either (a) explicitly document the limitation in the banner comment ("does not validate
`#anchors`"), or (b) capture the full target including the anchor and validate the file portion,
then skip pure-anchor links deliberately:
```bash
# capture full target, strip anchor for file check
done < <(grep -oP '\[.*?\]\(\K[^)]+' SKILL.md references/*.md examples/*.md | grep -v '^http')
# inside loop:
link_file="${link_target%%#*}"
[ -z "$link_file" ] && continue   # pure in-document anchor; skip file check
resolved="$src_dir/$link_file"
```

### WR-02: Link checker breaks on link text or paths containing `:` or `)`

**File:** `dev/check-links.sh:7,14`
**Issue:** Two fragile assumptions in the parsing:
1. `grep -oP` is run across multiple files, so each output line is prefixed `filename:match`.
   The loop reads it with `IFS=: read -r source_file link_target`. If a link *target* ever
   contains a colon (e.g., a URL that slipped past the `grep -v '^http'`, or a path with a
   drive-letter-like segment), `read` splits on the first colon only and `link_target` keeps
   the rest — usually harmless, but a target like `a:b.md` is silently mis-parsed.
2. `\[.*?\]` is non-greedy but still matches across an unexpected `]` — and the `(\K[^)]` /
   `[^)#]` capture stops at the first `)`. A link whose *target* legitimately contains an
   encoded `)` would be truncated. More realistically, link *text* containing `]( ` patterns
   (nested brackets) can cause `.*?` to match the wrong opening bracket.
The script works on today's clean inputs but has no defense against these. As the project's
declared validation tool, it should be robust to the content it scans.
**Fix:** At minimum add a comment documenting the assumptions (no colons in targets, no nested
brackets, no parens in paths). Better: split only on the first colon explicitly and validate:
```bash
while IFS= read -r line; do
  source_file="${line%%:*}"
  link_target="${line#*:}"
  ...
```

### WR-03: Link checker has no `set -euo pipefail` and exits 0 on partial failure

**File:** `dev/check-links.sh:1-15`
**Issue:** The script has no `set -e`/`set -u`/`set -o pipefail`. Consequences:
- If `grep` in the process substitution fails (e.g., a glob `references/*.md` expands to nothing
  because the script is run from the wrong directory after the `cd` partially succeeds), the
  `while` loop simply iterates zero times and the script prints "All links resolve OK" — a
  false pass.
- The script never sets a non-zero exit code when broken links are found. Line 15 prints
  `"$BROKEN broken link(s)"` but the script still exits 0. A CI gate or `&&` chain calling this
  script cannot detect failure programmatically — it would have to parse stdout.
The project context calls this the link-validation gate; a gate that always exits 0 cannot gate.
**Fix:**
```bash
#!/usr/bin/env bash
set -euo pipefail
...
if [ "$BROKEN" -eq 0 ]; then
  echo "All links resolve OK"
else
  echo "$BROKEN broken link(s)"
  exit 1
fi
```
Note: `set -e` interacts with `$((BROKEN+1))` returning 0 — guard with `BROKEN=$((BROKEN+1)) || true`
or use `(( BROKEN++ )) || true`.

### WR-04: `output-template.md` requires "exactly one chain per conclusion" but `SKILL.md` only requires "at least one"

**File:** `first-principles-thinking/references/output-template.md:95` vs `first-principles-thinking/SKILL.md:97`
**Issue:** `output-template.md:95` states: *"Every conclusion offered in this analysis must have
exactly one chain here — no more (no redundant restatement), no fewer (no orphaned conclusions)."*
`SKILL.md:97` describes the Derivation Chains artifact as *"one chain per conclusion"* but the
Phase 4 exit criterion (`SKILL.md:99`) only requires *"every conclusion offered has a complete
derivation chain"* — it does not forbid more than one. The validation rubric Criterion 4
(`validation-rubric.md:243-244`) scores *Sound* (a downgrade) when *"a conclusion has more than
one derivation chain."* So the three documents disagree on whether multiple chains per conclusion
is forbidden, tolerated, or merely penalized. `SKILL.md` is named as the authoritative spec
(README.md:33) yet states the loosest rule. A model following `SKILL.md` could produce an
analysis the rubric then downgrades.
**Fix:** Make `SKILL.md` Phase 4 explicit and aligned: state "exactly one chain per conclusion"
in both the named-artifact description and the exit criterion, matching `output-template.md` and
the rubric.

### WR-05: D-XX requirement IDs are referenced but never defined in any reviewed file

**File:** `first-principles-thinking/SKILL.md:71,81,142,150` and `references/output-template.md:44,58,83,114,134,150` and `references/validation-rubric.md:166,224,237`
**Issue:** Three files repeatedly cite stable requirement IDs — `D-03`, `D-07` — as if they are
defined somewhere ("the confidence caveat rules from D-07", "The escape valve still satisfies
D-03", "or an explicit 'unverified — flagged' note per D-07"). None of the seven reviewed files
defines what `D-03` or `D-07` are, or points to where they are defined. A reader (or the model
applying the skill) is told to comply with `D-07` with no way to look up its text. Either these
IDs refer to a planning-doc requirement list that was never surfaced into the skill, or they are
dangling references. Citing an authority that the document never provides weakens exactly the
auditability the skill is built to deliver.
**Fix:** Either (a) add a short "Requirement IDs" glossary to `SKILL.md` or `output-template.md`
defining D-03, D-07, and any other D-XX referenced, or (b) replace the D-XX citations with the
inline rule text they stand for (the rules *are* stated nearby in prose — the IDs add nothing the
reader can act on). Option (b) is preferable for a self-contained skill.

## Info

### IN-01: `.markdownlint.jsonc` leaves `MD040` enabled but disables everything else — config is stricter than the CLAUDE.md spec describes

**File:** `.markdownlint.jsonc:1-6`
**Issue:** CLAUDE.md's tooling guidance says to "Disable `MD013`", "Keep `MD003`", "MD040", "MD041",
and "Optionally relax `MD033`". The committed config sets `"default": false` then re-enables only
`MD003`, `MD040`, `MD041`. That is a valid, minimal interpretation, but it also silently disables
useful rules the spec did not ask to disable (e.g., `MD009` trailing spaces, `MD012` multiple blank
lines, `MD047` file-should-end-with-newline). With `default: false`, every future rule is opt-out
by omission. This is a deliberate-looking choice, but undocumented.
**Fix:** Add a `// comment` in the JSONC explaining the `default: false` posture and why only three
rules are enabled, so a future maintainer does not assume rules are missing by accident.

### IN-02: `output-template.md` Ground Truth definition contradicts `SKILL.md` on derived facts

**File:** `first-principles-thinking/references/output-template.md:76` vs `first-principles-thinking/SKILL.md:80`
**Issue:** `output-template.md:76` says a ground truth must be *"not derived from another item on
this list."* `SKILL.md:80` (Phase 3 irreducibility test) says it *"cannot be simplified further
without losing its essential claim"* and *"can be traced to a verifiable source."* These are close
but not identical tests — "not derived from another GT" is a stricter, distinct constraint that
`SKILL.md` does not state. A reader cross-referencing the two will not know which test governs.
**Fix:** State the same irreducibility test verbatim in both files, or have one explicitly defer
to the other ("see SKILL.md Phase 3 for the irreducibility test").

### IN-03: README "five-phase" summary omits the rubric feedback-loop step present in SKILL.md

**File:** `README.md:19-31` vs `first-principles-thinking/SKILL.md:148-157`
**Issue:** The README describes the methodology as a five-phase procedure and folds rubric scoring
into Phase 5. `SKILL.md` actually presents the rubric Validate/Fix/Repeat loop as a *separate*
"Before presenting conclusions" section after the five phases (lines 148-157). The README's framing
is defensible (the rubric is *applied during* Phase 5) but a reader comparing the two will see a
structural mismatch. Minor.
**Fix:** Add one sentence to the README noting the rubric is applied as an explicit
validate-fix-repeat loop before conclusions are presented.

### IN-04: `check-links.sh` `cd` failure message is silent

**File:** `dev/check-links.sh:5`
**Issue:** `cd "$SKILL_DIR" || exit 1` exits with code 1 but prints nothing. If a user runs the
script from the wrong directory, it exits silently with no diagnostic. For a dev tool, a one-line
error message materially improves usability.
**Fix:** `cd "$SKILL_DIR" || { echo "error: cannot cd to $SKILL_DIR (run from repo root)" >&2; exit 1; }`

### IN-05: `grep -oP` is GNU-specific; script is not portable to macOS/BSD

**File:** `dev/check-links.sh:14`
**Issue:** `grep -oP` (Perl-compatible regex) and `grep -v '^http'` chained after it rely on GNU
grep. On macOS the default `grep` is BSD grep, which has no `-P`. The script will fail with an
unclear error on a Mac. The shebang is `#!/usr/bin/env bash`, implying cross-platform intent.
**Fix:** Document the GNU-grep requirement in the banner comment, or detect and warn:
`command -v ggrep >/dev/null && GREP=ggrep || GREP=grep`.

### IN-06: README install commands assume the clone lands in the current directory

**File:** `README.md:71-79`
**Issue:** The personal-install block runs `git clone ...` then immediately
`cp -r first-principles-skills/first-principles-thinking ...`. This only works if the user's
`pwd` after cloning is the parent of `first-principles-skills`. The symlink line uses
`"$(pwd)/first-principles-skills/..."`, reinforcing that assumption. It is correct but implicit;
a reader who `cd`s into the clone will have the wrong relative path. Minor doc-clarity issue.
**Fix:** Add a comment: `# run these from the directory where you cloned the repo (not inside it)`.

---

_Reviewed: 2026-05-18_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
