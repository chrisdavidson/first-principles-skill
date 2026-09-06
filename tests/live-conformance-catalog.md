# Live Conformance Prompt Catalog — v9.0

## Purpose

This catalog is the prompt source for Phase 20's live `--probe` dispatches AND the run
inventory `scripts/report-conformance.py`'s roster floor reads by EQUALITY against the set of
discovered `.jsonl` capture stems under `tests/live-conformance-v9.0/`. Every row dispatched
here is one live run of the shipped `first-principles:first-principles` agent, scored by the
unmodified, CONTRACT-06-frozen `detect_defects`.

This file carries both the run inventory and, in the section below, the phase's written
decision record for the two Claude's-Discretion questions `20-CONTEXT.md` left open (D-20-A,
D-20-B, D-20-C). Both decisions precede any capture and any surface code — nothing downstream
of this file may re-litigate them mid-execution.

**Parser note:** `scripts/check-quality-harness.py::_read_quality_catalog` treats every line in
this file that starts with `|` as a table row and raises `ValueError` the instant one does not
belong to the `| ID | Prompt | Notes |` table below. For that reason the decision record states
its outcome classification and other structured facts as prose and bulleted lists rather than as
markdown pipe tables — no line before the `## Catalog` table's own header may start with `|`.

## Decision record

### D-20-A — What counts as a form defect, and what counts in the denominator

**"Zero form defects" is CONF-GATE's exact four counts**, and nothing wider:

1. `unreadable` — the row's `section_resolution` is not the literal `"OK"`
2. `heading_malformed_blocks` — counted unconditionally, even on an unreadable row
3. `nonconforming_verdict_cells` — counted only when the row resolved
4. `silent_untraced_claims` — counted only when the row resolved

**Reasoning (recorded, not implied):** these four are the project's already-published
conformance vocabulary. `docs/conformance-baseline.md` publishes the control group's zeros
against exactly these four counts on `shared-examples` and `generated-twin`, and
`scripts/check-conf-gate.py`'s `_CONF_TARGETS` pins the same four. Choosing all 13 pure-form
columns, or `_CORPUS_FORM_FIELDS`'s three, would produce a live rate that cannot be read against
the control group without a translation table. Consistency with the published control group is
worth more here than breadth, because CONF-10's whole value is comparability.

**Denominator: runs attempted = every row in this catalog = 8.** A run is attempted the moment
it is dispatched. Outcome is resolved mechanically by
`scripts/check-quality-harness.py::classify_invocation_outcome` over the run's own `.jsonl`,
never by a bare grep, and lands in one of four states (outcome → analysis `.md` written? →
counted in denominator? → counted in numerator?):

- `completed`, readable, all four counts zero → `.md` written: yes; denominator: yes; numerator:
  **yes — this is the numerator**.
- `completed`, readable, any of the four non-zero → `.md` written: yes; denominator: yes;
  numerator: no.
- `completed`, `SectionResolutionError` (unreadable) → `.md` written: yes; denominator: yes;
  numerator: no.
- `rate_limit_stub` / `transport_error_stub` / `no_terminal_result` → `.md` written: **no**;
  denominator: yes; numerator: no.

A stub counts in the denominator because CONF-10's literal text is "runs with zero form defects
over runs **attempted**". Counting it any other way would let a transport failure quietly vanish
from a rate this phase exists to publish honestly. Because a stub is a transport fact and not an
agent-output fact, the published section ALSO states a secondary rate conditional on
`outcome == "completed"`, and the run breakdown by outcome, so a reader can compute either
figure. Neither is hidden behind the other.

**Coupling to D-07's equality floor, resolved:** a stub produces a `.jsonl` with **no** `.md`
sibling (`_extract_and_persist_analysis` returns `None` for any non-`completed` outcome). The
roster floor therefore compares catalog ids against the discovered **`.jsonl` capture stems**,
never `.md` stems — every attempted run always writes a capture, so a stub can never make that
floor fail forever. The `.md`-present/absent state is carried as its own row field
(`analysis_present`) and its own outcome column, never conflated with roster membership.

