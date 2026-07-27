# DETECT-01 Red Run — v8.13 Phase 182

This file is the recorded, git-tracked red run required by DETECT-01 criterion 4. It matches
none of the FROZEN-EVIDENCE globs (`tests/step0-baseline-v*.md`, `tests/step0-captures-v*`,
`tests/routing-baseline-v3.*.md`, `tests/routing-battery-baseline-v4.3.md`,
`tests/routing-baseline-v7.11.md`, `tests/routing-battery-baseline-v7.11.md`,
`tests/focused-output-baseline-v*.md`, `tests/sub-skill-routing-baseline-v*.md`,
`tests/quality-catalog-v8.7.md`, `tests/quality-probe-v8.7`,
`tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7`,
`tests/quality-baseline-v8.7-postfix`), so it can be added without touching a frozen path.

All file paths in this document are given in inline code, never as a markdown link, so no link
gate can ever be tripped by this record.

## 1. What this is and why it exists

Two of the three D-18 contract checks in `scripts/check-quality-harness.py`
(`_verdict_conforms` and `_chain_block_well_formed`) are inverted against the canonical output
contract: `shared/spine/references/output-template.md` and
`shared/spine/references/validation-rubric.md` Criterion 2 both prescribe a Verdict token
followed by an em-dash and a justification, and the rubric names the bare token alone as the
defect, yet `_verdict_conforms` accepts only the bare token; separately, `_chain_block_well_formed`
matches per physical line, so the output template's own canonical multi-line Conclusion-chain
worked example fails the very detector built to check conformance to it. DETECT-01 encoded these
two mismatches as thirteen pre-registered fixtures (plus three observation-only rows) and pinned
nine of the thirteen as a deliberate, named red state — carried until DETECT-02 and DETECT-03
land — before any production line was touched. Criterion 4 requires this failure to be recorded,
not merely asserted: an assertion nobody has seen fail is an assumption, and a red run nobody
wrote down is not evidence. This file is that failure, written down.

## 2. Provenance

- **Base commit SHA the run was produced against:** `e1546769cc29d349bbc5291a228323e4a8850d88`
  (short `e154676`, Plan 182-01's final commit — the tree state in which
  `_CONTRACT_FIXTURES` / `_DETECT01_PINNED_RED` / `_selftest_contract_pin` /
  `contract_pin_strict_report` first exist and against which every run recorded in this file was
  produced). The phase's own pre-phase baseline, against which byte-identity of the two
  production functions is proven, is commit `6eca780` (`docs: scope the D-18 detector contract
  fix`) — see section 8.
- **Pin-hash value:** `5 8ecbaee0882c8f02f0760de8377db53720b1fb108951d0cb737e797f8b902add`
- **Pin-hash command** (covers `_verdict_conforms`, `_chain_block_well_formed`,
  `_VERDICT_VOCAB`, `_ARROW`, `_CHAIN_FORM_LINE_RE` — the five production symbols this phase is
  forbidden to touch):
  ```
  python3 -c 'import ast,hashlib,sys;src=open(sys.argv[1],encoding="utf-8").read();t=ast.parse(src);N={"_verdict_conforms","_chain_block_well_formed"};C={"_VERDICT_VOCAB","_ARROW","_CHAIN_FORM_LINE_RE"};s=[ast.get_source_segment(src,n) for n in t.body if (isinstance(n,ast.FunctionDef) and n.name in N) or (isinstance(n,ast.Assign) and any(getattr(x,"id","") in C for x in n.targets))];print(len(s),hashlib.sha256("\n".join(s).encode()).hexdigest())' scripts/check-quality-harness.py
  ```
- **`python3 --version`:** `Python 3.13.5`
- **`uname -srm`:** `Linux 6.12.57+deb13-amd64 x86_64`
- **Run date:** 2026-07-27

## 3. Pre-registered expectation table

All sixteen rows from Plan 182-01's pre-registration (measured 2026-07-27 against commit
`6eca780`), re-measured during this plan's execution against the live functions at commit
`e154676`.

