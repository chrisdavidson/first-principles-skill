# tests/summary-block-v9.16 — provenance

Four real analysis reports, copied byte-for-byte from their sources and adapted **only** to
Phase 74's two fixed Self-Audit Gate prose forms (the `**Pass N (before re-score):**` line and
the `**Gate result:**` line), each then carrying one `## Structured summary (process output)`
block transcribed from that copy's own prose. The checker (`scripts/check-summary-block.py`)
reads only these in-tree copies at test time — no fixture, self-test control, or CLI path opens
`~/Projects/agent-router` or any other path outside this repository (falsifier f6).

Every source was re-hashed against the plan-time sha256 before copying; all four matched, so no
mismatch-stop applied.

## Sources

| Fixture | Source (read-only, outside this repo) | sha256 |
|---|---|---|
| `personal-general.md` | `~/Projects/agent-router/integrations/first-principles/runs/2026-09-29-examples-latest/personal-general/.first-principles/analysis-20260930T033051Z.md` | `f3b1e9b2a52b4ddca2ea6d150574ecf485c2d2508b69a48f2d543f3de87edc1b` |
| `software-systems.md` | `~/Projects/agent-router/integrations/first-principles/runs/2026-09-29-examples-latest/software-systems/.first-principles/analysis-20260930T035620Z.md` | `35c8000f184064ba4175db9488bc2974e9835253ec1fe6a552c953283b6fa8e3` |
| `science-engineering.md` | `~/Projects/agent-router/integrations/first-principles/runs/2026-09-29-examples-latest/science-engineering/.first-principles/analysis-20260930T034552Z.md` | `4c3dcf819d59d34516e3479ebfba968941b964385b036816c8e3d4e96cae8d61` |
| `tb-01.md` | `tests/answer-first/documents/TB-01.md` (in-tree; also a byte-identical copy of `tests/answer-first/raw/TB-01.a1.files/analysis-20260930T023704Z.md`) | `4b535fbdb3a625656a97f785cf1cc06ad945ecceda65b0567a68bc82adc68d03` |

Re-hash command used immediately before each copy: `sha256sum <source>`. All four outputs matched
the sha256 values above (and the plan's pinned values) exactly.

## Role in CHECK-03's must-fail controls (see `75-04-PLAN.md`)

| Fixture | Role |
|---|---|
| `personal-general.md` | Source for M1–M5, M9 (missing-block/two-blocks/malformed-JSON/chain-confidence/re-entry-fired mutations built from this fixture); positive control P1. No Self-Audit Gate edge fired in the original run (`re_entry.fired: false`); keeps its §4 decoy sentence "There was therefore no Phase 2 re-entry." verbatim — a plain-prose re-entry-shaped sentence that is NOT a re-entry disclosure, guarding against a reader that free-text-searches for "re-entry" instead of reading the Gate span/disclosure region. |
| `software-systems.md` | Source for M6, M7 (re-entry-not-fired / single-pass-before-fix mutations); positive control P2. The Self-Audit Gate's Fix/Repeat edge fired once in the original run (`re_entry.fired: true`, two scoring passes); keeps its top `**Disclosed:**` paragraph verbatim and gains the Phase-74 fixed `**Pass 1 (before re-score):**` line carrying the first pass's two Hand-wavy bands (Criteria 3 and 4). |
| `science-engineering.md` | Source for M8 (conclusion-cut-at-a-colon mutation); positive control P3. §6's `**Recommended approach:**` text introduces a three-item list, kept verbatim so the block's `conclusion.recommendation` must carry the whole list, not just the text up to the first colon. |
| `tb-01.md` | Positive control P4. Exactly one Hand-wavy final band (Criterion 3) — the rubric's Hand-wavy-cap boundary (1 allowed) — as a real positive, distinct from the two-Hand-wavy-cleared must-fail shape (M9) built synthetically. |

## Adaptations (before / after, with reason)

Every adaptation below is the **only** text changed relative to the byte-for-byte copy; everything
else, including all arithmetic, every chain, every table row, and every Self-Audit Gate criterion
justification, is untouched. `diff <(sed -n '1,487p' <source>) <(sed -n '1,487p' personal-general.md)`
confirms nothing above personal-general's result line was touched (verify command in `75-03-PLAN.md`
Task 1's acceptance criteria; ran clean, exit 0).

### `personal-general.md`

1. **Gate result line (was line 488, free-form, unbolded lead-in `Gate result: `).**
   - Before: `Gate result: no criterion Absent; zero criteria Hand-wavy. The gate is cleared on the first scoring pass. The Fix/Repeat loop did not fire, and no re-entry edge fired during the run.`
   - After: the same sentence with its `Gate result: ` lead-in removed (so the real wording is kept
     verbatim, capitalised to start the paragraph), followed by a blank line and the Phase 74 fixed
     line: `**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no`
   - Reason: Phase 75's fixed-form requirement (74-prose-inserts.md B6); the checker's
     `_xc_gate_result`/`_xc_gate_passes` readers parse this exact line shape.
   - Untouched: line 166's decoy sentence `There was therefore no Phase 2 re-entry.` (M5 depends on
     it staying exactly as written — plain prose, not a Self-Audit Gate disclosure).

