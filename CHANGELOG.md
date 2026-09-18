# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Version stamps move in lockstep.** Plugin installs are version-gated, not content-gated,
so every release bumps all 17 stamps together — the 14 `shared/skills/*/SKILL.md` sources
(13 companion skills plus the `first-principles-analysis` launcher),
`shared/spine/SKILL.meta.yml`, `.claude-plugin/marketplace.json`, and
`first-principles/.claude-plugin/plugin.json`. A body edit without a bump never reaches an
installed session.

## [Unreleased]

## [9.3.2] — 2026-09-16

Amended on 2026-09-17, before publication, to restate the confidence-line rule below; the heading
keeps the original release date.

Released as a patch ahead of milestone v9.4.0 (Source-Literal Pinning): it ships Phase 42
(backlog 999.119) and Phase 41 (backlog 999.120) while Phases 36-39 remain open. Where the tree
names "v9.4.0 Phase 41" or "v9.4.0 Phase 42" — including the record's own phase directories —
that is the work's provenance; it ships in this release.

Closes backlog **999.119** as a **product change**: a derivation chain is now rated no higher than
the lowest-rated chain its head cites — the unverified-input rule (D-07)'s new transitivity ceiling.
The comparison is against the stated confidence label of each chain named on the head line, the line
before the first `→`. The rule is a ceiling that bounds a rating from above; it is never a reason to
rate a chain HIGH. A chain rated MEDIUM under a validation-rubric exception still caps the chains
that cite it. A MEDIUM or LOW confidence line explains only its own chain's rating, so its validity
never depends on how far away a cap originates. It names each unverified ground truth with the
verification that would remove it as a cause of the downgrade, and names each chain on its head
rated below HIGH, which it need not re-explain, since the cited chain's own confidence line carries
the explanation. For each downgrade cause belonging to the chain itself, such as a weak inference
step or an absent-fails derivation, the line says what would remove it as a cause of the downgrade
or gives a reason no verification path exists: for an absent-fails derivation, the rubric's
absent-fails exception, or an explicit account of why no available evidence settles that cause. The
absent-fails exception is the only exception that can stand in for a verification path, and
"speculative" is never such a reason. A speculative chain that another chain cites is load-bearing,
so the rubric's speculative-chain exception no longer covers it and the cited chain's own confidence
line states its verification path; a speculative chain with no verification path is not cited on
another chain's head, and stays speculative or moves to the Abandoned Reasoning section.

Names the edited surfaces:
- [`output-template.md`](first-principles/agents/references/output-template.md), the
  unverified-input rule (D-07), the §4 confidence placeholder, the §5 list of abandonment reasons
  and the §6 Conclusion confidence note;
- [`validation-rubric.md`](first-principles/agents/references/validation-rubric.md), Validate
  criterion and its exceptions summary: the ceiling in the Rigorous band and new banded violations
  in the Sound band; Rigorous requires, and Sound bands the omission of, naming each cited chain
  rated below HIGH; Sound also bands a confidence line that omits a downgrade cause of its own
  chain, or gives one with neither what would remove it nor a permitted no-path reason, and a
  chain that cites a speculative chain with no verification path; and the speculative-chain
  exception is narrowed, so a cited chain no longer carries it and a speculative chain with no
  verification path is not cited;
- the agent body's unverified-input notation, which gains the ceiling, now asks for the
  verification that would remove an unverified input as a cause of the downgrade, and deliberately
  keeps its existing "depending on" wording while saying that the explanation belongs on the line
  that rests on the unverified input directly, which a citing chain names and need not re-explain,
  with the template carrying the full statement, and its self-audit template-read paragraph, which
  now says the naming requirement covers inherited chains;
- the `/reason-upward` skill, which now states the unverified-input rule (D-07) inline where it
  previously only named it, defining in place the absent-fails exception, the only exception that
  can stand in for a verification path there.

The agent's reference tree carries no separate `reason-upward` file of its own, so the agent
reaches the rule through its body and the `output-template.md` link the body already carries — not
through a second generated reference sibling.

Evidence, reported as an observation:
[`tests/confidence-transitivity-v9.4/`](tests/confidence-transitivity-v9.4/README.md) holds five
live captures of one purpose-built prompt taken before the change and five after. A qualifying
chain — one whose head cites only MEDIUM chains and no unverified ground truth — was rated MEDIUM
or lower in K_before=0 of the Q_before=0 before-leg captures that contained one, and in K_after=0
of the Q_after=0 after-leg captures that contained one; every one of the five captures in each leg
contained no qualifying chain. The frozen v9.2.1 triage capture's single inversion (a HIGH decision
chain over three MEDIUM chains) stays the standing before-reading. Neither leg reproduced the
qualifying shape across five fresh generations, so this after-leg reading has no non-zero
before-leg base to compare against and no ratio comparison is possible in either direction. The
finding is scoped to what five fresh generations per side did not reproduce, and it neither
confirms nor refutes the ceiling clause's live effect. Captures on both sides name inherited MEDIUM
chains in their confidence lines, so that behaviour does not distinguish them. Separately,
`detect_defects` flags the triage capture's decision chain as a confidence inversion — the
violation the new clause describes — which checks the instrument against that fixture and says
nothing about the clause. This is a recorded observation at five captures per leg, not a gate.

The broader measure moved: `confidence_inversions` read nonzero in 2/5 captures before the change
and 0/5 after, each before-side case a MEDIUM chain citing a LOW chain — a shape the
qualifying-chain count excludes by design. That movement is an observation at N=5, where noise can
equal effect; it is not a gate, and it cannot be attributed to the change with confidence.

The after-side captures were taken before the wording-agreement edits that also ship in this
release. The Validate criterion's Rigorous band requires, and its Sound band bands the omission of,
naming each cited chain rated below HIGH, and the agent body's template-read paragraph now says the
template's naming requirement covers inherited chains. Each confidence line explains only its own
chain's rating: a cited chain is named there and explained on its own line, and each downgrade cause
of the chain itself gets what would remove it or a reason no verification path exists. That reason
is, for an absent-fails derivation, the absent-fails exception, which the template and the rubric's
Rigorous band name as the rubric's absent-fails clause and `/reason-upward`, which carries no
rubric, defines in place, or an explicit account of why no available evidence settles that cause. No
other exception can stand in for a verification path: the rubric's speculative-chain exception no
longer covers a chain that another chain cites, and a speculative chain with no verification path is
not cited. Those edits were not live-captured. The fixture README carries a dated erratum correcting
its own account of the readings.

No gate was added or registered. See [`CLAUDE.md`](CLAUDE.md) § CI gates for the current battery,
CI and coverage-headline totals — none of them moved and none is restated here.

Closes backlog **999.120** as an **apparatus change**: `detect_defects`
(`scripts/check-quality-harness.py`) gains a confidence dimension and a self-audit band census.
The claim-audience is the measurement instrument, not a plugin user.

`detect_defects` reads a chain block's own confidence label in exactly three shapes: on the
heading line, a parenthetical opening with a band word (for example `*(HIGH)*` or
`*(Confidence: HIGH — gloss)*`); on the heading line, a `Confidence:` label carrying the band
word, whether inside a parenthetical, inside the bold heading span, or after it; or, failing
both, a trailing line beginning `**Confidence:**`. These are the shapes found in the frozen live
captures and the shipped worked examples. A label in any other shape — a blockquoted marker
line or a list-item marker line, for example — is counted under `confidence_unparsed` rather than
read; `docs/data/conformance.json`'s `live_conformance.rows` carries the per-run reading. A
hyphenated compound label such as `Medium-high` is currently read by its first word.
`detect_defects` reports the reading across the new `high_conf_chains`,
`high_conf_unverified_head`, `confidence_inversions` and `confidence_unparsed` columns. An
unparsable label is counted under its own column rather than read as a clean zero.
`_SELFAUDIT_CONTRADICTIONS` gains an entry for the Validate criterion: a Rigorous self-report next
to a nonzero confidence-defect reading now counts as a self-audit disagreement, the same way it
already does for the Challenge Assumptions, Reason Upward and Conclusion-to-Ground-Truth
Traceability criteria. The new `selfaudit_bands_parsed` and `selfaudit_offvocab_bands` columns
make a `selfaudit_disagreements` zero readable — distinguishing "no criterion band was even
parsed" and "a band word outside the vocabulary was reported as its own finding" from genuine
agreement, over a widened set of the band-heading shapes the shipped analyses actually emit. A
leading acronym or ground-truth id in the prose right after a criterion heading is not read as a
band word.

`scripts/report-conformance.py` classifies `detect_defects`' provenance and measured-schema
columns by name rather than by position, so this widening did not require a second, parallel
positional literal to stay in sync by hand.

The after-leg evidence is a newly frozen fixture,
[`tests/reference-reads-v9.2.2/`](tests/reference-reads-v9.2.2/README.md), captured from a live
run and read against a pre-registered table of expected readings before any of this widening
existed.

Claim-surface correction: `detect_defects`' previously-pinned extractors are unchanged, but its
own column set is not "unmodified" — prose across the repository that called the detector
unmodified without qualification has been corrected to name the distinction.

No gate was added or registered; the work stays inside the existing self-test. No frozen TSV was
rewritten. See [`CLAUDE.md`](CLAUDE.md) § CI gates for the current battery, CI and
coverage-headline totals — none of them moved and none is restated here.

## [9.3.1] — 2026-09-16

Released as a patch ahead of milestone v9.4.0 (Source-Literal Pinning): this is that milestone's
Phase 40, shipped on its own while Phases 36–39 remain open. Where the tree names "v9.4.0
Phase 40" — including the record's own filename, `docs/v9.4-gate-retirement.md` — that is the
work's provenance; it ships in this release.

Closes backlog **999.104**, **999.105**, **999.106**, **999.107**, **999.108** and **999.109**,
each re-run against its own named check in its post-phase form at phase close, and resolves
**999.71** as moot. See
[`docs/v9.4-gate-retirement.md`](docs/v9.4-gate-retirement.md) for the measured evidence behind
every item and [`CLAUDE.md`](CLAUDE.md) § CI gates for the current battery, CI and coverage-headline
totals — neither is restated here.

This is an **apparatus change**: VAL-04 (4-gram trigger-collision scan), VAL-05 (2,000-character
description budget) and COLLIDE-01 (dual-install name-collision scan) are retired outright;
PROV-GUARD is relaxed from a CI job plus a battery live leg to a battery-only self-test;
`scripts/check-body-budget.py` and `scripts/census-delta-vectors.py` are deleted, neither having
ever been a registered gate. Each retirement's own measured mutation evidence — that the retired
check could not fail for a real reason — is in the record above; none of it changes what the agent
does.

Product-tier corrections landed alongside the apparatus change: `README.md`'s pre-commit hook
sentence, the skill-listing description-ceiling sentences in `CLAUDE.md` and
`docs/DEVELOPMENT.md`, the name-invariant enforcement row in `docs/CONFIGURATION.md`, and
PROV-GUARD's stated scope in `docs/requirements-traceability.md` all now describe what the shipped
apparatus actually does rather than a claim it never enforced.

REG-GUARD gains a new `disable-model-invocation` value assertion — an assertion inside an existing,
already-registered gate, not a new one — succeeding VAL-04's retired proxy check.

The counting rule (D-D) is amended: a battery or CI total may now fall for a gate a successor
retirement record names by name, rather than staying pinned to a fixed pair of digits. See
`docs/v9.4-gate-retirement.md` §4.

The phase's code review returned five product-tier findings (CR-01, CR-02, WR-01..WR-03) and one
apparatus-tier warning (WR-04), all fixed before release in `404dd69`, `e6faa31`, `8dd2442`,
`41f13ee`, `00dc8a2` and `1774596`: stale battery totals in `CLAUDE.md` and `docs/README.md` now
point at the generated total; `docs/ARCHITECTURE.md`'s battery chain gains VAL-05's missing
`24 → 23` step (with two added "NOT A COUNT CLAIM" exemption-ledger entries, its bound raised from
20 to 22); `docs/CONFIGURATION.md` lists all five pre-commit gates; the retirement record's
`_skill_io` importer count is corrected in place; and REG-GUARD's new assertion accepts only the
literal spelling `true`.

## [9.3.0] — 2026-09-14

Closes backlog **999.93** through **999.100** (the Trace Atlas milestone's own eight entries),
**999.101** (folded in as REL-24, D-01) and **999.102** (already resolved earlier in this
milestone by Phase 32.1, `eaf221b`) — each determination re-run against that entry's own named
check at `522c873`, and all ten read closed (999.100 with the residual disclosed under Known
limitations below). Five further entries carrying a same-window resolved
date — **999.36, 999.39, 999.56, 999.67, 999.78** — were confirmed closed by commits from earlier
milestones (v9.0.0/v9.2.1); named here only for completeness of the date-window search, none is
this milestone's own work.

This is an **apparatus milestone**, taken ahead of the apparatus-cost pivot (now v9.4.0): all
eight entries land in the matrix schema and its checking scripts, not in methodology text an agent
reads. **REL-24 is the one exception and this release's one change to what the agent is told** —
two sentences in `shared/spine/SKILL-body.md`'s failure-path prose, corrected under backlog
999.101.

Requirement groups, by ID: schema and statements (**SCHEMA-01, SCHEMA-02, STMT-01, STMT-02**,
999.96/999.100); row registration and residuals (**ROWS-01..05, RESID-01, RESID-02**,
999.93/999.94/999.95); reproducible-tier honesty and anchors (**TIER-01..04, ANCH-01, ANCH-02**,
999.97/999.98/999.99); release (**REL-19..REL-24**).

The coverage headline moved `239/132/0/371` (239 reproducible / 132 audit-only / 0 gap / 371 total)
to `244/151/0/395` (244 reproducible / 151 audit-only / 0 gap / 395 total) — 24 new rows registered
through `_rows_v93()`, swept across every covered surface by `HEADLINE-LOCK`'s mechanism, never by
hand — then to `243/152/0/395` (243 reproducible / 152 audit-only / 0 gap / 395 total) when the
phase's code review re-tiered TIER-03 audit-only (relabelling a live/manual row `battery-only`
stays green at every gate), in a second swept move — and to `240/155/0/395` (240 reproducible /
155 audit-only / 0 gap / 395 total) when the same review re-tiered SCHEMA-01, STMT-01 and ANCH-01
audit-only (each statement carries a clause no registered gate re-runs), in a third.

The battery registration count and the CI job count are unchanged from this milestone's own
baseline: by direct count through `scripts/check-registration.py`'s own parser, both at `fda29cc`
(the pre-registered milestone base) and at this phase's own base `3c0fed0`, and again after every
commit in between. Read the current totals from `CLAUDE.md`'s generated gate-table sentence
rather than from a digit restated here.

`[9.2.3]`, `[9.2.4]` and `[9.3.0]` were none of them published on their own — all three reach an
installed session together, whenever that install happens; this entry assumes no date for it.

A surfaces value, a battery-only marker and a live/manual label are hand-assigned classifications the matrix states, not measurements it proves.

### Added

- **Matrix schema — surfaces and statements (SCHEMA-01, SCHEMA-02, STMT-01, STMT-02; 999.96,
  999.100).** `MatrixRow` carries a `surfaces` field (skill slugs, `agent`, or `apparatus`),
  back-filled across every `_rows_v*()` batch and emitted into `docs/data/matrix.json`;
  `docs/requirements-matrix.md` carries a generated per-skill row count, with all 14 shipped skill
  slugs named by at least one row or recorded under its generated `### Uncovered` heading. Every
  row carries a non-empty one-line statement or the literal marker `statement unrecoverable`, and
  every one of the 395 rows now does. **Disclosed limits —** a fabricated but well-formed
  archive-sourced statement stays green at every gate that could plausibly read it (confirmed by a
  live break test this phase); archive fidelity is locally re-readable, never CI-checked.
- **Row registration and residuals (ROWS-01..05, RESID-01, RESID-02; 999.93, 999.94, 999.95).**
  Every v8.19, v8.20 and v8.21 requirement is now a matrix row (`_rows_v819()`, `_rows_v820()`,
  `_rows_v821()`), no registered gate's row count reads zero, and the two ACCEPTED-FINAL Step 0
  residuals (RR-108-04, RR-108-05) carry `residual/` rows. **Disclosed limits —** the
  every-registered-gate-is-cited claim, the docstring tier-justification prose, and a
  milestone-naming edit to the headline-history table are none of them re-run by any registered
  gate — each confirmed by a live mutate-and-restore break test, not merely asserted: re-pointing
  GATE-01's two citing rows away from `scripts/check-agent.py` (its citation count reads zero),
  deleting the HC-04 audit-only justification paragraph from `_rows_v819()`'s docstring, and
  redacting v8.19/v8.20/v8.21 from headline-history row 17 each left
  `scripts/check-traceability.py --self-test` green.
- **Release mechanics (REL-19..REL-23).** All 17 version stamps bumped to `9.3.0` in one commit
  (`51b3830`) carrying the body fix (`9e582cb`) to installed copies; `_rows_v93()` registered and
  wired into `build_matrix_rows()` (`522c873`), sweeping the headline in the same commit. No new
  `-ROWS` sentinel was added for `_rows_v93()` — a **LEVEL** determination, written into the
  function's own docstring: the batch stays inside TRACE-03's existing ROW-FIELDS and
  HEADLINE-LOCK legs, matching the standing pattern Phase 33 already declined a sentinel under.
  **Disclosed limits —** a tier swap between two `v9.3` rows that holds the tier counts constant,
  or a statement edit `emit` then regenerates, would pass both legs — a named residual, not closed.

### Changed

- **Reproducible-tier honesty and self-test anchors (TIER-01..04, ANCH-01, ANCH-02; 999.97,
  999.98, 999.99).** Every non-gate-artifact reproducible row now carries an explicit
  `rerun_by="live-manual"` label, and every row evidenced by `scripts/check-quality-harness.py`
  carries `rerun_by="battery-only"` — **999.97 is a re-point-and-label, not a tier split (D-T3):
  the headline's reproducible/audit-only shape is unchanged by this move.** Self-test anchors,
  read at `fda29cc` → phase base `3c0fed0` → `522c873`: anchored 35 of 229 → 52 of 239 → 55 of 244
  reproducible rows, call-checked 25 of 229 → 40 of 239 → 43 of 244. This phase's own movement is
  therefore 52 → 55 anchored and 40 → 43 call-checked; after the code review's re-tiers
  (`67c4cbe`) the two counts read 53 and 41 of 240. The anchor work spans three renamed scripts
  (`check-loop-closure.py`, `check-act-limb.py`, `check-registration.py`). **Disclosed limits —** a `rerun_by` label is a
  hand-assigned classification the matrix states, not a measurement it proves; a row could carry
  `live-manual` or `battery-only` incorrectly and no gate would catch it.