| id | kind | contract | observed | state | owner | source |
|----|------|----------|----------|-------|-------|--------|
| `V-ACCEPT-EMDASH` | verdict | True | False | RED | DETECT-02 | `output-template.md` line 69, verbatim |
| `V-ACCEPT-EMDASH-BOLD` | verdict | True | False | RED | DETECT-02 | line 69 text wrapped in `**` (criterion 1 "with bold emphasis") |
| `V-CHALLENGE-EMDASH` | verdict | True | False | RED | DETECT-02 | `output-template.md` line 70, verbatim |
| `V-DISCARD-EMDASH-BOLD` | verdict | True | False | RED | DETECT-02 | line 71 text wrapped in `**` |
| `V-BARE-TOKEN` | verdict | False | True | RED | DETECT-02 | rubric Criterion 2's named defect; the `Q-P2-run1` cell shape |
| `V-BARE-TOKEN-BOLD` | verdict | False | True | RED | DETECT-02 | the `Q-P2-run1` bolded cell shape |
| `V-OBS-ENDASH` | verdict | None | False | OBSERVE | DETECT-02 | en-dash separator — DETECT-02 must decide and document |
| `V-OBS-HYPHEN` | verdict | None | False | OBSERVE | DETECT-02 | hyphen separator — DETECT-02 must decide and document |
| `V-OBS-EMPTY-AFTER-DASH` | verdict | None | False | OBSERVE | DETECT-02 | justification empty after the dash — DETECT-02 must decide and document |
| `C-TEMPLATE-C1` | chain | True | False | RED | DETECT-03 | `output-template.md` lines 133-137, verbatim (criterion 3) |
| `C-TEMPLATE-FORMAT` | chain | True | False | RED | DETECT-03 | `output-template.md` line 108 chain-format block, verbatim |
| `C-MULTILINE-DIGITS` | chain | True | False | RED | DETECT-03 | constructed three-line chain in the template's shape |
| `C-TEMPLATE-TRADEOFF` | chain | True | True | GREEN-GUARD | — | `output-template.md` line 123, verbatim |
| `C-SINGLE-LINE` | chain | True | True | GREEN-GUARD | — | constructed; Phase 184 criterion 4 (single-line form must survive) |
| `C-NO-INTERMEDIATE` | chain | False | False | GREEN-GUARD | — | constructed negative; Phase 184 criterion 3 (no blanket pass) |
| `C-NO-INTERMEDIATE-MULTILINE` | chain | False | False | GREEN-GUARD | — | constructed negative; the blanket-pass sentinel a block-level matcher is most likely to break |

**Agreement:** every row's executed measurement agrees with Plan 182-01's pre-registration row
for row, exactly — no disagreement found, no finding to report.

Totals: **13 asserted** (6 verdict + 7 chain), **3 observation-only**, **9 PINNED-RED**
(6 → DETECT-02, 3 → DETECT-03), **4 GREEN-GUARD**.

## 4. Criterion 4 and the four GREEN-GUARD rows — unsoftened

Criterion 4 reads "every new test fails against unmodified `check-quality-harness.py`". Stated
plainly and without softening: **nine of the thirteen asserted fixtures fail today; four do
not.** The four that do not fail (`C-TEMPLATE-TRADEOFF`, `C-SINGLE-LINE`, `C-NO-INTERMEDIATE`,
`C-NO-INTERMEDIATE-MULTILINE`) are not pins and are not a shortfall against criterion 4 — they
are the negative and single-line guards that criterion 2 and Phase 184 criteria 3/4 explicitly
require to exist. Their job is to **fail after Phase 184** if the block-level fix DETECT-03
prescribes becomes a blanket pass (accepting a chain with no intermediate claim) or breaks the
single-line form Phase 184 criterion 4 requires to keep passing. No fixture was omitted from the
count and no fixture was downgraded to make the "nine of thirteen" figure tidier than it is.

## 5. The red run, verbatim

### Strict-mode reproduction command

```
python3 -c "import importlib.util as u, sys; \
s = u.spec_from_file_location('qh', 'scripts/check-quality-harness.py'); \
mm = u.module_from_spec(s); sys.modules['qh'] = mm; s.loader.exec_module(mm); \
sys.exit(mm.contract_pin_strict_report())"
```

