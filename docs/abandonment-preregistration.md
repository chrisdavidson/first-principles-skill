# Pre-Registration — Why does the agent sometimes abandon its output contract?

**Id:** `abandonment` · **Registered:** 2026-09-27, before any Phase 0 reading and before any
Phase 1 run under this id.
**Binding:** every phase's procedure, stop rule and decision rule below is fixed now. Phase 0 is
an offline reading of frozen transcripts; its only permitted effect on Phase 1 is the fix
selection §4 already maps out. A change to anything else requires a new id.

---

## 1. The question

**Contract abandonment** is a dispatched agent run whose document does not carry the six-section
output contract — fewer than 4 of the 6 section headings, the Stage A threshold. The agent
reasons, often well and at length, then organises the document its own way.

[`docs/w4-paired-reading.md`](w4-paired-reading.md) reported it without deciding it: 0 of 13
dispatched attempts on the v9.0.0 body, 3 of 17 on v9.12.0 (p = 0.17). The frozen `TB-08` is a
fourth instance on v9.12.0.

A preliminary read of those transcripts, made while scoping this plan and recorded here so that
Phase 0 is a test of it rather than a rediscovery:

- all four abandoned runs are **one-shot**: the subagent issued **zero tool calls** and answered in
  a single message;
- no run that read `output-template.md` abandoned the contract (32 of 32);
- both bodies state the six sections inline, word for word, under `## Output format`.

**H1 — the working hypothesis.** Abandonment is a property of one-shot runs, not of the body
losing the contract. A run that uses no tools never reaches the template read, and the inline
statement of the contract is not, alone, enough to hold a one-shot run to it.

## 2. Definitions

- **Dispatched attempt:** a run whose main session issued at least one `Agent` tool call.
- **Observable:** a dispatched attempt whose transcript carries at least one event with a
  non-empty `parent_tool_use_id`. Tool use is only countable on an observable attempt.
- **One-shot:** an observable attempt whose subagent issued zero `tool_use` blocks.
- **Template read:** the subagent issued a `Read` whose `file_path` ends `output-template.md`.
- **Abandoned:** fewer than 4 of 6 section headings in the extracted document, extracted by
  `tests/w4-paired/run_paired.py`'s `extract` (the Stage A extractor plus persisted hand-back
  recovery). A transport failure is neither abandoned nor kept; it is excluded.

## 3. Phase 0 — offline, zero spend, in this order

1. **Make the reading reproducible.** A committed tool reports, per attempt: arm/body, dispatched,
   observable, subagent tool-call count, template read, one-shot, abandoned. No figure in this
   plan's later phases may rest on an uncommitted script.
2. **Widen the evidence** to every frozen corpus whose transcripts carry subagent events:
   `tests/w4-paired/raw/`, `tests/emission-stage-a-v9.14/raw/` and `raw-attempt1/`,
   `tests/live-conformance-v9.0/*.jsonl`, `tests/quality-provenance-v8.24/*.jsonl`.
   `tests/trackb-run-v9.13/` is excluded: it carries no subagent events.
   **H1 holds** only if, over every observable dispatched attempt in that pool:
   - (a) every abandoned attempt is one-shot; and
   - (b) no attempt with a template read is abandoned.
3. **Inspect the dispatch side.** For every dispatched attempt, read the `prompt` the main session
   handed the `Agent` tool. Report its length and whether it matches
   `concise|brief|short|quick|summar|high[- ]level|don'?t (use|run)|no (tools|research|web)|without (research|tools)`
   (case-insensitive). **The dispatch side is implicated** if that pattern matches in at least
   half of the one-shot attempts **and** in at most a quarter of the others.
4. **Publish contract-emission reliability as a rate** — dispatched attempts that kept the
   contract, over dispatched attempts — beside the conformance rates, which are conditional on a
   readable document and so cannot show abandonment.

**Phase 0 stop rule.** If H1 fails (2a or 2b), Phase 0 publishes what it found and **Phase 1 does
not run under this id**.

## 4. Fix selection — mapped now, applied after Phase 0

| Phase 0 outcome | Fix Phase 1 tests |
|---|---|
| H1 holds, dispatch side implicated | **F3** — a change to the dispatch-facing text: the agent `description` in `shared/spine/SKILL.meta.yml`, worded against the specific pattern step 3 found. Its exact text is committed before any Phase 1 run. |
| H1 holds, dispatch side not implicated | **F2** — the block below, inserted in `shared/spine/SKILL-body.md` between the opening paragraph and `## Methodology`, verbatim. |
| H1 fails | none — see the stop rule |

**F2, verbatim:**

```markdown
**Output contract — this binds every response, including the shortest.** Whatever the problem,
and however direct the answer, the deliverable is one document whose top-level sections are
exactly these six, in this order: Problem Essence, Assumptions Table, Ground Truths, Derivation
Chains, Abandoned Reasoning, Conclusion. An answer organised any other way — by technique, by
step, or as a numbered outline of its own — does not satisfy the request, however sound its
reasoning. Section-by-section rules are under Output format below.
```

A closing self-check ("before returning, confirm the headings") was considered and rejected: it
sits at the end of a procedure a one-shot run never executes.