### Fixed

- **REL-24 — the agent body's failure-path prose, and this CHANGELOG (999.101, IN-01..IN-03).**
  The backstop in `shared/spine/SKILL-body.md` no longer tells a reader to assemble a document
  from "the section summaries below" — no such section summary exists at that position. It now
  names the six sections under `## Output format` by their own heading, and its incomplete-step
  clause names each of the closure ledger, the self-audit scan and the Self-Audit Gate
  individually, pairing each with a real cause (turns exhausted, or a named reference that could
  not be read), rather than a singular "which one." The developer selected the wider of two
  drafted scopes (**option-all**): all three mapped `section summaries` sites are fixed, not only
  the two IN-01/IN-02 sentences 999.101 originally named, taking the whitespace-flexible count to
  0 in both `shared/spine/SKILL-body.md` and the generated agent body. The third site is the
  template-read justification that `[9.2.4]`'s WR-05 (`38dcfbe`) last narrowed to what the body
  lacks: option-all re-points its phantom referent at the six-section document assembled without
  the template read, and carries WR-05's narrowed claim — the trailing `**Confidence:**` field and
  D-07's naming requirement are absent, the rating floor is not — over unchanged. Separately (IN-03), the
  released `[9.2.2]`, `[9.2.3]` and `[9.2.4]` entries above are corrected in place: each pointer at
  a local-only, git-ignored planning record is replaced by its own verbatim claim or dropped and
  named by backlog ID only, every remaining line-number citation is anchored to the release commit
  that carries it, and every battery/CI tally is anchored the same way — the count of such pointers
  across those three entries now reads 0, down from 5. **Disclosed limits —** obedience to either failure-path
  sentence stays with backlog 999.89; presence is checkable, obedience is not.

### Known limitations

- **999.100's statement-fidelity residual.** All 24 new `v9.3` rows classify `"archive"` and cite
  an archive file (`v9.3.0-REQUIREMENTS.md`) that does not exist until `/bm:complete-milestone`
  runs; the fidelity reading (`statements matching no cited source text`) will read 24, not 0,
  until that archive is created. Expected and time-bound, not a defect (Phase 32.1 D-02).
