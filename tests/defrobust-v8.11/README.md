# v8.11 DEFROBUST-02 — Two Mutually-Blind D-03 Reads / Phase 176

**Generated:** 2026-07-24. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to change an outcome. This directory holds the two independent, mutually-blind reader
passes that are the load-bearing evidence of the v8.11 definition-robustness test (`DEFROBUST-02`):
each pass applies the pre-registered D-03 include/exclude rule (`docs/v8.11-defrobust-protocol.md`) to
the four fork-sensitive analyses `Q-N2`/`Q-N3`/`Q-N4`/`Q-N6` frozen under
`tests/quality-baseline-v8.10-oos/analyses/`.

**This document records provenance and raw facts only. It computes no verdict and states no
CGATE-BUILD-01 disposition.** Whether the two reads agree — and the `CGATE-BUILD-01`
worth-committing / WON'T-DO disposition — is authored downstream in
`docs/v8.11-defrobust-reconciliation.md` (Plan 03), by mechanically applying the protocol's two-part
criterion and D-04 material-equivalence rule to these two captures. Nothing below was a target
(honesty-not-score, D-01 global).

## Provenance

| | |
|---|---|
| Invocation (per read, one live call each) | plain `claude -p` with the shared `read-input.md` delivered on **stdin** — **default model**, **no** `--plugin-dir first-principles`, **no** `--probe`, **no** first-principles agent dispatch of any kind |
| Source IDs | `read-A`, `read-B` |
| Shared input | `read-input.md` (assembled by concatenation from exactly the committed protocol + the four raw `Q-N` analyses; see "Leak-free by construction" below) |
| read-A dispatch (UTC) | start `2026-07-24T22:43:28Z`, end `2026-07-24T22:45:09Z`, duration 101s, exit 0 |
| read-B dispatch (UTC) | start `2026-07-24T22:43:28Z`, end `2026-07-24T22:45:06Z`, duration 98s, exit 0 |
| Execution | the two calls fired as two **separate** OS processes in parallel; neither shared inference context with, nor saw the output of, the other |
| `claude` CLI version | 2.1.219 (Claude Code) |
| Repo commit at run time | `cb62718` (the Phase-176 pre-registration anchor — protocol only; this capture-freeze commit lands strictly after it) |
| Live spend | **2 invocations** (2 blind reads, 0 judge, 0 first-principles-agent), both plain `claude -p` — see `manifest.tsv`. Under the protocol's Rule (9) reframing of Invariant 2 ("zero live first-principles-agent spend") these two general-reader passes are the permitted, bounded, one-shot cost |

## Contents

- `read-input.md` — the exact shared input fed identically to both reads: a fixed neutral instruction
  header, then the full committed text of `docs/v8.11-defrobust-protocol.md`, then the full text of
  `Q-N2`/`Q-N3`/`Q-N4`/`Q-N6` under labelled delimiters. Nothing else.
- `reads/read-A.md`, `reads/read-B.md` — the two raw `claude -p` captures, committed exactly as each
  live call produced them (each opens with its own model preamble; the two use structurally different
  formats — read-A tabulates the traced/untraced marks, read-B labels claims `LB-N` — a visible
  artifact of two genuinely independent contexts).
- `manifest.tsv` — one row per live invocation (`kind=blind-read`; 2 rows).

## Leak-free by construction (blindness integrity, D-02)

`read-input.md` was built by concatenating **only** the committed protocol and the four raw `Q-N`
documents. Neither read was given `docs/v8.10-correctness-instrument-design.md`, the designer's
claimed per-document verdicts, or the other read's output. Verified: every designer-answer phrase
greps to zero hits in `read-input.md`, and the raw-document region contains no D-03/CGATE/verdict
annotation.

**Note on the `correctness-instrument-design` filename in the input.** The string
`correctness-instrument-design` does appear in `read-input.md` — but only at five points, **all inside
the committed protocol region**, and each is a bare filename *citation* (naming the source of the
quoted rule at Rule (1); stating at Rules (7)/(8) that the design doc is *withheld* from the readers;
and pointing the downstream reconciler at its "Open risk" section). None reproduces the design doc's
substantive content or the designer's answers. The protocol's own leaked per-document verdicts —
present in the first draft of the anchor — were caught in a pre-read spot-check and scrubbed before
any read fired; the anchor commit `cb62718` is the corrected, leak-free protocol. Because Rule (8)
mandates feeding the protocol **verbatim**, the plan's literal `! grep -q 'correctness-instrument-design'`
sub-check cannot hold without stripping legitimate provenance from the protocol; the substantive
leak-freeness property (no design-doc content, zero designer-answer phrases) is what is asserted here
instead. See `176-02-SUMMARY.md` for the recorded deviation.

## Frozen-evidence discipline

These captures are committed exactly as the two live reads produced them. They are never regenerated
and never hand-edited to change what the evidence shows. Because `claude` inference is
non-deterministic, a bit-identical re-run is neither expected nor required — the reproducibility
guarantee is this committed, diff-visible freeze, not output determinism. Any post-hoc edit would be
visible in git diff / PR review and would violate this discipline. A read was eligible for a
*completeness* re-fire only (empty/truncated/failing to address all four docs); neither read needed
one, and no read was ever re-fired to change or align a verdict (honesty-not-score, D-01).