## 5. Phase 1 — pre-registered A/B

| Arm | Body |
|---|---|
| `control` | HEAD at the Phase 1 registration commit, whose plugin tree is byte-identical to `v9.12.0` |
| `fix` | the same, plus the selected fix, regenerated with `scripts/sync-content.py --write` |

**Prompts — 30 distinct, one generation per arm each, verbatim from their catalogs:**

- `tests/trackb-catalog-v9.13.md`: `TB-01` … `TB-10`
- `tests/quality-catalog-v8.10-oos.md`: `Q-N1` … `Q-N6`
- `tests/quality-catalog-v8.7.md`: `Q-P1` … `Q-P3`
- `tests/quality-catalog-v9.12-technique.md`: `QT-P1` … `QT-P3` (its own header states each is a
  full-composer prompt)
- `tests/premise-rejection-catalog.md`: `PR-P1`, `PR-P2`, `PR-N2` — **not** `PR-N1`, which missed
  dispatch in 5 of 6 w4-paired attempts
- `tests/step0-fixture-catalog.md`, full-composer rows only: `S-N02`, `S-N04`, `S-N07`, `S-A08`,
  `S-A12` — no focused-mode prompt, because a focused document is a different contract by design

**Transport:** as `docs/w4-paired-preregistration.md` §4, with one correction learned there —
every run starts in an **empty working directory**, so no prompt can be answered from this
repository's contents. Sequential; the arm that runs first alternates by prompt.

**Unit and retries.** Each prompt × arm needs one *dispatched, non-transport* attempt; a routing
miss is retried, at most twice. Abandonment is scored on that first dispatched attempt, and an
abandoned attempt is **not** retried — it is the outcome.

**Primary outcome:** abandoned dispatched attempts per arm.
**Secondary, reported:** one-shot rate per arm; abandonment among one-shot attempts; routing misses;
and, over the arm's readable documents, W4's A1 (malformed chain block) and A2 (nonconforming
verdict cell) document counts.

**Decision rule, fixed now.** `p` is a one-sided Fisher exact test, fix below control.

| Reading | Condition |
|---|---|
| **Fix reduces abandonment** | fix < control and `p ≤ 0.10` |
| **No reduction detected at this N** | anything else |

**Ship guardrail, fixed now.** Phase 2 runs only if the reading is *fix reduces abandonment*
**and** neither A1 nor A2 is worse in the fix arm by 3 or more documents. A fix that trades
abandonment for chain or verdict defects does not ship on this evidence.

**Phase 1 stop rule.** If either arm accumulates more than 5 routing misses that exhaust their
retries, the run stops and reports what it has.

## 6. Phase 2 — ship, only through the guardrail

The selected fix is edited into `shared/` (never the generated tree), regenerated, and released:
all 17 version stamps together, a CHANGELOG release entry that also carries the unreleased
measurement work, and the requirements-matrix rows that release owes. The reading is published
with its N. **Nothing here becomes a gate** — abandonment is a K-of-N live rate, barred from
gating by `docs/v8.7-constraint-teardown.md` §2 item 3.

## 7. What this cannot establish

- **Small counts.** Four abandonments motivate this. At roughly 15% abandonment, 30 attempts per
  arm detects a drop to near zero and little less; *no reduction detected* is weak evidence of no
  effect.
- **One-shot is a correlate until Phase 1.** Phase 0 can show that abandonment and one-shot
  co-occur. Only the A/B tests whether a text change moves abandonment.
- **A fix may move the one-shot rate instead of the contract.** That is why the one-shot rate is
  reported per arm.
- **Form, not quality.** `docs/v8.7-correctness-spot-check.md` measured that conformance does not
  predict correctness.

## 8. Amendments

### Amendment 1 — 2026-09-27, Phase 0, made after seeing the output it corrects

**Stated plainly: this amendment was made after the first Phase 0 run printed `H1: FAILS`, and
it reverses that verdict.** It is recorded so the reversal can be checked rather than trusted.

The first run scored all 8 `tests/live-conformance-v9.0/` captures and the
`tests/quality-provenance-v8.24/` capture as **abandoned**, and those nine were the entire
failure of both H1 conditions. The extractor had returned **0 words** for each. Those captures
predate the `[Subagent hand-back]` frame: the document arrives as the plain `tool_result` of the
main session's `Agent` call, which the Stage A extractor does not recognise.

The grounds are independent of the verdict and checkable:

- each corpus ships its own verbatim extraction beside the transcript (`<id>.md`), and every one
  is that `tool_result` less a ~20-word trailer — 9 of 9;
- `docs/conformance-baseline.md` scored all eight v9.0 documents `section_resolution OK`;
- a 0-word extraction of a dispatched run is an extraction failure by any reading of §2, not a
  document that dropped its headings.

**Change:** `tests/abandonment/phase0_reading.py` falls back to that unframed `tool_result` only
when the framed extraction is empty. It fires on exactly the nine legacy captures and on none in
`tests/w4-paired/` or `tests/emission-stage-a-v9.14/`. The frozen w4-paired extractor is
untouched.
