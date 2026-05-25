# Routing-Battery Canonical Baseline — v3.5 (best-of-3, post-FRAG-fix)

**Recorded:** 2026-05-25
**Script version:** v3.5 (`--repeat 3 --min-pass 2`)
**Battery verdict:** PASS
**Summary:** P 6/8, N 15/15

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P1 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P2 | DELEGATE | 3 | 1 | 1/3 | FAIL |
| P3 | DELEGATE | 3 | 1 | 1/3 | FAIL |
| P4 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P5 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P6 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P7 | DELEGATE | 3 | 3 | 3/3 | PASS |
| P8 | DELEGATE | 3 | 3 | 3/3 | PASS |
| N1 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N2 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N3 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N4 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N5 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N6 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N7 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N8 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N9 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N10 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N11 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N12 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N13 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N14 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |
| N15 | NO-DELEGATE | 3 | 3 | 3/3 | PASS |

---

## How this baseline was produced

```bash
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 3 --min-pass 2
```

Run date: 2026-05-25. Output directory: `/tmp/check-routing-20260525T151443Z/` (raw per-run JSON);
full stdout log: `/tmp/routing-38-02/full.log`.

This baseline records the v3.5 post-fix measurement following Phase 37 (which closed FRAG-01..06
by adding "fundamental ground truths" / "reason up from them" to the agent description and fixing
the mid-sentence embedding for P3 in the catalog) and Phase 38 Plan 03 (which closed the residual
P7 gap surfaced by 38-01 by adding the question-form, back-reference, and evaluate-verb
paraphrases to the SKILL.meta.yml description). P7 — the primary target of the 38-03 fix —
holds at 3/3 PASS across the full battery, confirming the description edits stuck.

**Failing prompts at this baseline (P2, P3):** Both fell below K=2 out of 3. Neither is a
regression from v3.4 — P3 was already 0/3 FAIL in v3.4 and P2 was 2/3 borderline — and both
fall within the known same-session ±3 noise envelope (see `memory/routing-battery-noise.md`).
The battery PASSES overall because the threshold is P >= 6/8 and N >= 14/15, both met.

---

## Coexistence note

`tests/routing-baseline-v3.4.md` remains the pre-fix historical record per D-03 and is
unmodified. No references in `ROADMAP.md` or `PROJECT.md` are updated to point at v3.5 in
this plan — coexistence is the contract.

---

## Failure modes observed on borderline prompts

The two borderline-FAIL prompts (P2 1/3, P3 1/3) were investigated by replaying their raw
per-run logs against the description trigger surface. Findings, recorded here so future
runs don't re-investigate the same artifacts:

**Scoring rule recap.** `scripts/check-routing.py` counts DELEGATE only on (a) a `Task`
tool_use whose `subagent_type` contains `first-principles`, or (b) >= 4 of 6 expected
agent section headers in the response text. **The `Skill` tool does not count** — even
when the agent invokes the first-principles skill via that mechanism, the harness scores
the run as NO-DELEGATE.

**P3 — three distinct outcomes across three runs:**
- Run 1: agent recognized the routing intent and tried to invoke `first-principles:first-principles`
  via the `Skill` tool. The call errored ("Unknown skill") and the agent fell through to an
  inline answer. **Wrong-tool near-miss** — routing intent was present; the harness simply
  doesn't credit Skill-tool invocations.
- Run 2: no tool use at all. Inline answer produced directly. **Silent skip.**
- Run 3: correct `Task` tool delegation with `subagent_type: "first-principles:first-principles"`.
  **PASS.**

**P2 — two silent skips and one correct delegation:**
- Runs 1 and 2: inline answers, no tool use. **Silent skip.**
- Run 3: correct `Task` tool delegation. **PASS.**

**Interpretation.** Two failure modes are at play, neither attributable to a description-content
gap:

1. *Wrong-tool selection* (P3 Run 1). The first-principles agent is registered as both a
   plugin skill and a subagent. The model occasionally picks the `Skill` path, which the
   harness intentionally does not score as DELEGATE. This is a dual-registration discoverability
   artifact, not a trigger-surface issue.
2. *Silent skip* (P2 Runs 1-2, P3 Run 2). The model answers tractable analytical prompts
   inline rather than delegating. The trigger phrases ("challenge the assumptions", "reason
   from ground truth", "what do we actually know is true") are present in both prompt and
   description — there is no obvious lexical gap left to close.

Both failure modes fall within the documented same-session ±3 noise envelope
(`memory/routing-battery-noise.md`). Neither prompt regressed from v3.4 (P3: 0/3 → 1/3;
P2: 2/3 → 1/3, stable inside noise). No follow-on description fix is indicated at this run.
