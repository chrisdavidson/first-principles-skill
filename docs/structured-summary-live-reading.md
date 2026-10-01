# Reading — structured-summary-live

[`docs/structured-summary-live-protocol.md`](structured-summary-live-protocol.md) is the
pre-registration this reading answers to. All figures below are copied from
`tests/structured-summary-live/{checks,result,crossread,manifest}.json`, never retyped from
memory; every command was re-run directly for this reading and its exit code recorded.

**Verdict:** FAIL — blocks, gate

| Criterion | Figure | Command | Exit |
|---|---|---|---|
| (a) runs | 14/14 complete, 14/14 correct body | `read.py verdict --leg runs` → `LEG runs: PASS (14/14 complete, 14/14 correct body)`; `77-falsifiers.sh f2` → `14 / 14` | **0** / **0** |
| (b) blocks | 9/14 pass the unchanged checker | `read.py verdict --leg blocks` → `LEG blocks: FAIL (9/14)`; `77-falsifiers.sh f4` → `checker pass 9/14` | **1** / **1** |
| (c) gate | 13/14 cleared | `read.py verdict --leg gate` → `LEG gate: FAIL (13/14)`; `77-falsifiers.sh f6` → `LEG gate: FAIL (13/14)` | **1** / **1** |
| (d) cost | median $2.8731 ≤ $3.00 (baseline $2.7343755) | `read.py verdict --leg cost` → `LEG cost: PASS (median $2.8731)`; `77-falsifiers.sh f7` → `2.8731109000000004` | **0** / **0** |

`read.py verdict --leg all` exits **1**. Per LIVE-01/LIVE-02's "Done when" wording, this run does
**not** hold 14/14 on blocks or on gate. LIVE-03 (cost) holds. This is reported plainly, not
softened: 5 of 14 reports fail the unchanged checker, and 1 of 14 fails to clear the gate — the
real reading this phase exists to produce, not a rate (§7) and not re-rolled.

## What ran

- **HEAD at dispatch:** `f0f18a310bbadac1d51c9699cace9a130a27d60a` (the 77-02 commit; `manifest.json["head_sha"]`).
- **`first-principles/` tree hash:** `e2dc163771e695fa7fd906ac5b5a2d8ec1596912`.
- **`shared/` tree hash:** `8ff27d3d5893cdb08b97c62e2afb5a2340ee645d`.
- **agent-router HEAD:** `d1c0bf96b1ad944836c38cf622b0b4d8c96423b0` — matches the protocol's §3 plan-time value.
- **Runner sha256 (pinned):** `1b9194802e482559028689c4a17f5d8cdff10d96746e7245b1c15b0e03006bf5`.
- **Checker sha256 (recorded in the manifest, checked by `cmd_check` before every read):** `473481374204089c1e2c79a7b43c20c829b8770d5d2ccdf88489efe427233b02`.
- **`phase75_close`:** `ab23ef45be849f9d4e66b73fcb8d37072a5efe87`.
- **Model and plugin version, every one of the 14 runs:** `claude-opus-5-5` / `9.15.0` — uniform
  across `checks.json`; no run used a model other than the baseline's, so no per-run disclosure
  beside the cost figure is needed.
- **Invocations (`manifest.json["invocations"]`):**
  - **k=1**, `2026-10-01T01:26:35.605428Z`, `runner_exit: 0`, `stubs: []`, `targets: []` (fresh
    start) — 3 examples produced zero analysis file despite the runner's own `complete` status:
    `personal-general-2`, `product-business-2`, `science-engineering`.
  - **k=2**, `2026-10-01T02:17:23.602952Z`, `runner_exit: 0`, `stubs: []`, `targets:
    [personal-general-2, product-business-2, science-engineering]` (the automatic
    `relaunch_targets`, never a hand-picked `--only`) — `zero_file: []`; all 3 produced a report.
    `resumed_utc` matches this invocation's own `utc`.
  - No usage/spend-limit stub occurred in either invocation (`stubs: []` both times) — no pause
    to report.
