# Testing Agents Headlessly: stream-json + jq Subagent Capture

> **TL;DR:** To verify that a Claude Code agent (subagent) actually ran in a
> headless `claude -p` session, use `--output-format stream-json --verbose` and
> parse the JSONL event stream with `jq` — `--output-format text` only surfaces
> the orchestrator's synthesized final answer, not the subagent's verbatim output.

This is the canonical, in-repo home for the routing-test methodology. The capture
technique described here is the reference pattern inherited by all measurement
scripts in `scripts/`. See [§8 Script inventory](#8-script-inventory) for the
current set of scripts and their CI status.

---

## 1. Why `--output-format text` doesn't work

When you invoke `claude -p "<prompt>"` with the default `--output-format text`,
stdout returns a single string: the **orchestrator's** synthesized final
response. If the orchestrator delegated the work to a subagent (via the `Task`
tool), the subagent's analysis — its 6-section output document, its section
headers, its verbatim reasoning — is consumed inside the orchestrator's context
and folded into a paraphrase. From `text` output alone you cannot prove that
delegation actually happened, nor inspect what the subagent said.

This was discovered the hard way in Phase 28 (v3.0 Behavioral Validation): early
routing batteries grepped stdout for agent section headers, saw nothing, and
falsely concluded the agent never ran. The fix is `--output-format stream-json`,
which emits one JSON event per line and surfaces every internal step —
including the `Task` tool_use that selects a subagent.

See `.planning/RETROSPECTIVE.md` (v3.0 section "Patterns Established" and "Key
Lessons") for the full discovery context.

---

## 2. The exact flag set

```bash
claude -p \
  --plugin-dir "$(pwd)/first-principles" \
  --no-session-persistence \
  --output-format stream-json \
  --verbose \
  --permission-mode bypassPermissions \
  "<prompt>"
```

Flag-by-flag:

- `--plugin-dir <path>`: loads the plugin so its agents are auto-discoverable
  for routing. Required when testing a plugin-shipped agent.
- `--no-session-persistence`: fresh session per invocation; no conversation
  state leaks between prompts in a battery.
- `--output-format stream-json`: emits JSONL events (one event per line) instead
  of a single synthesized string.
- `--verbose`: ensures `Task` tool_use events appear in the stream. Without it,
  some internal events are suppressed.
- `--permission-mode bypassPermissions`: required for non-interactive Task tool
  calls — see [§5](#5---permission-mode-bypasspermissions----why-its-load-bearing).

**No `--agent` flag.** Pinning an agent bypasses the routing decision. For a
routing test, leave the agent unpinned — that is what is being measured.

---

## 3. The two-signal DELEGATE-detection rule

Score a single prompt as **DELEGATE** if EITHER signal fires; **NO-DELEGATE**
otherwise. Both signals are needed because each catches a different failure
mode: Signal A proves the orchestrator structurally selected the agent; Signal
B proves the agent actually ran its methodology end-to-end.

### Signal A — `Task` tool_use with `subagent_type: first-principles`

The orchestrator emits a `Task` tool_use event whose input names the chosen
subagent. Targeted jq query (preferred):

```bash
jq -r '.. | objects | select(.name? == "Task") | .input? // empty | tostring' "$file" \
  | grep -ciE 'first-principles'
```

Raw-text regex fallback (when the stream uses non-standard event shapes):

```bash
grep -ciE '"(subagent_type|agent[_-]?name|agent_id)"[[:space:]]*:[[:space:]]*"first-principles' "$file"
```

A non-zero count fires Signal A.

### Signal B — ≥ 4 of 6 expected agent section headers

The first-principles agent emits a **6-section output document**: Problem
Essence, Assumptions Table, Ground Truths, Derivation Chains, Abandoned
Reasoning, and Conclusion — in that fixed order (per
`shared/spine/references/output-template.md`). Count Markdown headings that
match the canonical section names:

```bash
jq -r '.. | .text? // empty' "$file" \
  | grep -ciE '^#+[[:space:]]*(.*(essence|assumption|ground[- ]?truth|derivation|abandoned|dead[- ]?end|conclusion|verdict))'
```

A count ≥ 4 fires Signal B. (Threshold is 4 of the 6 output sections rather
than all 6 to tolerate partial outputs and section-name variants.)

### Verdict

`DELEGATE` if Signal A OR Signal B fires; `NO-DELEGATE` otherwise.

This two-signal rule is implemented in `scripts/check-routing.py`. The merged
battery (`scripts/check-routing-battery.py`, CI gate BATT-06) extends this
methodology with a second focused-output signal. The focused-output classifier
in `scripts/_battery_core.py` uses the constants `MIN_HEADER_HITS=2` and
`_COMPOSER_FOCUS_CEILING=4` to control technique-detection sensitivity and
anti-masking behavior — see [`TESTING.md#anti-masking-measurement-invariants`](TESTING.md#anti-masking-measurement-invariants)
for the canonical invariant documentation.

---

## 4. jq extraction strategies

Two queries, used in order:

- **Targeted (assistant content):**
  ```bash
  jq -r '.. | objects | select(.type? == "text") | .text // empty'
  ```
  Matches the canonical assistant-text event shape. Use first.

- **Broad fallback (any text node):**
  ```bash
  jq -r '.. | .text? // empty'
  ```
  Recursively walks the event stream for any `.text` field. Use when the
  targeted query returns empty — some event shapes emit text in non-standard
  positions (e.g. nested inside tool_result blocks).

The broad fallback exists because `stream-json` event shapes have varied
across Claude Code versions; the targeted-then-broad fallback is resilient
without losing precision when the canonical shape applies.

---

## 5. `--permission-mode bypassPermissions` — why it's load-bearing

Non-interactive headless sessions have no UI surface for tool-use approval
prompts. When the orchestrator wants to invoke the `Task` tool to delegate to
a subagent, Claude Code asks for permission. In an interactive session you
click "approve." In a `claude -p` session with no permission mode set, the
prompt blocks indefinitely — the harness hangs and the test never completes.

`--permission-mode bypassPermissions` pre-approves tool use for the session,
allowing the `Task` call to proceed. Discovery: Phase 28. Documented here so
no future author repeats the loss of a debugging afternoon.

---

## 6. `--bare` vs `--no-session-persistence`

Two superficially-similar flags with different effects:

- `--bare` strips OAuth context. The session has no plugin authentication.
  Unsuitable when the agent under test is loaded via a plugin that requires
  auth context (most plugin-shipped agents).
- `--no-session-persistence` keeps OAuth context but does not persist
  conversation state between invocations. Each `claude -p` call is a fresh
  session with full auth.

For routing batteries: use `--no-session-persistence`. `--bare` is a fallback
only when OAuth misbehaves and the agent is purely local.

---

## 7. Decision tree

```text
Do you need to verify the subagent actually ran?
├── Yes → --output-format stream-json --verbose
│         └── Parse with jq via the 2-signal rule above
└── No  → --output-format text is fine
          └── You'll see only the orchestrator's final answer
```

If you only need the user-visible answer and don't care whether routing
occurred, `text` is faster and simpler. The moment you need to prove
delegation happened — or inspect what the subagent emitted verbatim — switch
to `stream-json`.

---

## 8. Script inventory

The capture methodology in this doc is implemented across several scripts.
For gate run-commands see
[`TESTING.md#batt-06--check-routing-battery`](TESTING.md#batt-06--check-routing-battery).
For the full CI and pre-commit gate table see
[`ARCHITECTURE.md#ci-and-pre-commit-gate-inventory`](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).

### `scripts/check-routing.py` — developer-tool reference implementation

The original committed Python implementation of the capture method in this
doc. Parses a catalog of P/N prompts, issues each via the locked flag set
above, and scores DELEGATE/NO-DELEGATE using the two-signal rule.

**Not wired into CI.** This is a developer tool for local investigation and
regression testing. Its `--self-test` validates detection logic offline
against mocked event streams; its defaults are `--p-threshold 11`
(P-cases ≥ 11/13 DELEGATE) and `--n-threshold 18` (N-cases ≥ 18/20
NO-DELEGATE), with `--repeat 3 --min-pass 2`.

### `scripts/check-routing-battery.py` — merged dual-signal battery (BATT-06)

The current CI-wired battery. Captures each prompt in
`tests/routing-battery-catalog.md` once and scores **both** the
boundary-discipline signal (DELEGATE/NO-DELEGATE) and the focused-output
signal from the same `.jsonl` file. Wired into CI as **BATT-06** via
`--self-test` (offline deterministic self-check, no live `claude` session).

### `scripts/_battery_core.py` — battery core and detection constants

Houses the shared detection logic, catalog parsers, and transport used by
`check-routing-battery.py`. The authoritative home of the anti-masking
detection constants:

- `MIN_HEADER_HITS = 2` — minimum distinct technique-marker patterns that
  must match before a technique fires in the focused-output classifier.
- `_COMPOSER_FOCUS_CEILING = 4` — composer-structure hit ceiling controlling
  the `classify()` anti-masking override.

These constants are byte-locked. See
[`TESTING.md#anti-masking-measurement-invariants`](TESTING.md#anti-masking-measurement-invariants)
for the canonical invariant documentation.

### Two-layer Step 0 harness

The Step 0 harness measures the agent body's technique-selection logic at two
independent layers:

- **`scripts/check-step0-emulator.py`** (STEP0-08) — offline phrase-detection
  classifier. Reads the `**Phrase detection rules**` table from
  `shared/spine/SKILL-body.md` and compiles it into a deterministic regex
  classifier. No live `claude` session required. CI gate:
  [`TESTING.md#step0-08--check-step0-emulator`](TESTING.md#step0-08--check-step0-emulator).

- **`scripts/check-step0-live.py`** (STEP0-06) — live agent-body harness.
  Forces Step 0 classification through the approach-② `_wrap_for_bypass`
  bypass channel over the `stream-json` transport. Scores K-of-N results
  across the 12-row `tests/step0-fixture-catalog.md`. CI gate (offline
  self-test only):
  [`TESTING.md#step0-06--check-step0-live`](TESTING.md#step0-06--check-step0-live).

### Deprecated shims

`scripts/check-sub-skill-routing.py` and `scripts/check-focused-output.py`
are **deprecated thin shims** that translate old per-signal CLI flags onto the
merged battery's namespaced flags and delegate to `check-routing-battery.py`.
They exist for backwards compatibility only; new callers should invoke
`scripts/check-routing-battery.py` directly.

---

## 9. History / further reading

- **Pattern origin:** Phase 28 (v3.0 Behavioral Validation) — `--output-format
  text` discovery and the `--permission-mode bypassPermissions` discovery.
- **Operationalized:** Phase 29 (v3.0 Routing Catalog Rewrite) — locked the
  flag set and codified the two-signal detection rule in a bash harness.
- **Hardened:** Phase 30 (v3.1 Routing Quality Patch) — promoted the bash
  harness into the version-controlled `scripts/check-routing.py` and
  documented the pattern in this file.
- **Merged battery:** Phase 67–69 (v4.3 Unified Routing/Output Battery) —
  `check-routing-battery.py` and `_battery_core.py` introduced; the two
  deprecated shims reduced to thin delegating wrappers.
- **Two-layer Step 0 harness:** Phases 70–75 (v5.0–v5.1) —
  `check-step0-emulator.py` (STEP0-08) and `check-step0-live.py` (STEP0-06)
  added.
- **Cross-AI methodology context:** `.planning/RETROSPECTIVE.md` (v3.0 section
  "Patterns Established" and "Key Lessons").

---

## 10. Rerun-to-stability (v3.4)

The v3.1 harness ran each catalog prompt once. Phase 31 measured a ±3 P-prompt
swing in adjacent same-session runs against a byte-identical agent body (7/8 → 4/8
in under 30 minutes). Single-run verdicts cannot reliably attribute a FAIL to a
specific commit — the noise envelope is too wide.

v3.4 fixes this at the runner level with `--repeat N --min-pass K`: each prompt
runs N times and counts as PASS only if the expected verdict occurs in at least K
of those N runs. Session noise is absorbed without changing the P/N thresholds.

### Default (best-of-3)

```bash
python3 scripts/check-routing.py --catalog tests/routing-catalog.md
```

No extra flags needed. The defaults are `--repeat 3 --min-pass 2`: each prompt
runs 3 times; it passes only if the expected verdict occurs in ≥ 2 of 3 runs.
Wall-clock time: approximately 45–70 minutes for the full catalog.

### When to override

- `--repeat 1` — fast smoke check before a live coding session; same behavior as
  v3.1; **not for ship decisions** (noise envelope unmitigated).
- `--repeat 5 --min-pass 3` — high-confidence shipping run; requires a strict
  majority (3 of 5); approximately 2 hours wall-clock.

If `--min-pass` exceeds `--repeat` the script exits with code 2 before any prompt
runs — a deliberate guard against misconfiguration.

### What changes in the output

**`scores.tsv`** switches to per-run rows (v3.4 format). Each prompt produces N
rows with the header:

```
id	run	expected	actual	match
```

One row per run, `match` is 1 (match) or 0 (mismatch). All runs for a prompt are
grouped together in catalog order.

**`verdict.txt`** retains its summary lines unchanged (`BATTERY: PASS`, `P: x/y
N: x/y`) and appends a per-prompt K/N block below them:

```
Per-prompt K/N (best-of-3, K=2):
  P1: 3/3 PASS
  P2: 2/3 PASS
  N1: 3/3 PASS
  ...
```

The summary lines are always the first two lines — no existing parser that reads
only the summary is broken.

### Self-test

```bash
python3 scripts/check-routing.py --self-test
```

Validates the K-of-N aggregation logic entirely in-process (no `claude` calls).
Covers: legacy N=1 parity, 2/3 PASS, 1/3 FAIL, and K>N invalid-args rejection.

Canonical best-of-3 baseline: `tests/routing-baseline-v3.4.md`.
