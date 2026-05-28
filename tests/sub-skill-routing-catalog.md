# Sub-Skill Routing Catalog — v3.8 (FU-21-1 / FU-21-2 regression fixture)

**Status:** Committed repo fixture, consumed by `scripts/check-sub-skill-routing.py`.

**Purpose:** Pins the two v2.0 eval regressions and the two paired negative
controls Phase 46 must keep green. FU-21-1: P12 fails to load `:pre-mortem`
(oblique nervous-about-plan framing). FU-21-2: P24 routes to `:pre-mortem`
instead of `:inversion` (oblique figure-out-what-makes-it-go-wrong framing).
N1 guards Phase 46 `:pre-mortem` widening against over-trigger on
debugging-shaped prompts. N2 guards Phase 46 `:inversion` sharpening against
poaching legitimate plan-shaped `:pre-mortem` traffic.

**Run command:**

```
python3 scripts/check-sub-skill-routing.py --catalog tests/sub-skill-routing-catalog.md --repeat 5 --min-pass 3 --p-threshold 0 --n-threshold 2
```

**Expected baseline outcomes:** Against the current (pre-Phase-46) shipped
descriptions, P12 and P24 WILL FAIL — that IS the regression this fixture
pins. The two N-controls should PASS. Phase 46's re-run (with
`--p-threshold 2 --n-threshold 2`) is the success gate. `--p-threshold 0` is
used in Phase 45 because the script's overall PASS/FAIL exit code is
deliberately non-strict on P-failures here — the P-failures are *expected*.
Per-prompt verdicts in the output block are the gate, not the battery exit
code.

---

## Positive Cases — sub-skill that SHOULD load

| # | Prompt | Expected Sub-Skill | Trigger Class | Rationale |
|---|--------|--------------------|---------------|-----------|
| P12 | "The plan looks solid and the team is excited, but I am nervous. Before we lock it in, I want to surface every way this could blow up." | pre-mortem | oblique | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 42. FU-21-1: v2.0 eval monolith fired but v2.0 plugin loaded no skill. Phase 46 widens `:pre-mortem` description to cover this oblique framing. |
| P24 | "We are confident the data migration will go fine. I would rather figure out everything that would make it go wrong instead." | inversion | oblique | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 54. FU-21-2: v2.0 eval monolith fired but v2.0 plugin loaded `:pre-mortem` (wrong). Phase 46 sharpens the `:inversion` vs `:pre-mortem` boundary so confidence-flip / failure-mode-enumeration framings route to `:inversion`. |

---

## Negative Controls — proves Phase 46 edits don't over-trigger or under-trigger

| # | Prompt | Expected Sub-Skill | Off-Target Risk | Rationale |
|---|--------|--------------------|-----------------|-----------|
| N1 | "I'm nervous about my Python script — it crashes on startup and I can't figure out why. Surface what could be wrong with my error handling." | none-or-other | `:pre-mortem` over-trigger after FU-21-1 widening | Adjacent vocabulary (`nervous`, `surface`, `what could be wrong`) overlaps the widened `:pre-mortem` trigger surface, but the prompt is a debugging request explicitly excluded by the `shared/spine/SKILL.meta.yml` scope clause ("Not for routine code review, debugging, performance optimization, or general Q&A"). Style precedent: mirrors N5 and N13 in `tests/routing-catalog.md` — vocabulary-adjacent to the trigger class but off-scope. |
| N2 | "We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for?" | pre-mortem | `:inversion` poaching `:pre-mortem` traffic after FU-21-2 sharpening | Prompt is unambiguously plan-shaped (named plan, timeline, rollout) — the boundary marker that distinguishes `:pre-mortem` from `:inversion` per the `inversion.md` decision rule ("inversion stress-tests a claim; pre-mortem stress-tests a plan"). It also uses oblique "how this could go badly" / "failure modes" phrasing that overlaps the FU-21-2 P24 confusion zone. The N must hold to prove the sharpening was boundary-correct, not boundary-overshooting. Style precedent: v2.0 eval P09 / P10 (plan-shaped pre-mortem prompts that correctly loaded `:pre-mortem`). |
