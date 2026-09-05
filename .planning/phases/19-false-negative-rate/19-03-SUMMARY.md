---
phase: 19-false-negative-rate
plan: 03
subsystem: adversarial-corpus
tags: [testing, quality-harness, stratum-a, false-negative-rate]
dependency-graph:
  requires: []
  provides:
    - "tests/adversarial-corpus-v9.0/t03-composition-cycle.md"
    - "tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md"
    - "tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md"
    - "tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md"
    - "tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md"
  affects:
    - "plan 19-04 (catalog.md dispositions for t03/t04/t05/t06/t13)"
tech-stack:
  added: []
  patterns:
    - "GAP-6 composition chain heads (GT-n (label) + Cm (label) -> ... -> ...) to reach dependency_cycles/ungrounded_chains"
    - "Self-Audit Gate block placed after all of section 6's prose to avoid truncating conclusion_claims"
key-files:
  created:
    - tests/adversarial-corpus-v9.0/t03-composition-cycle.md
    - tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md
    - tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md
    - tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md
    - tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md
  modified: []
decisions: []
metrics:
  duration: "~55 minutes"
  completed: "2026-09-05"
---

# Phase 19 Plan 03: Stratum-A corpus items (dependency_cycles / ungrounded_chains / selfaudit_disagreements) Summary

Five hand-authored stratum-A corpus items aimed at the three `detect_defects` columns with
substantive reach — `dependency_cycles`, `ungrounded_chains`, `selfaudit_disagreements` — three
positive controls proving the columns are reachable, one genuine detector miss, and one disclosed
grounding-short-circuit bound, all measured against the unmodified CONTRACT-06-frozen harness.

## What Was Built

Five full six-section analyses under `tests/adversarial-corpus-v9.0/`, each form-clean
(`untraced_claims == 0`, `nonconforming_verdict_cells == 0`, `malformed_chain_blocks == 0`) and
each carrying a real derivation-graph or self-audit falsehood the three form checks cannot see.
No file under `shared/`, `first-principles/`, `scripts/` or `docs/` was touched. Verified by
running `scripts/check-quality-harness.py`'s unmodified `detect_defects` from a scratchpad
measurement script (never committed), plus `scripts/report-conformance.py --check` and
`bash scripts/check-firewall-battery.sh`.

## Measurement output — verbatim, all five items together

```
t03-composition-cycle.md {'conclusion_claims': 2, 'untraced_claims': 0, 'verdict_cells': 2, 'nonconforming_verdict_cells': 0, 'chain_blocks': 2, 'malformed_chain_blocks': 0, 'dependency_cycles': 2, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
  _dependency_cycles: ['c1', 'c2']
  _ungrounded_chains: []
  _selfaudit_disagreements: []
t04-chain-only-head-ungrounded.md {'conclusion_claims': 2, 'untraced_claims': 0, 'verdict_cells': 2, 'nonconforming_verdict_cells': 0, 'chain_blocks': 2, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 2, 'selfaudit_disagreements': 0}
  _dependency_cycles: []
  _ungrounded_chains: ['c1', 'c2']
  _selfaudit_disagreements: []
t05-selfaudit-overclaim-under-cycle.md {'conclusion_claims': 2, 'untraced_claims': 0, 'verdict_cells': 2, 'nonconforming_verdict_cells': 0, 'chain_blocks': 2, 'malformed_chain_blocks': 0, 'dependency_cycles': 2, 'ungrounded_chains': 0, 'selfaudit_disagreements': 1}
  _dependency_cycles: ['c1', 'c2']
  _ungrounded_chains: []
  _selfaudit_disagreements: [{'criterion': 4, 'claimed': 'Rigorous', 'contradicted_by': '_dependency_cycles', 'measured': 2}]
t06-hidden-cycle-past-head.md {'conclusion_claims': 2, 'untraced_claims': 0, 'verdict_cells': 2, 'nonconforming_verdict_cells': 0, 'chain_blocks': 2, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
  _dependency_cycles: []
  _ungrounded_chains: []
  _selfaudit_disagreements: []
t13-grounded-alongside-cyclic-ref.md {'conclusion_claims': 2, 'untraced_claims': 0, 'verdict_cells': 2, 'nonconforming_verdict_cells': 0, 'chain_blocks': 3, 'malformed_chain_blocks': 0, 'dependency_cycles': 2, 'ungrounded_chains': 2, 'selfaudit_disagreements': 0}
  _dependency_cycles: ['c2', 'c3']
  _ungrounded_chains: ['c2', 'c3']
  _selfaudit_disagreements: []
```

