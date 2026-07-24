# v8.10 Out-of-Sample Fresh-Analysis Baseline — CORRECTGATE-01 / Phase 173

**Generated:** 2026-07-24. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to change an outcome. This directory is the **out-of-sample control** the v8.9
DIAGNOSE-01 diagnosis never had (docs/v8.9-diagnose-contract-fix.md): six *fresh* first-principles
analyses, generated live under the current byte-frozen agent, on decision problems topic-distinct
from the three frozen v8.7 problems (Q-P1 REST/gRPC, Q-P2 subscription/loyalty, Q-P3 attic/windows).

**This document records provenance and raw facts only. It does not compute a verdict and states no
detector or defect number.** Whether each analysis's §6 conclusions trace to its §4 chains — and the
FIX-CONTRACT-01 stands / must-revisit disposition — is authored in Plan 03
(`docs/v8.10-fix-contract-oos-validation.md`), AFTER a detector-independent blind hand-read under the
pre-registered protocol (`docs/v8.10-fix-contract-oos-protocol.md`). No figure below was a target;
these are simply what six live generation-only dispatches produced (honesty-not-score, D-01 global).

## Provenance

| | |
|---|---|
| Command (per problem, one live call each) | `python3 scripts/check-quality-harness.py --probe <ID> --catalog tests/quality-catalog-v8.10-oos.md --plugin-dir first-principles --out /tmp/qh-173/captures` |
| IDs | Q-N1, Q-N2, Q-N3, Q-N4, Q-N5, Q-N6 |
| First dispatch launched (UTC) | 2026-07-24T15:08:58Z |
| Last dispatch completed (UTC) | 2026-07-24T15:48:58Z |
| `claude` CLI version | 2.1.218 (Claude Code) |
| Repo commit at run time | `b1b1768` (the Phase-173 pre-registration anchor — catalog + protocol; this capture-freeze commit lands strictly after it) |
| Catalog | `tests/quality-catalog-v8.10-oos.md` at commit `b1b1768` |
| Agent forced | `first-principles:first-principles`, via `--plugin-dir first-principles` on every (generation) dispatch; no judge dispatch was made, so no `plugin_dir=None` judge call exists |
| Arm | Single arm, **generation-only** (`--probe`) — no judging, no scoring. Deliberately NOT `--run` (which would add one judge call per analysis = 12 live calls); the milestone's live budget is ~6 fresh analyses |
| Problems (fresh, topic-distinct from the frozen three) | Q-N1 hire-vs-upskill Kafka/Flink capability (org/people); Q-N2 second roaster vs. second shift (manufacturing capex); Q-N3 native iOS/Android vs. Flutter consolidation (mobile/software); Q-N4 west-coast warehouse vs. 3PL (logistics build-vs-buy); Q-N5 part-time ML master's vs. self-study (personal/career); Q-N6 in-house CBCT vs. refer out (healthcare-ops capex) |
| Runs | 6 problems × 1 run = **6 generations** |
| Extraction | `extract_agent_analysis(<capture>.jsonl, subagent_type="first-principles:first-principles")` per capture (the `task_notification.summary` primary channel, never the top-level `result` paraphrase or `tool_result`); written to `analyses/<ID>.md` |
| Live spend | **6 invocations** (6 generation + 0 judge), one manifest row each, all outcome `completed`, **zero re-dispatches / zero 429s** — see `manifest.tsv` |

## Contents

- `analyses/Q-N{1..6}.md` — the six extracted analyses (one per fresh problem). Each is a full
  first-principles analysis carrying numbered sections §1–§6, derivation chains, and a conclusion.
  These `.md` files are the exact input both to Plan 03's hand-read (by eye) and to the offline
  `detect_defects()` detector.
- `captures/Q-N{1..6}.jsonl` — the raw `stream-json` generation captures, committed unmodified.
- `manifest.tsv` — one row per live invocation (all `kind=generation`; zero `judge` rows).
- `defect-incidence.tsv` — **added in Plan 03**, not part of this generation freeze: the offline
  detector's ten-column output over these analyses, produced after the blind hand-read for blindness.

## Frozen-evidence discipline

These captures and analyses are committed exactly as the live run produced them. They are never
regenerated and never hand-edited to change what the evidence shows. The heading depth of the
numbered sections varies across the six analyses (some render §1–§6 at `#`, some at `##`); this is
recorded as the raw form the agent emitted, not normalized — any downstream handling of that
variation belongs to Plan 03's reading and the Plan 174 instrument design, not to this frozen set.
Any post-hoc edit would be visible in git diff / PR review and would violate this discipline.