**Re-dispatch policy:** one dispatch per catalog row is the default. A row that returns a
transport-layer stub MAY be re-dispatched once, because a rate limit measures the transport, not
the agent. Evidence is never deleted: the superseded capture is moved to
`tests/live-conformance-v9.0/superseded/` (outside the non-recursive surface glob) and logged in
the fixture README's attempt table by sha256 and outcome. A row still stubbing after one
re-dispatch keeps its stub capture as the run of record, scores `no-analysis`, and carries a
`disposition` cell like any other non-clean run.

### D-20-B — Which body the runs measure, and what happens to defects found

**The runs measure HEAD**, not the `v8.26.0` tag.

**Reasoning:** `git diff --name-only v8.26.0..HEAD -- shared/ first-principles/` returns exactly
two path families, `shared/examples/*` and `first-principles/agents/references/examples/*` — the
28 worked-example files Phase 18 rewrote. The agent body, the output template and the validation
rubric are byte-unchanged since the tag. Those 28 files are agent reference siblings the agent
reads, so HEAD is strictly the more informative measurement: it is the only reading that can show
whether Phase 18's exemplar conformance propagates into live output. Checking out a stale tag
would dispatch prompts against a body no user has run since Phase 18 and produce a reading with
no forward value.

**This is a written reinterpretation of CONF-09's "the shipped v8.26.0 body"**, recorded in the
same voice and for the same reason as D-08's reinterpretation of CONF-09's other clause. The
exact 40-character body sha is recorded per-run in the fixture README (plan 20-03), so the
reading names its own subject rather than inheriting a stale label.

**Fix discipline (ROADMAP success criterion 3): file only, fix nothing in this phase.** Agent
output cannot be edited; the only lever would be the prescription under `shared/`, and using it
would require a second live round the rework cap of 2 cannot fund. Every non-clean run therefore
carries a `disposition` beginning with `fix` / `accept-with-reason` / `defer-with-owner`; a `fix`
disposition names the artifact or prescription file and is filed as a backlog item, executed in a
later phase. **A defect is filed against the artifact or the prescription and is never closed by
widening a detector.** The three CONTRACT-06 sha256 pins (`_chain_block_well_formed`,
`_conclusion_claims`, `_slice_sections`) stay byte-unchanged through this entire phase.

### D-20-C — Freezing (resolved here so task order downstream is unambiguous)

Both `tests/live-conformance-v9.0/` and `tests/live-conformance-catalog.md` are registered in
`_FROZEN_PATHS` — but **only in plan 20-06, in a commit strictly after the captures and the
catalog are already committed**. Registering earlier turns FROZEN-EVIDENCE red on its own
untracked-file sweep leg and, for the fixture directory, makes `is_frozen_destination` refuse
`--probe`'s `.md` write. The array moves 20 → 22 entries; the battery TOTAL stays at **25**,
because FROZEN-EVIDENCE's single `TOTAL=$((TOTAL + 1))` sits once before its if/elif/else
regardless of array length.

## Run command

```bash
mkdir -p /tmp/live-conformance-probe
python3 scripts/check-quality-harness.py --probe <ID> \
    --catalog tests/live-conformance-catalog.md \
    --out /tmp/live-conformance-probe
```

`--plugin-dir` does not need to be passed: `DEFAULT_PLUGIN_DIR` already resolves to
`REPO_ROOT / "first-principles"`, the working tree, not the installed plugin cache. `--catalog`
MUST be passed explicitly, because `DEFAULT_CATALOG` points at `tests/quality-catalog-v8.7.md`,
not this file. Captures land in a scratch `--out` first and are moved into
`tests/live-conformance-v9.0/` afterward, because `is_frozen_destination` refuses a write once a
path is registered in `_FROZEN_PATHS` — which this path is not, yet, per D-20-C.

## Provenance

All seven distinct prompts below are copied verbatim from their source catalogs, with no
rewording: `Q-P1`, `Q-P2` and `Q-P3` from `tests/quality-catalog-v8.7.md`'s `Prompt` column, and
`PR-P1`, `PR-P2`, `PR-N1` and `PR-N2` from the `Prompt` column of
`tests/premise-rejection-catalog.md` (a six-column catalog; only the `Prompt` cell is taken).
`PR-P1-R2` repeats `PR-P1`'s prompt text byte-for-byte under a distinct id, because `--probe`
names its output `<row.id>.jsonl` and two rows sharing an id would clobber each other.