### `python3` (exit code 1)

```
contract_pin STRICT-FAIL [DETECT-02] V-ACCEPT-EMDASH: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-ACCEPT-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-CHALLENGE-EMDASH: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-DISCARD-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-BARE-TOKEN: contract expects False, current code returns True — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-BARE-TOKEN-BOLD: contract expects False, current code returns True — carried until DETECT-02
contract_pin AXES C-TEMPLATE-C1: MULTILINE, NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-C1: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-TEMPLATE-FORMAT: NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-FORMAT: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-MULTILINE-DIGITS: MULTILINE
contract_pin STRICT-FAIL [DETECT-03] C-MULTILINE-DIGITS: contract expects True, current code returns False — carried until DETECT-03
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-ENDASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-HYPHEN: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-EMPTY-AFTER-DASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin: 13 asserted fixtures, 3 observation-only, 9 PINNED-RED carried (DETECT-02: 6, DETECT-03: 3) — this red state is the DETECT-01 deliverable, not a passing invariant
```

Exit code: **1**. Nine `STRICT-FAIL` lines, exactly matching the nine PINNED-RED rows in section 3.

### `python3 -O` (exit code 1)

```
contract_pin STRICT-FAIL [DETECT-02] V-ACCEPT-EMDASH: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-ACCEPT-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-CHALLENGE-EMDASH: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-DISCARD-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-BARE-TOKEN: contract expects False, current code returns True — carried until DETECT-02
contract_pin STRICT-FAIL [DETECT-02] V-BARE-TOKEN-BOLD: contract expects False, current code returns True — carried until DETECT-02
contract_pin AXES C-TEMPLATE-C1: MULTILINE, NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-C1: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-TEMPLATE-FORMAT: NON-NUMERIC-GT
contract_pin STRICT-FAIL [DETECT-03] C-TEMPLATE-FORMAT: contract expects True, current code returns False — carried until DETECT-03
contract_pin AXES C-MULTILINE-DIGITS: MULTILINE
contract_pin STRICT-FAIL [DETECT-03] C-MULTILINE-DIGITS: contract expects True, current code returns False — carried until DETECT-03
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-ENDASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-HYPHEN: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-EMPTY-AFTER-DASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin: 13 asserted fixtures, 3 observation-only, 9 PINNED-RED carried (DETECT-02: 6, DETECT-03: 3) — this red state is the DETECT-01 deliverable, not a passing invariant
```

Exit code: **1**. Byte-identical to the `python3` run — proof this is not a stripped-assertion
artifact of `-O`; the new code contains zero `assert` statements (see section 7).

### Default-mode gate run — `python3 scripts/check-quality-harness.py --self-test` (exit code 0)

stdout:

```
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
contract_pin: 13 asserted fixtures, 3 observation-only, 9 PINNED-RED carried (DETECT-02: 6, DETECT-03: 3) — this red state is the DETECT-01 deliverable, not a passing invariant
self-test: contract_pin sub-check PASSED
```

stderr:

