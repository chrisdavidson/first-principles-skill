# The section-3 provenance roll-up — the emission reading

**A recorded observation over frozen, git-tracked captures. It is never a gate, and it may not
become one:** [`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md) §2 item 3 bars
K-of-N live readings from gating. **Measured at:** `2f52f9e1`, 2026-10-05. **Inputs:** the ten frozen
corpora under `tests/` that PROV-ROLLUP's `--emission-reading` pairs with a transcript.

This page corrects the premise of backlog 999.181, that agents do not emit the roll-up. They do
emit its enumeration half, the `?`-marked ids with their `(N of M)` count, in every readable
capture. Its read-at-source half was not audited (see [What "(required)" binds](#what-required-binds)).
What they rarely emit is the template's exact line format, and that is all the old count measured.

---

## What "(required)" binds

The output template marks the section-3 provenance roll-up "(required)", and the one sentence
after that word binds two things (`shared/spine/references/output-template.md`): an enumerated
set of `?`-marked ground-truth ids with its `(N of M)` count, and, for every unsuffixed ground
truth feeding a HIGH-confidence chain, a named read-at-source location. The template adds that
"the named locations are the auditable part", and the agent body's exit criterion says the same.
Neither half binds the template's exact line format: the phase decision recorded here reads
"(required)" as binding the content, not the form, so no template, agent-body or exemplar text
changes.

**This page audits the first half only.** The enumeration with its count is present in every
readable capture below. The read-at-source half was **not** audited, and it is not met
everywhere: `tests/live-conformance-v9.0/Q-P1.md:90` reads `` **`?`-marked: GT-7, GT-14 (2 of 14).** ``
and is followed directly by section 4, whose chain C1 is HIGH, with no read-at-source location
on the roll-up. That document's ground-truth entries carry their own per-entry sources; whether
that satisfies the clause is a question the template does not settle, and PROV-ROLLUP's check 3
records the same ambiguity. This page therefore does not claim the requirement as a whole is
met in any capture.

The agent body prescribes the same content in its own words. Its Phase 3 exit criterion says
"Enumerate the `?`-marked ground truths by ID", and it has done so since commit `eb9d5e3e`
(release 8.17.0), the same commit that added the template clause. The body's example writes the
token with a backtick between the `?` and `-marked`, mid-paragraph, which is the form most agents
copy.

## Two readings, two instruments

| Reading | What it finds | Instrument |
|---|---|---|
| **Line format** | A line in section 3 that starts `?-marked:` and carries an `(N of M)` tail — the template's literal form | PROV-ROLLUP's locator, reproducible with `python3 scripts/check-provenance-rollup.py --emission-reading` |
| **Content** | An enumerated `?`-marked set with `(N of M)`, in section 3, in any glyph form or lead-in | A hand audit, listed capture by capture at the end of this page |

The content reading covers the body's backticked form, `**Provenance summary:**` and
`**Provenance summary.**` lead-ins, bolded variants, and one plain-language rewording. The line
format is a special case of the content, so **the line-format count is a lower bound on content
emission**, never an emission rate. Widening PROV-ROLLUP's locator to the content forms is backlog
999.187; it is not done here.

## The inclusion rule

A capture counts as carrying the content when one line of its section 3 enumerates its
`?`-marked ground truths by id and carries an `(N of M)` count. A `**Pre-check:**` line never
counts, wherever it sits: a pre-check lists only its chain head's identifiers. Glyph form and
lead-in do not matter.

**The empty set.** An explicit `none` with a zero count against M counts only when that
document's section 3 has no `?`-marked entry at all, because it is then the correct enumeration
of the empty set. One capture is admitted under this rule:
`tests/w4-paired/documents/PR-N1.old.r1.md`, line 66, which reads `` `?`-marked: none (0 of 9
numbered ground truths GT-1–GT-9 carry `?`) ``. Its section 3 lists GT-0 to GT-9 and none of
them carries a `?` suffix. A `none` line over a section 3 that has `?` entries would be excluded;
no such line occurs in this population.

**What this count does not audit.** The template says of the roll-up, "Neither an empty
enumeration nor a count of zero satisfies this on its own" (`shared/spine/references/output-template.md`).
That sentence concerns the roll-up as a whole, including its Read-at-source locations for every
unsuffixed ground truth feeding a HIGH-confidence chain (the body's wording since v9.10.0 is
"load-bearing"). This count audits the enumeration half only. A capture counted here has the
enumerated set and its count. That is not a finding that its roll-up fully satisfies the
template clause, and at least one counted capture (`tests/live-conformance-v9.0/Q-P1.md:90`,
above) does not carry the locations on its roll-up.

## Population

PROV-ROLLUP's `--emission-reading` pairs every `.md` capture under the ten corpora with its
transcript: the `.jsonl` of the same stem beside it, or under `../raw/`. READMEs and
orchestrator summaries are skipped. It finds **77** paired captures. **4** are unreadable,
because the agent was never dispatched and no analysis exists. **73** are readable.

## Overall

| Reading | Count | Of |
|---|---|---|
| Line format present | 30 | 77 paired (30 of 73 readable) |
| Content present (hand-audited) | 73 | 73 readable |
| Template read (the run opened the output template) | 59 | 77 paired (14 did not, 4 never dispatched) |

**Content (hand-audited):** 73 of 73 readable captures

## Template read against each reading

- **30 of 30** line-format emissions came from runs that read the template.
- **30 of the 59** template-reading runs produced the line format.
- **0** template-reading runs emitted no content.
- **14** runs never opened the template, and all 14 emitted the content.

The line format traces to the template; the content traces to the body.

## Per corpus

| Corpus | n | Unreadable | Line format | Content | Template read |
|---|---|---|---|---|---|
| adversarial-firing-v9.5 | 5 | 0 | 3 | 5 | 5 |
| baseline-reading-v9.6 | 5 | 0 | 5 | 5 | 5 |
| confidence-transitivity-v9.4 | 11 | 0 | 10 | 11 | 11 |
| emission-stage-a-v9.14 | 10 | 1 | 0 | 9 | 9 |
| live-conformance-v9.0 | 8 | 0 | 1 | 8 | 1 |
| quality-ledger-v8.26 | 1 | 0 | 0 | 1 | 0 |
| quality-provenance-v8.24 | 1 | 0 | 1 | 1 | 1 |
| rebaseline-reading-v9.6 | 5 | 0 | 4 | 5 | 5 |
| reference-reads-v9.2.1 | 1 | 0 | 0 | 1 | 0 |
| w4-paired, old arm | 15 | 2 | 4 | 13 | 10 |
| w4-paired, new arm | 15 | 1 | 2 | 14 | 12 |
| **Total** | **77** | **4** | **30** | **73** | **59** |

The w4-paired arms are split by the `.old.` / `.new.` filename infix.

**The two corpora 999.181 named** (emission-stage-a-v9.14 and live-conformance-v9.0, 18
captures): line format **1 of 18** (`tests/live-conformance-v9.0/PR-P2.md`); content **17 of 17
readable**. The eighteenth, `TB-08`, was never dispatched.

## Why 999.181 read "agents emit only the pre-check one"

A plain substring search for `?-marked:` finds `**Pre-check:**` lines and misses the section-3
summary, because the summary is usually written with a backtick between the `?` and `-marked`.
For example, `tests/emission-stage-a-v9.14/documents/TB-01.md:71`, inside `# 3. Ground Truths`,
reads:

> `` **Provenance summary:** `?`-marked: GT-6, GT-7, GT-8, GT-9 (4 of 9). Read-at-source: GT-1 — … ``

A pre-check cannot stand in for the roll-up: it lists only its own chain head's identifiers, has
no M, and names no read-at-source locations.

The plain-language rewording, the one content form neither the line-format locator nor the
backtick form covers, is `tests/confidence-transitivity-v9.4/CT-A5.md:174`:
`` **Unverified (`?`) entries:** GT-3, GT-4, … (12 of 15) ``.

## What is not claimed

- **No version effect.** The line-format rate differs between corpora, but the template clause
  and the body's exit criterion are textually identical across every version these corpora ran,
  and the corpora differ in prompt set. A difference between them is not attributable to either
  text, so no rate is given by version.
- **Nothing about live documents.** Live documents stay report-only in PROV-ROLLUP; this page
  reads frozen captures only.
- **Nothing about Read-at-source, and so nothing about the requirement as a whole.** See
  [What "(required)" binds](#what-required-binds) and [the inclusion rule](#the-inclusion-rule).

## Reproduction

Run every command from the repository root, in `bash` (R7–R9 use process substitution). Each uses
`/usr/bin/grep`, never a bare `grep`. Outputs were observed at `2f52f9e1`.

| # | Number on this page | Output at `2f52f9e1` |
|---|---|---|
| R1 | 77 paired captures | `77` |
| R2 | 30 line format, 4 unreadable, 73 readable | `43 absent` / `30 present` / `4 unreadable` |
| R3 | 30 of 30 line-format emissions read the template | `30 true` |
| R4 | 59 template read, 14 not read | `14 false` / `4 n/a` / `59 true` |
| R5 | 73 captures carry the content | `73` |
| R6 | every audited line, printed for inspection | 73 lines, one per listed capture |
| R7 | 0 template-reading runs emitted no content | empty output |
| R8 | 14 non-readers carry the content | `14` |
| R9 | the readable set equals the content set | empty output |
| R10 | the per-corpus table | the table's rows |
| R11 | named corpora: line format 1 of 18, content 17 of 17 readable | `16 absent` / `1 present` / `1 unreadable`, then `17` |
| R12 | the line-format figures are pinned in PROV-ROLLUP's self-test | exit 0 |

**R1** — total rows:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1' | wc -l
```

**R2** — line-format distribution:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1{print $4}' | sort | uniq -c
```

**R3** — template-read value among the line-format rows:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1 && $4=="present"{print $3}' | sort | uniq -c
```

**R4** — template-read distribution:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1{print $3}' | sort | uniq -c
```

**R5** — content count, from the list on this page:

```sh
awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | sort -u | wc -l
```

**R6** — print every audited line:

```sh
awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | sort -u | while IFS=: read -r f n; do printf '%s:%s: ' "$f" "$n"; sed -n "${n}p" "$f"; done
```

**R7** — template readers with no content (expect no output):

```sh
comm -23 <(python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1 && $3=="true"{print $1}' | sort) <(awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | cut -d: -f1 | sort -u)
```

**R8** — non-readers carrying the content:

```sh
comm -12 <(python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1 && $3=="false"{print $1}' | sort) <(awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | cut -d: -f1 | sort -u) | wc -l
```

**R9** — readable set against content set (expect no output):

```sh
comm -3 <(python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1 && $4!="unreadable"{print $1}' | sort) <(awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | cut -d: -f1 | sort -u)
```

**R10** — per-corpus rows from the instrument, then the per-corpus content count from the list:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1{split($1,p,"/"); c=p[2]; if(c=="w4-paired"){c=c ($1 ~ /\.old\./ ? " (old)" : " (new)")} n[c]++; if($4=="unreadable")u[c]++; if($4=="present")l[c]++; if($3=="true")t[c]++} END{for(c in n) printf "%s\tn=%d\tunreadable=%d\tline_format=%d\ttemplate_read=%d\n", c, n[c], u[c]+0, l[c]+0, t[c]+0}' | sort
awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | sort -u | awk -F: '{split($1,p,"/"); c=p[2]; if(c=="w4-paired"){c=c ($1 ~ /\.old\./ ? " (old)" : " (new)")} n[c]++} END{for(c in n) printf "%s\tcontent=%d\n", c, n[c]}' | sort
```

**R11** — the two named corpora:

```sh
python3 scripts/check-provenance-rollup.py --emission-reading | awk -F'\t' 'NR>1' | /usr/bin/grep -E '^tests/(emission-stage-a-v9.14|live-conformance-v9.0)/' | awk -F'\t' '{print $4}' | sort | uniq -c
awk '/<!-- content-list:start -->/,/<!-- content-list:end -->/' docs/rollup-emission-reading.md | /usr/bin/grep -oE 'tests/[A-Za-z0-9._/-]+\.md:[0-9]+' | sort -u | /usr/bin/grep -E '^tests/(emission-stage-a-v9.14|live-conformance-v9.0)/' | wc -l
```

**R12** — the line-format reading is pinned capture by capture (`[line-format-pin]`):

```sh
python3 scripts/check-provenance-rollup.py --self-test
```

The content figure is not pinned by any gate. It stands on the list below, which R5 counts and R6
prints.

## Hand-audited content list

Each entry is the first section-3 line of that capture carrying the content. Every line was
printed and checked by eye: it sits under the document's `3. Ground Truths` heading, it
enumerates `?`-marked ids (or, once, the empty set under the rule above), and it carries
`(N of M)`.

<!-- content-list:start -->

**adversarial-firing-v9.5**

- `tests/adversarial-firing-v9.5/PR-P1.md:370`
- `tests/adversarial-firing-v9.5/PR-P2.md:223`
- `tests/adversarial-firing-v9.5/Q-P1.md:95`
- `tests/adversarial-firing-v9.5/Q-P2.md:185`
- `tests/adversarial-firing-v9.5/Q-P3.md:292`

**baseline-reading-v9.6**

- `tests/baseline-reading-v9.6/PR-P1.md:154`
- `tests/baseline-reading-v9.6/PR-P2.md:63`
- `tests/baseline-reading-v9.6/Q-P1.md:194`
- `tests/baseline-reading-v9.6/Q-P2.md:133`
- `tests/baseline-reading-v9.6/Q-P3.md:213`

**confidence-transitivity-v9.4**

- `tests/confidence-transitivity-v9.4/CT-A1.md:166`
- `tests/confidence-transitivity-v9.4/CT-A2.md:197`
- `tests/confidence-transitivity-v9.4/CT-A3.md:59`
- `tests/confidence-transitivity-v9.4/CT-A4.md:156`
- `tests/confidence-transitivity-v9.4/CT-A5.md:174`
- `tests/confidence-transitivity-v9.4/CT-B1.md:65`
- `tests/confidence-transitivity-v9.4/CT-B2.md:60`
- `tests/confidence-transitivity-v9.4/CT-B3.md:182`
- `tests/confidence-transitivity-v9.4/CT-B4.md:175`
- `tests/confidence-transitivity-v9.4/CT-B5.md:135`
- `tests/confidence-transitivity-v9.4/CT-P1.md:186`

**emission-stage-a-v9.14**

- `tests/emission-stage-a-v9.14/documents/TB-01.md:71`
- `tests/emission-stage-a-v9.14/documents/TB-02.md:67`
- `tests/emission-stage-a-v9.14/documents/TB-03.md:155`
- `tests/emission-stage-a-v9.14/documents/TB-04.md:63`
- `tests/emission-stage-a-v9.14/documents/TB-05.md:186`
- `tests/emission-stage-a-v9.14/documents/TB-06.md:57`
- `tests/emission-stage-a-v9.14/documents/TB-07.md:198`
- `tests/emission-stage-a-v9.14/documents/TB-09.md:207`
- `tests/emission-stage-a-v9.14/documents/TB-10.md:59`

**live-conformance-v9.0**

- `tests/live-conformance-v9.0/PR-N1.md:75`
- `tests/live-conformance-v9.0/PR-N2.md:94`
- `tests/live-conformance-v9.0/PR-P1.md:105`
- `tests/live-conformance-v9.0/PR-P1-R2.md:222`
- `tests/live-conformance-v9.0/PR-P2.md:185`
- `tests/live-conformance-v9.0/Q-P1.md:90`
- `tests/live-conformance-v9.0/Q-P2.md:89`
- `tests/live-conformance-v9.0/Q-P3.md:46`

**quality-ledger-v8.26**

- `tests/quality-ledger-v8.26/PR-P1.md:86`

**quality-provenance-v8.24**

- `tests/quality-provenance-v8.24/PR-P1.md:108`

**rebaseline-reading-v9.6**

- `tests/rebaseline-reading-v9.6/PR-P1.md:58`
- `tests/rebaseline-reading-v9.6/PR-P2.md:39`
- `tests/rebaseline-reading-v9.6/Q-P1.md:54`
- `tests/rebaseline-reading-v9.6/Q-P2.md:211`
- `tests/rebaseline-reading-v9.6/Q-P3.md:129`

**reference-reads-v9.2.1**

- `tests/reference-reads-v9.2.1/DEMO-TRIAGE.md:183`

**w4-paired**

- `tests/w4-paired/documents/PR-N1.new.r1.md:77`
- `tests/w4-paired/documents/PR-N1.new.r2.md:55`
- `tests/w4-paired/documents/PR-N1.new.r3.md:67`
- `tests/w4-paired/documents/PR-N1.old.r1.md:66`
- `tests/w4-paired/documents/Q-P2.new.r1.md:71`
- `tests/w4-paired/documents/Q-P2.new.r3.md:185`
- `tests/w4-paired/documents/Q-P2.old.r1.md:162`
- `tests/w4-paired/documents/Q-P2.old.r2.md:61`
- `tests/w4-paired/documents/Q-P2.old.r3.md:50`
- `tests/w4-paired/documents/TB-02.new.r1.md:107`
- `tests/w4-paired/documents/TB-02.new.r2.md:221`
- `tests/w4-paired/documents/TB-02.new.r3.md:63`
- `tests/w4-paired/documents/TB-02.old.r1.md:63`
- `tests/w4-paired/documents/TB-02.old.r2.md:51`
- `tests/w4-paired/documents/TB-02.old.r3.md:60`
- `tests/w4-paired/documents/TB-06.new.r1.md:208`
- `tests/w4-paired/documents/TB-06.new.r2.md:55`
- `tests/w4-paired/documents/TB-06.new.r3.md:53`
- `tests/w4-paired/documents/TB-06.old.r1.md:62`
- `tests/w4-paired/documents/TB-06.old.r2.md:65`
- `tests/w4-paired/documents/TB-06.old.r3.md:142`
- `tests/w4-paired/documents/TB-10.new.r1.md:211`
- `tests/w4-paired/documents/TB-10.new.r2.md:104`
- `tests/w4-paired/documents/TB-10.new.r3.md:185`
- `tests/w4-paired/documents/TB-10.old.r1.md:156`
- `tests/w4-paired/documents/TB-10.old.r2.md:59`
- `tests/w4-paired/documents/TB-10.old.r3.md:54`

<!-- content-list:end -->