Each row's `Notes` cell states an origin sentence naming its source file and source row id
verbatim, followed by the literal marker `disposition: ` and a placeholder. `scripts/report-conformance.py`
(plan 20-04) parses the substring after the first occurrence of the literal `disposition: ` as
that row's disposition cell; plan 20-03 replaces each `MISSING` placeholder with the row's actual
disposition — `fix` / `accept-with-reason` / `defer-with-owner` / `clean` — once that run's
reading is known.

## Catalog

| ID | Prompt | Notes |
|---|---|---|
| Q-P1 | Our platform team runs 22 internal microservices that talk to each other over REST/JSON, handling 340,000 requests per minute at peak with a median inter-service latency of 48ms. Our infrastructure lead wants to migrate the six highest-traffic services to gRPC over the next two quarters, citing a competitor's public benchmark claiming 30 percent lower p99 latency. The migration needs 5 engineers for about 10 weeks, our on-call rotation currently has only 3 people covering it, and every team that consumes those services would have to regenerate client stubs and redeploy. Should we commit the team to this migration now, or hold off another year? | Prompt copied verbatim from `tests/quality-catalog-v8.7.md` row Q-P1. disposition: MISSING |
| Q-P2 | Our subscription product has 48,000 active members paying $19 a month, and monthly churn has climbed from 4.2 percent to 6.8 percent over the last two quarters. Customer success wants to launch a loyalty program that lets members redeem points for account credit, costing around $310,000 a year to run, betting it will pull churn back toward 5 percent. A rival service just launched a similar program last month. Marketing wants a final call within three weeks before the next board update. Should we fund the loyalty program at that price point? | Prompt copied verbatim from `tests/quality-catalog-v8.7.md` row Q-P2. disposition: MISSING |
| Q-P3 | Our 1948 house is losing around 35 percent of its heating energy through some combination of the attic and the windows. One contractor quoted $4,200 to blow in R-49 attic insulation, replacing the current R-13. A second quote came in at $18,500 for full triple-pane window replacement across all 14 windows. Our winter heating bill currently averages $410 a month over the four coldest months, and we plan to stay in this house for at least another 10 years. Should we do the insulation, the windows, both, or neither this year? | Prompt copied verbatim from `tests/quality-catalog-v8.7.md` row Q-P3. disposition: MISSING |
| PR-P1 | Reason from ground truth about how to cut our AWS bill. Everyone knows serverless is cheaper than containers, so I want to figure out the fastest path to migrating our services to Lambda | Prompt copied verbatim from the Prompt column of `tests/premise-rejection-catalog.md` row PR-P1. disposition: MISSING |
| PR-P2 | Reason from ground truth about our database costs. Everyone knows normalized schemas are slower than denormalized ones. What should we do about our reporting queries? | Prompt copied verbatim from the Prompt column of `tests/premise-rejection-catalog.md` row PR-P2. disposition: MISSING |
| PR-N1 | Reason from ground truth about our TLS setup. Certificates expire and an expired certificate breaks client connections, so I want the fastest path to automated renewal. | Prompt copied verbatim from the Prompt column of `tests/premise-rejection-catalog.md` row PR-N1. disposition: MISSING |
| PR-N2 | Reason from ground truth about our image pipeline. We process about 40,000 uploads a day and storage costs are climbing. What are the options? | Prompt copied verbatim from the Prompt column of `tests/premise-rejection-catalog.md` row PR-N2. disposition: MISSING |
| PR-P1-R2 | Reason from ground truth about how to cut our AWS bill. Everyone knows serverless is cheaper than containers, so I want to figure out the fastest path to migrating our services to Lambda | Same prompt text as row PR-P1 above, byte-for-byte, per D-02's within-body variance / cross-body longitudinal second run of the one prompt with a committed prior capture (`tests/quality-provenance-v8.24/PR-P1.md`, produced on the v8.24.0 body). disposition: MISSING |
