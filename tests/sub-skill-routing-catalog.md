# Sub-Skill Routing Catalog — v4.2 (Boundary Discipline Fixture)

**Status:** Committed repo fixture, consumed by `scripts/check-sub-skill-routing.py`.

## Purpose

This battery measures **boundary discipline**: all eleven sub-skills in the
`first-principles` plugin are registered `disable-model-invocation: true`
(Path 2 architecture, shipped in Phase 46). This means the orchestrator
**never** auto-routes to them. Every P and N row in this catalog therefore
correctly expects `none-or-other` — composer-routing is the architecturally
correct outcome at the orchestrator boundary.

## Division of Labor

Two batteries cover the original FU-21 regressions:

- **`scripts/check-sub-skill-routing.py`** (this catalog) — **boundary discipline**:
  verifies nothing auto-routes to slash-only stubs at the orchestrator boundary;
  all rows expect `none-or-other`.
- **`scripts/check-focused-output.py`** against `tests/focused-output-catalog.md`
  — **canonical FU-21-1 / FU-21-2 gate**: verifies that slash-invoked sub-skill
  calls produce the correct focused-technique output (the right analysis fires
  on explicit `/first-principles:pre-mortem` or `/first-principles:inversion`
  invocation).

## Run Command

```
python3 scripts/check-sub-skill-routing.py --catalog tests/sub-skill-routing-catalog.md --repeat 5 --min-pass 3
```

(No `--p-threshold` flag — the strict default applies; all P rows must pass.)

## Anti-Regression Warning

> Do not "fix" the catalog back to expecting direct sub-skill firing, and do not
> remove `disable-model-invocation: true` to make these prompts pass.
> The fixture, not the architecture, was wrong.

## History

This catalog was originally authored in Phase 45 against pre-Phase-46
descriptions. The Phase 46 design chose Path 2 (`disable-model-invocation: true`),
which made the original P12/P24/N2 expectations architecturally impossible.
Full diagnosis: `.planning/notes/fu21-fixture-contradiction-diagnosis.md`.
The v3.8 baseline and Phase 45 rationale are archived in the v3.8 phase archive.

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