```
contract_pin PINNED-RED [DETECT-02] V-ACCEPT-EMDASH: contract expects True, current code returns False — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; this entry is removed once it accepts the token-prefix + em-dash + justification form the template and rubric prescribe.
contract_pin PINNED-RED [DETECT-02] V-ACCEPT-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; removed once the bolded token-prefix + em-dash + justification form is accepted.
contract_pin PINNED-RED [DETECT-02] V-CHALLENGE-EMDASH: contract expects True, current code returns False — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; removed once the Challenge token-prefix + em-dash + justification form is accepted.
contract_pin PINNED-RED [DETECT-02] V-DISCARD-EMDASH-BOLD: contract expects True, current code returns False — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; removed once the bolded Discard token-prefix + em-dash + justification form is accepted.
contract_pin PINNED-RED [DETECT-02] V-BARE-TOKEN: contract expects False, current code returns True — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; removed once the bare token alone is correctly rejected.
contract_pin PINNED-RED [DETECT-02] V-BARE-TOKEN-BOLD: contract expects False, current code returns True — carried until DETECT-02
DETECT-02 owns `_verdict_conforms`; removed once the bolded bare token alone is correctly rejected.
contract_pin AXES C-TEMPLATE-C1: MULTILINE, NON-NUMERIC-GT
contract_pin PINNED-RED [DETECT-03] C-TEMPLATE-C1: contract expects True, current code returns False — carried until DETECT-03
DETECT-03 owns `_chain_block_well_formed`; removed once the template's own canonical multi-line worked example is accepted (also requires a decision on placeholder GT identifiers — see this plan's two-axis finding).
contract_pin AXES C-TEMPLATE-FORMAT: NON-NUMERIC-GT
contract_pin PINNED-RED [DETECT-03] C-TEMPLATE-FORMAT: contract expects True, current code returns False — carried until DETECT-03
DETECT-03 owns `_chain_block_well_formed`; removed once the placeholder GT identifier form (`GT-N`/`GT-M`) is accepted.
contract_pin AXES C-MULTILINE-DIGITS: MULTILINE
contract_pin PINNED-RED [DETECT-03] C-MULTILINE-DIGITS: contract expects True, current code returns False — carried until DETECT-03
DETECT-03 owns `_chain_block_well_formed`; removed once a multi-line chain block is matched at the block level.
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-ENDASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-HYPHEN: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
contract_pin OBSERVED [DETECT-02 undecided] V-OBS-EMPTY-AFTER-DASH: current code returns False — no contract expectation asserted; DETECT-02 must decide and document
```

Exit code: **0**. The same nine violations that fail strict mode are reported here as
`PINNED-RED` (tolerated because each is registered in `_DETECT01_PINNED_RED`), while the gate
itself stays green — the deliberate carry mechanism working as designed.

## 6. Two failure axes on the chain side

Two independent axes can each make a chain block fail `_chain_block_well_formed`'s per-line
match: **MULTILINE** (the prescribed form is matched per physical line, so a chain spread across
several lines fails even though the joined text would match) and **NON-NUMERIC-GT**
(`_CHAIN_FORM_LINE_RE` requires `GT-\d+`, so a document using placeholder identifiers like
`GT-N`/`GT-M` fails on a second, independent axis even when joined onto one line).

| fixture | per-line | joined | per-line, digits substituted | joined, digits substituted | axes |
|---------|----------|--------|------------------------------|------------------------------|------|
| `C-TEMPLATE-C1` | False | False | False | True | MULTILINE + NON-NUMERIC-GT |
| `C-TEMPLATE-FORMAT` | False | False | True | True | NON-NUMERIC-GT only |
| `C-MULTILINE-DIGITS` | False | True | False | True | MULTILINE only |

**Consequence:** the block-level match DETECT-03 prescribes is **necessary but not sufficient**
to make the verbatim template example (`C-TEMPLATE-C1`) pass. Phase 184's criterion 2 ("Phase
182's chain tests pass, including the template's own canonical example") therefore also requires
a decision on placeholder GT identifiers, not just a block-level rewrite of the matcher. Phase
182 characterises this finding; it does not decide it. This same necessary-but-not-sufficient
finding recurs as a gate blind spot in section 9 — the two sections cross-reference each other.

## 7. Fault-injection log

Ten lines, all `exit=1 matched=yes` — five failure paths, each exercised under both `python3` and
`python3 -O`, because a self-test whose only failure path is a bare `assert` is stripped under
`-O` and prints PASS while proving nothing. The new contract-pin code (`ContractFixture`,
`_contract_fixture_result`, `_chain_failure_axes`, `_selftest_contract_pin`,
`contract_pin_strict_report`) contains **zero `assert` statements**, checked at the AST level by
the existing `guardrail_a`/`guardrail_b` self-test items' pattern and confirmed here by direct
`python3 -O` execution producing byte-identical strict output to plain `python3` (section 5).

```
FI-1 py exit=1 matched=yes
FI-1 py-O exit=1 matched=yes
FI-2 py exit=1 matched=yes
FI-2 py-O exit=1 matched=yes
FI-3 py exit=1 matched=yes
FI-3 py-O exit=1 matched=yes
FI-4 py exit=1 matched=yes
FI-4 py-O exit=1 matched=yes
FI-5 py exit=1 matched=yes
FI-5 py-O exit=1 matched=yes
```

