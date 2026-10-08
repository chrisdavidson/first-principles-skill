# Persona views

A persona view is a sibling overlay of one delivered analysis, never an edit of it. It restates
only what the analysis already says, cited back to the analysis; the six sections of the
analysis remain the source of truth. A persona view adds no claim the analysis does not already
carry.

## Persona roster

| Slug | Title | Body words |
|------|-------|------------|
| decision-owner | Decision Owner | 90–170 |
| operator | Operator | 90–170 |
| risk | Risk | 90–170 |
| skeptic | Skeptic | 90–170 |

This table is the single source for role slugs, titles and word bands. Cells are plain text — no
backticks, no bold — so a checker can read them mechanically rather than this contract's bands
being retyped elsewhere.

## File format

Every persona view file carries this exact nine-line header, then a body:

```text
# <Title> memo — <analysis title>

> **To:** <Title>\
> **Re:** <analysis title>\
> **Basis:** <analysis link> · <report link> · <index link>\
> **Band (from §6):** HIGH|MEDIUM|LOW

*Derived from §6 and the structured summary of analysis-<UTC>.md; the six sections remain the source of truth.*

```

- Line 1 is `# <Title> memo — <analysis title>` (em dash), where `<Title>` is the roster's Title
  column and `<analysis title>` is the source analysis's own title: the text of its first `# ` heading (its H1), copied as written.
- Line 2 is blank.
- Line 3 is `> **To:** <Title>\`, ending in a hard-break backslash; `<Title>` equals the roster's
  Title column exactly, the same value as line 1's.
- Line 4 is `> **Re:** <analysis title>\`, ending in a hard-break backslash; identical to line 1's
  analysis title.
- Line 5 is `> **Basis:** `, then three Markdown links separated by ` · ` (a space, a middle
  dot, a space), then a hard-break backslash. The first link's text and target are both
  `<analysis basename>`, the basename of the analysis the view was derived from. The second
  link's text is `Report` and its target is `report-<UTC>.md`, where `<UTC>` is that basename's
  own stamp. The third link's text is `All files` and its target is `INDEX.md`.
  The three links reach the analysis, its reader report and the folder index, all of which sit
  beside the view. The PDF render points the report and index links at their PDFs and leaves the analysis name as
  plain text, since the analysis has no PDF.
- Line 6 is `> **Band (from §6):** HIGH|MEDIUM|LOW`, with no trailing backslash, equal to the
  analysis's own §6 `**Confidence:**` band.
- Line 7 is blank.
- Line 8 is the provenance sentence, italicised, verbatim: `*Derived from §6 and the structured
  summary of analysis-<UTC>.md; the six sections remain the source of truth.*` — naming the same
  basename as line 5.
- Line 9 is blank.
- Line 10 onward is the body: prose paragraphs separated by one blank line, each paragraph written
  on a single physical line — no bullets, numbered lists, headings, tables, code fences or
  blockquotes in the body, and no paragraph opening with bold text.

Body words are counted over everything after line 8, whitespace-separated.

## Citation grammar

A sentence ends at a `.`, `?` or `!` that is followed by whitespace or the end of the line —
except the `?` that closes a `GT-n?` id, and the `.` inside a decimal number, neither of which
ends a sentence.

Every body sentence carries at least one citation token, drawn from: `Cn`, `GT-n`, `GT-n?`, `A-n`,
`§1`–`§6`, or `§5 "<dead-end title>"`.

Resolution rules:

- `Cn` must name a chain the analysis's §4 declares.
- `GT-n` / `GT-n?` must be declared in §3, with the same `?` marking the analysis uses — citing
  `GT-5` when §3 declares `GT-5?` is an error, and citing `GT-5?` when §3 declares `GT-5` (no `?`)
  is equally an error.
- `A-n` must be within the §2 Assumptions Table's row count; row 1 is `A-1`.
- a quoted `§5 "<dead-end title>"` must match a `### Dead End:` heading in the analysis exactly.
- every number in the body — including a `%`, a `$` figure, a decimal, a thousands separator, and
  each end of a range — must appear as a number somewhere in the analysis text.
- the Band line (line 6) must equal the analysis's own §6 `**Confidence:**` band.

This grammar proves that every cited id resolves to something the analysis declares. It does not
prove that the cited id actually supports the sentence it is attached to — it is a
presence-and-resolution check, not a semantic-support check.

## Questions

Each role answers its fixed, ordered list of questions, held verbatim in its own section below.
The questions are the hidden order of the body: they are never printed. The body opens with a
paragraph that starts `In brief:` — one or two cited sentences carrying what the analysis gives
this reader, never a recommendation. Then exactly one paragraph per question, in the role's order,
each answering its question in prose. Every sentence in every paragraph, the `In brief:` paragraph
included, carries a citation token. Where an absent-input sentence applies, it is written inside
the paragraph that answers the question whose input is absent.