### `software-systems.md`

1. **First-pass paragraph (was line 451, free-form `**First scoring pass (before Fix):**` lead-in).**
   - Before: `**First scoring pass (before Fix):** Criterion 1 Rigorous; Criterion 2 Sound (the fix-cost bracket in C5 step 3 had no Assumptions Table row of its own); Criterion 3 **Hand-wavy** (GT-9 and GT-10 were unsuffixed, their sources reachable and read, yet each fed only MEDIUM chains); Criterion 4 **Hand-wavy** (C6's weighted-totals hop, which the endpoint depends on, rested on A-12 and A-16 without an `[Assumes:]` mark; C6 steps 1 and 9 were also unmarked); Criterion 5 Rigorous; Criterion 6 Rigorous. Two Hand-wavy bands broke the hand-wavy cap, so the **Fix/Repeat edge fired** once.`
   - After: the Phase 74 fixed line `**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2
     Sound · Criterion 3 Hand-wavy · Criterion 4 Hand-wavy · Criterion 5 Rigorous · Criterion 6
     Rigorous · Gate cleared: yes · Hand-wavy cap cleared: no`, followed by a plain paragraph (no
     line starting `**Pass` or `**Criterion`) carrying the original parenthetical reasons and
     closing sentence verbatim: "Criterion 2's reason: the fix-cost bracket in C5 step 3 had no
     Assumptions Table row of its own. Criterion 3's reason: GT-9 and GT-10 were unsuffixed, their
     sources reachable and read, yet each fed only MEDIUM chains. Criterion 4's reason: C6's
     weighted-totals hop, which the endpoint depends on, rested on A-12 and A-16 without an
     `[Assumes:]` mark; C6 steps 1 and 9 were also unmarked. Two Hand-wavy bands broke the hand-wavy
     cap, so the **Fix/Repeat edge fired** once."
   - Reason: same fixed-form requirement; the checker's Pass-line parser (`_parse_pass_line`) reads
     an 8-piece `·`-split line in this exact shape.
2. **Gate result line (was line 485).**
   - Before: `**Gate result:** no criterion Absent, no criterion Hand-wavy — gate cleared after one Fix/Repeat pass.`
   - After: the same sentence with its `**Gate result:**` lead-in removed, followed by a blank line
     and the fixed line `**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes`.
   - Reason: same fixed-form requirement.
   - Untouched: line 1's `**Disclosed:**` paragraph (M6 depends on it staying exactly as written —
     it is the only place the sentence naming the trigger for the Fix/Repeat edge appears verbatim
     outside the Gate section itself, and `re_entry.edges[0].trigger` is transcribed from it).

No other line in either file was changed. Markdown table cells, chain arithmetic, confidence
lines, dead-end entries and every other process-output section are byte-identical to the source.

### `science-engineering.md`

