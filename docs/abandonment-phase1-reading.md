# Contract abandonment — the Phase 1 reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/abandonment-preregistration.md`](abandonment-preregistration.md) §5, with
Amendments 2 and 3 (§8), both reporting-only.
**Captures:** `tests/abandonment/phase1/` (frozen) · **Re-derive:**
`python3 tests/abandonment/run_phase1.py read`

---

## The answer

**No reduction detected at this N. F2 does not ship, and Phase 2 did not run.**

| | `control` (`fe7fbba6`) | `fix` — F2 (`c9619457`) |
|---|---|---|
| **Abandoned — primary** | **2 of 10** | **4 of 10** (one-sided p = 0.93) |
| … of which delivery failures | 1 | 3 |
| Abandoned, delivery failures excluded *(sensitivity, decides nothing)* | 1 of 9 | 1 of 7 (p = 0.83) |
| One-shot attempts | 0 | 0 |
| Read the template | 6 | 9 |
| Guardrail — A1 / A2 documents, over readable documents | 5 of 6 / 3 of 6 | 2 of 5 / 3 of 5 — pass |

The fix arm is not better on the pre-registered outcome, and it is not better once delivery
failures are set aside either. The guardrail passed, but a guardrail only matters to a fix that
cleared the primary; this one did not.

**The run stopped at 20 of 60 cells**, under §5's stop rule: the fix arm's sixth cell exhausted
its routing retries. All 20 scored cells are the ten `TB-*` prompts on both arms; no `Q-*`,
`QT-*`, `PR-*` or `S-*` prompt was scored.

## What the run found instead

Phase 1 was built on Phase 0's H1 — that abandonment is a property of one-shot runs. **Under
Phase 1's conditions that mechanism did not appear at all:** zero one-shot attempts in either
arm. What did appear:

- **Delivery failures are most of it.** Four of the six scored abandonments were not the agent
  dropping the contract but the document failing to arrive whole: three hand-backs carrying only
  the document's tail (`TB-04.fix`, `TB-05.fix`, `TB-06.control` — each opening mid-sentence,
  after the subagent had used tools and in two cases read the template), and one run interrupted
  after two successful reads, whose entire hand-back is the harness string
  `[Request interrupted by user for tool use]` (`TB-08.fix`). In every run here — all 20, kept
  and failed alike — the agent executed as a background task that reported back through a
  `task_notification`, so that path is not itself the discriminator; what the truncated runs
  share is that the hand-back carried only a final message while the subagent streamed no text.
  **A user in that position receives the end of an analysis, not the analysis.** That is a
  product defect in delivery, not in the body, and F2 could not have touched it.
- **Two genuine abandonments, neither one-shot.** `TB-05.control` made 4 tool calls without
  reading the template and wrote a seven-part outline of its own. `TB-07.fix` made 12 tool calls,
  **read the template**, and still wrote a six-part outline of its own. Both contradict H1 as
  Phase 0 stated it; the second contradicts its condition (b) directly.
- **Routing, not the body, capped the run.** From an empty working directory, every `Q-N*` cell
  that ran — 11, since the stop rule fired before `Q-N6.control` — missed dispatch three times,
  33 attempts, every one answered directly by the main session. They are ordinary decision questions with no first-principles
  cue, and without a repository to ground a delegation decision the main session answers them
  itself. The agent `description` governs this; F2 changes only the body.

## Limits

- **Ten scored cells per arm, one prompt family.** A difference smaller than several attempts in
  ten would not show here.
- **Three kept documents are unreadable to the defect detector** (`TB-03.control`,
  `TB-04.control`, `TB-09.fix` — heading shapes its section resolver rejects), so the guardrail's
  A1/A2 counts rest on 6 and 5 documents.
- **The delivery-failure classification is post hoc.** It is reported, never decisive, and every
  figure above is given both ways.
- **Form, not quality** — `docs/v8.7-correctness-spot-check.md`.

## What this points at next

Not a body edit. In order of how much of the observed failure each would address:

1. **Delivery truncation** — the background-task hand-back path returning only a final message.
   It accounts for most of the failure seen here and is invisible to every conformance rate.
2. **Routing of uncued prompts** from a neutral working directory — six of 16 attempted prompts
   never reached the agent.
3. **Genuine abandonment** — two cases in twenty, neither of the Phase 0 shape.

## Falsifiers

```sh
# 1. The published primary and its reading are what the runner computes.
python3 tests/abandonment/run_phase1.py read | grep -q 'PRIMARY  abandonment fix 4/10 vs control 2/10'
python3 tests/abandonment/run_phase1.py read | grep -q -- '-> no reduction detected at this N'
python3 tests/abandonment/run_phase1.py read | grep -q 'PHASE 2  NOT AUTHORISED'
# 2. The sensitivity reading and its classification are what the runner computes.
python3 tests/abandonment/run_phase1.py read | grep -q "fix 1/7 vs control 1/9"
# 3. No one-shot attempt occurred in either arm.
python3 tests/abandonment/run_phase1.py read | grep -q 'control  abandoned 2/10  one-shot 0'
python3 tests/abandonment/run_phase1.py read | grep -q 'fix      abandoned 4/10  one-shot 0'
# 4. The captures have not been touched since they were frozen.
git diff --quiet HEAD -- tests/abandonment
```