PERSONA-GATE checks this structure — the `In brief:` paragraph first, one more paragraph than the
role has questions, no bullet line, no bold label, no printed question — and cannot check that each
paragraph answers its own question.

## Voice

A view describes what the analysis found, in the third person about the analysis. It carries no
imperative addressed to the reader, no "you" or "your" (so no "you should", "you must", "you need
to"), no verdict on the reader (for example on "your objection" or on the reader being right or
wrong), and it never restates the recommendation — it points to it (the Answer block and §6) with
the conditions the analysis says it depends on.

**Denylisted openers:** Build, Classify, Confirm, Consider, Decide, Finish, Keep, Move, Read, Reject, Risk-classify, Switch, Take, Treat; and the two-word opener "Do not".

PERSONA-GATE's PV-DIRECTIVE check is lexical — it flags a body sentence that opens with a
denylisted word, any "you" or "your", a verdict on the reader, or a run of six or more consecutive
words shared with §6's `**Recommended approach:**` paragraph; it over-reports by design and does
not judge meaning.

## Decision Owner

**Reads:** the `## Answer` block's Recommendation, Band and "Would change it"; §6 Conclusion; the
key risks named in any MEDIUM- or LOW-confidence chain.

**Writes:** what the analysis examined and why it matters, what it has settled, how sure it is and
why, and where the recommendation and the conditions it depends on are stated.

**Questions (in order):**

1. What was examined, and why does it matter?
2. What has it settled that I can rely on?
3. How sure is it, and what is it unsure about?
4. Where do I find the recommendation?

**Absent-input sentences:**

- "This analysis has no Answer block; its recommendation and the conditions it depends on are stated in §6."

## Operator

**Reads:** every §4 chain whose endpoint names an action; every `current constraint` assumption
that survived to Accept, with its expiry condition; §5 dead ends.

**Writes:** what the analysis means for the work in hand, which constraints hold and until when,
which paths were tried and set aside, and which facts are still missing.

**Questions (in order):**

1. What does this mean for the work in front of me?
2. Which constraints hold, and until when?
3. What was tried and set aside, and why?
4. What facts are still missing?

**Absent-input sentences:**

- "This analysis does not state an implementation path (§6)."
- "No accepted current constraint states an expiry condition (§2)."

## Risk

**Reads:** every `?`-marked ground truth (`read_at_source: false`); every assumption typed
`current constraint` or `untested belief`; each chain's confidence caveats; the §6 Pre-check line.

**Writes:** what risk the analysis retires, what is unverified, what could change, and what the
analysis itself flags for caution.

**Questions (in order):**

1. What risk does the analysis retire?
2. What is unverified?
3. What could change?
4. What does the analysis itself flag for caution?

**Absent-input sentences:**

- "Every ground truth was read at source (§3)."
- "No assumption is typed as a current constraint or an untested belief (§2)."

The "Every ground truth was read at source (§3)." sentence is only true when §3 declares no
`?`-marked ground truth; when §3 declares any `GT-n?`, this persona reads that ground truth
instead of using the fixed sentence.

## Skeptic

**Reads:** each chain's rival-ruled-out sentence inside its `**Confidence:**` line; the
lowest-confidence chain the Conclusion rests on, named as the weakest link; §5 dead ends.

**Writes:** what the argument rests on, which alternatives were considered and why they were set
aside, where the argument is weakest, and what evidence would overturn it.

**Questions (in order):**

1. What does the argument rest on?
2. What alternatives were considered, and why were they set aside?
3. Where is the argument weakest?
4. What evidence would overturn it?

**Absent-input sentences:**

- "This analysis records no abandoned line of reasoning (§5)."
- "No chain states a rival that was ruled out (§4)."

## Self-check before emitting

1. Header lines 1, 3–6 and 8 match the File format section exactly, including the hard-break
   backslash at the end of lines 3–5.
2. The Band line equals the analysis's §6 `**Confidence:**` band.
3. The body word count (everything after line 8) falls inside this role's band from the Persona
   roster.
4. Every body sentence carries at least one citation token, the In brief paragraph included.
5. Every cited `Cn`, `GT-n`/`GT-n?`, `A-n` or quoted dead-end title resolves against the analysis.
6. Every number in the body appears as a number in the analysis.
7. The body carries no heading, table, code fence, blockquote, bullet or numbered list.
8. Where an input is absent, the fixed absent-input sentence is used verbatim — never filled in
   with invented content.
9. The body opens with a paragraph that starts `In brief:`, then exactly one prose paragraph per
   role question in the role's order; no question is printed and no paragraph opens with a bold
   label.
10. No body sentence opens with a denylisted opener, uses you or your, passes a verdict on the
    reader, or repeats six or more consecutive words of §6's recommended approach.

The repo gate `scripts/check-persona-view.py` (PERSONA-GATE) enforces items 2 through 7, 9 and 10
mechanically; this list is what a writer checks before emitting a view.