No file printed `UNREADABLE` — `_slice_sections` resolved all six sections on every item. All
three form counts (`untraced_claims`, `nonconforming_verdict_cells`, `malformed_chain_blocks`)
are 0 on every item, satisfying CONF-07's form precondition.

## Per-item disposition

### t03-composition-cycle.md — stratum A, positive control for `dependency_cycles`

**Falsehood:** `Conclusion C1` ("adopt a write-through cache ahead of the next peak event") is
justified partly by `Conclusion C2` ("on-call load will fall once the cache is adopted"), and C2
is justified partly by C1 having already been adopted — each conclusion cites the other as
support in its own composition head (`GT-n (label) + Cm (label) -> ... -> ...`), a genuine
citation cycle dressed as a perfectly well-formed two-arrow chain on each side.

**Rule that ought to catch it:** `dependency_cycles` (`_chain_dependency_defects`'s cycle DFS).

**Measured:** `dependency_cycles == 2`, naming both `c1` and `c2`. `ungrounded_chains == 0` — this
diverges from the plan's own stated prediction ("`ungrounded_chains == 2`, a node inside a cycle
contributes no grounding of its own"); measured instead of assumed per the plan's own instruction.
The divergence is mechanical, not a defect in the item: `grounded()` short-circuits `True` the
moment a node has its own GT token in its head, *before* it ever recurses into the node's cited
dependencies — so a node that composes on `GT-n + Cm` is grounded on the strength of its own GT
alone, regardless of whether the co-cited chain is cyclic. This is the same short-circuit t13
exists to pin explicitly; t03 exhibits it as a side effect rather than as its own probe.

**Disposition:** accept-with-reason — caught, positive control proving the corpus run reaches
`dependency_cycles` on shipped corpus bytes. Not a hole.

### t04-chain-only-head-ungrounded.md — stratum A, positive control for `ungrounded_chains`

**Falsehood:** `Conclusion C1`'s head cites only `Conclusion C2` (no ground truth); `Conclusion
C2`'s head cites only `C3`, a chain identifier this two-chain document never defines. Section 3
states two real ground truths (submission-to-publish latency, CMS support-ticket volume) that
neither derivation chain ever reaches — the recommendation is derived entirely from chain-to-chain
composition, ultimately terminating on an undefined forward reference, with nothing anchored to a
stated fact.

**Rule that ought to catch it:** `ungrounded_chains` (`_chain_dependency_defects`'s `grounded()`
reachability search).

**Measured:** `ungrounded_chains == 2`, naming both `c1` and `c2`; `dependency_cycles == 0` — the
required combination (an item that also cycled would be t03's family, not t04's). The undefined
`C3` forward reference is intersected out of the known-chain-id set inside
`_chain_dependency_defects`, so it contributes no edge while still marking `Conclusion C2`'s block
as headed — exactly the mechanism the plan's `<interfaces>` block predicted.

Chain-block head lines (printed verbatim, neither contains `GT-`):
```
### Conclusion C1: The migration should be scoped as a review-workflow project, not a platform swap
C2 (the downstream editorial-consolidation conclusion) → the review-workflow friction that motivates the whole migration effort is, on inspection, the same friction the editorial-consolidation project already names as its own justification → framing the migration as a review-workflow project rather than a ground-up platform swap keeps the two efforts aligned rather than duplicated
### Conclusion C2: The migration should be sequenced after the editorial-consolidation project (C3) completes
C3 (the editorial-consolidation conclusion, a project not otherwise detailed in this analysis) → the consolidation project's own output determines which content types the new CMS actually needs to support → sequencing the CMS migration after consolidation avoids building support for content types that consolidation may retire
```
`grep -c 'GT-' t04-chain-only-head-ungrounded.md` returns `4` (section 3's two GT entries, cited
by label only, never inside a chain head).

**Disposition:** accept-with-reason — caught, positive control proving the corpus run reaches
`ungrounded_chains` without also triggering a cycle. Not a hole.

### t05-selfaudit-overclaim-under-cycle.md — stratum A, positive control for `selfaudit_disagreements`

**Falsehood:** Same two-chain composition cycle as t03 (re-voiced onto a dynamic-discount-engine
decision so the two files are not near-duplicates — `diff t03 t05` is 124 lines), plus a
Self-Audit Gate block placed after all of section 6's prose claiming `**Criterion 4: Reason
Upward**` — `Band: **Rigorous**` — while the analysis's own chains are genuinely circular.

**Rule that ought to catch it:** `selfaudit_disagreements`
(`_selfaudit_calibration_defects`, criterion 4 contradicted by `_dependency_cycles`).

**Measured:** `selfaudit_disagreements == 1`, entry `{'criterion': 4, 'claimed': 'Rigorous',
'contradicted_by': '_dependency_cycles', 'measured': 2}` — exactly the predicted shape.
`conclusion_claims == 2` (unchanged from t03's own reading), confirming the Gate was placed after
section 6's prose rather than inside it; a Gate placed mid-section would have truncated the slice
and driven the claim count toward 0, a silent false-clean the acceptance criteria specifically
guard against.

**Disposition:** accept-with-reason — caught, positive control confirming the Criterion-4
contradiction wiring end to end. Not a hole.

### t06-hidden-cycle-past-head.md — stratum A, the corpus's genuine miss

**Falsehood:** `Conclusion C1` ("the fee-schedule change's revenue gain is real") and `Conclusion
C2` ("the churn-driven loss should be weighed against keeping it") are genuinely circular: C1's
own prose states its practical conclusion holds only once C2's churn calculation is weighed
against it, and C2's own prose states its loss calculation is itself premised on the schedule C1
justifies keeping remaining in effect. Each chain's HEAD line cites only its own `GT-n` token —
grounded and acyclic on the surface — and the circular citation is stated in the paragraph that
follows the two-arrow chain, never in the head line `_chain_head_refs` reads.

**Rule that ought to catch it:** `dependency_cycles` / `ungrounded_chains` — predicted MISSED per
19-RESEARCH.md Q8/T-06 and Assumptions Log A2.

**Measured outcome: the predicted miss occurred.** `dependency_cycles == 0` and
`ungrounded_chains == 0` despite the real C1↔C2 circularity, because `_chain_head_refs` returns on
the first head-matching line of a block and never reads further into it — the later-line citation
is structurally invisible to the dependency graph. This is **outcome 1** of the three named in the
plan's `<action>` block (the predicted miss, not "the prediction was wrong" and not "the item does
not resolve").

Chain-block head lines (printed verbatim, both contain `GT-`, neither contains a `C<digits>`
token):
```
### Conclusion C1: The revenue gain from the fee-schedule change is real and material
GT-1 (per-transaction net revenue rose from $0.34 to $0.41) → the $0.07 per-transaction increase, applied across the platform's measured transaction volume for the same four-week window, produces a revenue gain large enough to be material at the portfolio level → the fee-schedule change is producing a real, measurable revenue gain
### Conclusion C2: The churn-driven revenue loss should be weighed against keeping the schedule
GT-2 (pricing-attributed cancellations rose from 6/week to 14/week) → the additional 8 pricing-attributed cancellations per week, valued at the platform's average per-merchant transaction revenue, produces a recurring revenue loss that compounds with each additional week the schedule remains in place → the churn-driven loss is a real, growing cost of keeping the fee-schedule change
```
Confirmed by direct regex check (`re.search(r"C\d+", line)`) against both head lines: no match on
either.

**Disposition:** defer-with-owner — backlog 999.4 / detector-reach review, deferred because the
detectors are frozen under CONTRACT-06 and this phase may not widen one. `scripts/` was not
touched in response to this measured miss (`git diff --stat scripts/` and
`git status --porcelain scripts/` both empty).

### t13-grounded-alongside-cyclic-ref.md — stratum A, disclosed detector bound

**Falsehood:** Three chains. `Conclusion C1`'s head composes on `GT-1 (label) + C2 (label)`;
`Conclusion C2`'s head composes on `C3 (label)`; `Conclusion C3`'s head composes on `C2 (label)` —
C2 and C3 form a genuine citation cycle. C1's practical conclusion is presented as grounded
because it names its own ground truth (GT-1), while half its stated support (the C2 branch) rests
on a chain that is itself circular.

**Rule that ought to catch it:** `ungrounded_chains` for the citing chain specifically — predicted
to NOT fire on C1, per 19-RESEARCH.md Q8/T-13.

**Measured:** `dependency_cycles == 2`, naming `c2` and `c3` — the cycle is correctly caught.
`ungrounded_chains == 2`, also naming `c2` and `c3`, with `c1` absent from both lists — the
assertion this item exists to pin. `grounded()`'s short-circuit (`if own_gt.get(node): return
True`) fires for C1 the moment it sees its own GT-1, before ever inspecting whether the chain it
co-cites (C2) is sound, so C1 reads fully grounded even though half its stated support is
circular. The overall item does not score fully clean — the C2/C3 cycle itself is still visible
in `dependency_cycles` — so this is not a clean single-column miss; it documents a real bound on
what `grounded()`'s short-circuit can see.

**Disposition:** accept-with-reason — a disclosed bound of `_chain_dependency_defects`'s grounding
short-circuit, recorded here rather than closed; closing it would require editing a detector this
milestone freezes (CONTRACT-06). Not treated as a fix target.

## Verification run

```
$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift

$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (25/25)

$ git diff --stat scripts/
(no output)

$ git status --porcelain scripts/
(no output)
```

`scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (1 prerequisite(s)
unmet; 24/25 passed)` because this worktree had no `.venv` with pytest for VAL-03's third leg
(`check-links_anchors_test.py`). Ran `uv sync` (the documented remedy in CLAUDE.md's VAL-03
description) to create `.venv`, which is gitignored and not a repository change; the battery then
reported `FIREWALL: GREEN (25/25)` on re-run.

## Deviations from Plan

None — plan executed exactly as written. All three tasks' predicted-vs-measured readings were
verified empirically rather than assumed, per the plan's own explicit instruction ("Measure and
record what you actually get"). t03's `ungrounded_chains` reading (0, not the plan's stated
prediction of 2) is not a deviation from the plan's *instructions* — the plan explicitly
anticipates this class of divergence and requires recording the actual measurement, which is done
above. t06's outcome (the predicted miss) is one of three explicitly pre-committed legitimate
outcomes named in the plan's own `<action>` block, not a deviation.

One environment fix, not a code deviation: created `.venv` via `uv sync` to satisfy VAL-03's
pytest prerequisite so the firewall battery could report GREEN rather than BLOCKED. No file
tracked by git was affected.

## Self-Check

- FOUND: tests/adversarial-corpus-v9.0/t03-composition-cycle.md
- FOUND: tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md
- FOUND: tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md
- FOUND: tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md
- FOUND: tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md
- FOUND: commit df4a27e (t03/t05)
- FOUND: commit 0943e94 (t04/t13)
- FOUND: commit 2ff3aba (t06)

## Self-Check: PASSED
