# Persona views

A persona view is a sibling overlay of one delivered analysis, never an edit of it. It restates
only what the analysis already says, cited back to the analysis; the six sections of the
analysis remain the source of truth. A persona view adds no claim the analysis does not already
carry.

## Persona roster

| Slug | Title | Body words |
|------|-------|------------|
| decision-owner | Decision Owner | 80–120 |
| operator | Operator | 100–150 |
| risk | Risk | 100–150 |
| skeptic | Skeptic | 80–120 |

This table is the single source for role slugs, titles and word bands. Cells are plain text — no
backticks, no bold — so a checker can read them mechanically rather than this contract's bands
being retyped elsewhere.

## File format

Every persona view file carries this exact five-line header, then a body:

```text
# <Title> view — <analysis title>

*Derived from §6 and the structured summary of analysis-<UTC>.md; the six sections remain the source of truth.*

**Band (from §6):** HIGH|MEDIUM|LOW

```

- Line 1 is `# <Title> view — <analysis title>` (em dash), where `<Title>` is the roster's Title
  column and `<analysis title>` is the analysis's own title.
- Line 2 is blank.
- Line 3 is the provenance sentence, italicised, verbatim: `*Derived from §6 and the structured
  summary of analysis-<UTC>.md; the six sections remain the source of truth.*` — `analysis-<UTC>.md`
  names the basename of the analysis the view was derived from; a view of a file named
  differently names that file's own basename in this sentence.
- Line 4 is blank.
- Line 5 is `**Band (from §6):** HIGH|MEDIUM|LOW`, equal to the analysis's own §6
  `**Confidence:**` band.
- Line 6 is blank.
- Line 7 onward is the body: paragraphs and `- ` bullets only — no other headings, no tables, no
  code fences, no numbered lists.

Body words are counted over everything after line 5, whitespace-separated; each bullet's leading
`- ` marker is not itself counted as a word.

## Citation grammar

A sentence ends at a `.`, `?` or `!` that is followed by whitespace or the end of the line —
except the `?` that closes a `GT-n?` id, and the `.` inside a decimal number, neither of which
ends a sentence.

Every body sentence, and every bullet, carries at least one citation token, drawn from: `Cn`,
`GT-n`, `GT-n?`, `A-n`, `§1`–`§6`, or `§5 "<dead-end title>"`.

Resolution rules:

- `Cn` must name a chain the analysis's §4 declares.
- `GT-n` / `GT-n?` must be declared in §3, with the same `?` marking the analysis uses — citing
  `GT-5` when §3 declares `GT-5?` is an error, and citing `GT-5?` when §3 declares `GT-5` (no `?`)
  is equally an error.
- `A-n` must be within the §2 Assumptions Table's row count; row 1 is `A-1`.
- a quoted `§5 "<dead-end title>"` must match a `### Dead End:` heading in the analysis exactly.
- every number in the body — including a `%`, a `$` figure, a decimal, a thousands separator, and
  each end of a range — must appear as a number somewhere in the analysis text.
- the Band line (line 5) must equal the analysis's own §6 `**Confidence:**` band.

This grammar proves that every cited id resolves to something the analysis declares. It does not
prove that the cited id actually supports the sentence it is attached to — it is a
presence-and-resolution check, not a semantic-support check.

## Decision Owner

**Reads:** the `## Answer` block's Recommendation, Band and "Would change it"; §6 Conclusion; the
key risks named in any MEDIUM- or LOW-confidence chain.

**Writes:** what to decide, how sure the analysis is, and what would change the advice — in the
fewest words a decision owner needs to act or to ask a sharper question.

**Absent-input sentences:**

- "This analysis has no Answer block, so the recommendation is read from §6."

## Operator

**Reads:** every §4 chain whose endpoint names an action; every `current constraint` assumption
that survived to Accept, with its expiry condition; §5 dead ends.

**Writes:** which steps to take, in what order, and which previously-tried paths not to repeat.

**Absent-input sentences:**

- "This analysis does not state an implementation path (§6)."
- "No accepted current constraint states an expiry condition (§2)."

## Risk

**Reads:** every `?`-marked ground truth (`read_at_source: false`); every assumption typed
`current constraint` or `untested belief`; each chain's confidence caveats; the §6 Pre-check line.

**Writes:** what is unverified, what could change, and what the analysis itself flags as a cause
for caution.

**Absent-input sentences:**

- "Every ground truth was read at source (§3)."
- "No assumption is typed as a current constraint or an untested belief (§2)."

The "Every ground truth was read at source (§3)." sentence is only true when §3 declares no
`?`-marked ground truth; when §3 declares any `GT-n?`, this persona reads that ground truth
instead of using the fixed sentence.

## Skeptic

**Reads:** each chain's rival-ruled-out sentence inside its `**Confidence:**` line; the
lowest-confidence chain the Conclusion rests on, named as the weakest link; §5 dead ends.

**Writes:** which rival explanation was considered and why it was ruled out, and where the
argument is weakest.

**Absent-input sentences:**

- "This analysis records no abandoned line of reasoning (§5)."

## Self-check before emitting

1. Header lines 1, 3 and 5 match the File format section exactly.
2. The Band line equals the analysis's §6 `**Confidence:**` band.
3. The body word count (everything after line 5) falls inside this role's band from the Persona
   roster.
4. Every body sentence and every bullet carries at least one citation token.
5. Every cited `Cn`, `GT-n`/`GT-n?`, `A-n` or quoted dead-end title resolves against the analysis.
6. Every number in the body appears as a number in the analysis.
7. The body carries no heading, table or code fence.
8. Where an input is absent, the fixed absent-input sentence is used verbatim — never filled in
   with invented content.

The repo gate `scripts/check-persona-view.py` (PERSONA-GATE) enforces items 2 through 7
mechanically; this list is what a writer checks before emitting a view.