1. **Gate result line (was line 357, free-form, unbolded lead-in `Gate result: `).**
   - Before: `Gate result: no Absent, 0 Hand-wavy — cleared on first scoring pass; Fix/Repeat not fired. Unresolved caveat carried: the C3/C4 Rivals-axis calibration noted under Criterion 5.`
   - After: the same sentence with its `Gate result: ` lead-in removed (capitalised to start the
     paragraph), followed by a blank line and the fixed line: `**Gate result:** cleared · passes: 1
     · Fix/Repeat fired: no`
   - Reason: same fixed-form requirement as the other three fixtures.
   - Untouched: §6's `**Recommended approach:**` text and its three-item list (M8 depends on the
     whole list surviving into `conclusion.recommendation`, not just the text up to the first
     colon).

### `tb-01.md`

1. **Gate result line (was line 373).**
   - Before: `**Gate result:** No criterion scored Absent (condition 1 cleared). Exactly one criterion (Criterion 3) scored Hand-wavy, which is within the "at most one Hand-wavy" cap (condition 2 cleared). The gate passes on this first scoring pass; no Fix/Repeat re-perception pass was required or performed.`
   - After: the same sentence with its `**Gate result:**` lead-in removed, followed by a blank line
     and the fixed line `**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no`.
   - Reason: same fixed-form requirement.
2. **D-16 single-value Type-cell corrections (§2, four rows; plan-directed, not a general taxonomy
   policy change).** Each annotated cell is corrected to the one enum type it already begins with,
   dropping the trailing parenthetical subtype — the subtype text itself is not deleted from the
   analysis (it stays inside the row's own prose elsewhere in the cell/verdict text), only the Type
   column's cell value changes:
   - A-3: `convention (industry narrative)` → `convention`
   - A-11: `convention (analogy to others)` → `convention`
   - A-12: `untested belief (premature optimization)` → `untested belief`
   - A-20: `physical law (protocol specification, invariant)` → `physical law`
   - Reason: the schema's `assumptions[].type` enum holds exactly the four taxonomy values; a live
     report's Type field is never null, so an annotated cell must resolve to one of the four before
     it can be transcribed (`SB-ASSUMPTION`'s enum check; plan-directed correction, `75-03-PLAN.md`
     Task 2).
3. **Techniques-not-applied block (§ heading `## Techniques not applied`, four lines) rewritten to
   the agent body's fixed form `- <technique> (Phase N) — not applicable — <reason>`.** Each
   reason kept verbatim; only the technique-name/phase prefix changed shape:
   - Before: `inversion — not applicable at Phase 5 (adversarial technique step) — the conclusion is a plan/recommendation, so pre-mortem applies there per the decision rule; inversion's Phase 2 invocation fired instead, against the "GraphQL is required" claim (Assumptions Table A-3, A-11, and the failure-guaranteeing preconditions that produced A-4, A-7, A-16).`
     After: `- inversion (Phase 5) — not applicable — the conclusion is a plan/recommendation, so pre-mortem applies there per the decision rule; inversion's Phase 2 invocation fired instead, against the "GraphQL is required" claim (Assumptions Table A-3, A-11, and the failure-guaranteeing preconditions that produced A-4, A-7, A-16).`
   - Before: `theoretical-limit — not applicable at Phase 1 — the essence is an architecture/design trade-off, not a convention-vs-physical-limit framing question; its Phase 4 invocation fired (chain C7, the propagation-delay floor).`
     After: `- theoretical-limit (Phase 1) — not applicable — the essence is an architecture/design trade-off, not a convention-vs-physical-limit framing question; its Phase 4 invocation fired (chain C7, the propagation-delay floor).`
   - Before: `fishbone — not applicable — causal breadth for the round-trip symptom was already achieved via five-whys causal mode (narrated at the top of section 4) plus the inversion pass's precondition enumeration, without needing a category-based brainstorm.`
     After: `- fishbone (Phase 2) — not applicable — causal breadth for the round-trip symptom was already achieved via five-whys causal mode (narrated at the top of section 4) plus the inversion pass's precondition enumeration, without needing a category-based brainstorm.` — phase sourced from
     `shared/spine/SKILL-body.md`'s Phase 2 (Challenge Assumptions) operation paragraph: "When the
     assumption space feels too broad to enumerate by intuition, use `{{TOOL:fishbone}}` to
     brainstorm causes by category, then bring each branch into this table as an `untested
     belief`."
   - Before: `five-whys, reduce-to-primitives mode — not applicable — the ground truths used (protocol specification clauses, pattern definitions) are already irreducible primitives confirmed by direct source reading; no compound claim required further decomposition. (Five-whys causal mode was applied separately, narrated in section 4, corroborating chain C1.)`
     After: `- five-whys (Phase 3) — not applicable — (reduce-to-primitives mode) the ground truths used (protocol specification clauses, pattern definitions) are already irreducible primitives confirmed by direct source reading; no compound claim required further decomposition. (Five-whys causal mode was applied separately, narrated in section 4, corroborating chain C1.)` — phase sourced
     from `shared/spine/SKILL-body.md`'s Phase 3 (Establish Ground Truths) operation paragraph: "To
     apply the irreducibility test rigorously, use `{{TOOL:five-whys}}` (reduce-to-primitives
     mode)"; the technique enum slot holds `five-whys` (the schema enum has no separate
     reduce-to-primitives-mode value), with "reduce-to-primitives mode" kept inside the reason text
     per the plan's own instruction, since the causal-mode invocation of the same technique slug
     fired elsewhere in this same report (`techniques.applied` below).
   - Reason: Phase 75's not-applied line-shape requirement so `_xc_techniques` can parse
     `technique`/`phase`/`reason` mechanically; the plan directs quoting the body line that fixes
     each phase number in this README rather than guessing it.

