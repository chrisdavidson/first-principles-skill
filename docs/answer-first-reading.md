# Reading — the answer-first live confirmation

**Id:** `answer-first` (`docs/answer-first-protocol.md`) · **N=3** registered prompts (`TB-01`,
`TB-04`, `TB-08`), 2 dispatched and scored, 1 exhausted without dispatch. Read 2026-09-29/30
against captures in `tests/answer-first/raw/` and `tests/answer-first/documents/`.

## Verdict against the registered pass rule

**The registered rule — "Pass = all 3 runs meet (a)-(e)" — cannot be fully evaluated: `TB-08`
never dispatched to the agent in any of its 3 attempts, so it was never scored.** Per §5's void
rules this is reported as what happened, not re-scored and not replaced with a substitute prompt.

**Of the 2 prompts that dispatched and were scored, both meet all five criteria (a)-(e) in
full, with zero permission denials and zero side files left behind.** This is a confirmation on
2 of 3 registered runs, not the pre-registered 3-of-3 — the third is a routing miss unrelated to
the answer-first mechanism under test, disclosed below rather than smoothed over.

## Per-run (a)-(e), with evidence

| Prompt | (a) resolves | (b) first heading | (c) clean before §6 | (d) chains valid | (e) ≤150 words | Overall |
|---|---|---|---|---|---|---|
| `TB-01` | PASS — six sections resolve | PASS — `## Answer` | PASS — clean | PASS — cites `C1, C2, C4, C8`, all present in §4 and all also cited in §6 | PASS — 112 words | **PASS** |
| `TB-04` | PASS — six sections resolve | PASS — `## Answer` | PASS — clean | PASS — cites `C6, C7`, both present in §4 and both also cited in §6 | PASS — 97 words | **PASS** |
| `TB-08` | — | — | — | — | — | **VOID — not dispatched** (3/3 attempts) |

## Observations

| Prompt | Total words | Words before `## 1.` | Appendix share of words | Side files left | Answer chains also cited in §6 |
|---|---|---|---|---|---|
| `TB-01` | 9,452 | 114 | 41% | none | yes |
| `TB-04` | 11,717 | 99 | 29% | none | yes |
| `TB-08` | — | — | — | — | — |

The "words before `## 1.`" figure is the Answer block itself (`_slice_sections` discards
everything before section 1's own heading, so this is not a defect — it is what a reader now
sees before reaching the six-section body). The appendix share (29–41%) is consistent with this
plan's own motivating measurement — process output ran 33–40% of a delivered document's words in
most of the frozen corpus and, before this change, was written first.

**First heading in each delivered file, verified byte-for-byte:** both `TB-01.md` and `TB-04.md`
open with `## Answer` at byte 0 — no preamble, no environment-state paragraph, nothing before it.

**Process-output placement, verified against each document's own heading list:** in both
documents, `## Appendix — process output` is the heading immediately following `## 6. Conclusion`
— no process-output block (the §6→§4 closure ledger, the Assumption Audit scan, the self-audit
scan, the adversarial pass record, the Techniques-not-applied block, or the Self-Audit Gate's
verdict blocks) leaked before it. `TB-01`'s appendix orders them: closure ledger, Assumption Audit
scan, self-audit scan, adversarial pass, Techniques not applied, Self-Audit Gate. `TB-04`'s
orders them: Assumption Audit scan, adversarial pass, Techniques not applied, closure ledger,
self-audit scan, Self-Audit Gate. Both are valid under the body's rule — process-output blocks
are emitted "in the order produced," not a fixed inter-block order — and both keep every block
under its own existing top-level heading, none of them renamed or merged.

## `TB-08` — the void, in full

All three attempts returned a `result` event, `subtype: "success"`, `dispatched: false`. The
main-session model answered inline instead of delegating, each time opening with a variant of
"This is a statistics reasoning question, not a coding task, so let me just work through it
directly" before working the yield-comparison question itself. This is a **routing miss** — the
prompt did not trigger delegation to the `first-principles` agent at all, on any of 3 attempts —
and is unrelated to the answer-first mechanism this run confirms: the mechanism was never
exercised for this prompt, so nothing about it passed or failed. `permission_denials` was empty
on every attempt, and `loaded_body` confirmed the working-tree plugin on every attempt, so this is
not the void-permission or wrong-body abort paths — it is squarely the "not dispatched" void rule
in §5, exhausted at the stated 3-attempt ceiling.

Per the coordinator's instruction and the protocol's own rule, `TB-08` is not re-run and no
substitute prompt is scored in its place under this id. A future run wanting a third scored
science-domain prompt would need its own id.

## What this run does and does not show

**Shows:** on the two prompts that did dispatch, the delivered file the agent handed off — under
a real, non-scripted `claude -p` invocation with `--permission-mode acceptEdits` and the
enumerated (amended, see the protocol's §7) allowlist rather than `bypassPermissions` — opened
with the Answer, kept the six sections unchanged and in order, and moved every process-output
block into the trailing appendix, with zero permission denials and zero stray side files. The
offline reader controls (EMIT-STAGE-A's C21) already proved the mechanism reads correctly and
that a mis-slice would be visible; this shows the real create/append/write-answer/assemble/check
sequence survives an actual live run on real prompts, twice.

**Does not show:** a rate. N=3 on one model is a pre-registered confirmation on named prompts,
not a K-of-N noise-floor reading (`docs/v8.7-constraint-teardown.md` §2 item 3) and not treated
as one — exactly as `docs/regression-rerun-protocol.md` scores its own four regressions. It also
does not exercise the science domain the way `TB-08` would have; that gap is disclosed here
rather than papered over with a substitute.
