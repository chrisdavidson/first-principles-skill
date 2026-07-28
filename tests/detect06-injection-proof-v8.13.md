# DETECT-06 Injection Proof — v8.13 Phase 187

This file matches none of the FROZEN-EVIDENCE globs (`tests/step0-baseline-v*.md`,
`tests/step0-captures-v*`, `tests/routing-baseline-v3.*.md`,
`tests/routing-battery-baseline-v4.3.md`, `tests/routing-baseline-v7.11.md`,
`tests/routing-battery-baseline-v7.11.md`, `tests/focused-output-baseline-v*.md`,
`tests/sub-skill-routing-baseline-v*.md`, `tests/quality-catalog-v8.7.md`,
`tests/quality-probe-v8.7`, `tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7`,
`tests/quality-baseline-v8.7-postfix`), so it can be added without touching a frozen path.

All file paths in this document are given in inline code, never as a markdown link, so no link
gate can ever be tripped by this record.

## 1. What this is and why it exists

DETECT-06 (Phase 187) strengthens `_selftest_contract_pin`'s Guard A inside
`scripts/check-quality-harness.py` so the canonical worked examples in
`shared/spine/references/output-template.md` and the Verdict vocabulary in
`shared/spine/references/validation-rubric.md` are extracted at runtime and checked against the
detector, rather than being hand-copied literals. Plans 187-01 and 187-02 built that guard. This
file is the fault-injection proof that the guard is load-bearing — that it actually fails when the
things it claims to check are broken — because in this milestone a green `QUAL-01` has repeatedly
coexisted with a broken invariant (D-18, DETECT-01 through DETECT-05), and an assertion nobody has
seen fail is an assumption.

Five injections plus a stayed-green control were run, each under both `python3` and `python3 -O`,
all staged through one uniform scratch-tree recipe (D-16) that copies the repo to a `mktemp -d`
directory, mutates only inside that copy, and writes nothing tracked. Twelve runs total.

## 2. Provenance