No other line in either file was changed.

## Transcription method (Task 1)

Each block was built in two passes:

1. **Mechanical extraction**, using only `awk`/`grep` over each copy's own section headings —
   never the checker — to get exact row/entry counts and raw cell text, e.g.:

   ```sh
   awk '/^## 2\./{s=1;next} /^## 3\./{s=0} s' "$f" | grep -E '^\|' | tail -n +3 \
     | nl -ba | sed -E 's/^ *([0-9]+)\t\| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|/row\1: type=[\3] verdict=[\5]/'
   ```

   run once per fixture against section 2 (Assumptions), and the equivalent `awk`/`grep` pattern
   used by falsifier f5 against sections 3–5 (Ground Truths / Derivation Chains / Abandoned
   Reasoning) and the `**Pass N (before re-score):**` lines, to get independent row/entry counts
   before any block existed to compare against.

2. **Field transcription**, reading each extracted row/chain/section against the fixture's own
   text and encoding the result as a small Python literal, then `json.dump(..., indent=2,
   ensure_ascii=False)`. The script used for `personal-general.md` and `software-systems.md`
   (`/tmp/.../scratchpad/build_blocks.py` and `build_blocks2.py` at execution time, not committed —
   throwaway):

   ```python
   import json

   def mkA(items):
       return [{"id": i, "type": t, "verdict": v} for i, t, v in items]
   def mkGT(items):
       return [{"id": i, "read_at_source": r} for i, r in items]
   def mkC(items):
       return [{"id": i, "confidence": c, "rests_on": r} for i, c, r in items]

   pg_assumptions = mkA([("A-1","convention","Discard"), ("A-2","untested belief","Discard"), ...])
   pg_gt = mkGT([("GT-1", False), ("GT-2", False), ..., ("GT-5", True), ...])
   pg_chains = mkC([("C1","MEDIUM",["GT-5","GT-6","GT-7","GT-8","GT-11?","GT-12?","GT-18?"]), ...])
   pg_dead_ends = [...]
   pg_block = {"schema_version": 1, "run_mode": "full-composer", "assumptions": pg_assumptions, ...}
   json.dump(pg_block, open("/tmp/pg_block.json", "w"), indent=2, ensure_ascii=False)
   ```

   (software-systems used the same three helper functions in `build_blocks2.py`.) Each field's
   value was read directly from the fixture text per the schema's own `source` note — e.g. every
   assumption's `verdict` is the token leading its Verdict cell before the em-dash; every chain's
   `rests_on` is the identifier list on the chain's own head line, before the first arrow, matching
   its `**Pre-check:** head` field; every `dead_ends` entry is a `### Dead End:` heading name.

