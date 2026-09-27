# Pre-Registration — How much of the agent's document reaches the caller?

**Id:** `delivery` · **Registered:** 2026-09-27, before any run under this id.
**Binding:** prompts, repeats, body, transport, capture and definitions are fixed below. This
is a **measurement**, not an A/B: it decides no body change. A fix it motivates is tested under
its own id.

---

## 1. Why

[`docs/abandonment-phase1-reading.md`](abandonment-phase1-reading.md) found that most
"abandonment" was **delivery failure**: 4 of 20 runs whose document did not reach the main
session whole. One cause is fixed — the agent delegating to itself, blocked at `749da354`. The
other three had no delegation, and could not be diagnosed because `--no-session-persistence`
discarded the agent's own transcript.

**The mechanism is already demonstrated in isolation.** A probe told the agent to write `ALPHA`,
call a tool, then write `OMEGA`. Its own transcript holds all three steps; the main session's
hand-back holds `OMEGA` and nothing else, and no subagent text was streamed. **A subagent's
hand-back is its final text message only.** Any document the agent writes across more than one
message, with a tool call between, arrives as its last part.

What is not known is **how often** the current body does that. This run measures it.

## 2. Design

- **Body:** the plugin tree at `58524e13` (self-delegation blocked), from a detached worktree.
- **Prompts:** `TB-01` … `TB-10`, verbatim from `tests/trackb-catalog-v9.13.md` — the family
  Phase 1 scored, so its 4-in-20 delivery failures are the reference.
- **Repeats:** 2 per prompt, 20 runs, sequential.
- **Transport:** as Phase 1 — `claude -p --model claude-sonnet-5 --plugin-dir <body>
  --output-format stream-json --verbose --permission-mode bypassPermissions`, from an **empty
  working directory** — **except that `--no-session-persistence` is dropped**, so the agent's
  own transcript (`~/.claude/projects/<cwd>/<session>/subagents/agent-*.jsonl`) survives and is
  copied beside each run's raw capture.
- **Retries:** a routing miss or a transport failure is retried, at most twice. No other attempt
  is retried.

## 3. Definitions

For each dispatched attempt, with the agent's own transcript in hand:

- **Emitted text:** every text block the agent wrote, in order, from its own transcript.
- **Delivered document:** what the main session received (the Phase 1 extractor).
- **Stranded words:** words of emitted text in messages *other than the last* — text the
  hand-back structurally cannot carry.
- **Delivery status**, first match wins:
  - `interrupted` — the delivered document is under 120 words;
  - `split` — at least 120 stranded words, and at least 4 of the 6 contract sections appear in
    the emitted text but fewer than 4 in the delivered document (the document existed and did not
    arrive);
  - `whole` — otherwise.
- **Delivery failure rate:** (`interrupted` + `split`) / dispatched attempts. This is reported as
  its **own number**, never folded into abandonment or conformance.
- **Abandoned (for reference):** fewer than 4 sections even in the emitted text — the agent did
  not write the contract at all, which delivery cannot explain.
- **Self-delegation:** any `Agent`, `SendMessage` or `ListAgents` call in the agent's own
  transcript. Expected 0 after `749da354`; any non-zero value is a finding.

## 4. What is reported

The delivery failure rate with its N, beside Phase 1's 4 of 20; the count of each status; for
every `split` attempt, how many messages the document spans and which tool calls separate them;
the abandonment count; and the self-delegation count. **A recorded reading, never a gate.**

## 5. What this cannot establish

- **Twenty runs, one prompt family, one model, today.**
- **Not a comparison.** Phase 1's figure is a reference, not a control arm: it ran on a
  different body, and before self-delegation was blocked.
- **The probe shows the mechanism exists; this run shows its rate.** Whether an instruction such
  as "your final message is the complete document" removes it is a separate, pre-registered test.