Per-path detail:

1. **FI-1 (unregistered mismatch):** deleted the `V-BARE-TOKEN` entry from
   `_DETECT01_PINNED_RED`. Matched stderr: `self-test FAIL: contract_pin unregistered mismatch
   V-BARE-TOKEN: contract expects False, current code returns True`.
2. **FI-2 (stale pin — the load-bearing path Phase 183 and Phase 184 will trip):** added a
   registry entry `"C-SINGLE-LINE": "fault injection re-proof — DETECT-03"` for a fixture that
   already matches its contract. Matched stderr: `self-test FAIL: contract_pin STALE PIN
   C-SINGLE-LINE — DETECT-03 has corrected the check; delete this entry from
   _DETECT01_PINNED_RED and let the fixture assert normally`.
3. **FI-3 (verbatim drift, Guard A):** changed `C-TEMPLATE-C1`'s leading `Conclusion C1` to
   `Conclusion C9`, breaking its literal-substring match against
   `shared/spine/references/output-template.md`. Matched stderr: `self-test FAIL: contract_pin
   Guard A C-TEMPLATE-C1 text is not a literal substring of
   shared/spine/references/output-template.md — verbatim lift drifted`.
4. **FI-4 (registry drift, Guard B):** added a registry entry keyed
   `"X-NONEXISTENT-FIXTURE"`, an id that names no fixture in `_CONTRACT_FIXTURES`. Matched
   stderr: `self-test FAIL: contract_pin Guard B unregistered fixture id in
   _DETECT01_PINNED_RED: X-NONEXISTENT-FIXTURE`.
5. **FI-5 (owner whitelist, Guard C):** changed the `V-BARE-TOKEN` registry reason string to
   "fault injection re-proof — mentions neither owner requirement", naming neither DETECT-02 nor
   DETECT-03. Matched stderr: `self-test FAIL: contract_pin Guard C reason for V-BARE-TOKEN names
   neither DETECT-02 nor DETECT-03`.

Every injection was reverted immediately after capture with `git checkout --
scripts/check-quality-harness.py`, under `set +e` with a `trap 'git checkout --
scripts/check-quality-harness.py' EXIT` installed before the injection so the revert runs on
every exit path including an abort, and the revert was proven each time by `git diff --quiet --
scripts/check-quality-harness.py` exiting 0 and the self-test exiting 0 again under both
interpreters. The FI-2 stale-pin path was independently re-proven a second time in this plan's
own `<verify>` block (Task 1), with the same discipline, immediately before this file was
written.

## 8. Byte-identity proof

- **Pin-hash, pre-phase base (commit `6eca780`):**
  `5 8ecbaee0882c8f02f0760de8377db53720b1fb108951d0cb737e797f8b902add`
- **Pin-hash, post-phase tree (commit `e154676` and unchanged through this plan):**
  `5 8ecbaee0882c8f02f0760de8377db53720b1fb108951d0cb737e797f8b902add`

Identical. Command (repeated from section 2):

```
python3 -c 'import ast,hashlib,sys;src=open(sys.argv[1],encoding="utf-8").read();t=ast.parse(src);N={"_verdict_conforms","_chain_block_well_formed"};C={"_VERDICT_VOCAB","_ARROW","_CHAIN_FORM_LINE_RE"};s=[ast.get_source_segment(src,n) for n in t.body if (isinstance(n,ast.FunctionDef) and n.name in N) or (isinstance(n,ast.Assign) and any(getattr(x,"id","") in C for x in n.targets))];print(len(s),hashlib.sha256("\n".join(s).encode()).hexdigest())' scripts/check-quality-harness.py
```

`git diff --stat 6eca780 -- scripts/check-quality-harness.py`:

```
scripts/check-quality-harness.py | 618 ++++++++++++++++++++++++++++++++++++++-
1 file changed, 614 insertions(+), 4 deletions(-)
```