3. **Independent cross-check**: falsifier f5 (awk/grep counts over each fixture's own §2–§5 and
   Pass lines, sharing no code with the checker or with step 2's transcription script) was run
   against each finished block and matched exactly (`prose=(...) block=(...)` equal on every
   fixture — see the plan's Task 2 verification output).

4. **Checker validation**: `python3 scripts/check-summary-block.py tests/summary-block-v9.16/<file>.md`
   was run against each finished fixture and returned `SUMMARY-BLOCK: PASS` with exit 0 before
   committing.

### `run_mode` evidence

Both `personal-general.md` and `software-systems.md` were invoked via
`/first-principles:first-principles-analysis` (the full-composer launcher skill) against a general
analysis prompt naming no technique constraint (`prompt.txt` in each source run directory);
neither report's prose states a Step 0 `MODE = ...` line (none of the four fixtures' source prose
does — Step 0 mode is not part of the six-section output contract), so `run_mode: "full-composer"`
is transcribed from the launcher invocation, not from an in-document `MODE` statement. Recorded
here per D-02/D-09 rather than left silently assumed.

### Transcription decision: `software-systems.md` assumption ids

The schema's `assumptions[].id` field is defined as "A-n, where n is the row's 1-based position in
the section 2 table" (`shared/spine/references/summary-schema.json`). `software-systems.md`'s own
prose labels each Assumption cell with an embedded `A-N:` id, and for 19 of its 22 rows that
embedded label already equals the row's position. For the table's last three rows, the embedded
labels are out of position order: row 20 is labelled `A-22:` in its own cell text, row 21 is
labelled `A-20:`, and row 22 is labelled `A-21:` (all verbatim in the untouched prose; this is not
an adaptation to the source). The block's `assumptions[].id` values for those three entries are
therefore `A-20`, `A-21`, `A-22` by row position, not the embedded `A-22`/`A-20`/`A-21` labels —
matching the schema's own definition and the checker's `SB-ASSUMPTION` cross-check, which flagged
the embedded-label ordering as a defect (`block id 'A-22' does not match its row position 'A-20'`)
when first tried. Downstream, `[Assumes: A-22]` in chain C7's derivation step cites the same
substantive assumption (Puma running two or more workers) that is now block-id `A-20` — a
pre-existing labelling inconsistency in the source document itself, not introduced by this
transcription, and outside the reach of any of the 15 Plan-02 cross-checks (none of them compares
a chain's inline `[Assumes: A-N]` mark against `assumptions[].id`).

### `techniques.applied` evidence

- **`personal-general.md`**: `inversion` — "The inversion procedure was applied to the implicit
  claim..." (§2); `five-whys` — "Irreducibility (five-whys, reduce-to-primitives mode) was applied
  to 'the raise is worth $70K'" (§3); `trade-off` — "Trade-off procedure opened with Read and
  applied (Phase 4)" (Options, appendix); `second-order` — the `[2nd]`/`[3rd]` actor/time-lens
  steps inside chain C6; `pre-mortem` — the Adversarial pass's Premise/Causes/Clusters/Disposition
  structure, confirmed by the Techniques-not-applied line "the Phase 5 pass used pre-mortem."
  `fishbone` and `estimate` have no applied-or-not-applicable evidence anywhere in the prose, so
  neither appears in `applied` or `not_applied` (never invented).
- **`software-systems.md`**: `inversion` — "Inversion applied to leadership's claim (Phase 2)"
  (§4 lead-in); `trade-off` — the "Trade-off analysis (process output)" appendix section (Options
  / Criteria & Weights / Scoring); `second-order` — the `[2nd]`/`[3rd]` steps inside chain C6, and
  "Second-order check: no extension step contradicts a ground truth" on C6's confidence line;
  `pre-mortem` — the Adversarial pass record, confirmed by the Techniques-not-applied line "Phase 5
  used pre-mortem (the adversarial pass below)." `five-whys`, `fishbone` (explicitly not applied),
  `estimate` and `theoretical-limit` (explicitly not applied, twice) have no applied evidence.
- **`science-engineering.md`**: `second-order` — the `[2nd]`/`[3rd]` actor/time-lens steps inside
  chain C5 ("added by the Phase 4 audit as a second-order scenario," A-12's Verdict cell);
  `pre-mortem` — the Adversarial pass's Premise/Causes/Clusters/Disposition/Falsification record,
  confirmed by Criterion 5's justification: "the pre-mortem record is complete with dispositions."
  `inversion`, `fishbone` and `trade-off` are explicitly not applied (§ Techniques not applied);
  `five-whys`, `estimate` and `theoretical-limit` (explicitly not applied twice) have no applied
  evidence anywhere in the prose.
- **`tb-01.md`**: `inversion` — "Inversion applied to leadership's claim" is software-systems'
  wording; tb-01's own Phase 2 firing is named directly in its own not-applied line for inversion's
  Phase 5 slot ("inversion's Phase 2 invocation fired instead, against the 'GraphQL is required'
  claim") and in the Adversarial-pass pre-mortem paragraph's parenthetical ("inversion was already
  applied in Phase 2 against the 'GraphQL is required' claim"); `five-whys` — the corroborating
  causal-mode narrative opening section 4 ("Corroborating technique (five-whys, causal mode),
  narrated before the chains it feeds"), confirmed separately by the five-whys not-applied line's
  own parenthetical ("Five-whys causal mode was applied separately, narrated in section 4,
  corroborating chain C1"); `theoretical-limit` — named as fired at Phase 4 in its own not-applied
  line's reason ("its Phase 4 invocation fired (chain C7, the propagation-delay floor)"), and chain
  C7's own text ("a floor set by physics and protocol overhead rather than by API paradigm");
  `trade-off` — chain C8's weighted-criteria scoring ("across seven weighted criteria... a
  mobile-scoped REST BFF scores 109..."); `second-order` — the `[2nd]`/`[3rd]` steps inside chain
  C8; `pre-mortem` — the Adversarial pass's own explicit label "**Adversarial technique —
  pre-mortem**" plus its Premise/Causes/Clusters/Disposition/Falsification/Tripwires record.
  `fishbone` is explicitly not applied.

## Transcription method (Task 2)

Same two-pass method as Task 1 (`build_blocks3.py` for `science-engineering.md`, `build_blocks4.py`
for `tb-01.md`, both throwaway scripts in the scratchpad, using the same `mkA`/`mkGT`/`mkC` helper
shape as `build_blocks.py`). `tb-01.md`'s assumption ids are read by row position directly from its
own cell labels (`A-1:` … `A-21:`), which already match position throughout — no
`software-systems.md`-style discrepancy exists in this fixture.

## Falsifier f5 output (final, all four fixtures)

```text
tests/summary-block-v9.16/personal-general.md prose=(18 20 8 4 0) block=(18 20 8 4 0)
tests/summary-block-v9.16/software-systems.md prose=(22 10 8 6 1) block=(22 10 8 6 1)
tests/summary-block-v9.16/science-engineering.md prose=(13 10 5 4 0) block=(13 10 5 4 0)
tests/summary-block-v9.16/tb-01.md prose=(21 6 8 4 0) block=(21 6 8 4 0)
```

`bash .planning/phases/75-summary-block-checker-and-gate/75-falsifiers.sh f5` exits 0 — every
fixture's prose-derived inventory (assumption rows, ground-truth declarations, chains, dead ends,
earlier Gate passes) equals its block's own array lengths, computed by code (awk/grep over section
headings) that shares nothing with `scripts/check-summary-block.py` or the transcription scripts
above.

`python3 scripts/check-summary-block.py tests/summary-block-v9.16/<file>.md` returns
`SUMMARY-BLOCK: PASS` (exit 0) for all four fixtures.

## Phase 80 backfill (2026-10-01)

Each fixture's block gained one key, `conclusion.rests_on`, transcribed from that copy's own
section 6 `**Pre-check:**` head (ids in head order, bands dropped, `?` kept). No prose line
changed. The source sha256 table above describes the pre-backfill copies — this backfill adds a
JSON key to the already-committed block only; it does not touch any `.md` prose line in any of the
four files.

| Fixture | `conclusion.rests_on` |
|---|---|
| `personal-general.md` | `["C1","C2","C3","C5","C6","C7","C8","GT-19?"]` |
| `science-engineering.md` | `["C1","C2","C3","C4","C5"]` |
| `software-systems.md` | `["C1","C2","C3","C4","C5","C6","C7","C8"]` |
| `tb-01.md` | `["C1","C2","C3","C4","C5","C6","C7","C8"]` |
