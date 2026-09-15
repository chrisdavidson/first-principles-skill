<!-- generated-by: gsd-doc-writer -->
# Testing

This document covers how to run every CI gate and the pre-commit gate locally (including offline `--self-test` modes), the anti-masking measurement invariants, and what the pre-commit gate checks. See [`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md) for the retirement of the body-budget gate that used to fire alongside it.

For the full at-a-glance gate inventory — every gate mapped to its owning script and job name — see [docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).

## CI gates — operational run-detail

<!-- GENERATED — DO NOT EDIT. Source: scripts/_gate_registry.py. Regenerate via: scripts/gen-gate-docs.py --write. -->
`docs/TESTING.md` is how to run every gate locally; `docs/gates/<GATE-ID>.md` is what each gate asserts and what it does not. One row below per registry entry — the id (or `—` for an entry with no standalone gate id), the detail page, and the exact local run command.

| Gate | Page | Run command |
|------|------|-------------|
| VAL-01 | [`docs/gates/VAL-01.md`](gates/VAL-01.md) | `claude plugin validate ./first-principles` |
| VAL-02 | [`docs/gates/VAL-02.md`](gates/VAL-02.md) | `markdownlint-cli2 --config .markdownlint.jsonc 'first-principles/**/*.md'` |
| VAL-03 | [`docs/gates/VAL-03.md`](gates/VAL-03.md) | `python3 scripts/check-links.py --self-test && python3 scripts/check-links.py && .venv/bin/python3 -m pytest scripts/check-links_anchors_test.py -q  # or any pytest-capable interpreter` |
| VAL-05 | [`docs/gates/VAL-05.md`](gates/VAL-05.md) | `python3 scripts/check-description-budget.py` |
| VERSION-01 | [`docs/gates/VERSION-01.md`](gates/VERSION-01.md) | `python3 scripts/check-version-stamps.py --self-test && python3 scripts/check-version-stamps.py` |
| REG-GUARD | [`docs/gates/REG-GUARD.md`](gates/REG-GUARD.md) | `python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py` |
| DUAL-04 | [`docs/gates/DUAL-04.md`](gates/DUAL-04.md) | `python3 scripts/sync-content.py --check` |
| GATE-02-v8.5 | [`docs/gates/GATE-02-v8.5.md`](gates/GATE-02-v8.5.md) | `python3 scripts/sync-content.py --self-test` |
| GATE-01 | [`docs/gates/GATE-01.md`](gates/GATE-01.md) | `python3 scripts/check-agent.py --self-test && python3 scripts/check-agent.py` |
| BATT-06 | [`docs/gates/BATT-06.md`](gates/BATT-06.md) | `python3 scripts/check-routing-battery.py --self-test` |
| STEP0-08 | [`docs/gates/STEP0-08.md`](gates/STEP0-08.md) | `python3 scripts/check-step0-emulator.py --self-test` |
| STEP0-06 | [`docs/gates/STEP0-06.md`](gates/STEP0-06.md) | `python3 scripts/check-step0-live.py --self-test` |
| TRACE-03 | [`docs/gates/TRACE-03.md`](gates/TRACE-03.md) | `python3 scripts/check-traceability.py --self-test` |
| QUAL-01 | [`docs/gates/QUAL-01.md`](gates/QUAL-01.md) | `python3 scripts/check-quality-harness.py --self-test` |
| PROV-GUARD | [`docs/gates/PROV-GUARD.md`](gates/PROV-GUARD.md) | `python3 scripts/check-provenance.py --self-test && python3 scripts/check-provenance.py` |
| HARN-01 | [`docs/gates/HARN-01.md`](gates/HARN-01.md) | `python3 scripts/check-act-limb.py --self-test` |
| HARN-02 | [`docs/gates/HARN-02.md`](gates/HARN-02.md) | `python3 scripts/check-loop-closure.py --self-test` |
| HARN-03 | [`docs/gates/HARN-03.md`](gates/HARN-03.md) | `python3 scripts/check-focused-parity.py --self-test` |
| SCAN-GUARD | [`docs/gates/SCAN-GUARD.md`](gates/SCAN-GUARD.md) | `python3 scripts/check-selfaudit-scan.py --self-test && python3 scripts/check-selfaudit-scan.py` |
| HC-BOUND | [`docs/gates/HC-BOUND.md`](gates/HC-BOUND.md) | `python3 scripts/check-high-confidence-bound.py --self-test` |
| CONF-GATE | [`docs/gates/CONF-GATE.md`](gates/CONF-GATE.md) | `python3 scripts/check-conf-gate.py --self-test && python3 scripts/check-conf-gate.py` |
| INVARIANT-CHECK | [`docs/gates/INVARIANT-CHECK.md`](gates/INVARIANT-CHECK.md) | `bash scripts/check-firewall-battery.sh  # INVARIANT-CHECK runs inline; no standalone command` |
| FROZEN-EVIDENCE | [`docs/gates/FROZEN-EVIDENCE.md`](gates/FROZEN-EVIDENCE.md) | `bash scripts/check-firewall-battery.sh  # FROZEN-EVIDENCE runs inline; no standalone command` |
| — | [`docs/gates/PRECOMMIT-sync-drift-gate.md`](gates/PRECOMMIT-sync-drift-gate.md) | `python3 scripts/sync-content.py --check` |
| — | [`docs/gates/PRECOMMIT-conformance-generator-self-test.md`](gates/PRECOMMIT-conformance-generator-self-test.md) | `python3 scripts/report-conformance.py --self-test` |
| — | [`docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`](gates/PRECOMMIT-conformance-baseline-drift-gate.md) | `python3 scripts/report-conformance.py --check` |
| — | [`docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`](gates/PRECOMMIT-claim-surface-generator-self-test.md) | `python3 scripts/gen-gate-docs.py --self-test` |
| — | [`docs/gates/PRECOMMIT-claim-surface-drift-gate.md`](gates/PRECOMMIT-claim-surface-drift-gate.md) | `python3 scripts/gen-gate-docs.py --check` |
| CONF-SURFACE | [`docs/gates/CONF-SURFACE.md`](gates/CONF-SURFACE.md) | `python3 scripts/gen-gate-docs.py --self-test && python3 scripts/gen-gate-docs.py --check` |
<!-- END GENERATED -->

## Routing battery (developer tools — not in CI)

Two developer tools let you run live routing batteries against a Claude session. Neither is wired into CI.

**Main-agent routing battery** — tests DELEGATE / NO-DELEGATE routing for the orchestrating agent:

```sh
python3 scripts/check-routing.py --catalog tests/routing-catalog.md --repeat 5 --min-pass 3
python3 scripts/check-routing.py --dry-run --catalog tests/routing-catalog.md   # parse-only, no live session
```

**Merged dual-signal battery (live run)** — see [`docs/gates/BATT-06.md`](gates/BATT-06.md) for the `check-routing-battery.py` live invocation.

Routing outcomes vary between sessions, plugin sets, and Claude routing-model versions. Never attribute a single FAIL to one commit without a same-window control run. Each prompt gets a fresh `claude -p` session.

**Retired shims.** Retired at the 2026-08-16 audit ([`audit-2026-08-16-duplication-staleness.md`](audit-2026-08-16-duplication-staleness.md)): the two deprecated shims `check-sub-skill-routing.py` and `check-focused-output.py`, plus `check-inventory.py`. Call `check-routing-battery.py` directly, with its namespaced `--boundary-*` / `--focused-*` threshold flags.

## Pre-commit gates

Five gates fire on every `git commit` when a hook mechanism is installed — the sync-drift gate, the conformance generator self-test, the conformance-baseline drift gate, the claim-surface generator self-test, and the claim-surface drift gate. Both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` run the same five, in the same order — see `CLAUDE.md`'s `### Pre-commit gates` section for the full per-gate detail. For how to install the hook, see [docs/DEVELOPMENT.md](DEVELOPMENT.md).

### Body-size report (not a gate — TEARDOWN-01)

**Owning script:** `scripts/check-body-budget.py`

Reports the current line count of `first-principles/agents/first-principles.md` on every run; it no longer exits nonzero because of the body's size and no longer blocks a commit. The 644-line figure survives in the script as an annotated historical reference constant (`MAX_LINES: int = 644`), retained for its fitted-limit provenance rather than as an enforced bound.

```sh
python3 scripts/check-body-budget.py           # report the live agent body's line count
python3 scripts/check-body-budget.py --self-test  # run offline reporting-correctness fixtures
```

This is no longer a gate to fix — the historical remediation advice (reduce `shared/spine/SKILL-body.md` or the `shared/agent/` phase fragments) no longer applies to a commit path. See [`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md) for the evidence and the standing record.

### Sync-drift gate

**Owning script:** `scripts/sync-content.py --check`

Blocks the commit if `shared/` and the generated `first-principles/` tree have diverged. This is the same check as CI gate DUAL-04 — it fires before the commit to catch drift locally.

```sh
python3 scripts/sync-content.py --check    # detect drift
python3 scripts/sync-content.py --write    # fix drift (regenerate)
```

### Conformance-baseline drift gate

**Owning script:** `scripts/report-conformance.py --check`

Blocks the commit if `docs/conformance-baseline.md` or `docs/data/conformance.json` no longer match a fresh `report-conformance.py` run. Unlike the sync-drift gate above, this gate has **no CI counterpart and no battery id** — by decision D-06 it is deliberately absent from both `scripts/check-firewall-battery.sh` and `.github/workflows/validation.yml`, so it fires only at commit time. It fails on staleness of the committed baseline, never on a conformance count being too high — no count in that baseline gates anything.

`docs/conformance-baseline.md` publishes five labelled surfaces: `shared-examples`, `generated-twin`, `adversarial-corpus`, and, as of Phase 20, `live-conformance` — the agent's own live-invoked output, captured under `tests/live-conformance-v9.0/` and scored by the same unmodified, frozen `detect_defects`. `live-conformance` has **no CI job and no battery gate**; its published rate is a recorded observation stated with its N, never a pass/fail threshold, and it is subject to the same K-of-5 noise discipline documented under [Measurement layers](MEASUREMENT-MAP.md#measurement-layers) — this drift gate only keeps the published reading byte-reproducible against the committed captures, it never blocks on the rate itself. `tests/live-conformance-v9.0` and `tests/live-conformance-catalog.md` are registered `_FROZEN_PATHS` entries (see [FROZEN-EVIDENCE](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory)).

```sh
python3 scripts/report-conformance.py --check    # detect drift
python3 scripts/report-conformance.py            # fix drift (regenerate)
```

**Bypass** for intentional in-progress work:

```sh
git commit --no-verify
```

## Anti-masking measurement invariants

The routing battery's focused-output scoring depends on two constants in `scripts/_battery_core.py`:

```
MIN_HEADER_HITS: int = 2       # scripts/_battery_core.py, line 2156
_COMPOSER_FOCUS_CEILING: int = 4   # scripts/_battery_core.py, line 2178
```

**`MIN_HEADER_HITS=2`** — the minimum number of distinct technique-category header hits required for the battery to classify an output as a focused single-technique response. An output must match at least two distinct headers from the technique's category set; a single incidental match does not trigger focused-mode classification. This prevents false-positive focused classifications from incidental prose matches.

**`_COMPOSER_FOCUS_CEILING=4`** — the threshold above which the battery classifies an output as full-composer rather than focused single-technique. An output scoring four or more composer-structure hits is classified `full-composer`; an output scoring fewer hits may still be classified as focused if the single-technique signal is strong enough. This ceiling distinguishes a focused output that touches a few structural elements from a full multi-technique composition.

The two constants are no longer locked the same way. `MIN_HEADER_HITS` is still asserted by a literal drift guard inside the `self_test_boundary()` sentinels in `scripts/_battery_core.py` (BATT-06 `--self-test`) — any edit to it trips those sentinels directly. `_COMPOSER_FOCUS_CEILING`'s literal `== 4` drift guard was retired under TEARDOWN-02 (`docs/v8.7-constraint-teardown.md`); the freeze on retuning its value is released, though the value itself stays 4. What survives is RR-77-08's pair of surviving conjuncts (`_rr7708_composer == 3` and `_rr7708_composer == _COMPOSER_FOCUS_CEILING - 1`), which prove the ceiling still constrains classification — **not** "without pinning its literal value": together the two conjuncts still entail `_COMPOSER_FOCUS_CEILING == 4` exactly, so an edit to the constant alone still trips BATT-06. Removing the literal drift guard did not make the constant freely editable in practice; a future retune is a two-part edit — the constant itself and the fixture that proves the relative check load-bearing (`163-02-PLAN.md`'s flagged assumption) — not a one-line change.

## Quick reference

Run all offline gates locally in sequence:

```sh
python3 scripts/check-body-budget.py    # reports body size; not a gate (TEARDOWN-01)
python3 scripts/check-agent.py --self-test
python3 scripts/check-agent.py --file first-principles/agents/first-principles.md
python3 scripts/check-links.py
python3 scripts/check-description-budget.py
python3 scripts/sync-content.py --check
python3 scripts/check-routing-battery.py --self-test
python3 scripts/check-step0-emulator.py --self-test
python3 scripts/check-step0-live.py --self-test
python3 scripts/check-traceability.py --self-test
python3 scripts/check-quality-harness.py --self-test  # QUAL-01 (v8.7 Phase 164)
```

Or with `uv` (auto-resolves Python deps):

```sh
uv run scripts/sync-content.py --check
uv run scripts/check-agent.py --file first-principles/agents/first-principles.md
```

## See also

- [docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory) — full gate inventory (canonical source)
- [docs/DEVELOPMENT.md](DEVELOPMENT.md) — pre-commit hook install paths and standard editing loop
- [docs/CONFIGURATION.md](CONFIGURATION.md) — frontmatter invariants and plugin configuration
- [docs/testing-agents-headlessly.md](testing-agents-headlessly.md) — methodology behind the routing battery (two-signal detection, `--permission-mode bypassPermissions`)