- **Checker falsifier** (§5's own, unchanged-checker claim): `git diff
  ab23ef45be849f9d4e66b73fcb8d37072a5efe87..HEAD -- scripts/check-summary-block.py` — **empty
  output**, exit 0. `scripts/check-summary-block.py` has not moved since `PHASE75_CLOSE`.

## Before and after

The table from `read.py table`, verbatim:

| example | before: status · cost $ · words · turns · gate | after: status · block present · checker · cost $ · words · turns · gate · trace.py gate |
|---|---|---|
| composed-inversion-second-order | complete · $2.6845 · — · 4 · cleared | complete · yes · PASS · $3.0415 · — · 4 · cleared · cleared |
| decompose-irreducibility | complete · $2.2139 · — · 4 · cleared | complete · yes · PASS · $2.6898 · — · 4 · cleared · cleared |
| estimate-fermi | complete · $3.9279 · — · 5 · cleared | complete · yes · PASS · $2.7047 · — · 2 · cleared · cleared |
| ishikawa-fishbone | complete · $2.6805 · — · 6 · cleared | complete · yes · PASS · $2.4225 · — · 6 · cleared · not cleared |
| personal-general | complete · $3.3094 · — · 5 · cleared | complete · yes · FAIL · $3.3600 · — · 6 · cleared · cleared |
| personal-general-2 | complete · $2.9142 · — · 4 · cleared | complete · yes · FAIL · $2.5585 · — · 5 · cleared · cleared |
| product-business | complete · $2.4182 · — · 6 · cleared | complete · yes · PASS · $2.0147 · — · 3 · cleared · cleared |
| product-business-2 | complete · $2.3324 · — · 5 · cleared | complete · yes · PASS · $2.5601 · — · 5 · cleared · cleared |
| science-engineering | complete · $1.6107 · — · 4 · cleared | complete · yes · FAIL · $4.6977 · — · 4 · not cleared · cleared |
| science-engineering-2 | complete · $3.4643 · — · 7 · cleared | complete · yes · PASS · $3.2235 · — · 5 · cleared · cleared |
| self-application | complete · $3.3760 · — · 3 · cleared | complete · yes · FAIL · $4.1385 · — · 4 · cleared · cleared |
| software-systems | complete · $2.6453 · — · 5 · cleared | complete · yes · PASS · $3.2956 · — · 5 · cleared · cleared |
| software-systems-2 | complete · $3.2282 · — · 4 · cleared | complete · yes · FAIL · $2.3993 · — · 3 · cleared · cleared |
| theoretical-limit-carnot | complete · $2.7842 · — · 4 · cleared | complete · yes · PASS · $3.8900 · — · 5 · cleared · not cleared |

after median cost: $2.8731 (n=14); before median cost: $2.7344 (n=14).

**The "words" column prints `—` for all 28 cells, before and after — this is a bug in the frozen
`read.py`, not a missing figure.** `cmd_table` reads `r.get("words")`, but `run.py`'s own
`summary.json` schema names the field `analysis_words` (confirmed directly on both
`tests/structured-summary-live/raw/summary.json` and `tests/structured-summary-live/baseline/summary.json`
— `sorted(keys())` on either contains `analysis_words`, never `words`). `read.py` is frozen for
this plan (no code edit), so the figure is computed here directly from `analysis_words` instead of
through the broken column:

| example | before words | after words | Δ |
|---|---|---|---|
| composed-inversion-second-order | 8746 | 8608 | −138 |
| decompose-irreducibility | 6561 | 7312 | +751 |
| estimate-fermi | 10876 | 8421 | −2455 |
| ishikawa-fishbone | 10743 | 9646 | −1097 |
| personal-general | 9416 | 12184 | +2768 |
| personal-general-2 | 8329 | 9138 | +809 |
| product-business | 8491 | 7289 | −1202 |
| product-business-2 | 8893 | 8741 | −152 |
| science-engineering | 6189 | 12220 | +6031 |
| science-engineering-2 | 10232 | 11483 | +1251 |
| self-application | 9168 | 10712 | +1544 |
| software-systems | 10300 | 12412 | +2112 |
| software-systems-2 | 11428 | 8619 | −2809 |
| theoretical-limit-carnot | 7020 | 8523 | +1503 |

**after median words: 8939.5 (n=14); before median words: 9030.5 (n=14); Δ −91.** The median
moves *down*, not up. The block adds words by construction — the fenced JSON appendix is literal
added content on every report that carries one — but this single-sample-per-example comparison is
dominated by ordinary run-to-run variance in the prose itself (several deltas exceed ±2,000 words
in both directions, e.g. science-engineering +6,031, software-systems-2 −2,809), which swamps the
appendix's fixed addition in the median. This is exactly the "one sample per example" caveat
(protocol §7) made visible in a single number, not a signal that the block shrinks reports.

## Shortfalls

5 of 14 reports fail the unchanged checker: `personal-general`, `personal-general-2`,
`science-engineering`, `self-application`, `software-systems-2`. Every finding below is read from
the report's own prose against its own block, not inferred from the finding message.

### personal-general, personal-general-2, self-application, software-systems-2 — all `SB-TECHNIQUES`

All four share one root cause: a `Techniques not applied:` line that names **which mode** or
**which sub-phase name** of a two-mode/two-phase companion technique did not apply, in a form the
checker's `_TECH_NOT_APPLIED_LINE_RE` cannot parse. The regex accepts exactly `<technique>` or
`<technique> (Phase N)` before the em-dashes
(`^(?P<tech>[a-z-]+)(?:\s+\(Phase\s+(?P<phase>[1-5])\))?\s+—\s+not applicable\s+—\s+(?P<reason>.+)$`,
`scripts/check-summary-block.py:768-771`) — nothing else may sit between the technique slug and
the em-dash.

| Example | Offending line (verbatim) | Parses? |
|---|---|---|
| `personal-general` (line 412) | `five-whys causal mode (Phase 3) — not applicable — there is no recurring symptom to root-cause; reduce-to-primitives mode was applied instead` | No — `causal mode` sits between the technique name and `(Phase 3)` |
| `personal-general-2` (line 312) | `five-whys (causal mode) — not applicable — there is no recurring symptom to trace` | No — `(causal mode)` is not `(Phase N)` |
| `self-application` (line 316) | `theoretical-limit (Phase 1 reframe) — not applicable — nobody claims the budget figure is a physical bound, so separating convention from hard bound does not reframe the question.` | No — `reframe` after the phase digit |
| `self-application` (line 318) | `five-whys (causal mode) — not applicable — there is no recurring failure symptom to drill. Reduce-to-primitives mode was applied in Phase 3.` | No — same as `personal-general-2` |
| `software-systems-2` (line 300) | `five-whys (reduce-to-primitives) — not applicable — the ground truths are quoted vendor or NIST text, definitions, or bracketed estimates, with no compound claim left to reduce` | No — a mode name in place of `(Phase N)` |

**The block's `not_applied` entries are correct in every one of the five cases** — checked
directly against each report's own JSON: `personal-general`'s `not_applied[3]` is `{"technique":
"five-whys", "phase": 3, "reason": "there is no recurring symptom to root-cause; reduce-to-primitives
mode was applied instead"}`, matching the prose line's content word for word once the mode
qualifier is set aside; the same holds for the other four. The cascade findings the checker also
reports (`"not_applied[3]: block technique 'five-whys' disagrees with the document's
'inversion'"` on `personal-general`, and the equivalent pair on `self-application`) are **not** a
second, independent defect — they are the mechanical consequence of one unparseable line dropping
out of the parsed list and shifting every later index, confirmed by re-counting: `personal-general`
has 5 block entries against 4 parseable prose lines (the 412 line excluded); `self-application` has
5 against 3 (both 316 and 318 excluded).

**Which side is wrong:** the agent, in these five lines, wrote a form the template never
prescribes and the shared worked examples never teach. `shared/spine/SKILL-body.md:125`'s literal
prescribed form is `<technique> — not applicable — <reason>` — bare technique name, no phase
annotation at all in that literal text. The `(Phase N)` suffix is a convention the body does not
write down but that every one of the other 9 passing reports, and 3 of these same 5 reports' other
lines (`theoretical-limit (Phase 1)`, `theoretical-limit (Phase 4)`, `fishbone (Phase 2)`,
`inversion (Phase 5)`), use successfully and consistently. None of the 14 worked examples under
`shared/examples/` carry a `Techniques not applied:` block at all (`/usr/bin/grep -c "not
applicable" shared/examples/*.md` — no match anywhere), and `self-application`'s own worked
example — the one it re-read, flagged below — has `"techniques": null` with no not-applied prose
(D-15), so this was not taught by anything the agent read. It is a self-inflicted formatting
inconsistency, visible within the same block: `self-application` writes `theoretical-limit (Phase
4)` correctly two lines after writing `theoretical-limit (Phase 1 reframe)` incorrectly;
`personal-general` writes `theoretical-limit (Phase 1)`, `theoretical-limit (Phase 4)`, `fishbone
(Phase 2)` and `inversion (Phase 5)` correctly and only the five-whys line adds the stray "causal
mode" words. **Side needing the change: template** — `SKILL-body.md:125` prescribes a bare
`<technique> — not applicable — <reason>` form with no syntax for naming which of a two-mode or
two-phase technique's invocations is meant, even though the body itself names two techniques
(`theoretical-limit`, `inversion`) as invoked at two phases and documents five-whys as carrying two
named modes (`SKILL-body.md:565-576`) — the gap the agent was filling in, inconsistently, five
times out of fourteen. Loosening the checker's regex to accept a free-text qualifier would let a
wrong value through unnoticed (every historical commit the protocol's §5 table lists tightened or
widened the checker only against a named, verified form); the fix belongs in the template, giving
the agent one documented way to write the disambiguator, not in the checker.

### science-engineering — `SB-CHAIN-RESTS-ON` and `SB-REENTRY`, the sole gate-not-cleared example

**`SB-CHAIN-RESTS-ON`:** `"C1: block rests_on ['GT-10', 'GT-4', 'GT-5?', 'GT-6?'] disagrees with
section 4's head refs ['GT-5?']"`. Reading chain C1 in the report (line 116): its true head line
is `GT-4 (lift energy) + GT-5? (appliance figures) + GT-6? (standby) + GT-10 (PVGIS consumption is
all connected equipment; PR 0.67 includes inverter loss) → lifting 0.2 m³/day ...` — four GT refs,
exactly what the block's `rests_on` lists. The checker's `_chain_head_refs` (`scripts/check-quality-harness.py:5681-5726`)
scans forward and returns on the **first** line matching its head-token pattern; two lines earlier
(line 101) the chain's intro prose reads `Appliance energy table (power × hours, or annual ÷ 365),
using GT-5? figures:` — no arrow, but it does contain a `GT-5?` token, so `_chain_head_refs`
mistakes this scene-setting sentence for the chain's head and returns only `{GT-5?}`, never
reaching the real head three lines later. Confirmed directly: calling `_chain_head_refs` on the
extracted C1 block returns `({'GT-5?'}, set())`. **The block is right; the checker's head-line
detector is wrong** — it stops at the first GT-mentioning line rather than the first line that is
actually a chain head (one followed by an arrow-chain). Side needing the change: **checker**
(a parser bug, not a disagreement about the analysis).

**`SB-REENTRY`:** `"re_entry.fired is false but a **Disclosed:** paragraph at the top of the
document names a re-entry edge"`. The report's own opening line (line 1) reads: `**Disclosed:**
... The cabin's exact coordinates were also not supplied, and chain C7 shows they matter. **No
re-entry edge fired.**` — the block's `re_entry.fired: false` is correct, and the prose explicitly,
affirmatively agrees with it. The checker's `_ANY_EDGE_NAME_RE` (`scripts/check-summary-block.py:1055-1057`)
is `re-entry edge|Fix/Repeat|return(?:ed)? to Phase [12]|re-open`, a plain substring search with no
negation handling — it matches the literal substring "re-entry edge" inside "No re-entry edge
fired," reads that as *naming* a fired edge, and rule R6 (`"fired is False and has_reentry_disclosure"`,
`scripts/check-summary-block.py:1438-1443`) fires a false positive. **The block and the prose
agree; the checker misreads a negated sentence as a positive disclosure.** Side needing the
change: **checker**.

Because `SB-REENTRY` is one of the `GATE_CODES` the `gate_cleared` rule checks
(`read.py`'s `GATE_CODES` tuple), this single false positive is what keeps `science-engineering`'s
gate from clearing under this protocol's rule, even though the block's own `gate.cleared: true` and
the prose's own last `**Gate result:** cleared` line both say it cleared, and `trace.py`'s own
(stricter) `cleared` re-derivation also reads `true` for this example (`trace_cleared_after: true`,
`checks.json`). The 13/14 gate figure is real under the rule as specified, and it traces to one
checker defect, not a wrong analysis.

**Summary of side attribution — shortfalls:**

| Example | Finding(s) | Block correct? | Side needing the change |
|---|---|---|---|
| personal-general | `SB-TECHNIQUES` ×5 | Yes | template (no syntax for a mode/phase qualifier) |
| personal-general-2 | `SB-TECHNIQUES` ×2 | Yes | template |
| science-engineering | `SB-CHAIN-RESTS-ON`, `SB-REENTRY` | Yes | checker (two independent false positives) |
| self-application | `SB-TECHNIQUES` ×8 | Yes | template |
| software-systems-2 | `SB-TECHNIQUES` ×2 | Yes | template |

No shortfall in this run traces to the worked examples teaching a wrong form, and none traces to
the block itself being wrong — every block value checked above matches its own report's prose once
the format mismatch is read through. The checker is not edited here (D-07, protocol §5); both
defects named above are recorded as findings for a future phase.

## Block vs parser

`crossread.json` records 39 disagreements across 14 examples between the block and agent-router's
`trace.py` prose parser (`parse_analysis`). Every category below was read against `trace.py`'s own
source (`~/Projects/agent-router/integrations/first-principles/trace.py`) to decide which side was
wrong; `trace.py` is owned by agent-router, not this repository (CONTEXT.md's deferred TRACE-01).

**`run_mode` — block correct, parser never extracts a value (13 of 14 examples; `ishikawa-fishbone`
carries `focused-five-whys`, all others `full-composer`).** `trace.py`'s `RUN_MODE` regex requires
a literal `Run mode`/`Mode`/`MODE` label followed by `:` or `=` somewhere in the prose
(`trace.py:171-173`). None of the 14 live reports write such a label anywhere outside the JSON
block (`/usr/bin/grep -ni mode` on a representative report finds only the block's own lowercase
`"run_mode": "full-composer",` line, which the regex's case-sensitive label words do not match).
Nothing in `shared/spine/SKILL-body.md` requires the agent to state the mode in prose — D-04 makes
the block process output about the analysis, and `run_mode` is schema-required in the block, never
in a labeled prose sentence. This is a one-directional parser coverage gap in `trace.py`, not a
disagreement: the block is the only place this field is recorded, correctly, in every report.

**`re_entry.fired` (block `false`, parser `null`) — 6 examples: `decompose-irreducibility`,
`estimate-fermi`, `ishikawa-fishbone`, `product-business`, `software-systems-2` (block `true` here,
parser still `null`), `theoretical-limit-carnot`.** `trace.py`'s `edge` extraction
(`trace.py:257`) requires the literal word "re-entry" to appear anywhere in the text; when nothing
fired, these reports correctly carry no re-entry disclosure at all (the protocol requires one only
"when true," §4(b)/D-02), so the word never appears and `trace.py` returns `None` for the whole
`re_entry` object rather than a `{"fired": false}` dict — a coverage gap, not a disagreement, except
for `software-systems-2`, where the block says `true` and the prose does use the word "re-entry"
in its Disclosed paragraph (`"One re-entry edge fired, the Self-Audit Gate's Fix/Repeat loop."`) —
there `trace.py` still read `null` in the crossread; its `NO_EDGE` match or the single-sentence
`[^.\n]*` extraction window is not reproduced here in detail because the block's own value is
independently checker-verified correct (`checker_passed: true`, `checker_exit: 0` for
`software-systems-2`'s re-entry fields) and this instrument is out of this repo's scope to fix.

**`gate.passes` (block `2`, parser `1`) — 7 examples, every example where `fix_repeat_fired` is
true: `composed-inversion-second-order`, `personal-general`, `personal-general-2`,
`product-business-2`, `science-engineering-2`, `self-application`, `software-systems`.**
`trace.py`'s `_gate_passes` (`trace.py:185-195`) counts a pass by finding repeated
`**Criterion N: ...** ... Band: X` blocks for the same criterion number. This repo's template
(D-18, Phase 74) shows the *earlier* pass in a fixed one-line summary form instead —
`**Pass 1 (before re-score):** Criterion 1 Rigorous · Criterion 2 Sound · ...` — and only the
*final* pass uses the repeated per-criterion block form `trace.py` scans for. `trace.py` therefore
sees one set of criterion blocks, not two, and undercounts every re-scored run to 1. Confirmed on
`composed-inversion-second-order`'s report: line 339 carries the one-line `Pass 1 (before
re-score):` summary and lines 343-373 carry the full per-criterion Pass 2 blocks — exactly the
shape D-18 prescribes. **The block is correct in all 7 cases; `trace.py` cannot read this repo's
prescribed earlier-pass form at all.** This is the modern shape of the handoff's old "7 of 8
re-scored runs lost the first pass" finding (below) — now the block, not `trace.py`, is the record
a reader should use, and every one of this run's 7 multi-pass examples shows the gap.

**`gate.cleared`, `label: parser_rule` — 2 examples: `ishikawa-fishbone`, `theoretical-limit-carnot`.**
Exactly the divergence protocol §4(c) names: both reports' final pass carries one `Hand-wavy` band
and no `Absent` (`ishikawa-fishbone`: `[Sound, Rigorous, Hand-wavy, Rigorous, Rigorous, Sound]`;
`theoretical-limit-carnot`: `[Rigorous, Sound, Hand-wavy, Sound, Rigorous, Rigorous]`), which the
rubric's one-`Hand-wavy`-cap rule clears (block `gate.cleared: true`) and which `trace.py`'s own
stricter rule (`"cleared": not ({"Absent", "Hand-wavy"} & set(passes[-1].values()))`, `trace.py:288-290`)
rejects outright. Neither side is wrong about the facts; `trace.py` applies a different, stricter
rule by design, shown here only as the informational `trace.py gate` column and never as the
measure (protocol §4(c)).

**`conclusion.recommendation` — 9 examples.** Every one of these 9 entries is a pure truncation
artifact, not a content disagreement: `trace.py`'s `_trunc(rec.group(1), 400)` (`trace.py:121-122,
294`) cuts the recommendation at exactly 400 characters with no ellipsis. Checked directly for all
9: the parser's value is `block[:400]` character-for-character (`b_rec.startswith(stripped)` is
`True` in every case; `len(stripped) == 400` in every case). `read.py`'s own `crossread_example`
has a boundary bug that keeps this from being labeled `parser_cut` in the committed JSON — its
condition is `len(stripped) < 400`, which excludes the common case where `_trunc` cuts at exactly
the 400-char ceiling (it should read `<= 400`); `read.py` is frozen for this plan, so this is
disclosed rather than fixed. Under D-17, the block carries the recommendation "in full" — the block
is the complete, correct record in all 9 cases, and `trace.py`'s 400-character cap is a known,
deliberate limit on its own side (`MAX_TEXT`), not a defect in the analysis.

### The handoff's six parser failures, revisited against this run's blocks

| Handoff finding | What the block now records | Matches the prose? |
|---|---|---|
| personal-general re-entry misread as fired | `re_entry.fired: true`, edge `"the Self-Audit Gate's Fix/Repeat loop"`, with a trigger sentence — read directly from the block, no parsing of free prose needed | Yes — the `**Disclosed:**` paragraph states the Fix/Repeat loop fired once with the same trigger; the checker found no `SB-REENTRY` finding on this example |
| software-systems Fix/Repeat not recorded | `re_entry.fired: true`, `gate.fix_repeat_fired: true`, edge recorded | Yes — the Disclosed paragraph explicitly uses the word "re-entry" ("One re-entry edge fired, the Self-Audit Gate's Fix/Repeat loop") and `trace.py` itself now agrees (no `gate.passes` or `re_entry.fired` crossread entry at all — wait, `gate.passes` does disagree, see above; `re_entry.fired` is read correctly by both sides here) |
| 7 of 8 re-scored runs lost the first pass | Every multi-pass block (7 of 14 this run) carries `gate.passes: 2` and both passes' bands in full | Yes in every case — `trace.py` still undercounts to 1 (see `gate.passes` above), but a reader using the block, as this protocol does, gets the correct count every time |
| product-business-2 gate result missed | `gate.cleared: true`, prose `**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes` | Yes — checker found no gate-related finding; no `gate.cleared` crossread entry at all |
| estimate-fermi gate result missed | `gate.cleared: true`, single pass, prose Gate result line reads `cleared` | Yes — same, no crossread entry |
| science-engineering / self-application recommendation cut at a colon | Both blocks carry the `conclusion.recommendation` field in full (845 and 484 characters respectively) | Yes, from the block; `trace.py` still truncates at a fixed 400-character length (no longer specifically at a colon — see `conclusion.recommendation` above), but the block is the complete record a reader should use |

All six of the handoff's original findings are resolved **as read from the block**: in every case
the block now carries the correct value, directly, without depending on `trace.py`'s prose
guessing. The two findings that persist in `trace.py`'s own reading (`gate.passes` undercounting on
re-scored runs, and the 400-character recommendation cut) are now TRACE-01's problem to fix on
agent-router's side, not this repository's — the block gives agent-router's reader a direct,
correct value to use instead, which is this phase's purpose.

## self-application

Checker result: **FAIL** (`SB-TECHNIQUES` ×8, the mode/phase-qualifier shortfall documented
above — the block's content is correct; see Shortfalls). Gate: **cleared**
(`gate_cleared: true`, no gate-related finding).

**It read its own worked example again.** `tests/structured-summary-live/raw/summary.json`'s own
`read_own_example` field for `self-application` is `true` (and was also `true` in the
`2026-09-29` baseline — D-12's documented repeat). This is **not** visible in
`tests/structured-summary-live/checks.json`'s own `read_own_example` field, which reads `false`
for every example including this one: `read.py`'s `cmd_check` computes it as
`bool(row.get("self_application"))` (`read.py:347`), but `run.py`'s `summary.json` schema names
the field `read_own_example`, not `self_application` — there is no key by that name on the row, so
the expression is unconditionally `False` for every example, and the `†` marker `cmd_table` would
print for a true value (`read.py:585`) can never fire. Running `read.py table` live for this
reading reproduces this directly: the self-application row carries no `†`. **This means the
`self-application †` marker printed in `.planning/phases/77-live-14-run-confirmation/77-03-SUMMARY.md`'s
committed table was not produced by the tool as that plan's own text claims ("verbatim") — it was
added by hand**, disclosed here rather than silently repeated. `read.py` is frozen for this plan,
so the bug (wrong field name) is recorded, not fixed; the underlying fact itself — self-application
read its own example — is independently confirmed from `run.py`'s own correctly-named field and is
not in question.

Per D-12 and protocol §6: a pass (or in this run, a fail) on a read-its-own-answer-key run is not
independent evidence either way, and this row is reported separately rather than folded into any
aggregate claim about the format's general behavior. It still counts in the literal 14 for every
criterion in §4, per the protocol.

## What this does and does not show

One sample per example, on one model (`claude-opus-5-5`, plugin `9.15.0`): this run shows the
format holding on 9 of these 14 particular reports and failing on 5, with every failure traced to
a specific, named cause (four to one template gap, repeated five times across three examples; one
to two checker parsing bugs). It is not a rate — a single run of 14 is a pre-registered
confirmation on named prompts, not a K-of-N noise-floor reading
(`docs/v8.7-constraint-teardown.md` §2 item 3), and the 9/14 and 13/14 figures are not re-rolled
to chase a better number. Cost is one sample per example (median $2.8731, n=14); a different
model, a different day, or a different sampled completion could move any individual figure.
`self-application`'s row is read-its-own-example contaminated by construction and is reported
separately rather than blended into the aggregate. The block-vs-`trace.py` crossread shows the
block is a strictly more complete and more correct record than agent-router's own prose parser on
every field compared here — not a claim that `trace.py` is wrong to exist, only that it reads less
than the block now carries directly.