- **The older `[9.0.0]`–`[9.1.0]` CHANGELOG pointers are not swept.** Four lines citing an
  untracked, local-only planning path stay byte-identical, anchored at `3c0fed0`: lines 462, 578,
  591, 1339 (D-03 scopes IN-03's fix to `[9.2.2]`/`[9.2.3]`/`[9.2.4]` only).
- **`[9.2.3]` (`154644e`) and `[9.2.4]` (`fda29cc`) are released but untagged.** Retro-tagging both
  is left to `/bm:complete-milestone`.
- **REL-23, recurrence not compliance.** Reading 1 of all eight `rederive.py` subcommands was
  taken after `522c873` (the last commit touching `scripts/check-traceability.py` at the time);
  every difference from the phase-base reading was explained, none filed to backlog. Reading 2 is
  taken after this entry's own commit and published, whatever it reads, in the dated release
  readings section of the requirements traceability document, by the record-only commit that
  follows this one.

## [9.2.4] — 2026-09-12

Closes the five product-tier warnings (**WR-01..WR-05**) that 999.92's phase code review raised
against `[9.2.3]`. `[9.2.3]` was never published on its own; both releases reach an installed
session together. No file under `scripts/` or `tests/` changed and no pinned body sentence was
edited, so the coverage headline and the gate totals are unchanged — read them from `CLAUDE.md`'s
generated gate-table sentence rather than from a digit restated here.

### Fixed

- **WR-01 — Phase 5 Operation no longer orders the criteria applied at that step**
  (`28113d1`). `[9.2.3]` deferred the rubric *read* to the Self-Audit Gate but left "apply them"
  in place, so the only compliant reading was to score from recollection — the failure the rubric
  imperative names. The sentence now defers the *application* as well: the rubric is opened once,
  and its criteria applied once, at the Self-Audit Gate, immediately after that read.
- **WR-02 — the failed-rubric-read case is carved out of the six-verdict-block imperative**
  (`4084e4e`). "Emit the Self-Audit Gate's six verdict blocks … regardless of what other scoring
  instrument the analysis contains" followed the new "emit no verdict blocks" failure clause with no
  exception. It now ends: unless the rubric read failed, in which case no verdict block is emitted,
  neither the Validate/Fix/Repeat loop nor any Absent-verdict route runs, and the failed read is
  disclosed.
- **WR-05 — the template imperative's justification narrowed to what the body lacks**
  (`38dcfbe`). The paragraph claimed the body did not carry the D-07 rating floor; the unverified
  input notation does. It now names only what is actually absent: the trailing `**Confidence:**`
  field and D-07's requirement that a MEDIUM or LOW line name the `GT-N?` input behind it. This
  adds one line, so every later body line moves down by one — the line numbers in `[9.2.3]`
  describe `154644e`.
- **WR-03, WR-04 — `[9.2.3]` corrected in place** (`31ccb64`, `c442975`). Its claim that
  verdict-block vocabulary "can only have come from an actual read" was false: three other linked
  references carry those tokens, so only a `Read` of `references/validation-rubric.md` is evidence
  of the rubric read. Its "confirmed referents" list named an earlier draft's referents, not the
  shipped sentence's. The same evidence bound is recorded on backlog 999.89, whose census it
  constrains.

### Known limitations

- **WR-01, WR-02 and WR-05 change what the agent is instructed to do.** Gates confirm the text is
  present and well-formed; they cannot confirm a run obeys it. The *after* reading remains backlog
  **999.89**. Presence is checkable, obedience is not.
- **The review's three info findings are not addressed by this release:** "the section summaries
  below" has no section summary below it (IN-01); the backstop names which step did not complete
  but not why, so a failed rubric read reads like turn exhaustion (IN-02); and `[9.2.3]` pointed
  readers at a local-only, git-ignored planning record for its enumerations (IN-03) — corrected in
  place by `[9.3.0]`.

## [9.2.3] — 2026-09-12

Closes backlog **999.92** (Priority-order #1, the Self-Audit Gate half of R1) and 999.88 review
**WR-01**. The Self-Audit Gate's scoring vocabulary — the five tokens `Rigorous`, `Sound`,
`Hand-wavy`, `Band:` and `Quoted span` — is the larger half of R1's finding: nothing instructed the
agent to open `validation-rubric.md`, so every verdict block was scored against criteria the agent
re-authored from recollection. This release makes that read fire, and closes the failure-disclosure
gap WR-01 found in 999.88's own template imperative. No matrix rows are registered by this release
(no requirement IDs are mapped to this phase), so the coverage headline is unchanged at `229
reproducible / 116 audit-only / 0 gap / 345 total`, and the firewall battery tally and CI job
count are unchanged at **26/26** (24 `gate`/`gate_prereq` call sites plus 2 inline checks) and
**23** respectively — both established by direct count through `scripts/check-registration.py`'s
own parser at `154644e`.

**The bound this release ships under, now covering two read imperatives.** It shows both
imperatives are *present*. It shows nothing about a run *obeying* either of them. The *after*
reading for both is backlog **999.89**, whose census must also count `Read` of
`references/validation-rubric.md` now — that dependency is recorded against backlog 999.89, not
built here. Restated verbatim, on one line:
**presence is checkable, obedience is not.**

### Added

- **Read imperative for the Self-Audit Gate's rubric — 999.92** (`7c31c886d2bc0d673fd2173865b0941f931a7712`).
  One paragraph in `shared/spine/SKILL-body.md` (line 311), emitted through `sync-content.py` to
  `first-principles/agents/first-principles.md` (line 358). It names `Read`; fires once, after the
  self-audit scan is emitted and before the first verdict block — the rubric's own text states the
  scan itself "is not performed here", so the read governs scoring, not the scan's construction. Its
  failure sentence, paired in the same commit: "If that read fails, do not score from recollection:
  emit no verdict blocks, and disclose that the Self-Audit Gate did not run under the rule that
  closes this section." The Phase 5 Operation site (`shared/spine/SKILL-body.md:175`, emitted
  `:222`) gained a tool-free pointer sentence deferring to this read, so the imperative still fires
  exactly once per analysis. This phase deliberately declined 999.88's own precedent of naming its
  template's tokens: the five rubric-only tokens still read **0** in the body on both surfaces.
  That zero bounds what the body itself supplies, and nothing more: three other references the
  body links carry the same vocabulary — `examples/ishikawa-fishbone.md` all five tokens,
  `examples/composed-inversion-second-order.md` every token but `Quoted span`, and
  `assumption-taxonomy.md` `Hand-wavy` — so a verdict-block token in a live run's output is not
  evidence of the rubric read; only a `Read` `tool_use` of `references/validation-rubric.md` is.
  Every referent the shipped justification sentence cites resolves in
  `shared/spine/references/validation-rubric.md`: the scoring scale (`## Scoring Model`), the
  Absent verdict (that section's **Absent** level and its **Gate:** rule), the two conditions that
  clear the gate (`## How to Apply This Gate`'s two numbered conditions, restated as the **Pass:**
  line under `## Scoring Model`), and the fields a verdict block carries (`## Verdict Block
  Format`). This list was re-confirmed at the phase's code review (WR-04), which found that the
  record first published here named an earlier draft's referents instead.

### Fixed

- **WR-01 — the template imperative's failure-disclosure clause; the backstop widened**
  (`8d2ffb44b0b86d498b2fe517f7556076937196da`). 999.88's own `output-template.md` imperative
  (`shared/spine/SKILL-body.md:194`) shipped with no paired failure clause. It now carries one:
  "If that read fails, still assemble the document from the section summaries below, and disclose
  the failed template read under the rule that closes 'Before presenting conclusions'." The shared
  backstop sentence following the pinned `_BODY_DONOTPRESENT_AMENDED` sentence was widened in the
  same commit from its stale two-item "either" (a leftover from a two-item pre-amendment form) to
  cover all three pinned items plus a failed template read, naming that failure distinctly as "a
  document assembled from the section summaries alone" so a reader can tell a skipped gate from a
  skipped template read. The pinned sentence itself stayed byte-intact throughout.

### Changed

- **Read-imperative census, both surfaces.** Read imperatives in the agent body directed at a
  file, each naming its tool: **2 at `da59f3e`, 3 at `154644e`**, on both
  `shared/spine/SKILL-body.md` (lines 145, 194, 311, all at `154644e`) and
  `first-principles/agents/first-principles.md` (lines 192, 241, 358, all at `154644e`). A bare
  integer does not satisfy this by the agent body's own Phase 3 rule; each of the six qualifying
  sentences names its tool (`Read`) explicitly at the cited line, confirmed by direct read of both
  files at `154644e`.

### Known limitations

- **The new imperative has no paired failure-disclosure clause** (`[9.2.2]`'s Known limitations)
  is **closed by this release** — both this phase's rubric imperative and 999.88's template
  imperative now carry one, and the shared backstop covers both plus the ledger/scan/gate triad.
- **Nothing pins any of five unpinned product spans** shipped by this phase (the rubric imperative,
  its failure clause, the site-2 pointer, the WR-01 clause, and the widened backstop). The
  REACH-or-LEVEL determination — REACH, permitted, declined — is recorded against backlog 999.91
  (widened by this release rather than filing a new sibling entry). A skipped Self-Audit Gate's
  conclusions are still presented, under the top-of-response
  disclosure that they are unaudited — no confidence cap is introduced by this release.
- **No emitted artifact can only be produced by having opened `output-template.md`**, unchanged.
  Filed as backlog **999.90**, product tier.
- **No live run was taken by this release**, so obedience is unverified. Backlog **999.89** owns
  the *after* reading for both this phase's rubric imperative and 999.88's template imperative; its
  goal is amended, not yet built.

## [9.2.2] — 2026-09-12

Closes backlog **999.88**: the agent body referenced `output-template.md` four times and
instructed nobody to open it. The template now carries a read imperative in Phase 3's voice —
naming its tool, placed ahead of the emission rather than beside it — and the run's *before*
reading is frozen as tracked evidence first. No matrix rows are registered by this release: all
three plans carry `requirements: []`, so the coverage headline is unchanged at `229 reproducible /
116 audit-only / 0 gap / 345 total`. The firewall battery tally is unchanged at **26/26** and the
CI job count unchanged at **23**, both established by direct count through
`scripts/check-registration.py`'s own parser at `da59f3e`, rather than the battery's `GREEN` line.

**The bound this release ships under, stated rather than implied.** It shows the imperative is
*present*. It shows nothing about a run *obeying* it. The *after* reading — a `reference_reads`
census over a live capture — is filed as backlog **999.89** and is not in this release. Restated
verbatim, on one line: **presence is checkable, obedience is not.**

### Added

- **Read imperative for the output template — 999.88** (`956d033`). One paragraph in
  `shared/spine/SKILL-body.md` (line 194), emitted through `sync-content.py` to
  `first-principles/agents/first-principles.md` (line 241). It names `Read`, fires once
  immediately before emission, and justifies itself by what the body's own inlined section
  summaries *omit*: the `**Confidence:**` field the template requires at the end of every
  Derivation Chain's conclusion block (§4) and again at the end of the Conclusion section (§6),
  and the `Unverified input rule (D-07)` (§4) that forces that field to MEDIUM or LOW whenever a
  chain rests on a `GT-N?` input. Both referents were confirmed present in
  `shared/spine/references/output-template.md` (lines 332-335 and 369) and confirmed absent from
  the body's summaries, before the wording was fixed. The body's `### Turn discipline` rule —
  *"Spend turns on what advances a named artifact"* — is resolved by placement plus an in-sentence
  carve-out naming the signed-off analysis as that artifact, not by exempting the new instruction
  from the rule.
- **Frozen capture fixture — 999.88** (`4bd08ee`). `tests/reference-reads-v9.2.1/` — six files:
  the prompt catalog, the raw `DEMO-TRIAGE.jsonl` capture, the extracted analysis, two detector
  readings, and a chain-of-custody README — registered as the 24th `_FROZEN_PATHS` entry. The
  five copied files are proven byte-identical to their session-scratchpad originals by `cmp` and
  `sha256sum`. The `tool_use` census re-derived from the *frozen* copy, not the scratchpad, reads
  **WebFetch 3, Agent 1, Skill 1, ToolSearch 1, Bash 1, and zero `Read`/`Grep`/`Glob` calls** —
  the reading that made 999.88 a real defect rather than a suspected one. The directory keeps its
  `v9.2.1` name: it is named for the plugin version at freeze time, and `FROZEN-EVIDENCE` blocks
  renaming it. **Disclosed limits —** the `_FROZEN_PATHS` registration is not a new gate. It
  extends an existing inline check's array, which increments the battery tally once regardless of
  array length; the README states this in writing so the registration is not later mistaken for
  coverage.

### Changed

- **Read-imperative census, both surfaces.** Read imperatives in the agent body directed at a
  file, each naming its tool: **1 at `3c3ed42`, 2 at `da59f3e`**, on both
  `shared/spine/SKILL-body.md` (lines 145, 194, both at `da59f3e`) and
  `first-principles/agents/first-principles.md` (lines 192, 241, both at `da59f3e`). The baseline
  was re-derived at review from `git show 3c3ed42:shared/spine/SKILL-body.md`, not carried forward
  from a plan's claim. A bare integer does not satisfy this by the agent body's own Phase 3 rule;
  each of the four qualifying sentences names its tool (`Read`) explicitly at the cited line,
  confirmed by direct read of both files at `da59f3e`.

### Known limitations

- **The new imperative has no paired failure-disclosure clause** (product tier, warning, 0
  blocking — phase-999.88 review WR-01). The body's *other* file-directed read imperative (Phase
  3's) pairs with an explicit failure record and a no-silent-fallback clause; the *Before
  presenting conclusions* section carries its own "reference file unavailable" backstop. This one
  carries neither, so a failed `Read` is not required to be disclosed — the silent-omission shape
  the rest of the document repeatedly warns against. Open, not closed by this release.
- **Priority-order #1 is still open.** R1 names both `output-template.md` and the Phase 5 rubric;
  this release closes only the first. Closing one of a pair reads as closing the pair, so the
  pairing bound is published rather than left implied, and the countable exit criterion is
  recorded as 1 to 2 — the unpaired scope — not 1 to 3.
- **No emitted artifact can only be produced by having opened the template**, so the read's
  absence stays invisible to any offline check. Filed as backlog **999.90**, product tier.
- **Nothing pins the new imperative's literal**, so a prose edit can dissolve it without failing
  a gate. Filed as backlog **999.91**, apparatus tier.

## [9.2.1] — 2026-09-12

Closes backlog **999.78**: v9.2.0 gave all 13 focused stubs one byte-identical handoff tail that
hands their output to the main agent as unclassified candidates for Phase 2; three of them —
`identify-essence` (Phase 1), `reason-upward` (Phase 4), `validate` (Phase 5) — do not emit
Phase-2-shaped output, so each stub's closing handoff now hands its output to the phase its own
declared type belongs to. Covers **handoff shapes** (HAND-01 through HAND-05) and **release**
(REL-14 through REL-18). The coverage headline moves `225 reproducible / 110 audit-only / 0 gap /
335 total` to `229 reproducible / 116 audit-only / 0 gap / 345 total` (10 requirements registered
as matrix rows via `_rows_v921()`, 4 reproducible + 6 audit-only — HAND-01/02/03 were published as
`reproducible` at milestone close and re-tiered `audit-only` at the phase-31 review, CR-01, because
`check-focused-parity.py` pins no per-routed-stub destination literal; see
`docs/requirements-traceability.md` headline-history row 16). The firewall battery tally is
unchanged at **26/26** and the CI job count unchanged at **23** this milestone — the unchanged
totals are established by direct count at both `PHASE_BASE` (`c571ccf`) and this release. Backlog
**999.16**, open since Phase 11, is carried forward to **v9.3.0** by this release, not closed:
D-29-B's recorded answer ("no — focused surfaces are parity-enforced, not contract-registered")
stands as a decision of record, but ships only once its two remaining requirements land.

### Changed

- **Handoff shapes — 999.78** (HAND-01 through HAND-05). `identify-essence`'s closing handoff now
  routes its Essence Statement into the Input Contract's Problem statement and Key constraints
  fields as a framing, naming both fields and stating that a framing is not a candidate fact for
  Phase 2 (**D-29-A**). `reason-upward`'s closing handoff routes its Derivation Chains to Phase 5
  validation, with the ground truths those chains cite entering Phase 2 as candidates the run did
  not verify (**D-29-A**). `validate`'s closing handoff routes its findings as the Phase 5 verdict
  to act on, naming no re-entry edge that does not already exist (**D-29-A**). The remaining ten
  unclassified-facts stubs keep the v9.2.0 tail byte-unchanged. **D-29-C** records, as a decision
  of record, that Stub-13's remaining phase-of-origin classes are best distinguished by four
  groups derived from each stub's own declared phase — that re-partition itself did not ship in
  this release. **Disclosed limits —** `check-focused-parity.py --self-test` (the gate backlog
  999.78's own entry names as the one a prose-only edit could break) exits 0, and the type-mismatch
  reading is 0 at final HEAD, down from 3 at `1dc0892` — but the narrowing this release shipped is
  one-directional: re-adding the superseded Phase-2 tail to a routed stub still passes both legs
  (tracked as backlog **999.80**), and the narrowed population carries no floor of its own (tracked
  as backlog **999.79**). Both are open, apparatus tier; the remaining re-partition work moves to
  **v9.3.0**.

### Added

- **Release** (REL-14 through REL-18). Every hand-maintained version stamp reads `9.2.1` (17,
  `VERSION-01` green); 10 matrix rows registered via `_rows_v921()` (4 reproducible + 6
  audit-only) and the coverage headline moved by `HEADLINE-LOCK`'s sweep. The recurrence reading,
  stated as a frozen literal: the pre-registered type-mismatch pattern set, fixed before the first
  content edit and stated here rather than referenced — **R18-DEFECT**, the count of
  `shared/skills/*/SKILL.md` files whose frontmatter matches `Slash-only Phase (1|4|5) stub` and
  whose body contains `candidate inputs for Phase 2`; **R18-POP**, the count of those same files
  NOT matching `Slash-only Phase (2|3) stub` that contain that same tail (its population includes
  the eight correctly-unclassified no-declared-phase stubs by construction, so its target is 8, not
  0); and **R18-BARE**, the whole-tree count of files containing `candidate inputs for Phase 2`
  across `shared/` and `first-principles/`, via `/usr/bin/grep -rl … | wc -l`. That set read
  `0 / 8 / 20` at `PHASE_BASE` (`c571ccf`), `0 / 8 / 20` after this release's last commit touching
  either tree (`9bbcbc4`), and `0 / 8 / 20` re-confirmed after this entry's own commit — each by
  direct count over the three patterns above, never by reading the battery's own verdict line. The
  pre-registration baseline the same three patterns read before the routing edit was
  `3 / 11 / 26`. `tests/step0-captures-v7.11/` is byte-unchanged. Restated verbatim,
  on one line: **presence is checkable, obedience is not.** **Disclosed limits —** R18-POP's
  non-zero reading (`8`) is the correctly-unclassified no-declared-phase stub floor, not a
  residual defect; the standing-limit sentence proves each class's tail is present and the
  superseded tail is absent, never that a run obeys the routing it describes.

### Fixed

- **Input Contract — phase-28 review CR-01** (`1dc0892`). Bullet 4 of the shipped Input Contract
  claimed "Supplying a fact raises its priority for the Phase 3 verification step; it does not
  discharge that step." No such rule exists in the methodology — Phase 3's read-trigger is
  HIGH-confidence-chain membership alone, and Phase 2's stakes-escalation rule keys on the stakes
  of the conclusion; neither distinguishes a supplied fact from a discovered one. The bullet now
  states only what is implemented: **supplying a fact does not discharge Phase 3 verification for
  it.** The candidate-entry semantics, both provenance labels and `HARN-02`'s literals are
  untouched. This overturns the fourth sentence of **D-28-01**'s locked wording, by explicit
  developer decision at the phase-28 review gate. It reaches an installed session for the first
  time at `9.2.1`, because the stamps still read `9.2.0` when it landed — by this file's own
  preamble, a body edit without a bump never reaches an installed session. Recorded here at the
  phase-31 review (CR-02), which found it named in neither the `[9.2.0]` nor the `[9.2.1]` entry.
- **Matrix deliverable paths — 999.67** (`7dfd75f`). Four `deliverable_path` values in
  `_rows_*()` carried a trailing slash; dropped, and `docs/requirements-matrix.md` and
  `docs/data/matrix.json` regenerated. Same unrecorded window as the entry above, lower weight.

## [9.2.0] — 2026-09-12

Closes backlog **999.50** and **999.51**: a fact the user supplies — or a focused run hands over —
enters the main analysis as a candidate that Phase 2 classifies and Phase 3 verifies, never as a
ground truth exempt from challenge. Covers **supplied inputs** (SUP-01, SUP-02), **focused
handoff** (SUP-03, SUP-04), **guards** (GUARD-01 through GUARD-03), and **release** (REL-09
through REL-13). The coverage headline moves `217 reproducible / 106 audit-only / 0 gap / 323
total` to `225 reproducible / 110 audit-only / 0 gap / 335 total` (12 requirements registered as
matrix rows via `_rows_v92()`, 8 reproducible + 4 audit-only). The firewall battery tally is
unchanged at **26/26** and the CI job count unchanged at **23** this milestone — the unchanged
totals are themselves the success criterion (REL-10), established by direct count at both
`PHASE_BASE` (`1ccc90e`) and this release.

### Changed

- **Supplied inputs — 999.50** (SUP-01, SUP-02). Input Contract bullet 4 told the agent to treat a
  supplied fact as a "fixed starting point rather than assumptions to challenge," contradicting the
  mid-run paragraph in the same file that says an input "does not become a ground truth by virtue
  of arriving from the user." The bullet now routes each supplied fact into Phase 2 as a candidate,
  names the label it enters with (`reported-by-delegate` if it names a source, `unverified` if
  not), and points at the Phase 3 verification step without restating it. **D-B:** the label is
  carried by a pointer in the bullet; the three `reported-by-delegate` enumerations
  (`SKILL-body.md`, `output-template.md`, `validation-rubric.md`) were not widened, and widening is
  a later, separate change only if the pointer reads wrong in practice. **Disclosed limits —** a
  user's own first-hand observation names no source, so it enters `unverified` and carries `?`; an
  over-flagged ground truth costs a confidence caveat (D-28-03). The slot keeps its name, `Known
  ground truths` (D-28-05).
- **Focused handoff — 999.51** (SUP-03, SUP-04). Every focused stub's closing handoff now hands its
  output to the main agent as candidate inputs for Phase 2 and states at the handoff that the run
  opened no cited source, carrying its `?` marks forward; the re-derived population is 13 stubs
  (the `first-principles-analysis` launcher carries none). **Disclosed limits —** the tail is
  hand-copied into each stub source rather than generated from one token; HARN-03's per-stub
  assertion is the drift guard.

### Added

- **Guards** (GUARD-01, GUARD-02, GUARD-03). HARN-02 and HARN-03 each gained one presence literal
  and one absence literal inside an existing check, each with its own negative control; each
  extension's REACH-or-LEVEL determination is written on its gate page — see
  `docs/gates/HARN-02.md` § "REACH-or-LEVEL determination" and `docs/gates/HARN-03.md` §
  "REACH-or-LEVEL determination." The standing limit, in plain words:
  **presence is checkable, obedience is not.**
  These checks prove the new wording is present; no gate proves that a run
  obeys it. **Disclosed limits —** the absence literals match the exact superseded
  wording only; HARN-02 reads the `shared/` source, not the emitted agent body (DUAL-04 covers that
  agreement); HARN-02's and HARN-03's gate pages were promoted into `NARRATIVE_ENTRIES` to host the
  determinations, which turns off spelled-out-number containment on those two pages — the new
  prose was held to the stricter standard before it landed.
- **Release** (REL-09 through REL-13). Every hand-maintained version stamp at `9.2.0` (17,
  `VERSION-01` green); 12 matrix rows registered and the headline moved by `HEADLINE-LOCK`'s sweep
  (see `docs/gates/CONF-SURFACE.md` bound (14) for the two surfaces that sweep verifies but does
  not write). The recurrence reading, stated as a frozen literal: the exemption-shape pattern set —
  seven phrases, "rather than assumptions to challenge," "fixed starting point," "as/into/to/in
  (the) Known ground truths," "already verified," "exempt from challenge/classification/Phase,"
  "not challenged," and "without being challenged" — was fixed before the Input Contract was
  edited, and read `32` across `shared/` and `first-principles/` at `1ccc90e`. The reading of
  record, taken after this release's last commit touching either tree and re-confirmed after this
  entry's own commit, via `/usr/bin/grep -rzoiE` over that pattern set: **0**.
  `tests/step0-captures-v7.11/` is byte-unchanged. **Disclosed limits —** the reading is a pattern
  match, not a semantic proof: a reworded exemption in a shape outside the seven patterns would not
  be seen. The quantity-shaped sites the v9.1 recurrence reading recorded were deliberately left
  untouched so the next milestone's root replan (backlog 999.77) measures against this release
  unchanged. Nothing mechanical joins `_rows_v92()` to the requirement roster; it was checked by
  hand. One deviation was recorded during this release: plan 28-04 reworded a `CLAUDE.md`
  delta-chain hop's line wrapping before writing it to disk, after an in-process literal scan
  caught that the first draft would have introduced a new hand-maintained count literal that did
  not exist before the edit.

## [9.1.0] — 2026-09-11

Ships the milestone that names the mechanism behind the class [8.26.0] and [9.0.0] both shipped
live instances of — a hand-written prose claim whose truth is a digit no gate can dispute — and
lets the known-wrong sentences fall out of that answer rather than being fixed one at a time: the
**diagnosis** (PROSE-01 through PROSE-04), **containment reach** (CONTAIN-01 through CONTAIN-04),
the **generalized digit-narrowing rule and generated narrative regions** (NARR-01, NARR-02), the
**ratchets** (RATCHET-01 through RATCHET-04), and the **release act itself** (REL-05 through
REL-08). The coverage headline moves `208 reproducible / 97 audit-only / 0 gap / 305 total` to
`217 reproducible / 106 audit-only / 0 gap / 323 total` (18 requirements registered as matrix rows
via a new `_rows_v91()`, 9 reproducible + 9 audit-only), and the firewall battery tally is
unchanged at **26/26** this milestone — the unchanged total is itself a success criterion (D-D),
never an incidental fact.

### Added

- **Diagnosis** (PROSE-01 through PROSE-04). Named the mechanism: containment's `N → M`
  delta-exemption class strips the whole vector including its terminus, so a chain whose final
  value has gone stale reads as exempt rather than as a hit, indistinguishable to the checker from
  one that is current. A sibling site (`CLAUDE.md`'s own Review protocol paragraph, CR-02 below)
  was named before any fix was written. States in writing that the answer covers the
  **quantity-shaped** class only — a claim whose truth is a digit corroborable against a generated
  fence — and that the **consistency-shaped** class (one rule stated two contradictory ways, no
  digit to check) is out of scope, filed as backlog 999.50 and 999.51. Each of v9.0.0's carried
  findings now carries a recorded disposition: **CR-01** closed at Phase 25's chain-terminus arm,
  demonstrated failing-before and passing-after by mutation on a disposable scratch copy; **CR-02**
  dispositioned by routing rather than by fix — it states no digit, so nothing in this milestone's
  quantity-shaped scope can corroborate or contradict it — filed as backlog 999.55; **CR-03**
  remains accepted with its original bound, since `docs/README.md` carries no recognised generated
  fence for anything to compare its claim against, filed as backlog 999.54; **P-CR-01** (found by a
  post-`[9.0.0]`-entry review, never named in that entry) closed by the fix already shipped under
  it, commit `b661281`. **Disclosed limits —** `docs/v9.1-claim-containment-diagnosis.md` § 3 is a
  dated record of these dispositions as they stood at diagnosis time (2026-09-09); CR-01's own
  closure happened afterward, in Phase 25, and is stated here rather than on that page, which this
  milestone does not reopen as a region host.
- **Containment reach** (CONTAIN-01 through CONTAIN-04). `CONF-SURFACE`'s containment check now
  reaches `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md` and `docs/gates/*.md`, floored by
  a set-equality roster rather than a subset check; a chain-terminus arm
  (`chain_terminus_problems`) watches an `N → M` delta chain's own final value against its live
  source, the falsifiable closing point for CR-01 above; every REACH-or-LEVEL determination behind
  a containment change is written before the mechanism exists, not after. The deferred-literal and
  deferred-containment ledgers are both reconciled against a live re-adjudication of every entry —
  their growth-only/size-only bound (RATCHET-02, below) and the reconciliation deltas themselves
  are stated in `docs/gates/CONF-SURFACE.md`'s own disclosed-bounds section rather than restated
  here. **Disclosed limits —** the cannot-reach residue behind the reach above is its own count,
  never absorbed into it: `tests/premise-rejection-catalog.md`'s second G3 demonstration target
  carries no generated region at all, and `docs/COMPONENT-DIAGRAM.md`'s Mermaid node label sits
  inside a fenced code block a non-fenced marker line cannot bracket — both named individually in
  `docs/gates/CONF-SURFACE.md`'s disclosed bounds rather than fixed. This release's own act added
  a fresh entry to the deferred-containment ledger — a currently-correct digit with no
  corroborating generated field, the same raw shape this milestone's mechanism targets — tracked
  by the same growth-only bound rather than hidden; see that page for the entry.
- **The generalized rule and generated narrative regions** (NARR-01, NARR-02). `docs/PROCESS.md`
  section 2's digit-narrowing rule is generalized from the gate-battery count to every restated
  moving count on a product surface, pointing at `docs/gates/CONF-SURFACE.md`'s own generated
  `registered_surfaces` figure rather than stating a population as a digit. Two generated narrative
  regions (`CLAUDE.md`, `docs/README.md`, `docs/MEASUREMENT-MAP.md` — a third host added beyond the
  two originally scoped) now render their own coverage-headline sentence from the live harvested
  fact, wired into `scripts/gen-gate-docs.py --check`'s drift check alongside the pre-existing
  literal scanner. Filtering a fresh literal scan to the surfaces this migration reaches finds
  **zero** non-exempt hits, out of 80 total, all exempt. **Disclosed limits —** that zero is
  narrowed-scope, not tree-wide: the two cannot-reach residues named above
  (`tests/premise-rejection-catalog.md`, `docs/COMPONENT-DIAGRAM.md`) sit outside every region a
  narrative-region mechanism could bracket, named as a published, counted residue rather than
  silently absorbed into the zero.
- **The ratchets** (RATCHET-01 through RATCHET-04). `scripts/gen-gate-docs.py --check` runs the
  narrative-restatement census unconditionally on every commit (RATCHET-01), demonstrated by a
  four-arm mutation proof (two independent host surfaces plus the census arm each fail with a
  named file and line; the unmutated arm passes). The deferred-literal ledger carries a
  non-increase assertion with a growth-only/size-only bound restricted to `_CONTAINMENT_LEDGER_MAX`
  and `_DEFERRED_LEDGER_MAX` moving in one direction only, at a size a human re-adjudicates
  (RATCHET-02). A diff-review scan flagging a removed literal replaced by a hedge word was
  **dropped** rather than shipped: RATCHET-03 is discharged by a recorded verdict citing the
  meta-guard-regress argument its own proposer raised, not by a shipped scan — no new gate,
  holding D-D. Every one of RATCHET-01 through RATCHET-03's mechanism changes carries a written
  REACH-or-LEVEL determination made before the mechanism existed (RATCHET-04). **Disclosed
  limits —** none beyond what CONTAIN-04's bullet above already states; RATCHET-02's bound is
  cited there rather than restated twice.
- **The release act itself** (REL-05 through REL-08). All 17 hand-maintained version stamps read
  `9.1.0`, `VERSION-01` green, `sync-content.py --check` clean, `VERSION-01`'s PASS proven
  non-vacuous by mutation on a scratch copy (REL-05). The firewall battery tally is unchanged at
  **26/26** — established by a direct count of gate and inline-check registrations at both the
  phase's base commit and this release's own HEAD, with the battery's own printed tally cited only
  as corroboration (REL-06). This milestone's 18 requirements are registered as matrix rows behind
  a live-derived `V91-ROWS` equality sentinel (9 reproducible + 9 audit-only), and the
  coverage-headline move above is produced by `HEADLINE-LOCK`'s sweep across every
  `COVERED_HEADLINE_SURFACES` member plus both tracked matrix artifacts, never a hand edit
  (REL-07). Verification for this entry itself is measured against **product recurrence** — does
  this milestone's own defect class recur, counted the way `docs/PROCESS.md` counted its four
  prior recurrences — never against whether the new convention was followed; both instruments'
  readings (a frozen-scanner arm and an independent two-reader prose arm), at both the pre-release
  and post-release timing, are published unreconciled in `docs/conformance-baseline.md`'s
  `recurrence-reading` section rather than restated here (REL-08). **Disclosed limits —**
  `HEADLINE-LOCK` verifies every `COVERED_HEADLINE_SURFACES` member, but `gen-gate-docs.py --write`
  produces only the narrower, `_NarrativeRegion`-backed subset of three; the remaining two members
  (`docs/requirements-traceability.md`, `docs/COMPONENT-DIAGRAM.md`) require a manual edit on every
  headline move that `HEADLINE-LOCK` then verifies rather than produces — named in full in
  `docs/gates/CONF-SURFACE.md`'s disclosed bounds. Separately, nothing mechanical joins the 18
  matrix rows `_rows_v91()` registers to the requirement roster in `.planning/REQUIREMENTS.md`;
  the correspondence was checked by hand this phase, and a stronger, roster-derived equality check
  was considered and rejected as out of this phase's own scope.

**Addendum 2026-09-11, recurrence reading:** `docs/PROCESS.md`'s same-class trip, the rework
limit that halts a phase when a defect class it closed recurs, fired on this release's
post-release recurrence reading, read milestone-scoped as the ship phase's own context decided
before any reading was taken. The ship phase therefore closed halted for a root replan while this
release shipped in full; the halt is a statement about rework and changes no requirement's
verdict. The trip rests on sites both independent prose readers recorded at both timings, among
them `README.md:143`, `docs/CONFIGURATION.md:148`, `docs/DEVELOPMENT.md:171`,
`docs/ONBOARDING.md:113`, `docs/TESTING.md:117` and `docs/TESTING.md:118`; no firing site is
disputed. The reading also found sites made stale during the release block itself, true before
the release acts and false after them because the matrix-row registration moved their live
value: `CLAUDE.md:334`, `docs/README.md:27`, `docs/README.md:157` and, recorded by a single reader
only and so disputed, `docs/README.md:36`. The reach map of every site the scanner arm could not
see, grouped by why, is carried to planning-backlog entry 999.77, with dated pointers on 999.54,
999.57 and 999.58 for the sites those entries already own. The figures are in
`docs/conformance-baseline.md`'s `recurrence-reading` section and are not restated here. This
milestone shipped with its own goal measurably unmet: the quantity-shaped defect class it set out
to contain still recurs in prose its mechanism does not reach.

## [9.0.0] — 2026-09-09

Ships the milestone that measures and closes the exemplar-conformance gap [8.26.0] disclosed: the
**conformance baseline** (CONF-01, CONF-02), **exemplar conformance and the `CONF-GATE` ratchet**
(CONF-03 through CONF-06), the **adversarial corpus and its published false-negative rate**
(CONF-07, CONF-08), **live conformance** (CONF-09, CONF-10), the **generated claim surface**
(CONF-11 through CONF-13), the **depth rule with the review protocol and rework cap** (CONF-14,
CONF-15), and the **release act itself** (REL-01 through REL-04). The coverage headline moves
`192 reproducible / 94 audit-only / 0 gap / 286 total` to `208 reproducible / 97 audit-only / 0 gap
/ 305 total` (19 requirements registered as matrix rows via a new `_rows_v9()`, 16 reproducible +
3 audit-only), and the firewall battery tally moves **24/24** to **26/26** this milestone —
`CONF-GATE` (Phase 18) moved it 24 → 25, `CONF-SURFACE` (Phase 21) moved it 25 → 26.

### Added

- **Conformance baseline** (CONF-01, CONF-02). `docs/conformance-baseline.md` and
  `docs/data/conformance.json` report every `_DEFECT_RECORD_FIELDS` reading for all 14
  `shared/examples/*.md` files and separately for `shared/spine/references/output-template.md`,
  naming files the detector cannot read rather than skipping them; `--check` reproduces the
  committed artifacts byte for byte and exits 1 on drift. **Disclosed limits —** the file states
  no target and blocks no gate; its numbers are dated, a measurement rather than a contract.
- **Exemplar conformance and the `CONF-GATE` ratchet** (CONF-03 through CONF-06). All 14 shipped
  worked examples now resolve into six template sections (`0 of 14` unreadable, both
  shared-examples and generated-twin); `0` of 77 §2 verdict cells are non-conforming; `0` of 31
  chain blocks are malformed; §6 untraced claims read `2` (both marked, `0` silent), with the
  marked-claim residual pinned by `scripts/check-conf-gate.py`'s `_MARKED_RATCHET = 4` — a ratchet
  that may fall, never rise. `CONF-GATE` is a standing battery gate moving the tally 24 → 25.
  **Disclosed limits —** `heading_malformed_blocks == 0` proves conformance to
  `_chain_block_well_formed`'s measured reach (the head and first hop only), not to R7 as
  published; the `untraced_claims` reading does not reach zero by design — a marked caveat still
  scores untraced (`R-CLAIM-CAVEAT-MARKED`), and driving it to zero would mean inventing
  citations; `shared/spine/references/output-template.md`'s §4 worked examples are measured but
  not gated, because they deliberately include non-conforming forms as labelled teaching
  contrasts; and the closure-ledger citation route (`- "quoted claim" → chain Cn`) has zero
  shipped exemplars.
- **Adversarial corpus and its false-negative rate** (CONF-07, CONF-08). `tests/adversarial-corpus-v9.0/`
  ships 13 analyses that pass every form check while being substantively wrong, each with a
  written statement of what is false about it and which rule ought to have caught it; every item
  is filed with a named disposition — fix, accept-with-reason, or defer-with-owner. **Disclosed
  limits —** the published false-negative rate is **10 of 13**: the unmodified, CONTRACT-06-frozen
  `detect_defects` did not catch the catalogued falsehood in 10 of the 13 items (Stratum A 2 of 5,
  Stratum B1 1 of 1, Stratum B2 7 of 7). Stratum B2 (7 of the 13) is reachable by nothing this
  project ships.
- **Live conformance** (CONF-09, CONF-10). 8 live runs are captured on the shipped v8.26.0 body
  across the fixture set, each committed under `tests/live-conformance-v9.0/` with its full
  `detect_defects` reading; a live conformance rate is published in `docs/conformance-baseline.md`
  as an observation with its N stated, never a gate. **Disclosed limits —** the published rate is
  **5 of 8** (primary and secondary conditional rate agree; all 8 attempted runs completed),
  subject to the K-of-5 governing record's noise discipline (`docs/v8.7-constraint-teardown.md`
  §2 item 3: at N=5, noise equals effect). On this surface `heading_malformed_blocks`'s own
  denominator is nearly empty — the `### Conclusion` heading sweep found 6 blocks total across the
  8 resolved runs and none at all in 7 of them — so a quarter of the clean verdict's four counts is
  carried by a single run, not by all of them.
- **Generated claim surface** (CONF-11 through CONF-13). Every registered gate script supports
  `--describe`, emitting its own documentation row from its live constants; `CLAUDE.md`'s CI-gate
  table and `docs/ARCHITECTURE.md`'s inventory are generated from those emissions, with per-gate
  detail on `docs/gates/<GATE-ID>.md` and a gate failing when committed text no longer matches
  emitted text; a standing scanner drives hand-maintained branch-count literals in prose to **0**
  non-exempt. **Disclosed limits —** the scanner's `headline-provenance-delta` exemption class
  strips the entire `N → M` delta run, including its terminus, so a chain whose final value has
  gone stale is indistinguishable from one that is current and reads as exempt rather than as a
  hit — stated here as the requirement's own measured bound (D-11), not discovered by a reader.
- **Depth rule, review protocol and rework cap** (CONF-14, CONF-15). `docs/PROCESS.md` states the
  depth rule — "a guard guards the product; a guard is not itself guarded" — with the
  `999.27 → 999.28 → 999.30` chain cited as its measured justification; `CLAUDE.md`'s "Review
  protocol" section states the product/apparatus tier cut, the `/bm:code-review` output shape, and
  the block-on-product-findings-only rule. **Disclosed limits —** neither is enforced by any
  script, control, or CI job; `CLAUDE.md` states this plainly in its own words.
- **19 new traceability-matrix rows** (16 reproducible + 3 audit-only) via a new `_rows_v9()`,
  moving the coverage headline `192/94/0/286` → `208/97/0/305`. **Disclosed limits —** of the 16
  reproducible rows, only REL-03 carries a `_self_test_*`-prefixed anchor that `_resolve_artifact()`
  dispatch-checks; the other 15 carry a bare script path, because none of those five scripts
  (`report-conformance.py`, `check-conf-gate.py`, `check-firewall-battery.sh`, `gen-gate-docs.py`,
  `check-version-stamps.py`) defines a `_selftest_`/`_self_test_`-prefixed symbol — each script's
  own `--self-test`/`--check` CLI surface supplies that guarantee instead.

**Exemplar-conformance disclosure closed (SHIP-05).** `[8.26.0]` measured, with the unmodified
frozen detectors (`_slice_sections`, `_verdict_conforms`, `_conclusion_claims`,
`_chain_block_well_formed`), that the 14 shipped worked examples in `shared/examples/` violated
R1 through R12 at 68-100%: **4 of 14** unreadable by `_slice_sections`; **69/69** section-2 verdict
cells non-conforming; **56/58** section-6 claims untraced, with **0** carrying the
`no chain — flagged assumption only` marker; **19/28** chain blocks malformed. Re-derived
2026-09-09 with the same unmodified detectors: **0 of 14** unreadable, on both the shared-examples
and generated-twin columns; **0 of 77** section-2 verdict cells non-conforming — the denominator
moved **69 → 77** because CONF-03 made the four previously-unreadable files readable, exposing
verdict cells the detector had never been able to count; **2 of 77** section-6 claims untraced,
both marked and **0** silent — the denominator moved **58 → 77** for the same reason, and this
reading does not reach zero by design: a marked caveat still scores untraced
(`R-CLAIM-CAVEAT-MARKED`), and driving it to zero would mean inventing citations, not closing a
gap; **0 of 31** chain blocks malformed — the denominator moved **28 → 31** for the same reason.
Stating that these three denominators moved is the honest reading of this pair; pairing the old
`69/69` against the new `0/77` as though they shared one denominator would not be.

**Three accepted findings ship live and uncorrected.** Per decision D-14
(`.planning/phases/23-ship-v9-0-0/23-CONTEXT.md` — gitignored, and since relocated under
`.planning/milestones/v9.0.0-phases/`, so a reader of the published repo cannot open it; the
disposition it records is restated in full in the three bullets below), this release discloses
three findings that `docs/v9.1-claim-containment-diagnosis.md` § 3 accepted with a stated,
falsifiable bound apiece — the disposition of record for all three below. None of the three
sentences is corrected, deleted, or reworded by this release; each ships exactly as found.

**Correction, dated 2026-09-17 (v9.4.0 Phase 43):** as published, the D-14 citation above and the
CR-02 citation below named `.planning/` paths bare — the decision authorising this disclosure, and
the source record behind one of the findings — neither openable by a reader of the published repo
(backlog 999.59); the gitignore disclosure and the tracked-surface pointer are added by this note,
and the findings, dispositions and bounds themselves are unchanged. The disposition of record for
all three findings is `docs/v9.1-claim-containment-diagnosis.md` § 3, which is tracked, and no
finding's disposition rested on a `.planning/` path.

- **CR-01** — `docs/gates/CONF-SURFACE.md` § "Disclosed bounds", bound (6) narrates the
  deferred-literal ledger's growth history and states a most-recent hop of `182 → 184`, while the
  live `_DEFERRED_LEDGER_MAX` in `scripts/gen-gate-docs.py` reads `181`. The standing scanner's
  `N → M`-shaped exemption class strips the whole delta vector including its terminus, so a stale
  terminus and a current one are indistinguishable to it. Disposition: accepted, closing at
  Phase 25's chain-terminus arm (CONTAIN-02). See `docs/v9.1-claim-containment-diagnosis.md` § 3.
- **CR-02** — as published, `CLAUDE.md` § "Review protocol" **cited** CR-05 as "an edit made in
  `scripts/` that produced a product-tier defect," but CR-05's own `File:` field names only `docs/`
  prose (`docs/README.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md`). That field
  lives in `.planning/phases/21-generate-the-claim-surface/21-REVIEW.md`, which is gitignored and
  since relocated, so it is unreadable from the published tree; it is reproduced verbatim in
  `docs/v9.1-claim-containment-diagnosis.md` § 3, which is tracked — read the claim there.
  Disposition: accepted, dispositioned by routing rather than by fix, filed as backlog 999.55. See
  `docs/v9.1-claim-containment-diagnosis.md` § 3.

  **Correction, dated 2026-09-17 (v9.4.0 Phase 43):** that `CLAUDE.md` sentence was corrected in
  this same phase under backlog 999.55 — it now names the `docs/` files CR-05's `File:` field
  names — so this bullet's original present tense no longer described the live page and is
  restated in the past tense: what v9.0.0 shipped, not what `CLAUDE.md` says today. The dated
  transcript in `docs/v9.1-claim-containment-diagnosis.md` § 3's CR-02 subsection no longer
  reproduces either, and carries the same note.
- **CR-03** — `docs/README.md` **stated, in two places**, that `whole-system-remeasure-verdict.md`
  is cited by 13 matrix rows — the § "Standing of the nine milestone documents" row for that
  document, and its § "Reference & history" row — against a live distinct-row count in
  `docs/data/matrix.json` of 12, a raw substring count over-counting one row that cites the
  document twice. Disposition: accepted, with the bound that nothing this milestone reaches it —
  `docs/README.md` carries no recognised generated fence to compare the claim against — filed as
  backlog 999.54. See `docs/v9.1-claim-containment-diagnosis.md` § 3.

  **Correction, dated 2026-09-17 (v9.4.0 Phase 43):** this bullet named only the first of the
  two occurrences while the introducing paragraph above frames the three findings as the
  disposition of record shipping "exactly as found", which read as complete coverage of a defect
  it covered half of (backlog 999.58); the second occurrence is named above as of this note. Both
  occurrences were also reworded off the count in the same phase under backlog 999.54, so this
  bullet's original present tense no longer described the live page and is restated in the past
  tense — what v9.0.0 shipped, not what `docs/README.md` says today.

## [8.26.0] — 2026-09-04

Ships three deliverables that make the emission rendering contract's own claims checkable: the
**chain-head grammar** (Phase 13, CHAINHEAD-01..07), the **closure-ledger claim inventory**
(Phase 14, LEDGER-01..04), and the **self-audit scan** (Phase 15, SCAN-01..04). `output-template.md`
section 4 now states the head-line grammar prescriptively — consumed inputs are `GT-N` or `Cn`
identifiers, each optionally glossed in parentheses, joined by `+`, with the first arrow closing
the head — byte-identical across four canonical surfaces, with a conforming and a non-conforming
worked example scored by the unmodified `_chain_block_well_formed` and a sha256 pin freezing it.
The section 6 → section 4 closure ledger's claim-extraction rule (R11) and caveat rule (R12) are
stated on all three contract surfaces, with the 2026-09-02 PR-P1 analysis committed as
`tests/quality-ledger-v8.26/` and pinned at its measured reading. Phase 5 now emits a chain-form
and claim-inventory scan as process output; Criteria 4 and 6 quote that scan as their evidence
rather than asserting a band, and SCAN-GUARD asserts the scan's presence, placement and coherence
in the emitted tree. The coverage headline moves `175 reproducible / 91 audit-only / 0 gap / 266
total` to `192 reproducible / 94 audit-only / 0 gap / 286 total` (20 requirements registered as
matrix rows via a new `_rows_v826()`), and the firewall battery tally stays **24/24** — SCAN-GUARD
was registered at Phase 15 and already moved it 23 to 24; this milestone registers no new gate.

### Added

- **Chain-head grammar** (`output-template.md` §4, CHAINHEAD-01..07). The head-line grammar is
  stated prescriptively with a conforming and a non-conforming worked example (including the
  possessive/prose form, `C2's threshold`, that the 2026-09-02 run actually emitted), registered
  byte-identical across four canonical surfaces in QUAL-01's cross-surface literal set, and frozen
  under a sha256 digest pin (`_selftest_chain_detector_pin`) over `_chain_block_well_formed`'s own
  source. **Disclosed limits — POSITIONAL, not universal:** R7's, R9's and R10's bounds are
  measured properties of the frozen form check, not of the grammar itself. R7/R9 bind the rule in
  every input position, but the mechanical check reaches only the head and the first hop, so it
  under-detects the same violation later in a chain; R10 discloses the mirror-image bound — a head
  or first hop that closes its own sentence before the next arrow is scored malformed even though
  it violates none of R1-R9, and that over-rejection is itself positional.
- **Closure-ledger claim inventory** (LEDGER-01..04). R11 (claim extraction) and R12 (caveat) are
  now stated on all three contract surfaces, matching what `_conclusion_claims` extracts; the
  2026-09-02 analysis is registered as a fixture asserting its measured reading (one untraced
  claim, the trade-offs paragraph). **Disclosed limits:** a bare bold lead-in alone on its line is
  a section-intro label and escapes the claim obligation; a bold span whose closing `**` does not
  immediately follow a colon is never matched; a short unpunctuated list item is under the
  assertiveness floor; and a caveat carrying the `no chain — flagged assumption only` marker still
  scores untraced BY DESIGN — the marker discloses the gap, it does not discharge the claim.
  `_slice_sections`' section 6 now stops at the first ATX heading not inside a fenced code block,
  and never later than the Self-Audit Gate (the Gate cap); an unterminated fence in section 6
  returns nothing, per CommonMark.
- **Self-audit scan** (SCAN-01..04). Phase 5 emits a chain-form and claim-inventory scan as
  process output, one row per chain block and one per section-6 claim; Criteria 4 and 6 quote that
  scan as their evidence rather than asserting a band; SCAN-GUARD asserts the scan's presence,
  placement and internal coherence on both the agent and skill-stub surfaces. **Disclosed limits:**
  SCAN-GUARD does not assert that a scan row's content is correct, and does not assert that a live
  run complied with the prescription (that needs 999.12/999.13). No focused-mode skill stub carries
  Criterion 4 or 6 at all (backlog 999.16 remains open), and the SCAN-04 emission-cost comparison
  (2,288 vs. an independent 1,381-character reconstruction) is disclosed as unfalsifiable rather
  than settled.
- **20 new traceability-matrix rows** (17 reproducible + 3 audit-only) via a new `_rows_v826()`,
  moving the coverage headline `175/91/0/266` → `192/94/0/286`. The SCAN-01..03 anchor entries are
  not dispatch-checked by `_resolve_artifact()` — `check-selfaudit-scan.py` has no
  `_selftest_*`-prefixed symbol — so a call-site census in `V826-ROWS` covers them instead; that
  census counts source text without observing behaviour.

**Exemplar-conformance disclosure (SHIP-05).** Re-derived at execution time (2026-09-04) with the
unmodified frozen detectors (`_slice_sections`, `_verdict_conforms`, `_conclusion_claims`,
`_chain_block_well_formed`) over the 14 shipped worked examples in `shared/examples/`: **4 of 14**
are unreadable by `_slice_sections`; **69/69** section-2 verdict cells are non-conforming; **56/58**
section-6 claims are untraced, with **0** carrying the `no chain — flagged assumption only` marker;
**19/28** chain blocks are malformed. This release adds R7 through R12 while shipping exemplars
that violate R1 through R12 at 68-100%. Publishing the rules while omitting that number is the one
option inconsistent with this project's own disclosure discipline. **v9.0.0** is the milestone
that closes this gap.

## [8.25.0] — 2026-09-01

Widens `HEADLINE-LOCK` from one current-fact surface to five — `CLAUDE.md`, `docs/README.md`,
`docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md`, plus the pre-existing
`docs/requirements-traceability.md` — recognising both the prose and compact-slash renderings
and distinguishing historical/delta statements from current-fact claims (Phase 10,
HEADLINE-01..05); and makes the emission rendering contract in `output-template.md` §4/§6 and
`SKILL-body.md` prescriptive enough to be mechanically checked — chain hop wrapping, citation
form, and the verdict-expiry worked example (Phase 11, CONTRACT-01..06). The coverage headline
moves `161/91/0/252 → 174/92/0/266`. No new gate was registered this milestone — the firewall
battery tally stays **23/23**.

### Added

- **`HEADLINE-LOCK` widened to five `COVERED_HEADLINE_SURFACES` members.** `CLAUDE.md`,
  `docs/README.md`, `docs/MEASUREMENT-MAP.md`, and `docs/COMPONENT-DIAGRAM.md` now carry the
  same self-test-asserted, non-vacuity-controlled headline check that previously covered only
  `docs/requirements-traceability.md`. Both the prose form
  (`N reproducible / M audit-only / 0 gap / T total`) and the compact slash form (`N/M/0/T`) are
  recognized as the same claim; a two-layer history classifier (whole-file membership plus a
  figure-adjacent arrow layer) exempts genuine historical/delta statements — such as
  `docs/v8.0-final-closure.md`'s frozen v8.0 count and the traceability ledger's move-history
  rows — from tripping the gate, without exempting a stale current-fact line on the same surface.
- **Emission rendering contract made mechanically checkable.** `output-template.md` §4 states
  the chain-hop no-wrap and brevity rules with conforming and non-conforming worked examples;
  §6 states the citation form to the same standard; the Verdict Vocabulary section carries a
  worked `current constraint` expiry example. `SKILL-body.md` restates the identical no-wrap,
  brevity, citation, and head-form rules as shared verbatim literals. QUAL-01 Item 24 extracts
  all eight worked examples from the shipped canonical bytes and scores them with the unmodified
  detectors (`_chain_block_well_formed`, `_verdict_conforms`, `_claim_is_traced`), plus
  cross-surface literal reconciliation and a registry lock.

## [8.24.0] — 2026-08-31

Ships capture-based provenance verification: the generation `.jsonl` capture is now retained
beside the extracted analysis, a real capture fixture is committed, and PROV-GUARD — the first
check in the stack that can falsify a `*Provenance: read-at-source*` label against what the run
actually fetched — is registered in CI and the firewall battery. Records fact, not form. New
gate PROV-GUARD; the firewall battery moves **22/22 → 23/23**.

### Added

- **PROV-GUARD**, a new offline gate (`scripts/check-provenance.py`), registered as a CI job
  (`check-provenance (PROV-GUARD)`) and a battery `gate` call, both running `--self-test` and the
  live leg. It parses an analysis's section 3 ground truths and provenance labels, joins every
  `read-at-source` GT to the real `WebFetch`/`Read` call in the run's stored `.jsonl` capture that
  fetched its cited source, and requires every numeric/currency literal the GT states to appear
  verbatim in that source's retrieved text. Live result:
  `7/7 sources matched, 35/35 literals located`. **What it does not assert:** it does not verify a stated number means what the
  analysis says it means, nor that the citing chain is valid inference (backlog `999.4`); the
  literal regex also matches digit tails of identifiers (`x86` yields `86`), which is expected
  behaviour, not a parser bug; whole-span bold/quoted matching was measured and rejected
  (4/11 bold spans, 4/8 quoted spans located); PROV-04's no-network control blocks `socket` but
  does not cover a `subprocess` shell-out.
- **Capture retention and a committed fixture.** `--probe` and `--single` now persist the
  extracted analysis beside its source `.jsonl`, closing the standing blocker on verifying those
  paths after the run ends. `tests/quality-provenance-v8.24/` is committed and registered as a
  whole-directory entry in the battery's FROZEN-EVIDENCE path list.
- **Provenance findings as named `_DEFECT_RECORD_FIELDS` columns**, not audit-only underscore
  fields, so a fabricated or mislocated literal reaches the emitted TSV alongside every other
  defect.
- **15 traceability-matrix rows** for the milestone's requirements, via a new `_rows_v824()`
  locked by a V824-ROWS count sentinel. The coverage headline moves
  `147/90/0/237 → 161/91/0/252`.
- **Gate-count tallies corrected** across `scripts/check-firewall-battery.sh`'s header (stale
  since v8.21.0, omitting REG-GUARD), `CLAUDE.md`, and `docs/ARCHITECTURE.md` — each now reads
  the post-PROV-GUARD numbers.

### Changed

- **The chain-dependency and self-audit findings now reach the emitted TSV.** Three columns
  were appended to `_DEFECT_RECORD_FIELDS` — `dependency_cycles`, `ungrounded_chains`,
  `selfaudit_disagreements` — closing the 8.23.0 known limitation. They were previously
  audit-only fields, reachable only by importing the module and reading the returned dict, so
  `--detect-defects` reported nothing about cycles or self-audit disagreement.
- `read_defect_incidence` now maps columns **by header name** when a header is present,
  falling back to positional mapping only for a headerless file. All twelve committed
  defect-incidence TSVs in `tests/` are the original ten-column shape; a positional reader
  keyed to the current field count would have rejected every one of them the moment the schema
  widened. The reader stays loud on a ragged row or a header missing a required flag column
  (T-164-12 discipline). Pinned by self-test Item 18, whose controls (f)-(h) assert the three
  appended columns carry **non-zero** findings and track their audit-only lists — pinning them
  only at zero, which every other fixture reports, would have passed with the columns hardcoded
  to a constant.

### Fixed

- **A closure ledger was scored as a traceability defect rather than as traceability.** Found
  by re-running the PR-P1 fixture live against the working tree while verifying the three new
  columns above. The analysis traced its Conclusion claims through an explicit
  `§6→§4 closure ledger` — each claim quoted beside the chain that produced it — instead of
  inline parentheticals. `_conclusion_claims` mined the ledger's own rows as ten additional
  claims (7 → 14) while `_claim_is_traced`, which only accepts a citation found *inside* the
  claim text, left the three claims those rows discharged counted as untraced (0 → 3). The
  new `selfaudit_disagreements` column then escalated that into a Criterion 6 over-claim
  finding. **The rubric does not support the charge**: Criterion 6 requires only that each
  claim "traces to a specific named derivation chain in section 4" and does not prescribe
  where the citation sits, and `output-template.md` §6 prescribes three prose blocks with no
  inline-citation instruction at all. So an agent that traced its claims *more* explicitly
  scored worse on both numerator and denominator, and the widened schema turned a detector
  blind spot into an accusation. The detector was the defect, not the verdict — the same
  shape as the 8.23.0 Criterion 4 finding, with the surfaces reversed.

  Two independent halves: `_conclusion_claims` no longer mines fenced code blocks (verbatim
  structural content, not section-6 prose), and `_claim_is_traced` accepts a closure-ledger
  entry that quotes the claim and cites a real chain. Ledger credit is deliberately narrow —
  an entry must cite a chain id that actually appears in section 4, quote at least four
  content tokens, and cover 70% **of the fragment's** tokens (never the claim's, so a long
  claim cannot absorb a short unrelated quote). Re-scored: the live run moves from
  `claims 14, untraced 3, selfaudit_disagreements 1` to `claims 4, untraced 0,
  selfaudit_disagreements 0`; the two prior runs, which cite inline and have no fenced §6
  content, are byte-unchanged.

  Pinned by self-test Item 17 (`_selftest_ledger_traceability`), ten controls: three
  positive/fault-injection, four anti-overreach (a ledger citing a chain that does not exist,
  a sub-minimum fragment, a fragment quoting something else, a long claim absorbing a short
  quote), one discriminating the fence rule from the claim filter, and one frozen-corpus
  movement pin. Five fault injections each fail the sub-check on the control that owns it.
- **The frozen corpus gained a count pin the flags could not provide.**
  `_CALIBRATION_UNTRACED_FLAGS` is saturated at `[1, 1, 1, 1, 1, 1]` and is therefore
  structurally blind to any movement in the counts beneath it — the blindness
  184-REVIEW.md WR-01 found in `_CALIBRATION_CHAIN_FLAGS`, which stayed green through a +7
  false-positive regression. `_CALIBRATION_CONCLUSION_CLAIMS` and
  `_CALIBRATION_UNTRACED_CLAIMS` pin what the flags cannot see, measured before the change
  above and re-measured byte-identical after it. Two of the five fault injections move the
  frozen corpus and are caught only by this pin.
- Corrected the 8.23.0 entry's chain-form figures, which were captured at intermediate states
  and did not reproduce against the detector shipped in that same release.
- QUAL-01's coverage description in `CLAUDE.md` and `docs/ARCHITECTURE.md` had not been
  updated for the chain-heading, chain-dependency and self-audit-reconciliation checks.
- Self-test items 14-16 were registered above item 13, so they executed before it and the
  numbering implied a sequence that did not hold. Registrations relocated; execution order now
  matches.


## [8.23.0] — 2026-08-31

Ships the arrow-led chain-form fix and the three measurement-instrument defects found while
verifying it. No new gate; the firewall battery stays at 22/22. Content-only release —
without this stamp bump the 8.22.0 install would never see any of it.

### Fixed

- **Derivation chains rendered as ordered lists.** Neither `shared/spine/SKILL-body.md` nor
  `shared/spine/references/output-template.md` said how a chain carrying more hops than fit on
  one line should be rendered; both showed only the single-line form. A live run needed six hops
  and rendered them as `1.` / `2.` / `3.`, which splits one chain into disconnected GT-headed
  one-hop fragments. Both surfaces now state the arrow-led wrap and name the ordered-list
  rendering as non-conforming. Measured against the detector **as shipped in this release**:
  the pre-fix analysis scores 5 of 6 chain blocks malformed with 1 of 8 §6 claims untraced; the
  post-fix analysis scores 0 of 7 malformed with 0 of 7 untraced. (The pre-fix figure was
  originally observed as 6 of 6 against the detector of the day; it reads 5 of 6 here because
  the GAP-6 fix below now accepts that analysis's one composition head — the number moved
  because a definition changed, which is the intended behaviour of a pinned figure, not drift.)

- **GAP-5 — the detector could not parse the chain heading the template prescribes.**
  `output-template.md` §4 prescribes `### Conclusion C1: [text]`, but `_CHAIN_HEADING_RE`
  anchored its label immediately after the hashes, so only the `Chain `-prefixed and bare forms
  parsed. **The failure direction was silently green:** with zero chain ids `_chain_blocks`
  falls back to one whole-section block whose single well-formed chain suppressed every
  malformed one, reporting `malformed_chain_blocks: 0` on a document with two. A
  malformed-chain regression on any analysis following the template was invisible to the
  harness. Pinned by self-test Item 14.

- **GAP-6 — composition chain heads rejected.** `GT-5 (label) + C6 (label)` scored malformed
  whatever its arrow form, while `GT-5 (label) + GT-2 (label)` scored well-formed — yet two
  shapes the output template itself produces are compositions (the trade-off matrix collapse
  and the second-order extension). Composition is now accepted. Because GT-only heads were
  acyclic *by construction* — a ground truth is an axiom and cannot depend on a chain — the
  widening ships with `_chain_dependency_defects()`, reporting cycles and chains that reach no
  ground truth by any path; without it the change would have traded a false positive for a
  false negative on circular reasoning, which the validation rubric names as an abandonment
  reason in its own right. Pinned by self-test Item 15.

- **Criterion 4 scored reasoning quality but not chain form, and the Self-Audit Gate was never
  reconciled against measurement.** Two live runs scored themselves Criterion 4 — Rigorous with
  Gate: PASS, one of them with every chain mechanically malformed. The verdicts were defensible:
  Criterion 4's band descriptors scored only semantics, and the prescribed rendering appeared in
  the criterion's preamble and in none of its four bands. The rubric was the defect, not the
  verdict. The Rigorous band now requires the rendering and the Sound band names ordered-list
  rendering as the demotion; `_selfaudit_calibration_defects()` reconciles claimed bands against
  the measured record so the self-report is falsifiable rather than merely stated. Only a
  claimed **Rigorous** is contradicted — the other bands already concede a defect. Pinned by
  self-test Item 16.

### Added

- `tests/premise-rejection-catalog.md` — candidate fixture covering a stressor class no
  existing fixture reached: a false premise asserted as consensus while the solution is
  pre-selected. The only pre-existing "Everyone knows" rows are slash-invoked
  `/first-principles:inversion`, where the premise is the *named subject* of the requested
  technique. 2×2 factorial over (premise contested × solution pre-selected), with an
  anti-contrarianism control so an agent that rejects every premise handed to it fails.
  **Not wired to any gate** — no script reads it and no CI job runs it; committed as a proposal
  with its promotion targets and their costs recorded in the file.

### Known limitations

- The dependency (`_dependency_cycles`, `_ungrounded_chains`) and self-audit
  (`_selfaudit_disagreements`) results are audit-only fields on `detect_defects`, **not**
  `_DEFECT_RECORD_FIELDS` columns: that schema is compared column-by-column against the
  committed calibration corpus, and adding a column is a separate decision. Consequence:
  nothing gates on cycles or on self-audit disagreement — both are visible to a caller, not
  to CI.
- Both live runs behind these fixes are n=1 and recorded as observations, not gates, per the
  governing record in `docs/v8.7-constraint-teardown.md` §2 item 3.


## [8.22.0] — 2026-08-30

First published release since 8.17.5. Tags `v8.18.0`, `v8.19.0` and `v8.20.0` were cut but
never released, so installs remained on 8.17.5; this release carries their content forward.

**Version note.** The `v8.21.0` tag is superseded and should not be used: it was cut without
bumping the 17 stamps, so the content at that tag stamps itself `8.20.0`. Installing it would
have been an inert update for anyone already on 8.20.0 — the v8.14 failure mode. The tag is
left in place on origin rather than moved; 8.22.0 replaces it. The REG-GUARD work that tag was
meant to carry is released here.

### Added

- **REG-GUARD** — offline plugin registration completeness gate
  (`scripts/check-registration.py`). Verifies every skill directory under
  `first-principles/skills/` and the main agent carry a frontmatter `name:` matching their own
  directory/file basename, and that any manifest-declared additional paths resolve inside the
  plugin. Registered as CI job `check-registration (REG-GUARD)` and in the firewall battery,
  both running `--self-test` and the live scan. Self-test carries 24 isolated control fixtures
  with positive and anti-masking negative controls; because those fixtures are tempdir/in-memory
  and never read the shipped tree, only the live leg asserts the invariant on the shipped
  plugin. Battery moved from 21/21 to 22/22.

### Fixed

- **GATE-01 was not provably validating the shipped agent.** `claude plugin validate` (VAL-01)
  never reaches the agent at all: the CLI walks *subdirectories* of `agents/` and skips flat
  `agents/*.md`, so it validates the 29 reference siblings under `agents/references/` — which
  are not agents — and misses `agents/first-principles.md`, which is. Verified against a
  minimal probe plugin: a flat `agents/solo.md` alone emits no `Validating agent:` line.
  `claude plugin details` confirms the loader is correct where the validator is not
  (`Agents (1)`), so this is an upstream CLI bug, not a plugin defect. That left GATE-01 as the
  sole validator of the agent frontmatter, carrying weight it was not built to carry:
  - `AGENT_FILE` was dead code; the battery and CI each passed the same relative path via
    `--file`, making the gate cwd-sensitive and its target silently re-pointable. `--file` now
    defaults to the repo-anchored constant and both live legs drop the argument.
  - A clean PASS was unfalsifiable. `_assert_live_coverage()` now mutates the frontmatter the
    run actually read (stripping `name:`) and fails unless the checker reports that specific
    defect, so a vacuous checker cannot report green.
  - The live leg prints a `COVERAGE — validated <path>` line.

### Known issues

- The 29 `No frontmatter block found` warnings from `claude plugin validate` are the upstream
  misclassification described above and are expected. They are deliberately **not** silenced:
  adding frontmatter would make 29 inert content files look like agent definitions, which is
  worse than the warning.
- VERSION-01 checks that the 17 stamps agree with *each other*, not that they agree with the
  git tag — which is why the `v8.21.0` mislabel passed every gate. `claude plugin tag`
  validates tag-vs-manifest agreement and is the intended guard for future releases.

## [8.20.0] — 2026-08-30

Hardens the HARN-01 gate with complete structural isolation coverage: all 16 neutralizable
branches now carry named control fixtures, and an anti-masking assertion gates on full coverage.

### Changed

- **HARN-01 self-test hardening: 16/16 branch coverage with anti-masking assertion.**
  - Coverage: **8 body-side branches** (B-01, B-02, B-03, B-04-tools, B-04-imperative,
    B-05-termination, B-06-not-found-assign, B-12-table) **+ 8 rubric-side branches** (R-01,
    R-02-slice, R-02-whole, R-03-block, R-04-crit2, R-04-crit5, R-05-pointer, R-07-band).
  - Each branch has a named isolation control fixture ensuring the gate detects its removal or
    mutation without misclassifying it as a pass.
  - **Anti-masking gate:** `_check_negative()` records a `branch_id` when each fixture correctly
    fails. The run fails naming any uncovered branches unless the recorded set equals all 16.
    This prevents a fixture being silently disabled while the gate still reports PASS.
  - **Control count:** Phase 7 delivered 8 fixtures (50 controls); Phase 8 delivered 8 more
    fixtures (8 additional controls), for a total of **58 controls** (50 → 58).
  - Coverage moved **8/16 → 16/16**. Documentation: `scripts/check-act-limb-branches.md` lists
    every branch with its line number, condition, neutralization point, and owning fixture.
- **The battery remains unchanged at 21/21.** HARN-01 was hardened, not added. The gate was
  registered in v8.18.0 and this release tightens its control structure.
- **All 17 hand-maintained version stamps moved to `8.20.0`** in lockstep.

The HARN-01 controls are structural assertions over the emitted tree. They prove each branch's
decision logic cannot be individually neutralized without detection; they do not measure agent
behavior on a live run. MEAS-01 (live harness for evidence acquisition) and MEAS-02 (quality
A/B) remain deferred.

## [8.19.0] — 2026-08-30

Implements the HIGH-confidence bound gate (HC-BOUND) and tightens confidence scoring in the
Self-Audit Criterion 3 (Evidence) and Criterion 5 (Conclusion). Reconstructed from annotated tag.

### Added

- **HC-BOUND gate** — structural validation asserting Phase 5 confidence tightening is present
  and well-formed in both the canonical and emitted rubric surfaces. Three documented EXCEPT
  exceptions (unreachable sources, speculative chains, absent-fails derivations) are verified.

### Changed

- **Criterion 3 (Evidence) tightening:** At least one HIGH-confidence chain must support each
  cited reachable source. Chains lacking HIGH-confidence assignment are listed and flagged during
  the analysis.
- **Criterion 5 (Conclusion) tightening:** Every conclusion must rest on at least one
  HIGH-confidence chain. LOW- and MEDIUM-only conclusions are flagged.
- **Anchor-control ratchet:** 19 controls added to the self-test to verify the tightened
  boundary and exception handling.
- **The battery moved 20 → 21** with HC-BOUND registration in CI.
- **All 17 hand-maintained version stamps moved to `8.19.0`** in lockstep.

HC-BOUND is a structural gate: it asserts the prescribed prose is present and well-formed in
the emitted rubric. It does not measure whether the agent actually *achieves* the confidence
bound on a live run. MEAS-01 and MEAS-02 remain deferred.

Source: `git show v8.19.0` (annotated tag body).

## [8.18.0] — 2026-08-29

Closes the four PRAOR-loop gaps found by the 2026-08-27 review of the agent body against
Perceive → Reason → Act → Observe → Report: no Act limb, an unreachable evidence rule, no
Observe→Perceive return edge, and stub/focused-mode divergence. Full record:
[`docs/v8.18-praor-loop-closure.md`](docs/v8.18-praor-loop-closure.md).

### Added

- **Phase 3 gains a bounded evidence-acquisition step.** The methodology now names a
  verification action — open the cited source with `Read`/`Grep`/`WebFetch` — that makes
  `read-at-source` provenance reachable rather than only a label the agent could apply without
  earning it. The provenance rule states plainly what each suffix means: a ground truth the
  agent actually read carries `read-at-source`; a well-formed citation it did not open stays
  `reported-by-delegate` and keeps its `?`. When a source cannot be opened, the failure is
  recorded — which source, why unreachable — and there is no silent fallback to an unmarked
  ground truth. The step names its own bound (which ground truths earn a read — those feeding
  HIGH-confidence chains — and which do not) so it cannot starve the Self-Audit Gate's turn
  budget under `maxTurns: 60`, since the gate runs last and is what gets dropped when a budget
  runs out.
- **Observe→Perceive re-entry edges.** A Criterion 1 Absent verdict now has a named, bounded
  route back to Phase 1 to re-frame the Essence Statement, and `input-contract.md` states that
  `AskUserQuestion` may re-open input mid-run when validation reveals a missing input, not only
  before the analysis starts. Every re-entry edge carries a stated maximum number of
  re-perception passes, and a fired edge is recorded — what changed and why — so a reader can
  tell a revised analysis from a first draft.
- **A scope-proportionate `{{FOCUSED_VALIDATION}}` step**, now emitted into all 13 focused slash
  stubs (`shared/skills/<slug>/SKILL.md`), giving a slash-invoked technique an Observe limb
  instead of stopping at its raw procedural output.
- **Three new offline gates** — HARN-01 (`scripts/check-act-limb.py`), HARN-02
  (`scripts/check-loop-closure.py`), HARN-03 (`scripts/check-focused-parity.py`) — each asserting
  its corresponding closure is present and well-formed in the emitted tree, with negative
  controls proving every tree-reading assertion site can fail. All three are registered in
  `scripts/check-firewall-battery.sh` and gained a CI job in `.github/workflows/validation.yml`.
- **23 v8.18 traceability rows** (`_rows_v818()` in `scripts/check-traceability.py`, 21
  reproducible / 2 audit-only) and the `V818-ROWS` sentinel pinning the tier partition by
  requirement ID — the first **v8.x** milestone requirement block registered as matrix rows
  since v7.9 (the v7.11 block, `_rows_v711()`, registered 11 audit-only rows in between).

### Changed

- **Step 0's execution-branching parenthetical now names Validate** among the phases that run
  under focused mode, closing the gap where the agent's own documentation understated what its
  internal `focused-<technique>` mode did.
- **The offline battery moved 17 → 20**, all three new gates registered and green.
- **All 17 hand-maintained version stamps moved to `8.18.0`** in lockstep; `check-version-stamps.py`
  reports all 17 in agreement.
- **The coverage headline moved 126/88/0/214 → 147/90/0/237**, the first v8.x milestone block
  since v7.9 to register matrix rows — a stated departure from the historical Phase 142 D-01 note
  (which reasoned no further block should register after v8.0's "final" accounting), left
  byte-intact with a dated addendum beside it in `docs/requirements-traceability.md`. The
  discriminator: v8.18's 21 reproducible requirements are each backed by a re-runnable offline
  gate, the first requirement block since v7.9 with that property.
- **`docs/v8.0-final-closure.md`'s immutability trait is lifted.** That document previously kept
  its coverage figures deliberately untouched on the reasoning that rewriting them would falsify
  the historical record; that reasoning's founding premise — that v8.0 wrapped the project and no
  further milestone would move the headline — expired once the headline moved for the first time,
  well before this release. The document's current-state claims (§4's superseded-by note, the
  standing banner, the battery-tally line) now read `147/90/0/237` and `20/20`, in a new dated
  addendum appended in the same append-only shape as its existing 2026-07-19 FREEZE-02 addendum;
  its own v8.0-dated measurement (`133/96/0/229`, battery `15/15`) is left untouched as the
  historical fact it records. This is a v8.18.0 policy change in its own right, separate from the
  figure move above — the `## [8.17.2]` entry's correction note (below) records only that the
  figure moved; this bullet is where the freeze-lift itself is recorded.

### Fixed

- **Self-Audit Criterion 3's `read-at-source` rule was unreachable** — no step existed that could
  earn the label. Closed by the evidence-acquisition step above.
- **A Criterion 1 Absent verdict had no named route back** to Phase 1 or to re-opening input.
  Closed by the Observe→Perceive edges above.
- **The 13 focused stubs stopped at raw technique output** instead of completing the loop with a
  validation step. Closed by the `{{FOCUSED_VALIDATION}}` snippet above.
- **VAL-03's third leg shelled out to an interpreter that could not import pytest**, which made
  `bash scripts/check-firewall-battery.sh` report `FIREWALL: RED` on an otherwise clean tree —
  indistinguishable from a real link-check regression. `resolve_pytest_python()` now tries
  `.venv/bin/python3` first, then `python3`, each confirmed by an `import pytest` preflight, and a
  `gate_prereq()` wrapper reports an unmet prerequisite as a third, distinguishable outcome —
  `FIREWALL: BLOCKED`, exit 2 — that a real gate failure still outranks.

The three new gates are structural: they assert the prescribed prose is present and well-formed
in the emitted tree, not that the agent performs the acquisition step or fires a re-entry edge on
any given live run. MEAS-01 (a live harness for the Act limb) and MEAS-02 (a quality A/B for
evidence acquisition versus confidence downgrade) remain deferred v2 requirements — see
`docs/v8.18-praor-loop-closure.md` §7.

## [8.17.5] — 2026-08-17

Closes **D-02**, the last of the three link surfaces. Every markdown link the plugin ships now
resolves.

### Fixed

- **Skill-stub cross-technique links target the peer stub.** The 12 remaining broken links
  (`](pre-mortem.md)` ×4 and `](second-order.md)` ×2 in `skills/inversion/SKILL.md`,
  `](inversion.md)` ×3 and `](trade-off.md)` ×2 in `skills/second-order/SKILL.md`,
  `](five-whys.md)` in `skills/fishbone/SKILL.md`) now point at
  `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md`.

  **This was a different defect from the agent surface's**, which is why it was held back rather
  than swept in with v8.17.4. The agent surface had *no* resolution — a bare filename resolved
  against the session working directory. A skill stub *does* get resolution: the harness resolves
  a slash-invoked skill against its own directory. These links broke because that mechanism
  pointed them somewhere wrong — `skills/inversion/pre-mortem.md` does not exist. Absent
  resolution and a wrong path need different fixes.

  The target was a genuine choice between three options, and the peer-stub file link won because
  it leaves the surrounding prose byte-identical, resolves on disk, and unlocks the VAL-03
  promotion below. The alternatives — a backticked `/first-principles:pre-mortem` namespace ref
  (more idiomatic for a slash-invoked skill, but rewrites 12 sentences) and a link into the
  agent's own reference tree (a layering smell) — were considered and declined.

- **The four `references/<slug>-detail.md` pointers stay file-relative.** They already resolve
  against the stub's own directory, which is exactly how the harness loads a skill.
  `_absolutise_skill_peer_links()` runs *after* `_rewrite_detail_link()` specifically so the
  detail target has a `/` by then and falls outside the bare-filename pattern; the reverse order
  would mis-target it as a peer skill.

### Changed

- **VAL-03 now full-checks `first-principles/skills/*/SKILL.md`, retiring D-05's deferral.** That
  surface was namespace-only for exactly one reason: full-checking it would have failed the 12
  links above, and D-02 deferred deciding where they should point. With the decision made, the
  glob was promoted into `FULL_CHECK_GLOBS`. It stays in `NAMESPACE_ONLY_GLOBS` as well —
  `_collect_files` dedups by resolved path and the surface legitimately wants both axes. The live
  scan went from 221 to 237 checked links.

- **The self-test's disjointness assertion became an overlap-and-dedup assertion.** The two glob
  lists were disjoint and the self-test asserted it; `SKILL.md` is now deliberately in both. The
  underlying risk is unchanged — main() must visit the shared file, exactly once — so the check
  now asserts the overlap is precisely what is intended and that dedup collapses it, rather than
  asserting an overlap of zero.

- **D-06's honesty note is superseded and says so.** It recorded that both newly-added VAL-03
  surfaces matched zero live findings, making the `--self-test` fixture the only thing keeping
  them load-bearing. That is no longer true: `skills/*/references/*.md` matches 4 real files and
  `skills/*/SKILL.md` now contributes 16 real relative links. The namespace-ref axis is still
  vacuous (zero backticked refs in any stub) and the PASS line still says so.

- **GATE-02-v8.5 sweeps the skill-stub surface too**, mirroring v8.17.4's agent-side sweep, and
  fails loudly if it matches zero stubs. An unrecognised bare target raises at generation.

- **A fourth broken link, found by sweeping rather than by a gate.** After the three surfaces
  were done, a plugin-wide resolve-every-link sweep turned up one more:
  `agents/references/examples/self-application.md` **quoted** the agent body's
  `](references/assumption-taxonomy.md)` inside prose, and markdown rendered that quotation as a
  live link resolving to `agents/references/examples/references/…` — a path that never existed.
  It survived because `references/examples/` was excluded from VAL-03 as "illustrative content,
  NOT link-checked source". Being illustrative makes a file's links no less broken. The glob is
  now full-checked, and the quotation is described rather than reproduced, since it was never
  navigation. The example's own point is unaffected; the stale pre-8.17.3 body text it quotes is
  now marked as historical.

  Worth noting how it was found: three gates were green and the three surfaces I set out to fix
  were all correct. What surfaced it was asking a different question — *does every link in the
  shipped tree resolve?* — instead of *did my change work?*

### Where each surface now stands

| Surface | Link form | Why |
|---|---|---|
| Agent body | `${CLAUDE_PLUGIN_ROOT}/agents/references/…` | read with the session cwd in force; substitution documented for agent content |
| Agent reference siblings | `${CLAUDE_PLUGIN_ROOT}/agents/references/…` | same, but the token is inference-resolvable rather than documented-substituted (v8.17.4) |
| Skill stubs — cross-technique | `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` | peer content lives under its own skill directory |
| Skill stubs — detail pointers | `references/<slug>-detail.md` | resolves against the stub's own directory, which is how a skill is loaded |
| Worked examples | prose, no live links | the one link there was a quotation, not navigation |
| `shared/` sources | bare filenames | canonical and surface-neutral; each emitter rewrites for its own surface |

Plugin-wide verification: **57 links checked across the shipped tree, 0 unresolvable.**

### Still owed

**No live run has verified that the Self-Audit Gate now fires.** Unchanged across 8.17.3, .4 and
.5. All three remove documented causes; none is evidence.

Battery: 17/17 GREEN. Three fault injections: a broken peer link in a stub (VAL-03 reports it —
proving the promotion is non-vacuous), the peer rewrite removed (GATE-02's stub sweep names
`fishbone`, `inversion` and `second-order`), and the glob demoted back to namespace-only (the
self-test's non-vacuity and overlap assertions both fire).

## [8.17.4] — 2026-08-17

Closes the second-hop residual v8.17.3 named and deferred. **Overturns DEC-A.**

### Fixed

- **The agent's reference siblings are now anchored to each other.** v8.17.3 fixed the first hop
  (agent body → `references/validation-rubric.md`) and left 16 links *between* files in
  `first-principles/agents/references/` bare — 4 `-detail.md` pointers plus 12 cross-technique
  links (`](pre-mortem.md)`, `](inversion.md)`, `](trade-off.md)`, `](five-whys.md)`). So an
  agent that successfully opened `five-whys.md` and followed its pointer to `five-whys-detail.md`
  failed at the second hop in exactly the way the first hop used to. All 16 now carry the
  `${CLAUDE_PLUGIN_ROOT}/agents/references/` prefix. With the four `-detail.md` files and the
  three spine references carrying zero relative links, the agent-side reference graph is now
  clean end to end.

- **`shared/references/*.md` deliberately keeps the bare form.** The rewrite lives at the
  emission layer (`_absolutise_agent_ref_links()` in `sync-content.py`), not in the source,
  because those same 16 links also feed the skill stubs — where the correct target is a
  different path. Skill stubs are byte-unchanged by this release.

### Changed

- **DEC-A is overturned, deliberately and by name.** DEC-A held that an agent reference sibling
  must keep its bare pointer because it lands in the same directory as its detail file. That
  reasoning was true of the filesystem and false of the reader: a model opens these files with
  the *session* working directory in force, so "same directory" never applied to it.
  GATE-02-v8.5's (g) assertion is inverted to match — anchored exactly once, bare **zero** times.

- **GATE-02-v8.5 gained a directory-wide bare-target sweep.** The per-slug loop only ever visited
  the four `SLUGS_WITH_DETAIL` pointers; the 12 cross-technique links lived in files it never
  named, so a per-slug assertion could not have caught them and could not catch a future one. The
  sweep asserts the property that actually matters — no emitted agent reference file carries a
  bare markdown target — and fails loudly if it matches zero files rather than reporting a
  vacuous clean.

- **An unrecognised bare `.md` target now raises.** The allowed-target set is derived from
  `TOOLS` / `SLUGS_WITH_DETAIL` / `SPINE_REFERENCES` rather than hand-maintained. A bare link to
  something not emitted into that directory is a typo: passing it through would leave the
  same-class bug alive with no signal, and anchoring it blindly would mint a broken absolute
  path.

### Scope of the claim on this surface — narrower than the agent body's

The documented substitution table covers **"Skill and agent content"** — the registered
component content the harness itself loads. These reference siblings are **not** registered
components; they are plain files the model opens with Read, and the docs are **silent** on
whether placeholders are substituted inside them (checked 2026-08-17 against
`code.claude.com`'s plugins-reference and skills pages; the env var is also not exported to an
agent's Bash). The token is used here because it is **self-describing and inference-resolvable**
— the model reached the file via an already-expanded absolute path, so
`${CLAUDE_PLUGIN_ROOT}/agents/references/x.md` is trivially recoverable, whereas a bare `x.md`
requires reconstructing the directory from nothing. This is a strictly better pointer, not a
guaranteed-substituted one. v8.17.3's substitution claim applies to the agent body and is not
restated here.

### Still open

The **12 cross-technique links reaching the skill stubs** (`](five-whys.md)` in
`skills/fishbone/SKILL.md`) remain broken, and this is not the same defect wearing a different
hat. Those break because they point at a *wrong path* inside a resolution mechanism that works —
a slash-invoked skill does resolve against its own directory — whereas the agent surface had no
resolution at all. The correct target is genuinely undecided (`D-02`): the peer skill stub at
`${CLAUDE_PLUGIN_ROOT}/skills/five-whys/SKILL.md`, or the same content on the agent surface at
`${CLAUDE_PLUGIN_ROOT}/agents/references/five-whys.md`. Those are not interchangeable, so the
choice is a decision, not a sweep.

Also still owed, unchanged from 8.17.3: **no live run has verified the Self-Audit Gate now
fires.**

Battery: 17/17 GREEN. Three fault injections: a broken anchored link on the sibling glob (VAL-03
reports it), an unrecognised bare target (emission raises), and the rewrite call removed
(GATE-02's sweep names `inversion.md` and `second-order.md` — files the per-slug loop never
visits).

## [8.17.3] — 2026-08-16

Fixes the reason the agent could not open its own Self-Audit Gate.

### Fixed

- **Agent-body reference links are now plugin-root-anchored.** Every `references/…` link the
  agent body carried was file-relative. An agent body is read with the *session* working
  directory in force — not the directory the agent file lives in — so
  `references/validation-rubric.md` resolved against the user's project, where it does not
  exist, and the read failed. All 25 of the agent body's reference links (21 in
  `shared/spine/SKILL-body.md` plus the four `-detail.md` pointers `sync-content.py` emits onto
  the agent surface) now carry the `${CLAUDE_PLUGIN_ROOT}/agents/references/` prefix, which
  Claude Code substitutes in agent and skill content wherever it appears. This reaches the
  Self-Audit Gate, the output template, the assumption taxonomy, the fourteen worked examples,
  and the four on-demand detail appendices.

  The live v8.14.0 run against the Umesh Bhatt article is the observation behind this: zero
  `Band:` / `Rigorous` / `Hand-wavy` markers across 533k characters — the Phase 5 gate never
  fired. Absolutising the link removes one of that failure's two documented causes (the other,
  a name collision with a user-requested rubric, was addressed at 8.15.0). **It is not proof the
  gate now fires** — no live run has been taken since; that measurement is still owed.

- **Skill stubs deliberately keep the file-relative form.** A slash-invoked skill is resolved by
  the harness against its own skill directory, so `references/<slug>-detail.md` already works
  there. `_rewrite_detail_link()` in `sync-content.py` now takes a per-surface prefix
  (`AGENT_REF_PREFIX`) instead of one hardcoded form.

**Known residual — this fixes the first hop, not the whole chain.** The agent's own reference
siblings under `first-principles/agents/references/` still carry 16 file-relative links between
each other (`](pre-mortem.md)`, `](five-whys-detail.md)`, and so on). Those resolve correctly
*within that directory* but not from a session working directory, so an agent that successfully
opens `${CLAUDE_PLUGIN_ROOT}/agents/references/five-whys.md` and then follows its pointer to
`five-whys-detail.md` fails in exactly the way this release fixes one level up. Left alone
deliberately: it is outside the agent body, and the bare form there is a DEC'd invariant
(DEC-A) that GATE-02-v8.5 actively asserts, so changing it is a separate, gated decision rather
than a tail of this one. The Self-Audit Gate, output template, assumption taxonomy and worked
examples are all reached in one hop from the body and are therefore unaffected by this residual.

### Changed

- **VAL-03 resolves `${CLAUDE_PLUGIN_ROOT}` rather than skipping it.** The cheap accommodation
  would have been to skip the unfamiliar prefix the way `http://` is skipped — which would have
  dropped the entire agent body out of link checking while `check-links.py` still printed PASS.
  `_resolve_link` maps the token onto `first-principles/` instead, so every absolutised link is
  still validated, and validated against the path the agent will actually open. Section 8 of the
  `--self-test` pins this with a positive assertion, a non-vacuity check that the rubric really
  is there, and a negative control; both a repointed target and a reversion-to-skip were
  fault-injected and caught.
- **GATE-02-v8.5 asserts the two assembly surfaces separately.** The drift guard previously
  expected one rewritten pointer form on both the agent body and the skill stub. It now expects
  the plugin-root-anchored form on the agent body — *and zero file-relative fallbacks there* —
  and the file-relative form on the stub.

Battery: 17/17 GREEN.

## [8.17.2] — 2026-08-16

Closes all six streams of the 2026-08-16 duplication-and-staleness audit (PR #8).

**Agent and skill content are byte-unchanged from 8.17.1.** `shared/` was not touched by this
release, so the assembled agent body and all fourteen skill stubs are identical. The only shipped
change inside the plugin is `first-principles/README.md`, which had still described v3.0.0. The
version moves because installs are version-gated, not content-gated — a stamp that does not
advance is a change that never reaches a session. Do not read a behaviour difference into this
bump; there is none to read.

### Added

- **SEMGATE now locks all six documented technique-overlap pairs, not three.** The audit's CAP-1
  finding was that `fishbone ↔ five-whys`, `theoretical-limit ↔ estimate` and
  `pre-mortem ↔ trade-off` were disambiguated only in reference prose — no catalog row, no
  precedence lock — so a Step 0 phrase-table reorder could silently flip any of them, and VAL-04
  is structurally blind to that axis. Six rows added to `tests/step0-fixture-catalog.md`
  (S-A07…S-A12: a co-fire row and a `full-composer` boundary control per pair) plus three
  catalog-independent assertions in `check-step0-emulator.py`, so deleting a row cannot make the
  assertion vacuous. Each pair was **measured before it was asserted** and all three already
  resolved as intended, so no phrase table was reordered and no version bump is involved.
  Proven by three injections against the live tree — a wrong expected value, a drifted catalog
  prompt, and a fishbone/five-whys row swap that flips S-A07 — because every new fixture passing
  on the first run is how a vacuous gate looks.
- **VERSION-01 gate — the stamp-lockstep rule above is now enforced.**
  `scripts/check-version-stamps.py` discovers every hand-maintained version stamp by glob and
  asserts they all carry the same value. Until now nothing checked this: `sync-content.py` copies
  `metadata.version` through per-file rather than propagating one source of truth, and the
  documented "version string invariant" checks a stamp's *format*, not its agreement with the
  others — so a single missed stamp shipped an inert update with every gate green, which is what
  happened at v8.14. Wired into `.github/workflows/validation.yml` and
  `scripts/check-firewall-battery.sh`; battery composition moves 16 → 17. The stamp count is
  reported, never asserted, so adding a skill does not require editing the gate.

### Removed

- **Three retired scripts**, none of which had a live consumer:
  `scripts/check-sub-skill-routing.py` and `scripts/check-focused-output.py` (deprecated thin
  shims — `check-routing-battery.py` had already replaced both, and its own header said so), and
  `scripts/check-inventory.py` (a requirement-ID auditor whose input corpus,
  `.planning/milestones/*-REQUIREMENTS.md`, is gitignored and superseded by
  `docs/requirements-traceability.md` under CANON-01; no requirement in the traceability surface
  referenced its AUDIT-01..04 IDs). `tests/test_81_inventory.py` went with the last of these,
  having loaded it by hard path.
- `scripts/check-body-budget.py` was **kept**, deliberately. TEARDOWN-01 retired the body-budget
  gate but preserved the reporter, and the firewall battery's untallied `[INFO]` line still
  consumes it. Only its documentation footprint was pruned.
- **Guards migrated, not dropped.** `tests/test_65_doc_invariants.py` had pinned the two shims
  across six tests — their self-tests, the boundary p-threshold default of 2, the catalog dry-run
  parse, and a `CLAUDE.md` mention. Each invariant moved onto `check-routing-battery.py` under its
  namespaced `--boundary-*` / `--focused-*` flags, plus a new guard asserting the three retired
  scripts do not reappear. Two of the old tests would have kept passing vacuously: one was
  satisfied by the sentence *recording* the retirement, and one pinned flag spelling rather than
  the threshold values it existed to protect.
- The `v3.8/EVAL-01` matrix row named `check-focused-output.py` as its `deliverable_path`. That
  field is reported but never existence-resolved (only `artifact_link` is), so a dangling path
  would have failed silently — it is repointed at the successor with the substitution recorded,
  and `docs/requirements-matrix.md` / `docs/data/matrix.json` regenerated. Row count unchanged
  at 214.

### Changed

- **`tests/` is classified, and nothing is deleted.** 550 tracked files sorted into three tiers —
  **102 gate-pinned** (opened at runtime by an offline gate, or `artifact_link`-resolved),
  **7 live-unwired**, **441 archive** — recorded in a new `tests/README.md` with the decision and
  its reasoning. The audit's two-way pinned/archival split was the wrong shape: it hid the middle
  tier. Re-running its trace reproduced the 441 aggregate but disagreed on the composition, and
  its pinned breakdown never summed to its own headline (56 + 24 + 16 + 6 + 4 = 106, under a
  headline of 110). Zero `step0-baseline-v*.md` files are opened by any gate; the audit's six came
  from counting `deliverable_path` entries, which are reported and never existence-checked.
- **`scripts/trace-tests-usage.py`** — new manual reporting tool that re-derives that
  classification by tracing `open` events under `sys.addaudithook` while each gate runs. The audit
  called its own trace reproducible while it existed only as prose; this makes the claim literal.
- **7 pytest suites carrying 123 assertions are run by no CI job** — CI runs pytest on exactly one
  path, `scripts/check-links_anchors_test.py`. Among them are the retirement guards migrated into
  `test_65_doc_invariants.py` one commit earlier. Named as a tier rather than silently reclassed;
  wiring them into CI is logged as follow-up.
- **The nine surviving milestone documents in `docs/` are adjudicated, and none deleted.** They
  had survived the 2026-08-16 prune as an undifferentiated block, with nothing distinguishing a
  rule still in force from a measurement true only of its date. Each now opens with a **Standing**
  banner giving its class and its live dependents; `docs/README.md` carries the summary table. The
  audit posed it as "governing record or historical narrative?" — that binary fits four of them.
  Five are neither: *frozen evidence*, cited for provenance by live artifacts while asserting
  nothing current. A third class covers `gen-01-rearch-milestone.md`, the only one of the nine a
  gate resolves (TRACE-03 fixture (9) deep-resolves its `artifact_link`; verified by removing the
  file and watching `--self-test` exit 1). "Gate-pinned" first had to be disentangled from an
  index artefact: removing *any* of the nine fails VAL-03 because `docs/README.md` links all
  nine, which measures the index rather than the document. The verdicts live in the documents rather than only in
  an index because the failure being closed — `v8.0-final-closure.md` calling a moved figure
  "final" — persisted exactly because its warning sat in `CLAUDE.md` instead.
- **`v8.14-delivery-verification.md` is the case against pruning by reference count.** Fewest
  inbound references of the nine, and least prunable on merit: it is the published form of a
  pre-registered STOP still governing Phases 189–191 and GREENMEAN-01's WON'T-DO scope.
- **`first-principles/README.md` rewritten.** The shipped plugin README still described v3.0.0 —
  a "plugin contents removed" banner, six companion tools, six worked examples, and no mention of
  the `skills/` directory. It now describes what the plugin actually ships (8 technique references
  with 4 detail siblings, 3 spine references, 14 worked examples, 14 slash-invocable skills), each
  count verified against the tree. Its outbound links stay absolute, and the file now says why, so
  the v8.17.1 defect is not reintroduced by a later tidy-up. **This is shipped content: it reaches
  installed users only on the next version bump.**
- Repo documentation consolidated onto one owner per topic, and a set of stale claims corrected
  along the way — including a mechanism that six documents had backwards (`{{TOOL:slug}}`
  substitutes a *name*, not a procedure, so the technique procedures are not inlined into the
  agent body). Full record in
  [`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md).
- **The Self-Audit Gate rename reached the user-facing docs.** 8.15.0 renamed the Validation
  Rubric to the Self-Audit Gate because two instruments shared one name, but the change stopped at
  the agent surface: `README.md` (×4), `docs/ARCHITECTURE.md` and `docs/METHODOLOGY-CHEATSHEET.md`
  kept the old name — the exact collision the rename existed to remove. The file is still
  `validation-rubric.md`. One occurrence remains in shipped content
  (`shared/skills/first-principles-analysis/SKILL.md`) and is logged as follow-up, since changing
  it requires a regen and a version bump.
- The coverage headline now has one authoritative home. Three surfaces asserted the superseded
  v8.0 figure (133/96/0/229) as current against the real 147/90/0/237;
  `docs/requirements-traceability.md` is the single source, and `docs/v8.0-final-closure.md` keeps
  its numbers unedited with a superseded-by note, since it is the record of what v8.0 measured.

  > **Correction (v8.18.0, 2026-08-29).** This entry originally quoted the real figure as
  > `126/88/0/214` — accurate when 8.17.2 shipped, now superseded by the v8.18 matrix-row
  > registration (`147/90/0/237`, see `docs/requirements-traceability.md` headline-history row 8).
  > Separately, `docs/v8.0-final-closure.md`'s "keeps its numbers unedited" policy described above
  > was itself **lifted at v8.18.0** — its premise (that v8.0 had wrapped the project) expired when
  > the project resumed. See the `## [8.18.0]` entry below.

## [8.17.1] - 2026-08-16

### Fixed

- **Links in shipped plugin content escaped the plugin root.** Four relative links pointed
  above `first-principles/` with `../` — one in the agent body
  (`agents/first-principles.md` → `../../docs/testing-agents-headlessly.md`) and three in
  `first-principles/README.md` (→ `../README.md`, `../CHANGELOG.md` ×2). Inside the repo they
  resolved, so no gate caught them: `check-links.py` validates the repo tree, where the
  targets exist. For anyone who installs the plugin standalone — the normal case, since
  `docs/` and the repo root are never delivered — all four were dead. Each is now an absolute
  URL into the GitHub repo, which resolves from either surface. The agent body carries no
  other outbound link, and no `../` link remains anywhere in `shared/` or `first-principles/`.

A patch release, not a minor: this fixes a defect and opens no milestone. It is the project's
first patch version — every prior release was milestone-numbered `X.Y.0`. All 17 version
stamps moved in lockstep per the note above, because without the bump the fix would never
reach an installed session.

Non-shipping change in the same window: `docs/` was pruned of 34 historical milestone
documents (61 tracked entries → 27, −898 KB). Removed files remain in git history; see the
**Retrieving removed documents** note at the top of `docs/README.md`.

## [8.17.0] - 2026-08-16

Fixes the defect recorded below: the `?`-count is now **enumerated by ID** rather than asserted
as an integer, and the Self-Audit Gate checks the enumeration against the Ground Truths list
instead of quoting it.

### Changed

- **Phase 3 exit criterion now requires an enumeration, not a count** (`shared/spine/SKILL-body.md`).
  Write `?-marked: GT-2, GT-5, GT-9, GT-14 (4 of 22)` — the list, not the number. **A stated
  integer no longer satisfies the criterion**, on the grounds that an integer cannot be checked
  against the list it summarizes and an enumeration can, by inspection. Where a count accompanies
  an enumeration and the two disagree, **the enumeration governs.**
- **Output template's provenance summary** updated to the same form, with a worked example
  (`shared/spine/references/output-template.md` §3).
- **Self-Audit Gate Criterion 3 now verifies rather than quotes** (`shared/spine/references/validation-rubric.md`).
  Explicit instruction added: *"Check the enumeration, do not quote it."* Quoting the analysis's
  own provenance summary as the satisfying span does not discharge the criterion — that verifies a
  summary was written, not that it is correct. The gate must read the Ground Truths list, collect
  the IDs actually carrying `?`, compare, and cite the comparison.
- **Band ladder retightened for this criterion.** A bare count with otherwise-correct suffixes now
  bands **Sound** rather than Rigorous. **An enumeration that disagrees with the list bands
  Hand-wavy** — a mismatch understates unverified inputs in the direction that flatters the
  analysis, and unlike a bare count it was checkable, so it is a stronger failure than never
  enumerating at all.

### Known defect (fixed above; retained for the record)

The defect this release fixes, as originally recorded:

#### The `?`-count exit criterion was satisfied in form and failed in substance

v8.16.0's Phase 3 exit criterion requires the count of `?`-marked ground truths to be stated
explicitly. **Across every draft observed in post-release testing, a count was stated and none
was correct.** Three runs against the same prompt — two turn budgets, both agent versions:

| Draft | Stated | Actual |
|---|---|---|
| full-composer, `maxTurns: 60`, base | 24 of 41 | **31 of 41** |
| same run, consolidated after revision | 17 of 45 *(while enumerating 20 IDs)* | **21 of 57** |
| full-composer, `maxTurns: 30` | 17 of 22 *("the unsuffixed five")* | **15 of 22** *(seven unsuffixed)* |

The consolidated draft is the sharpest case: it reports the same quantity **three different ways
inside one document** — a header figure, an enumeration of a different length, and an actual
suffix count that matches neither.

**Self-Audit Gate Criterion 3 passes all three.** It quotes the stated count as its satisfying
span rather than recomputing it, so the gate verifies *that a count was stated*, not *that it is
correct*. In the `maxTurns: 30` draft the Gate quotes `"Count of ?-marked ground truths: 17 of
22"` verbatim and bands the criterion **Sound**.

**Why this one is worth fixing before the others.** Every other Gate criterion is a judgement
call — whether an essence statement is specific enough, whether a chain has a genuine
intermediate. This one is arithmetic over a document the agent has already written, and it is
the criterion the provenance discipline leans on hardest: the count is the summary statistic a
reader uses to calibrate the whole analysis. A wrong count understates unverified inputs by up
to seven ground truths, in the direction that flatters the analysis.

**Fix, implemented in this release:** derive the count rather than assert it — the `?`-marked IDs
are enumerated, and the Gate checks the enumeration against the Ground Truths list rather than
quoting the stated number. An enumeration is checkable by inspection; a bare integer is not.

*Not a regression: the criterion was new in 8.16.0 and never reported a correct figure in the
one release it shipped in.*

## [8.16.0] - 2026-08-16

Source-provenance discipline for ground truths. Both changes come from the same observed
failure: a fabricated figure carried a well-formed citation to a real paper that did not
contain it, propagated into a HIGH-confidence derivation chain, and reached the conclusion.
A citation being *present* passed every check the agent had.

### Added

- **Source-provenance labels on every ground truth** (Phase 3, `shared/spine/SKILL-body.md`).
  One test decides the label: *did this analysis read the asserted figure or wording in the
  cited source?* Three values — `read-at-source` (no suffix), `reported-by-delegate` (`?`
  required), `unverified` (`?` required). Provenance is scored on what the analysis did, never
  on who supplied the claim: a well-formed citation from a capable sub-agent is
  `reported-by-delegate` until someone opens the source.
- **Delegate-reported ground-truth form** in `shared/spine/references/output-template.md` §3,
  alongside the existing verified and unverified forms, plus a required provenance summary.
- **Provenance check** prepended to Criterion 3 of the Self-Audit Gate, applied before banding.

### Changed

- **The `?` suffix is now the default rather than the exception.** It is dropped only when a
  read-at-source location can be named. A delegate report counts as read-at-source only when it
  quotes the source's own wording and that quote was checked.
- **Phase 3 exit criterion** now requires the count of `?`-marked ground truths to be stated
  *and* every unsuffixed ground truth feeding a HIGH-confidence chain to name where its figure
  was read. A bare count of zero no longer satisfies the criterion — the named read-locations
  are the auditable part.
- **Self-Audit Gate Criterion 3 band ladder retightened.** An unsuffixed, unread ground truth
  feeding a HIGH-confidence chain now bands at **Hand-wavy**; it previously banded at **Sound**,
  which is precisely the defect above passing at a tolerated level. The MEDIUM/LOW-confidence
  case stays at Sound, so the ladder still discriminates.

### Note

The binary `GT-N` / `GT-N?` notation is deliberately unchanged. Provenance layers on top of it
rather than introducing a third symbol, so D-07, the exact-tie tiebreak, the MEDIUM/LOW
confidence rule, and all four Criterion 3 bands keep working without re-verification.

## [8.15.0] - 2026-08-16

Findings from the first real-world audit of the shipped agent — a full-composer run against a
Medium article, reconstructed from the raw subagent transcript rather than from the written
output.

### Added

- **"Turn discipline" section** in the agent body, placed before Step 0. Prescriptive rather
  than prohibitive on purpose: the observed run reached for `Monitor` first and fell back to
  `sleep` loops anyway, so the text names the alternative — dispatched work notifies on
  completion, so stop and wait for the notification rather than polling.
- **Carry-forward rule for regenerated analyses.** The observed run emitted three complete
  full-length analyses and each rewrite silently lost artifacts: the Essence Statement was
  present in drafts 1 and 2 and absent from the deliverable, and `GT-N?` marks decayed 13 → 2 →
  0 while a fabricated figure's usage rose 0 → 6 → 8. A rewrite is now a revision — confirm
  every named artifact survives or is explicitly retired.
- **Honest-failure clause.** If the closure ledger or the gate could not run, say so at the top
  of the response, naming which. A stated omission is recoverable; a silent one is not.

### Changed

- **`maxTurns` raised 30 → 60.** The observed run used 32 assistant turns against a cap of 30,
  with roughly 9 spent on tool-schema fetches and seven consecutive busy-wait loops polling for
  dispatched sub-agents. The Fix/Repeat loop runs last and is therefore what gets dropped when
  the budget runs out — and it was.
- **The Validation Rubric is renamed the Self-Audit Gate.** The request asked for "a validation
  rubric scoring the article's argument"; the agent produced one and let it stand in for its own
  gate, which never ran. Two different instruments shared a name. The disambiguation lives in
  `SKILL-body.md`, not only in the reference file, because the whole failure was that the linked
  file never got opened: the gate scores *this analysis's* structure, a subject-matter rubric is
  a separate deliverable, and both must appear.
- `docs/CONFIGURATION.md` and `docs/FIVE-PHASE-FLOW.md` updated in the same commit so no tracked
  prose asserts the old value or the old name. `docs/CONFIGURATION.md` also carried a
  pre-existing stale `metadata.version` of `"8.0.0"`.

### Note

The file path `references/validation-rubric.md` is deliberately unchanged despite the rename —
`check-quality-harness.py` copies it *by name* into the QUAL-01 frozen packet and asserts on the
entry list, `check-traceability.py` pins it as a `deliverable_path`, and `sync-content.py` keys
its INLINE list on the slug. The frozen quality baseline records the rubric by path only, so
retitling does not affect pre/post comparability.

## Earlier releases (1.0 – 8.14)

This changelog was not maintained between 3.8.0 and 8.15.0. The entries below are
**reconstructed from the annotated git tags** and carry only each release's headline — no
Added/Changed/Fixed decomposition, because that detail was never recorded here and inventing it
would misrepresent the record. **For any release below, the annotated tag body is the
authoritative account** (`git show <tag>`). Releases **3.0.0 through 3.8.0 are omitted from this
table** — they already carry full hand-written entries further down.

Note also that the repository history was rewritten on 2026-07-28 (removal of `docs/history/`
and 237 raw test captures), so commit SHAs referenced in material predating that date are stale;
tag names remain valid.

| Tag | Date | Headline |
|---|---|---|
| `v8.14-greenmean` | 2026-07-29 | v8.14 GREENMEAN-01 — the milestone that stopped itself |
| `v8.14` | 2026-07-29 | Builder Retirement & Traceability Reconciliation |
| `v8.13` | 2026-07-28 | DETECTFIX-01 — Correct the Inverted D-18 Defect Checks |
| `v8.12` | 2026-07-26 | REALREAD-01 — First Read of Real Work Output |
| `v8.11` | 2026-07-24 | DEFROBUST-01 — D-03 Definition-Robustness Test |
| `v8.10` | 2026-07-24 | CORRECTGATE-01 — A Correctness Instrument for the DIVERGE Class |
| `v8.9` | 2026-07-24 | DIAGNOSE-01 — Diagnose the Failed §6→§4 Contract Fix |
| `v8.8` | 2026-07-23 | Technical-Debt Clean-Up & Framing Correction |
| `v8.7` | 2026-07-23 | Analysis Correctness, Constraint Teardown & Output-Contract Integrity |
| `v8.6` | 2026-07-21 | Agent-Body Procedure Compression |
| `v8.5` | 2026-07-20 | Context Optimization: Execute the Reference-File Split |
| `v8.4` | 2026-07-19 | Implementation-Readiness Evaluation |
| `v8.3` | 2026-07-18 | Technique & Context-Length Optimization Evaluation |
| `v8.2` | 2026-07-18 | Deep Investigation of the 19 Not-Approved Grok Items |
| `v8.1` | 2026-07-16 | Grok Recommendations Review & Selective Implementation |
| `v8.0` | 2026-07-06 | Final Release (project wrapped) |
| `v7.13` | 2026-07-02 | Live Re-Measure — RR-130-01 Fix + Step 0 Residuals |
| `v7.12` | 2026-06-30 | Diagnose & Fix RR-130-01 (Main-Routing Inline-Answering Regression) |
| `v7.11` | 2026-06-30 | Live Re-Measure of the Whole System |
| `v7.10` | 2026-06-28 | Evaluate Gaps & Technical Debt Misaligning Agent Goals |
| `v7.9` | 2026-06-27 | Close the 5-Fix Over-Routing Fishbone (Fix #3 / Fix #4 / Fix #5) |
| `v7.8` | 2026-06-25 | Step 0 Over-Routing Precision — Negative-Match Guard & Stay-in-Composer Default |
| `v7.7` | 2026-06-24 | Fix the S-P01/S-P03 Step 0 Under-Routing Regressions |
| `v7.6` | 2026-06-23 | Validate the Merge — Live 8-Technique Step 0 Re-Baseline |
| `v7.5` | 2026-06-21 | Execute the decompose→five-whys Merge |
| `v7.4` | 2026-06-20 | Measure the Expansion — Live 9-Technique Step 0 Re-Baseline |
| `v7.3` | 2026-06-20 | Introduce Tier-1 Rigor — the theoretical-limit Skill |
| `v7.2` | 2026-06-19 | Introduce Tier-1 Rigor — the estimate Skill |
| `v7.1` | 2026-06-19 | Introduce Tier-1 Rigor — the decompose Skill |
| `v7.0` | 2026-06-18 | Documentation Refresh & System-Connection Docs |
| `v6.4` | 2026-06-17 | Resolve v6.3 Carry-Forward Residuals (RR-92-01 / RR-92-02) |
| `v6.3` | 2026-06-16 | GEN-01 Step 0 Classifier Rearchitecture |
| `v6.2` | 2026-06-15 | Close the Last Two Documented Gaps |
| `v6.1` | 2026-06-15 | Close Actionable Traceability Gaps |
| `v6.0` | 2026-06-14 | Requirements & Traceability Alignment |
| `v5.3` | 2026-06-14 | Live S-P Routing — Close Remaining Detector Residuals |
| `v5.2` | 2026-06-13 | Live S-P Routing Fix |
| `v5.1` | 2026-06-12 | Step 0 Live Detector Closure |
| `v5.0` | 2026-06-12 | Step 0 Measurement Harness |
| `v4.3` | 2026-06-11 | Unified Routing/Output Battery |
| `v4.2` | 2026-06-10 | Sub-Skill Battery Fixture Correction |
| `v4.1` | 2026-06-06 | Builder Auto-Install Flag |
| `v4.0` | 2026-06-04 | Programmatic Skill/Agent Builder |
| `v3.13` | 2026-06-03 | Routing Catalog v3.2 Content Coverage |
| `v3.12` | 2026-05-30 | Phase-Level Slash Commands |
| `v3.11` | 2026-05-29 | P8 Routing Forward Monitoring |
| `v3.10` | 2026-05-29 | Phase 46 Convention Closure |
| `v3.9` | 2026-05-29 | P8 Routing Fix + Phase 45 Convention Restoration |
| `v2.0` | 2026-05-22 | Collection-of-Skills Plugin |
| `v2.0.0` | 2026-05-21 | Collection-of-Skills Plugin (dual-publish) |
| `v1.2` | 2026-05-20 | Forward Consequence-Tracing Tools (Inversion + Second-Order Thinking) |
| `v1.1` | 2026-05-19 | Ishikawa (Fishbone) Diagram Tool |
| `v1.0` | 2026-05-18 | Enhanced Skill |

---

The 3.0.0 – 3.8.0 entries below are the original hand-written records, kept verbatim.

## [3.8.0] - 2026-05-28

### Added

- `scripts/check-focused-output.py` — verifies that agent analysis outputs stay focused on first-principles methodology (not off-topic delegation); includes `--self-test` fixture battery and a LOAD-BEARING Probe 3 sanity feed.
- `scripts/check-sub-skill-routing.py` — verifies that companion-tool invocations (`/first-principles:fishbone` etc.) are correctly routed to the named sub-skill rather than delegated to the main agent.
- Sub-skill routing catalog at `tests/sub-skill-routing-catalog.md` (P12, P24, N1, N2 prompts).
- Sub-skill routing baseline at `tests/sub-skill-routing-baseline-v3.8.md`.
- Focused-output baseline at `tests/focused-output-baseline-v3.8.md`.
- Six namespaced companion-tool skills under `first-principles/skills/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}/` — standalone slash-only skills (`/first-principles:<name>`) for direct invocation of individual techniques without triggering the full agent. Each has `disable-model-invocation: true`.
- `generate_skill_stub` in `scripts/sync-content.py` with six corresponding `shared/skills/` sources; skill stubs are now generated alongside the agent surface.
- `GENERATED` marker prepended to every byte-identical emission in the generated agent tree so code reviewers can skip the `shared/`↔`first-principles/` mirror.
- `.reviewignore` at repo root declaring the generated mirror as review-skippable.

### Fixed

- Signal A routing-envelope override now takes priority over composer-structure cardinality classifier, fixing false sub-skill delegation on routing prompts that carry both signals.
- `_extract_assistant_text` tightened to top-level assistant entries only, preventing nested tool-result text from inflating detection scores.
- Sibling-shared boilerplate in six technique-skill descriptions reworded to eliminate ~60 false-positive 4-gram collisions that blocked `check-trigger-collisions.py` on CI push.
- `sync-content.py` docstrings on three verbatim-copy generators corrected — they previously claimed "NO marker expansion, NO edits" after the GENERATED marker prepend was added.
- Agent marker's primary canonical source now named as a navigable path (`shared/spine/SKILL-body.md`) instead of freeform prose.

## [3.7.0] - 2026-05-27

### Added

- Mandatory Assumption Audit protocol in the validation rubric (`shared/spine/references/validation-rubric.md`): exhaustive enumeration of assumptions by scanning each derivation-chain step, replacing the prior opportunistic-listing approach.
- `[Assumes: X]` annotations on derivation-chain steps in `science-engineering-2.md` worked example.
- Assumption Audit section in `software-systems.md` worked example.
- Routing baseline v3.7 at `tests/routing-baseline-v3.7.md` — BATTERY PASS: P 10/10, N 17/17.

### Changed

- Validation rubric Criteria 1, 2, and 4 Rigorous descriptors rewritten with structural/observable tests instead of subjective phrases ("withstand inspection by a skeptic").
- Validation rubric Criteria 5 and 6 Rigorous descriptors: modal verbs removed; compliance is now detectable from output structure alone.

## [3.6.0] - 2026-05-26

### Added

- Two new routing catalog prompts: P9 (chemistry/first-principles of reaction kinetics) and P10 (earth science/continental drift).
- Two new N-case catalog rows: N16 and N17 (science-lookup questions that should NOT delegate).
- Routing mini-catalog v3.6 fixture at `tests/routing-mini-catalog-v3.6.md` (P9, P10, N16, N17).
- Routing baseline v3.6 at `tests/routing-baseline-v3.6.md` — BATTERY PASS: P 8/10, N 17/17.

### Changed

- Battery thresholds rescaled to P ≥ 8/10 and N ≥ 15/17 to match the expanded 10P/17N catalog.

## [3.5.0] - 2026-05-25

### Added

- P3+P7 mini-battery catalog fixture at `tests/routing-mini-catalog-p3p7.md` for fast-iteration confirmation before running the full battery.
- P7-targeted paraphrases added to agent description: question-form (`"Is our reasoning sound..."`), back-reference (`"evaluate whether a claim..."`), and evaluate-whether variants.
- Routing baseline v3.5 at `tests/routing-baseline-v3.5.md` — BATTERY PASS: P 6/8, N 15/15.

### Fixed

- P3 routing fragility: prompt mid-sentence rewritten to eliminate structural embedding that suppressed delegation.
- P7 routing fragility: vocabulary gap closed — agent description now covers the "evaluate whether" and question-form trigger shapes that P7 exercises.

## [3.4.0] - 2026-05-25

### Added

- `--repeat` and `--min-pass` flags on `check-routing.py` enabling K-of-N aggregation: run each prompt N times, require K passes — reduces false FAIL/PASS verdicts from single-run non-determinism.
- K>N guard and K-of-N self-test fixtures in the battery runner.
- Rerun-to-stability methodology documented in `docs/testing-agents-headlessly.md` (Section 10).
- Routing baseline v3.4 at `tests/routing-baseline-v3.4.md` — canonical best-of-3: P 6/8, N 15/15.

## [3.3.0] - 2026-05-25

### Added

- `scripts/check-body-budget.py` — checks generated agent body against the ~500-line target; includes `--self-test`.
- `scripts/git-hooks/pre-commit` — combined body-budget + sync-drift gate; blocks commits that would push the agent body over budget or leave `shared/` and the generated agent tree out of sync.
- `scripts/install-hooks.sh` — idempotent installer that symlinks the above hook into `.git/hooks/pre-commit` (preserves any existing hook as `.bak` on first run).
- `scripts/smoke-test-hook.sh` — end-to-end smoke test for the pre-commit hook.
- `.githooks/pre-commit` extended with body-budget gate (for contributors using the `core.hooksPath` opt-in path).
- Contributor setup documentation in README.md for both hook opt-in paths.

## [3.2.0] - 2026-05-24

### Added

- `shared/spine/references/assumption-taxonomy.md` — canonical classification guide for the five assumption types used in Phase 2 (physical law, engineering constraint, current constraint, convention, untested belief); emitted to `first-principles/agents/references/assumption-taxonomy.md`.
- Phase 2 cross-reference from assumption-taxonomy to the agent body.
- Self-application worked example (`shared/examples/self-application.md`) — first-principles analysis applied to a live design decision about the agent itself (body length vs. scope).
- Four second-pass worked examples covering distinct reasoning shapes not present in the original six:
  - `software-systems-2.md` — Build vs. Buy (authentication service); capability-cost-risk trade-off shape.
  - `product-business-2.md` — Feature prioritization under a binding engineering-capacity constraint.
  - `personal-general-2.md` — Mortgage paydown vs. index investment; quantitative expected-value chain.
  - `science-engineering-2.md` — In-service mechanical component failure analysis; diagnostic/backward-reasoning shape.
- Worked Examples navigation subsection added to the agent spine.
- All five new examples synced to the generated agent surface.

### Changed

- Spine appendices (assumption taxonomy, output template, validation rubric) extracted out of the inlined agent body into on-demand reference files, reducing recurring token cost per invocation.

## [3.1.0] - 2026-05-23

### Added

- `scripts/check-routing.py` — headless routing battery: issues each catalog prompt through `claude -p --output-format stream-json`, scores DELEGATE / NO-DELEGATE from the event stream, and exits non-zero if P-case or N-case thresholds are not met.
- `tests/routing-catalog.md` — initial routing test catalog: 8 P-cases (should delegate) and 15 N-cases (should NOT delegate), with per-prompt annotations and pass thresholds.
- `docs/testing-agents-headlessly.md` — documents the stream-json methodology, two-signal detection rule, jq extraction strategies, and `--permission-mode bypassPermissions` requirement for reproducible headless agent testing.
- Routing baseline v3.1 recorded in `tests/routing-catalog.md`.

### Fixed

- Agent description scope-line tightened to explicitly exclude performance optimization, debugging, and general Q&A — closes a class of false-positive delegations where the agent was invoked for routine coding tasks.

## [3.0.0] - 2026-05-23

### Removed

- Standalone monolith skill at `first-principles-thinking/`. Users who copied this to `~/.claude/skills/` should remove that local copy manually:
  `rm -rf ~/.claude/skills/first-principles-thinking`
- 7 namespaced plugin skills at `first-principles/skills/{thinking,five-whys,pre-mortem,trade-off,fishbone,inversion,second-order}/`. The Phase 26 forwarding language ("still installable") is superseded — these surfaces no longer exist.

### Added

- First-principles agent surface at `first-principles/agents/first-principles.md` (initially shipped Phase 23 in the v3.0-alpha series; now the sole installable interface).
- 6 on-demand companion-tool reference siblings under `first-principles/agents/references/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}.md`.
- 6 worked-example siblings under `first-principles/agents/references/examples/` (migrated from the deleted monolith examples directory).

### Upgrade path

- Install: `claude --plugin-dir ./first-principles` for dev, or via the marketplace (`/plugin marketplace add chrisdavidson/first-principles-skill` then `/plugin install first-principles@first-principles-skill`).
- Invoke: `@agent-first-principles:first-principles` (auto-routing) or `/first-principles:first-principles` (explicit).
- If you previously copied `first-principles-thinking/` into `~/.claude/skills/`, delete that local copy manually — Claude Code does not auto-remove it.

### Reference

- Per-technique deep procedures now ship as agent-loaded reference files (`first-principles/agents/references/`).
- The 5-phase methodology text formerly carried by the monolith body is inlined in the agent body itself.