The additions are confined to the new `ContractFixture` dataclass, `_CONTRACT_FIXTURES`,
`_DETECT01_PINNED_RED`, `_chain_failure_axes`, `_contract_fixture_result`,
`_selftest_contract_pin`, `contract_pin_strict_report`, and the item-13 self-test dispatch plus
its docstring correction inside `self_test()` — no line of `_verdict_conforms`,
`_chain_block_well_formed`, `_VERDICT_VOCAB`, `_ARROW`, or `_CHAIN_FORM_LINE_RE` changed, which
is exactly what the unchanged pin-hash proves mechanically.

## 9. Removal protocol, and what the forcing function does not catch

| fixture id | owning requirement | phase that deletes the entry |
|------------|--------------------|-------------------------------|
| `V-ACCEPT-EMDASH` | DETECT-02 | Phase 183 |
| `V-ACCEPT-EMDASH-BOLD` | DETECT-02 | Phase 183 |
| `V-CHALLENGE-EMDASH` | DETECT-02 | Phase 183 |
| `V-DISCARD-EMDASH-BOLD` | DETECT-02 | Phase 183 |
| `V-BARE-TOKEN` | DETECT-02 | Phase 183 |
| `V-BARE-TOKEN-BOLD` | DETECT-02 | Phase 183 |
| `C-TEMPLATE-C1` | DETECT-03 | Phase 184 |
| `C-TEMPLATE-FORMAT` | DETECT-03 | Phase 184 |
| `C-MULTILINE-DIGITS` | DETECT-03 | Phase 184 |

The six verdict ids are deleted by DETECT-02 in Phase 183; the three chain ids are deleted by
DETECT-03 in Phase 184. Leaving an entry in place after its owning requirement lands makes
QUAL-01 fail as a **STALE PIN** — the mechanical forcing function proven in section 7, FI-2 —
so the carry cannot silently outlive its reason.

That forcing function has two honest limits, stated here with equal prominence, not only the
second.

**First limit — STALE PIN detects a complete fix, not a partial one.** It fires only when a
pinned fixture's result flips to match its `expected` value. A **partial** correction leaves the
not-yet-flipped entries **validly** pinned, no STALE PIN fires, and QUAL-01 stays green on a
half-corrected check. Two concrete cases: a `_verdict_conforms` that starts accepting `Accept —
justification` while still accepting the bare token leaves `V-BARE-TOKEN` (expected `False`)
legitimately pinned and the gate green; and a `_chain_block_well_formed` that gains the
block-level match without a decision on placeholder GT identifiers leaves `C-TEMPLATE-C1`
legitimately pinned and the gate green — which is section 6's necessary-but-not-sufficient
finding arriving here as a gate blind spot, so the two sections must be read together. Name the
countermeasure explicitly: **`contract_pin_strict_report()` exiting 0 is the completeness check,
and Phase 183 and Phase 184 MUST run it** — it is the only signal that says an owner's red is
fully gone. A green QUAL-01 while `_DETECT01_PINNED_RED` is non-empty means "the carried red is
still carried", never "the contract holds".

**Second limit — ownership claims are made visible, not prevented.** The registry's reason
strings are restricted to DETECT-02 and DETECT-03 (Guard C) so the registry cannot be repurposed
to silence an unrelated regression, but the residual risk is a reviewer accepting a false
ownership claim inside a diff, which the mechanism surfaces (the reason string is right there to
read) and cannot itself stop.

## 10. Succession

DETECT-06 (Phase 187) replaces the four verbatim fixture copies (`V-ACCEPT-EMDASH`,
`V-CHALLENGE-EMDASH`, `C-TEMPLATE-C1`, `C-TEMPLATE-FORMAT`, and `C-TEMPLATE-TRADEOFF`) with
runtime extraction from `shared/spine/references/output-template.md` and adds the rubric's
Criterion 2 Verdict form sourced the same way from
`shared/spine/references/validation-rubric.md`. The literal-substring Guard A written here
(section 7, FI-3) is the **weak form** of that guard — it proves today's copy is faithful, but a
copy can still drift from its source between phases. Phase 187 makes the fixture track the
template at run time rather than a copy that must be kept in sync by hand.
