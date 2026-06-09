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

**Expected baseline outcomes** (v2 detection — see Plan 45-04 SUMMARY):
Against the current (pre-Phase-46) shipped descriptions, prompts that
"should route to a specific sub-skill" mostly fail in the same way: the
orchestrator invokes the `first-principles:first-principles` composer
agent instead of a specific sub-skill, classifying as `none-or-other` under
the v2 verifier. This means:

- **P12** (expected `pre-mortem`) — FAIL (FU-21-1 reproduced; composer-routing)
- **P24** (expected `inversion`) — FAIL (FU-21-2 reproduced; composer-routing)
- **N1** (expected `none-or-other`) — PASS (composer-routing = none-or-other = matches expected)
- **N2** (expected `pre-mortem`) — FAIL (composer-routing; same regression class as P12. N2's expected outcome is **forward-looking** — it should PASS post-Phase-46, proving `:inversion` sharpening did not poach plan-shaped `:pre-mortem` traffic)

So the v3.8 baseline is expected to show 3 of 4 prompts failing under K-of-N.
That is the evidence Phase 46 will be measured against: P12, P24, and N2 must
all start PASSing post-Phase-46 (with their respective expected sub-skills
firing), while N1 must STAY PASSing (proving `:pre-mortem` widening did not
over-trigger on debugging prompts). `--p-threshold 0` is used in Phase 45
because the battery-level PASS/FAIL exit code is deliberately non-strict on
P-failures here — the failures are *expected*. Per-prompt verdicts in the
output block are the gate, not the battery exit code.

---

## Boundary Discipline — composer-routing expected (no auto-route to slash-only stubs)

| # | Prompt | Expected Sub-Skill | Trigger Class | Rationale |
|---|--------|--------------------|---------------|-----------|
| P12 | "The plan looks solid and the team is excited, but I am nervous. Before we lock it in, I want to surface every way this could blow up." | none-or-other | oblique | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 42. Under the Path 2 / Phase 46 architecture, all eleven sub-skills are registered `disable-model-invocation: true` (slash-only stubs); the orchestrator never auto-routes to them. Composer-routing (`none-or-other`) is the architecturally correct outcome. FU-21-1 correctness is now measured by `scripts/check-focused-output.py`. |
| P24 | "We are confident the data migration will go fine. I would rather figure out everything that would make it go wrong instead." | none-or-other | oblique | Verbatim from `.planning/eval/v2.0-routing-prompts.md` line 54. Under the Path 2 / Phase 46 architecture, all eleven sub-skills are registered `disable-model-invocation: true`; the orchestrator never auto-routes to them. Composer-routing (`none-or-other`) is the architecturally correct outcome. FU-21-2 correctness is now measured by `scripts/check-focused-output.py`. |

---

## Negative Controls — confirms boundary discipline in all directions

| # | Prompt | Expected Sub-Skill | Off-Target Risk | Rationale |
|---|--------|--------------------|-----------------|-----------|
| N1 | "I'm nervous about my Python script — it crashes on startup and I can't figure out why. Surface what could be wrong with my error handling." | none-or-other | `:pre-mortem` over-trigger after FU-21-1 widening | Adjacent vocabulary (`nervous`, `surface`, `what could be wrong`) overlaps the widened `:pre-mortem` trigger surface, but the prompt is a debugging request explicitly excluded by the `shared/spine/SKILL.meta.yml` scope clause ("Not for routine code review, debugging, performance optimization, or general Q&A"). Style precedent: mirrors N5 and N13 in `tests/routing-catalog.md` — vocabulary-adjacent to the trigger class but off-scope. |
| N2 | "We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for?" | none-or-other | (migrated) | Under the Path 2 / Phase 46 architecture, `none-or-other` (composer-routing) is the only architecturally correct outcome at the orchestrator boundary — sub-skills are `disable-model-invocation: true` and never auto-route. The pre-mortem-vs-inversion boundary-correctness intent of this prompt (plan-shaped traffic must not be poached by `:inversion`) has migrated to the focused-output catalog (`tests/focused-output-catalog.md`), where slash-invoked technique dispatch is the canonical FU-21 gate. |