- **Base commit SHA the phase started from:** `4b47700` (the pre-phase base for Phase 187, per
  `187-RESEARCH.md`'s Pre-Phase Baseline table).
- **Commit the twelve runs in this file were actually run against:** `98c6656` (Plan 187-02's
  final commit — Guard A already carries the strengthened seven-fixture template extraction from
  Plan 187-01 and the two rubric-derived Criterion 2 fixtures plus the six-check anti-blanket-pass
  sweep from Plan 187-02).
- **`python3 --version`:** `Python 3.13.5`
- **`uname -srm`:** `Linux 6.12.57+deb13-amd64 x86_64`
- **Run date:** 2026-07-28
- **Scratch-tree mechanism (D-16):** each injection took a fresh `mktemp -d` copy of `scripts/`,
  `shared/`, `tests/`, and `first-principles/`, mutated only the copy, ran `--self-test` against
  the copy under both interpreters, and removed the copy immediately after (`rm -rf`). Nothing
  tracked was written at any point — verified in section 5 below.
- **Measured `REPO_ROOT` inside the scratch copy (the precondition INJ-3/INJ-4/INJ-5 depend on,
  D-14):** `REPO_ROOT` is `Path(__file__).resolve().parents[1]` — purely a function of where the
  running script sits on disk. Asserted directly before any injection ran: a scratch copy was made
  at `/tmp/detect06-hPs9Lm`, the scratch copy's module was loaded via
  `importlib.util.spec_from_file_location`, and `mm.REPO_ROOT` printed exactly
  `/tmp/detect06-hPs9Lm` — equal to the scratch directory, not the original repository. The
  unmutated scratch copy's `--self-test` also exited `0` under both interpreters at that same
  moment (`ctrl_py_exit=0`, `ctrl_pyO_exit=0`), confirmed again independently by the full CTRL run
  in section 3 below. Had `REPO_ROOT` instead resolved to the original tree, INJ-3/INJ-4/INJ-5
  would have silently read unmutated files and proven nothing — this was measured, not assumed.

## 3. The twelve-run matrix

Columns: injection id, interpreter, exit code, fired, stayed green, evidence.

| Injection | Interpreter | Exit | Fired | Stayed green | Evidence |
|---|---|---|---|---|---|
| CTRL | python3 | 0 | nothing | all 13 labelled lines PASSED | §3.0 |
| CTRL | python3 -O | 0 | nothing | all 13 labelled lines PASSED | §3.0 |
| INJ-1 | python3 | 1 | `defects` + `contract_pin` sub-checks (verdict-axis mismatches) | 11 of 13 sub-checks (`guardrail_a`, `guardrail_b`, `scoreline`, `blinding`, `tabulation`, `baseline`, `run_layer`, `compare`, `limitation1_chainlabels`, `limitation2_citationnorm`, `limitation3_extractionscope`) | §3.1 |
| INJ-1 | python3 -O | 1 | identical to python3 above | identical to python3 above | §3.1 |
| INJ-2 | python3 | 1 | `defects` + `contract_pin` sub-checks (chain-axis mismatches) | same 11 of 13 sub-checks as INJ-1 | §3.2 |
| INJ-2 | python3 -O | 1 | identical to python3 above | identical to python3 above | §3.2 |
| INJ-3 | python3 | 1 | `contract_pin` sub-check only, mode 2 on `C-TEMPLATE-C1` | 12 of 13 sub-checks — `defects` stays PASSED here, unlike INJ-1/INJ-2 | §3.3 |
| INJ-3 | python3 -O | 1 | identical to python3 above | identical to python3 above | §3.3 |
| INJ-4 | python3 | 1 | `contract_pin` sub-check only, mode 1 on `C-TEMPLATE-FORMAT` | 12 of 13 sub-checks (all except `contract_pin`) | §3.4 |
| INJ-4 | python3 -O | 1 | identical to python3 above | identical to python3 above | §3.4 |
| INJ-5 | python3 | 1 | `contract_pin` sub-check only, rubric vocabulary mismatch | 12 of 13 sub-checks (all except `contract_pin`) | §3.5 |
| INJ-5 | python3 -O | 1 | identical to python3 above | identical to python3 above | §3.5 |

**Finding.** All ten injection runs exit `1`; both CTRL runs exit `0` with thirteen labelled
`sub-check PASSED` lines and the `contract_pin: 36 asserted fixtures, 0 observation-only, 0
PINNED-RED carried` summary line. Every FAIL set is byte-identical between `python3` and
`python3 -O` for every injection — the AST assert-count in `scripts/check-quality-harness.py` is
`0` (measured, both before and after this matrix), so `-O`'s assertion-stripping does not hollow
any of the twelve runs.

### 3.0 CTRL — unmutated scratch copy

```
--- python3 ---
self-test: guardrail_a sub-check PASSED
self-test: guardrail_b sub-check PASSED
self-test: scoreline sub-check PASSED
self-test: blinding sub-check PASSED
self-test: tabulation sub-check PASSED
self-test: baseline sub-check PASSED (quality-baseline-v8.7, quality-baseline-v8.7-regenerated, quality-baseline-v8.7-postfix)
self-test: defects sub-check PASSED
self-test: run_layer sub-check PASSED
self-test: compare sub-check PASSED
self-test: limitation1_chainlabels sub-check PASSED
self-test: limitation2_citationnorm sub-check PASSED
self-test: limitation3_extractionscope sub-check PASSED
contract_pin: 36 asserted fixtures, 0 observation-only, 0 PINNED-RED carried (DETECT-02: 0, DETECT-03: 0) — this red state is the DETECT-01 deliverable, not a passing invariant
self-test: contract_pin sub-check PASSED
EXIT=0
--- python3 -O ---
(identical thirteen lines)
EXIT=0
```

**Finding.** The stayed-green baseline: on an unmutated scratch copy, every one of the thirteen
labelled self-test items PASSES under both interpreters, and `contract_pin:` reads `36 asserted
fixtures, 0 observation-only, 0 PINNED-RED carried` — the exact figure Plan 187-02 left the real
tree at. This is what every injection below is measured as a departure from.

### 3.1 INJ-1 — revert `_verdict_conforms` to its pre-DETECT-02 body

Spliced via `git show a30746d~1:scripts/check-quality-harness.py`, which recovers the
pre-DETECT-02 body (strip emphasis/whitespace/trailing punctuation, then bare-token membership in
`_VERDICT_VOCAB`), over the current body in the scratch copy only. Recovered form (unique in the
pre-fix file, spliced verbatim):

```python
def _verdict_conforms(cell: str) -> bool:
    """A Verdict cell conforms after stripping emphasis, whitespace, and trailing punctuation."""
    s = cell.strip()
    s = re.sub(r"^[*_]+", "", s)
    s = re.sub(r"[*_]+$", "", s)
    s = s.strip().rstrip(".,;:!").strip()
    return s.lower() in _VERDICT_VOCAB
```

FAIL lines (verbatim, identical under both interpreters):

```
self-test FAIL: contract_pin unregistered mismatch V-ACCEPT-EMDASH: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch V-ACCEPT-EMDASH-BOLD: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch V-CHALLENGE-EMDASH: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch V-DISCARD-EMDASH-BOLD: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch V-BARE-TOKEN: contract expects False, current code returns True
self-test FAIL: contract_pin unregistered mismatch V-BARE-TOKEN-BOLD: contract expects False, current code returns True
self-test FAIL: contract_pin unregistered mismatch V-RUBRIC-CRIT2-EMDASH: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch V-RUBRIC-CRIT2-BARE: contract expects False, current code returns True
self-test FAIL: contract_pin Guard A [mode 3: DETECTOR REGRESSION against the canonical contract] V-ACCEPT-EMDASH — the extracted text equals the pinned literal, but the detector no longer agrees with the canonical contract: expected True, observed False
self-test FAIL: contract_pin Guard A [mode 3: DETECTOR REGRESSION against the canonical contract] V-CHALLENGE-EMDASH — the extracted text equals the pinned literal, but the detector no longer agrees with the canonical contract: expected True, observed False
self-test FAIL: contract_pin Guard A [rubric mode 3: DETECTOR REGRESSION against the canonical contract] the constructed cells equal their pinned literals, but the detector no longer agrees with the canonical contract: emdash expected True observed False, bare expected False observed True
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Accept' em-dash form 'Accept — justification' does not conform but must
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Accept' bare form 'Accept' conforms but must not
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Challenge' em-dash form 'Challenge — justification' does not conform but must
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Challenge' bare form 'Challenge' conforms but must not
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Discard' em-dash form 'Discard — justification' does not conform but must
self-test FAIL: contract_pin Guard A [rubric anti-blanket-pass] token 'Discard' bare form 'Discard' conforms but must not
self-test: contract_pin sub-check FAILED
```

Also fires (pre-existing `defects` sub-check assertions, corroborating that the numeric calibration
vector distinguishes correctness even where a saturated binary flag cannot — the exact asymmetry
Phase 185 recorded for this same splice):

```
self-test FAIL: defects conformant record expected {..., 'nonconforming_verdict_cells': 0, 'verdict_flag': 0, ...}, got {..., 'nonconforming_verdict_cells': 3, 'verdict_flag': 1, ...}
self-test FAIL: defects defective record expected {..., 'nonconforming_verdict_cells': 1, ...}, got {..., 'nonconforming_verdict_cells': 3, ...}
self-test FAIL: defects one-hash-depth variant record differs from the two-hash original
self-test FAIL: defects appendix variant record differs from the no-appendix original
self-test FAIL: defects calibration nonconforming_verdict_cells vector expected [13, 8, 10, 8, 7, 15], got [13, 8, 10, 8, 7, 4]
self-test: defects sub-check FAILED
```

Stayed green (identical under both interpreters): `guardrail_a`, `guardrail_b`, `scoreline`,
`blinding`, `tabulation`, `baseline`, `run_layer`, `compare`, `limitation1_chainlabels`,
`limitation2_citationnorm`, `limitation3_extractionscope` — 11 of 13.

**Finding.** INJ-1 proves the verdict check is live in the guard (D-14 criterion 3, half 1): it
fires `V-ACCEPT-EMDASH` and `V-CHALLENGE-EMDASH` exactly as pre-measured at plan time, and — as the
plan flagged this as an observed rather than predicted figure — `V-RUBRIC-CRIT2-EMDASH` and
`V-RUBRIC-CRIT2-BARE` are also observed to fire, since both plans' fixtures dispatch through the
same reverted `_verdict_conforms`. The rubric branch's own six-check anti-blanket-pass sweep
(Plan 187-02) fires all six checks — direct evidence that `V-RUBRIC-CRIT2-BARE`'s negative is
load-bearing against exactly this reversion, corroborating Plan 187-02's own INJ-1 splice.

### 3.2 INJ-2 — re-anchor `_GT_HEAD_RE`

Single-line change in the scratch copy's `scripts/check-quality-harness.py`:
`_GT_HEAD_RE = re.compile(_GT_TOKEN_WIDE)` → `_GT_HEAD_RE = re.compile("^" + _GT_TOKEN_WIDE)`.

FAIL lines (verbatim, identical under both interpreters):

```
self-test FAIL: contract_pin Guard A [mode 3: DETECTOR REGRESSION against the canonical contract] C-RENDER-EXAMPLE-PREFIX — the extracted text equals the pinned literal, but the detector no longer agrees with the canonical contract: expected True, observed False
self-test FAIL: contract_pin Guard A [mode 3: DETECTOR REGRESSION against the canonical contract] C-RENDER-SECONDORDER-PREFIX — the extracted text equals the pinned literal, but the detector no longer agrees with the canonical contract: expected True, observed False
self-test FAIL: contract_pin unregistered mismatch C-RENDER-BACKTICK: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch C-RENDER-BLOCKQUOTE-BOLD: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch C-RENDER-EXAMPLE-PREFIX: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch C-RENDER-LIST-ITEM: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch C-RENDER-SECONDORDER-PREFIX: contract expects True, current code returns False
self-test FAIL: contract_pin unregistered mismatch C-WRAP-BULLETED: contract expects True, current code returns False
self-test: contract_pin sub-check FAILED
self-test FAIL: defects calibration malformed_chain_blocks vector expected [2, 2, 2, 2, 3, 3], got [5, 2, 3, 3, 3, 5]
self-test: defects sub-check FAILED
```

Stayed green (identical under both interpreters): `guardrail_a`, `guardrail_b`, `scoreline`,
`blinding`, `tabulation`, `baseline`, `run_layer`, `compare`, `limitation1_chainlabels`,
`limitation2_citationnorm`, `limitation3_extractionscope` — 11 of 13.

**Finding.** INJ-2 proves the chain check is live in the guard (D-14 criterion 3, half 2): it fires
`C-RENDER-EXAMPLE-PREFIX` and `C-RENDER-SECONDORDER-PREFIX`'s mode-3 DETECTOR REGRESSION lines
exactly as pre-measured, and — matching the plan's explicit prediction — does **not** name
`C-TEMPLATE-C1`, which flips under neither this injection nor INJ-1. The calibration vector's
numeric excursion `[5, 2, 3, 3, 3, 5]` reproduces the historical `37fea87` regression Phase 184
independently bisected, corroborating this milestone's repeatedly-cited discriminating asymmetry
(numeric vector fires while `chain_flag` alone would have stayed saturated).

### 3.3 INJ-3 — mutate the template's C1 example

In the scratch copy's `shared/spine/references/output-template.md`, the wording inside the C1
block was changed while the `### Conclusion C1:` heading line was left intact: the final arrow
line `→ [conclusion — the claim this chain establishes]` was changed to
`→ [conclusion — the claim this chain PROVES-MUTATED]`.

FAIL line (verbatim, identical under both interpreters):

```
self-test FAIL: contract_pin Guard A [mode 2: extraction mismatch] C-TEMPLATE-C1: the template's example changed and the fixture literal needs updating
self-test: contract_pin sub-check FAILED
```

Stayed green (identical under both interpreters): `guardrail_a`, `guardrail_b`, `scoreline`,
`blinding`, `tabulation`, `baseline`, `defects`, `run_layer`, `compare`,
`limitation1_chainlabels`, `limitation2_citationnorm`, `limitation3_extractionscope` — 12 of 13.
Notably `defects` itself stays PASSED here, unlike INJ-1/INJ-2 — this mutation is confined to the
C1 example's wording, which the `defects` sub-check's own fixed conformant/defective/calibration
records do not exercise.

**Finding.** INJ-3 proves the extraction genuinely tracks the file rather than a copy: mutating
only the scratch copy's template (never the tracked tree) produces a FAIL naming `C-TEMPLATE-C1`
specifically, and the substring-discrimination measurement in section 4 below shows this is the one
injection whose old, weak substring-only check would ALSO have caught it — INJ-3 alone does not
discriminate runtime extraction from a faithful copy.

### 3.4 INJ-4 — delete the anchor label

The anchor label `**Chain format:**\n` (immediately preceding the ` ```text ` fence) was deleted
from the scratch copy's `shared/spine/references/output-template.md`, leaving the fenced block
itself — `GT-N + GT-M → [intermediate claim] → [conclusion]` — in place.

FAIL line (verbatim, identical under both interpreters):

```
self-test FAIL: contract_pin Guard A [mode 1: anchor unresolved] C-TEMPLATE-FORMAT: anchor '**Chain format:**' in shared/spine/references/output-template.md did not resolve (label matched 0 times (need exactly 1)) — remedy: re-anchor the guard
self-test: contract_pin sub-check FAILED
```

Stayed green (identical under both interpreters): `guardrail_a`, `guardrail_b`, `scoreline`,
`blinding`, `tabulation`, `baseline`, `defects`, `run_layer`, `compare`,
`limitation1_chainlabels`, `limitation2_citationnorm`, `limitation3_extractionscope` — 12 of 13.

**Finding.** INJ-4 proves the D-10 hard-FAIL path actually fires: with the anchor gone but the
fenced block's literal text still physically present in the file, the guard names the specific
anchor and file and states the `re-anchor the guard` remedy — no fallback to the substring check it
replaced, and no silent pass. Section 4 below records the substring measurement that makes this the
discriminating injection D-11 needs: unlike INJ-3, the old check would have stayed GREEN here.

### 3.5 INJ-5 — mutate the rubric's vocabulary list

In the scratch copy's `shared/spine/references/validation-rubric.md`, Criterion 2's vocabulary
phrase was changed from `records Accept, Challenge, or Discard as a leading token` to
`records Accept, Challenge, or Reject as a leading token`.

FAIL line (verbatim, identical under both interpreters):

```
self-test FAIL: contract_pin Guard A [rubric vocabulary mismatch] validation-rubric.md Criterion 2's derived vocabulary ('accept', 'challenge', 'reject') and _VERDICT_VOCAB ('accept', 'challenge', 'discard') have diverged
self-test: contract_pin sub-check FAILED
```

Stayed green (identical under both interpreters): `guardrail_a`, `guardrail_b`, `scoreline`,
`blinding`, `tabulation`, `baseline`, `defects`, `run_layer`, `compare`,
`limitation1_chainlabels`, `limitation2_citationnorm`, `limitation3_extractionscope` — 12 of 13.

**Finding.** INJ-5 proves the D-07 derived Criterion 2 fixture tracks the rubric: the FAIL line
carries both tuples — the vocabulary derived from the mutated rubric text
(`('accept', 'challenge', 'reject')`) and the hand-maintained `_VERDICT_VOCAB`
(`('accept', 'challenge', 'discard')`) — so a rubric edit that silently drifted the vocabulary away
from the harness's own constant is caught rather than passing unnoticed.

## 4. What the substring check would and would not have caught

D-11's claim is that the strengthened guard's equality check is strictly stronger than the weak
substring-only check it replaces (`fx.text in source_text`). Both INJ-3 and INJ-4 were measured
directly against this predicate on the MUTATED scratch source, not assumed:

| Injection | Fixture | Original literal still a substring of the mutated file? | Substring check would have... |
|---|---|---|---|
| 3 (`INJ-3`) | `C-TEMPLATE-C1` | `False` (measured) | FAILED too — does not discriminate |
| 4 (`INJ-4`) | `C-TEMPLATE-FORMAT` | `True` (measured) | stayed GREEN — this is the discriminating row |

Both values match the plan's pre-registered expectation exactly (`False` for INJ-3, `True` for
INJ-4); neither observation diverged from the prediction.

**INJ-3 alone does not discriminate extraction from copying.** Mutating the C1 block's wording
necessarily removes the fixture's literal text from the file altogether — `C-TEMPLATE-C1`'s
pinned literal is no longer present anywhere in the mutated `output-template.md`, so even the
old, weak `fx.text in source_text` substring check would have failed on this exact mutation. INJ-3
proves the guard notices a template change; it does not by itself prove the guard is doing anything
the old check could not already do.

**INJ-4 is the row that does discriminate.** Deleting the anchor label `**Chain format:**` leaves
the fenced block's own text — `GT-N + GT-M → [intermediate claim] → [conclusion]`, `C-TEMPLATE-FORMAT`'s
full pinned literal — physically present and unchanged elsewhere in the mutated file. The old
substring check (`fx.text in source_text`) would therefore have stayed GREEN on this exact mutation,
because "is the literal present somewhere in the file" says nothing about whether the *structural
anchor* that is supposed to locate it still resolves. The strengthened guard's anchor-resolve step
fails first, before equality or detector-verdict is ever checked — that asymmetry (INJ-3 caught by
both checks, INJ-4 caught only by the new one) is the direct, measured evidence that equality-via-a-
resolved-anchor is strictly stronger than the old bare substring check, not merely a different way
of expressing the same guarantee.

## 5. Nothing tracked was mutated

Confirmed after the full twelve-run matrix, against the real tracked tree (not any scratch copy):

```
$ git status --porcelain shared/ first-principles/
(empty)

$ git status --porcelain -- tests/
(empty)

$ git diff --quiet -- tests/step0-baseline-v*.md tests/step0-captures-v* tests/routing-baseline-v3.*.md tests/routing-battery-baseline-v4.3.md tests/routing-baseline-v7.11.md tests/routing-battery-baseline-v7.11.md tests/focused-output-baseline-v*.md tests/sub-skill-routing-baseline-v*.md tests/quality-catalog-v8.7.md tests/quality-probe-v8.7 tests/quality-baseline-v8.7-regenerated tests/quality-baseline-v8.7 tests/quality-baseline-v8.7-postfix; echo $?
0

$ ls -d /tmp/detect06-* 2>/dev/null | wc -l
0

$ python3 -c "import ast;print(sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(open('scripts/check-quality-harness.py').read()))))"
0

$ python3 scripts/check-quality-harness.py --self-test 2>&1 | grep -c "sub-check PASSED"
13

$ python3 scripts/check-quality-harness.py --self-test >/dev/null 2>&1; echo $?
0

$ bash scripts/check-firewall-battery.sh 2>&1 | tail -3
[PASS] FROZEN-EVIDENCE  git diff --quiet: frozen baselines/captures unmodified (D-04)

FIREWALL: GREEN (16/16)
```

Every scratch directory created during this matrix (`/tmp/detect06-hPs9Lm`, `/tmp/detect06-qO3asn`,
`/tmp/detect06-GUVOr9`, `/tmp/detect06-AQV8TN`, `/tmp/detect06-fhb2Ic`, `/tmp/detect06-MJlVDP`,
`/tmp/detect06-Ko6zWN`) was removed with `rm -rf` immediately after its runs — none remains.

**Attribution.** Only the fired status of the five named injections (INJ-1 through INJ-5) and the
CTRL stayed-green baseline, as recorded in sections 3 and 4 above, is attributed to DETECT-06 in
this file. This guard covers the seven enumerated template fixtures and the two rubric-derived
Criterion 2 fixtures — an example added to `output-template.md` later is not automatically covered
by this guard (D-04's in-source coverage-limit comment states the same limit beside
`_CONTRACT_EXTRACTION_TABLE`). D-01 is the standing evidence that this gap is real: two template
examples (`C-RENDER-EXAMPLE-PREFIX`, `C-RENDER-SECONDORDER-PREFIX`) were added to
`_CONTRACT_FIXTURES` after `tests/detect01-red-run-v8.13.md` §10 pre-registered its five-fixture
succession list, and nothing noticed until this phase's own live enumeration caught it. This file
does not claim the coverage gap is closed — only that the guard fires correctly, by fault
injection, on the fixtures it does cover.
