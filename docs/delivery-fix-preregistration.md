# Pre-Registration — Does the final-message rule deliver the whole document?

**Id:** `delivery-fix` · **Registered:** 2026-09-28, before any run under this id.
**Binding:** fix, prompts, repeats, transport, definitions and the success rule are fixed below.

---

## 1. The defect and the fix

[`docs/delivery-reading.md`](delivery-reading.md): the caller receives only the agent's **final**
message. In 6 of 20 runs the agent's reasoning and document together reached the per-message
output limit — `stop_reason=max_tokens` at exactly 64,000 output tokens, of which the document
was 2,149 to 4,550 words — the harness told it to resume, the document continued in a new
message, and in 5 of the 6 the caller received only that continuation.

The document is a small share of the budget; extended thinking is most of it. **Shortening the
document would therefore not fix this and would cost fidelity**, which is the one thing a fix
here may not do. The fix is instead a rule, `d29637f7` on branch `delivery-fix`, inserted into
`shared/spine/SKILL-body.md` before "Open the output template once":

> **Your final message is the whole deliverable — never a fragment of it.** Whoever dispatched
> this analysis receives your final message and nothing else: text in any earlier message never
> reaches them. Your reasoning and the document share one output budget per message, so a long
> analysis can be cut off mid-document by the output limit. If that happens, finish the document
> where it broke off, then send **one more message containing the complete six-section document
> again, verbatim, from its first heading to its last line** — every section, table, chain and
> confidence line exactly as written, nothing condensed, summarised or omitted. Do the same if
> you are told the reader received only part of it. Re-sending text you have already written
> needs no new reasoning; do not re-derive anything while you do it.

## 2. Design

- **Body:** the plugin tree at `d29637f7`.
- **Prompts:** the four whose runs lost sections: `TB-02`, `TB-03`, `TB-04`, `TB-06`, verbatim
  from `tests/trackb-catalog-v9.13.md`.
- **Pass 1:** 3 repeats each, 12 runs. **Pass 2**, only if pass 1 produces fewer than 3
  cut-off events: 3 more repeats each, 12 more runs. No further passes.
- **Transport and capture:** identical to `delivery` — empty working directory, session
  persistence on, the agent's own transcript copied beside each run; routing misses and transport
  failures retried at most twice.

## 3. Definitions

- **Cut-off event:** a run in which some agent message stopped with `stop_reason=max_tokens`.
- **First rendering:** the text messages from that first cut-off message up to, but not including,
  the next message that follows a tool call or a message sent to the agent from outside —
  i.e. the document as first written, across its continuation.
- **Received:** what the caller receives (`received_by_caller`: the completed
  `task_notification` summary, else the framed hand-back).
- **Whole with fidelity:** the received document carries every contract section the first
  rendering carries, **and** its word count is at least **90%** of the first rendering's.

## 4. Success rule, fixed now

**The fix is operational** if at least 3 cut-off events occur across the passes run, and **every**
cut-off event is *whole with fidelity*.

**Not operational** if any cut-off event is not. **Inconclusive** if fewer than 3 cut-off events
occur in 24 runs — the fix was not exercised.

**Reported, not decided:** runs without a cut-off whose caller still lost sections (a regression
the rule must not cause); a re-send that itself hits the output limit; the fidelity ratio of every
cut-off event.

## 5. What this cannot establish

- **Twelve to twenty-four runs, four prompts.** "Operational" means the rule worked on every
  cut-off seen, not that it cannot fail.
- **No concurrent control arm.** The reference is the frozen `delivery` corpus on the same
  prompts and transport, one day earlier, judged by this document's own §3 before any run here:
  **0 of its 6 cut-off events is whole with fidelity** (fidelity 0.26–0.92). Its sixth,
  `TB-10.r2`, carried every section only because the agent re-sent a *condensed* document — 78%
  of the words — which is exactly the fidelity loss the 90% floor exists to catch.
- **Word count is a floor on fidelity, not proof of it.** Section presence plus a 90% word floor
  catches truncation and summarising; it does not certify the re-send verbatim.

## 6. Outcome and deviation — v1 is not operational

**Deviation, stated:** the run was stopped after its first scored run. §4 makes a single cut-off
event that is not *whole with fidelity* sufficient for **not operational**, so no later run could
change the verdict; the remaining 11 generations would have spent budget without bearing on it.

**The deciding event, `TB-02.r1`:** the agent hit the output limit at 6,872 words, finished the
tail (317 words) and **ended its turn** — it re-sent only after the main session reported
receiving "the tail end". The re-send then reproduced the six sections almost word for word
(166→166, 870→870, 927→925, 1,615→1,610, 401→401, 666→617) but **dropped all 2,478 words of
process output** — the assumption audit, adversarial pass, self-audit scan and Self-Audit Gate
verdicts — because the rule named "the complete six-section document". Fidelity 0.651: **LOST**.

Both failures shape v2, registered separately in
[`docs/delivery-fix-2-preregistration.md`](delivery-fix-2-preregistration.md).
