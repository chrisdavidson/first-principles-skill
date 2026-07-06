# Measurement Map

Terse maintainer reference for the layered measurement stack. Use this to read off which gate owns which residual, which script runs each layer, and what the live thresholds are. For how to **run** each gate, see [TESTING.md](TESTING.md). For how each script reads what, see [ARCHITECTURE.md](ARCHITECTURE.md#measurement-subsystem).

---

## Measurement layers

| Layer | Script | CI gate | What it measures |
|-------|--------|---------|------------------|
| Main routing battery | `scripts/check-routing.py` | None — developer tool only | Main-agent DELEGATE / NO-DELEGATE boundary (see [Routing battery — developer tools](TESTING.md#routing-battery-developer-tools--not-in-ci)) |
| Merged routing battery | `scripts/check-routing-battery.py` | **BATT-06** | Boundary + focused-output dual-signal (see [BATT-06](TESTING.md#batt-06--check-routing-battery)) |
| Step 0 emulator | `scripts/check-step0-emulator.py` | **STEP0-08** | Offline phrase-detection MODE classifier (see [STEP0-08](TESTING.md#step0-08--check-step0-emulator)) |
| Step 0 live harness | `scripts/check-step0-live.py` | **STEP0-06** | Live MODE classification via approach-② bypass channel (see [STEP0-06](TESTING.md#step0-06--check-step0-live)) |
| Traceability matrix | `scripts/check-traceability.py` | **TRACE-03** | Capability → requirement → test mapping (see [TRACE-03](TESTING.md#trace-03--check-traceability)) |
| BATT-06 sentinels | `scripts/_battery_core.py` → `self_test_boundary()` | BATT-06 (via merged battery `--self-test`) | Anti-masking constants + honest-state carry-forward vectors |

`check-routing.py` is **not wired into CI** — developer tool only. All other layers above run in `.github/workflows/validation.yml`.

For the stream-json capture method behind the live layers (approach-② bypass, two-signal DELEGATE rule), see [testing-agents-headlessly.md § 3](testing-agents-headlessly.md#3-the-two-signal-delegate-detection-rule) and [§ 8](testing-agents-headlessly.md#8-script-inventory).

---

## Residual ownership

This table is the core lookup. Source: `CLAUDE.md`, `scripts/_battery_core.py` (`self_test_boundary()`), `scripts/check-step0-emulator.py` (Category 3), and [requirements-traceability.md](requirements-traceability.md) (canonical full Active-Surface detail and coverage headline).

| Residual | Description | Owning gate(s) | Artifact |
|----------|-------------|----------------|---------|
| **RR-114-01** (supersedes RR-108-01, supersedes RR-95-01; chain: RR-79-02->RR-92-01->RR-95-01->RR-108-01->RR-114-01) | S-P02 inversion carry-forward (1/5 at v7.6 re-baseline Phase 114, no change vs v7.4 1/5). **[v8.0 ACCEPTED-FINAL]** True K/N: 1/5 (v7.13 live). Terminal disposition — project wrapped. | **BATT-06** | `_battery_core.self_test_boundary()` → RR-114-01 sentinel |
| **RR-108-02** (supersedes RR-95-02; chain: RR-79-03->RR-92-02->RR-95-02->RR-108-02 CLOSED) | S-P05 trade-off **CLOSED at 4/5** ≥ min-pass at Phase 114 v7.6 re-baseline (lone canonical improver; ID retained, sentinel re-pointed to v7.6 vector [2,2,2,2,1] as regression guard) | **BATT-06** | `_battery_core.self_test_boundary()` → RR-108-02 sentinel (CLOSED, regression guard) |
| **RR-79-01** | S-P01 pre-mortem honest carry-forward (4/5 at v6.4 re-baseline) | **BATT-06** | `_battery_core.self_test_boundary()` → RR-79-01 sentinel |
| **RR-77-08** | `_COMPOSER_FOCUS_CEILING=4` lock (anti-masking) | **BATT-06** | `_battery_core.self_test_boundary()` → RR-77-08 sentinel |
| **RR-80-01** | S-N04 negative-control over-routing dip (CLOSED 4/5 at v6.4) | **STEP0-08** (emulator assertion) **+ BATT-06** (marker-counting assertion) — dual-layer | `check-step0-emulator.py --self-test` Category 3; `_battery_core.self_test_boundary()` RR-80-01 |

**RR-80-01 dual-layer detail:** STEP0-08 (`check-step0-emulator.py --self-test`) owns the emulator-layer assertion — the S-N04 prompt fires no trigger phrase and is classified `full-composer` (catalog-independent inline literal). BATT-06 (`_battery_core.self_test_boundary()`) owns the marker-counting assertion — one bare pre-mortem hit (count=1) is below `MIN_HEADER_HITS` (2), so `classify()` returns `"none"`, not `"focused-pre-mortem"`.

For the complete Active-Surface list and the coverage headline (133 reproducible / 96 audit-only / 0 gap / 229 total), see [requirements-traceability.md](requirements-traceability.md).

---

## Live thresholds and constants

### Main routing battery (`scripts/check-routing.py`)

Source: `scripts/check-routing.py` argparse defaults (lines 41–42).

- P-cases: **≥ 11/13 DELEGATE**
- N-cases: **≥ 18/20 NO-DELEGATE**

Catalog: `tests/routing-catalog.md`. Developer tool — not in CI.

### Merged routing battery (`scripts/check-routing-battery.py`)

Source: `scripts/check-routing-battery.py` `build_parser()` defaults.

| Signal | Threshold |
|--------|-----------|
| `--boundary-p-threshold` | 2 |
| `--boundary-n-threshold` | 2 |
| `--focused-p-threshold` | 4 |
| `--focused-n-threshold` | 1 |

Catalog: `tests/routing-battery-catalog.md`. CI gate: BATT-06.

### Anti-masking constants (`scripts/_battery_core.py`)

Source: `scripts/_battery_core.py`.

- `MIN_HEADER_HITS = 2` — minimum distinct technique-marker hits for a technique to enter the `fired` set
- `_COMPOSER_FOCUS_CEILING = 4` — threshold above which composer-structure hits suppress the focused-mode classification

Both constants are byte-locked by the BATT-06 self-test sentinels (RR-77-08 for the ceiling, `self_test_boundary()` drift guards for `MIN_HEADER_HITS`). Canonical explanation: [CONFIGURATION.md § Anti-masking measurement invariants](CONFIGURATION.md#anti-masking-measurement-invariants) and [TESTING.md § Anti-masking measurement invariants](TESTING.md#anti-masking-measurement-invariants).

---

## See also

- [TESTING.md](TESTING.md) — how to run each gate (operational run-detail, pre-commit gates)
- [ARCHITECTURE.md](ARCHITECTURE.md#measurement-subsystem) — measurement subsystem inventory; [CI and pre-commit gate inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory)
- [CONFIGURATION.md](CONFIGURATION.md#anti-masking-measurement-invariants) — anti-masking invariant rationale
- [requirements-traceability.md](requirements-traceability.md) — canonical residual ownership and coverage headline
- [testing-agents-headlessly.md](testing-agents-headlessly.md#8-script-inventory) — script inventory and stream-json capture method
