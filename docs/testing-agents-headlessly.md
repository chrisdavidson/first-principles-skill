# Testing Agents Headlessly: stream-json + jq Subagent Capture

> **TL;DR:** To verify that a Claude Code agent (subagent) actually ran in a
> headless `claude -p` session, use `--output-format stream-json --verbose` and
> parse the JSONL event stream with `jq` — `--output-format text` only surfaces
> the orchestrator's synthesized final answer, not the subagent's verbatim output.

This is the canonical, in-repo home for the routing-test methodology used by
`scripts/check-routing.py` and `tests/routing-catalog.md`. Future agent authors:
inherit this pattern; do not re-derive it.

---

## 1. Why `--output-format text` doesn't work

When you invoke `claude -p "<prompt>"` with the default `--output-format text`,
stdout returns a single string: the **orchestrator's** synthesized final
response. If the orchestrator delegated the work to a subagent (via the `Task`
tool), the subagent's analysis — its 5-phase output, its section headers, its
verbatim reasoning — is consumed inside the orchestrator's context and folded
into a paraphrase. From `text` output alone you cannot prove that delegation
actually happened, nor inspect what the subagent said.

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
  calls — see §6.

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

The first-principles agent emits a 6-section output document. Count Markdown
headings that match the canonical section names:

```bash
jq -r '.. | .text? // empty' "$file" \
  | grep -ciE '^#+[[:space:]]*(.*(essence|assumption|ground[- ]?truth|derivation|abandoned|dead[- ]?end|conclusion|verdict))'
```

A count ≥ 4 fires Signal B. (Threshold is 4/6 rather than 6/6 to tolerate
partial outputs and section-name variants.)

### Verdict

`DELEGATE` if Signal A OR Signal B fires; `NO-DELEGATE` otherwise.

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

## 8. Reference implementation

`scripts/check-routing.py` is the committed Python implementation of every
pattern in this doc. It parses a catalog of P/N prompts, issues each via the
locked flag set above, and scores DELEGATE/NO-DELEGATE using the two-signal
rule. Its `--self-test` mode validates the detection logic offline against
mocked event streams — no `claude` invocation required.

```bash
# Self-test the detection logic (no live claude calls):
python3 scripts/check-routing.py --self-test

# Run the live battery against the checked-in catalog:
python3 scripts/check-routing.py --catalog tests/routing-catalog.md
```

The original bash harness pattern is in
`.planning/milestones/v3.0-phases/29-routing-catalog-rewrite/29-01-PLAN.md`.

---

## 9. History / further reading

- **Pattern origin:** Phase 28 (v3.0 Behavioral Validation) — `--output-format
  text` discovery and the `--permission-mode bypassPermissions` discovery.
- **Operationalized:** Phase 29 (v3.0 Routing Catalog Rewrite) — locked the
  flag set and codified the two-signal detection rule in a bash harness.
- **Hardened:** Phase 30 (v3.1 Routing Quality Patch) — promoted the bash
  harness into the version-controlled `scripts/check-routing.py` and
  documented the pattern in this file.
- **Cross-AI methodology context:** `.planning/RETROSPECTIVE.md` (v3.0 section
  "Patterns Established" and "Key Lessons").
