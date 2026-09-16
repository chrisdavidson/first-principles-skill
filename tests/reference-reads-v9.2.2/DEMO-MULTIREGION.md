# Demonstration: multi-region database latency, run through the first-principles plugin at v9.2.2

**What this is.** A scenario authored for `first-principles:first-principles`, run live against the
working tree at plugin version **9.2.2**, with the agent's full output, an independent verification
of its factual claims, and an assessment of what the machinery actually did. This is a demo
artifact, not project documentation — deliberately untracked, outside every gate's scan scope.

## Provenance

Stated first, because a live-run result is worthless without the transport that produced it
(`memory/agent-testing-reads-plugin-cache.md`: the in-session Agent tool reads a frozen plugin
cache, not the working tree).

| Fact | Value |
|---|---|
| Repository HEAD | `da59f3e` |
| Plugin version | **9.2.2** — all 17 stamps agree (`check-version-stamps.py` PASS, self-test exit 0) |
| Version verified before the run | yes — `.claude-plugin/marketplace.json` `"version": "9.2.2"` read first |
| Agent body | `first-principles/agents/first-principles.md`, 787 lines, `maxTurns: 60` |
| Gate state at run time | `FIREWALL: GREEN (26/26)` |
| Transport | `docs/testing-agents-headlessly.md` §2 flag set, verbatim |
| Plugin surface | `--plugin-dir first-principles` — the working tree, not the installed cache |
| Model | pinned `ANTHROPIC_MODEL=claude-opus-5` |
| `claude` CLI | 2.1.268 |
| Invocations | 1 generation. No judge invocation — a demonstration, not a scored measurement. |
| Wall clock / cost | 742 s (12 min 22 s) / $3.02 |
| Capture | 94 JSONL events, sidechain included |

Exact command:

```bash
ANTHROPIC_MODEL=claude-opus-5 claude -p \
  --plugin-dir "$(pwd)/first-principles" \
  --no-session-persistence \
  --output-format stream-json \
  --verbose \
  --permission-mode bypassPermissions \
  "$(cat prompt.txt)"
```

No `--agent` flag: the agent was left unpinned so routing was exercised rather than bypassed.

## The scenario

Authored for this demonstration, in no committed catalog. Built to exercise four parts of the
methodology rather than merely to be realistic — and deliberately in a different shape from the
previous demo (`DEMO-first-principles-ticket-triage.md`), which was a cost/accuracy trade-off.
This one is a **physics-bounded architecture decision**:

1. **A fact with a hard physical floor** — the speed of light in fibre. This is what the
   `theoretical-limit` technique exists for, and it is one of the project's weaker measured
   residuals (RR-108-05, S-P14, 0/5 on the v7.13 live baseline). Worth seeing whether it fires.
2. **An embedded false analogy** — "the CDN cut asset load times 80%, so moving the database
   closer will do the same." The trap is that a CDN works *because assets are immutable*; a
   mutable replica can be stale or it can make the writer wait, and the scenario's own compliance
   requirement forbids the first.
3. **A quantity the decision depends on that nobody has measured** — what share of the 780 ms is
   network round-trip versus query and application time.
4. **A self-defeating constraint** — synchronous replication is proposed *because* stale reads are
   a compliance problem, but synchronous replication is exactly what puts a ~200 ms penalty on
   every commit, including the Boston users who are currently fine.

The prompt, verbatim:

> We run a B2B SaaS product on a single primary Postgres in AWS us-east-1. Our Sydney customers
> are our fastest-growing segment and they complain constantly that the app "feels slow" — our p95
> page-interaction latency from Sydney is 780 ms against 180 ms from Boston. Last year we put our
> static assets behind a CDN and asset load times dropped about 80 percent, so our VP of
> Engineering wants to apply the same principle to the database: go multi-region active-active
> with a Postgres cluster in ap-southeast-2 and synchronous replication, on the reasoning that
> moving the data closer to the user will cut Sydney latency by a similar proportion. The project
> is scoped at two engineers for four months. Our workload is roughly 85 percent reads by request
> count, but we have never instrumented what share of that 780 ms is network round-trip versus
> query and application time. A stale read that shows a customer an out-of-date invoice is a
> compliance problem for us. Should we do it?

### Pre-run classification (offline, deterministic)

Before spending anything live, the scenario was classified on the offline Step 0 emulator, which
parses the phrase table straight out of the canonical agent body:

```
$ python3 scripts/check-step0-emulator.py --prompt "$(cat prompt.txt)"
full-composer
```

`full-composer` means the prompt trips none of the single-technique trigger rules, so the run
exercises the whole five-phase path with companion techniques selected internally.

## What the run did

Full `tool_use` census across every event, sidechain included:

```
Agent: 1   (subagent_type = first-principles:first-principles)
Read: 2
WebFetch: 10
Bash: 1
ToolSearch: 1
```

**Routing (Signal A) fired**: the orchestrator structurally selected
`first-principles:first-principles` rather than answering inline.

**Both reference files were opened** — this is the notable one:

```
first-principles/agents/references/output-template.md
first-principles/agents/references/validation-rubric.md
```

Ten WebFetches, all to real, checkable sources:

| Source | Used for |
|---|---|
| `en.wikipedia.org/wiki/Optical_fiber` | GT-1, fibre signal speed |
| `cloudping.co` (and `/grid`, which 404'd) | GT-3, measured us-east-1 ↔ ap-southeast-2 RTT |
| `postgresql.org` — replication comparison, WAL config, admin functions, warm standby | GT-4 through GT-7 |
| `docs.pgedge.com/spock_ext/conflicts` | GT-8, multi-master conflict resolution |
| `rfc-editor.org/rfc/rfc8446` | GT-15 — **opened, claim not located, failure record written** |
| `docs.aws.amazon.com/global-accelerator/...` | A11 — **opened, claim not located, failure record written** |

## Independent verification

Everything below was checked against the source or recomputed from scratch, not taken from the
run's own self-report.

### GT-1 — fibre signal speed: **verified verbatim**

Independently fetched `en.wikipedia.org/wiki/Optical_fiber`. Both literals the run quoted appear
exactly as stated:

- *"a signal using optical fiber for communication will travel at around 200,000 kilometers per second"* ✓
- *"a core of doped silica with an index around 1.4475"* ✓

### GT-2 — great-circle distance: **reproduced independently**

Computed by haversine **before** the run was launched, from Sydney (−33.8688, 151.2093) to Ashburn
VA (39.0438, −77.4874): **15,674 km**. The run reported 15,674 km. Exact match.

The run marked this `GT-2?` anyway, because its coordinates came from recall rather than a
gazetteer. That is the correct call — the arithmetic being right does not make the inputs sourced.

### C2's theoretical limit: **arithmetic reproduces**

```
2 × 15,674 km ÷ 200,000 km/s = 156.7 ms
```

The run stated ≈157 ms. ✓ Computed independently at a second refractive index (n = 1.4675, giving
204,288 km/s) the floor is 153.4 ms; with a realistic 1.4× route factor it rises to ~215 ms. The
measured 201.34 ms sits inside that envelope, so the run's "measured exceeds the law-permitted
floor by ~44 ms" is physically coherent.

### C6's estimate: **reproduces, and matches an independent derivation**

I derived this before reading the run's answer: Boston's network floor is ~9 ms, so of its 180 ms
p95 roughly 171 ms is application time; if Sydney's application time is similar, ~609 ms of
Sydney's 780 ms is network, which at ~215 ms RTT is ≈2.8 serial round trips.

The run's bracket, independently: 600 ÷ 220 = 2.73, 600 ÷ 175 = 3.43, central 600 ÷ 195 = 3.08. All
three recompute exactly. Same conclusion, reached by a different decomposition.

This is the load-bearing insight of the whole analysis — **the gap is on the client-to-app leg,
which the database does not sit on** — and it was reached, not pattern-matched.

### Mechanical detector: **clean on every flag**

`scripts/check-quality-harness.py --detect-defects` over the analysis document (sections 1–6):

| Column | Value |
|---|---|
| `conclusion_claims` | 7 |
| `untraced_claims` / `untraced_flag` | **0 / 0** |
| `verdict_cells` / `nonconforming_verdict_cells` / `verdict_flag` | 20 / **0** / 0 |
| `chain_blocks` / `malformed_chain_blocks` / `chain_flag` | 11 / **0** / 0 |
| `dependency_cycles` | 0 |
| `ungrounded_chains` | 0 |
| `selfaudit_disagreements` | **0** |

The agent's own closure ledger self-reported *"7 claims … 0 claims untraced."* The independent
mechanical detector returns 7 and 0. **Self-report and detector agree** — which is not something
to assume, since making them disagree is exactly what H1–H3 of
`REVIEW-agent-improvement-opportunities.md` are about.

*Correction recorded, because the first reading was wrong.* My first two detector runs returned
15 claims / 8 untraced. Both were extraction artifacts: I had included the orchestrator's
closing commentary ("Decision: No…", the process disclosures) after section 6, whose bold-colon
lead-ins the extractor reads as Conclusion claims. Cutting at the end of section 6 — the actual
analysis document — gives 7 / 0. The inflated figures were mine, not the run's.

## Assessment

### What worked

**The false analogy was killed, not absorbed.** A1 ("moving data closer cuts latency by roughly the
CDN's 80%") is the prompt's central premise. It is marked **Discard** in the assumptions table, and
C4 states the reason as a mechanism rather than a dismissal: a CDN escapes the consistency cost
only for content that is never rewritten. The analogy also appears in section 5 as an explicit dead
end — *"it uses an analogy as evidence, and the premise it needs — immutability — is false for a
database."*

**The theoretical-limit technique fired, and mattered.** C2 is a genuine ceiling argument: no
product, protocol or configuration puts a cross-region synchronous commit under ~150 ms, because
signal speed bounds it. It also correctly reports the ~44 ms of headroom between the physical floor
and the measured RTT as the *only* engineering-addressable part — a distinction a weaker analysis
would blur.

**It found the question behind the question.** The prompt asks "should we move the database." The
analysis answers that (no) and then relocates the actual problem: the 600 ms gap is ~3 serial
client-to-app round trips, a leg the database does not sit on. The recommendation is consequently
"instrument first, then cut round trips" — not the proposed migration, and not merely a refusal.

**The self-defeating constraint was caught.** C8: a low-latency active-active design resolves write
conflicts by last-write-wins (GT-8, quoted from pgEdge Spock docs), which produces exactly the
silently-overwritten invoice state the compliance requirement forbids. The design defeats its own
motivation.

**Provenance discipline held under failure.** Three sources were opened and did *not* support the
claim being made of them. In all three the run wrote a Phase 3 failure record and kept the `?`
rather than quietly asserting the claim:
- `cloudping.co/grid` → HTTP 404, fell back to the site root and said so.
- RFC 8446 → opened, the one-round-trip wording was not located → `citation does not support the claim`, GT-15 stays `?`.
- AWS Global Accelerator → opened, it confirms anycast routing but says nothing about edge handshake termination → A11 stays flagged.

The third is the impressive one: the doc *sounded* like it would support the claim, and the run
refused to let it.

**8 of 15 ground truths carry `?`.** Including ones nothing forced it to mark — GT-10 ("the app
tier is in us-east-1") is flagged as *inferred, not stated*, which is true of the prompt.

**Confidence lines and verdict vocabulary are correct throughout.** Every chain carries a
`**Confidence:**` line naming its weakest link and what would raise it. Every self-audit verdict
block uses the rubric's real vocabulary (`Quoted span` / `Band: Rigorous|Sound`). Criterion 5 was
scored **Sound, not Rigorous**, with the reason given — one Conclusion claim rests on no HIGH
chain. The run marked itself down where the rubric required it.

### What did not

**One fabricated premise in a process disclosure.** The Step 0 disclosure reads: *"the phrase table
matches 'pre-mortem' and 'second-order' in your list of things to cover."* The prompt contains
neither word, and no list of techniques — verified: `grep -ic` returns 0 for "pre-mortem",
"second-order", "premortem" and "technique". The classification it landed on (`full-composer`) is
the same one the offline emulator gives, so the *outcome* is right; the stated reason for it
describes a prompt that was never sent. A reader auditing the run would be checking a premise that
does not exist.

This is a real defect and it sits in the one place the methodology's own discipline does not reach:
process disclosures are prose *about* the run, not a chain with ground truths, so nothing in the
Self-Audit Gate or the mechanical detector scores them.

**MEDIUM overall, honestly.** The headline verdict is MEDIUM because the recommended path rests on
GT-9?, GT-10? and GT-14? until the instrumentation runs. That is the correct rating and the run
says so — but it means the deliverable is "here is what to measure first," not "here is the answer."
For this scenario that is the right shape; for a reader wanting a decision it is worth naming.

### Bearing on backlog 999.88

> **CORRECTED 2026-09-12, after this section was first written.** The original text called this
> run a second draw from an unchanged surface and concluded the failure was "intermittent, not
> deterministic." That was **false**, and the error was load-bearing. Commit `956d033`
> — *"feat(999.88): make output-template.md a read imperative in the agent body"* — landed
> **between** the two runs, and is an ancestor of this run's commit:
>
> ```
> $ git show 3c3ed42:first-principles/agents/first-principles.md | grep -c "Use Read on the"
> 0
> $ git show da59f3e:first-principles/agents/first-principles.md | grep -c "Use Read on the"
> 1
> $ git merge-base --is-ancestor 956d033 da59f3e && echo ancestor
> ancestor
> ```
>
> The body was NOT unchanged. What follows is the corrected reading.

999.88 records that nothing in the agent body instructed the agent to open `output-template.md`,
diagnosed from a run at HEAD `3c3ed42` that opened neither reference file. The entry has since
shipped in three plans, and `956d033` is the commit that landed its fix: a read imperative at the
head of `## Output format` (line 241 of the emitted body at `da59f3e`), naming the tool —
*"Use Read on the [First Principles Analysis Output Template]…"* — in Phase 3's voice.

**This run, at `da59f3e`, is the *after* reading of that fix.** It opened both reference files.

The two runs are therefore a **before/after pair at N=1 each**, not two draws from one surface:

| | `3c3ed42` — before `956d033` | `da59f3e` — after |
|---|---|---|
| Read of `output-template.md` | none | yes |
| `Confidence:` lines | absent (finding P4) | present on every chain |
| Verdict vocabulary | invented (finding P3) | correct `Rigorous`/`Sound` |
| Nonconforming verdict cells | 20/20 | **0/20** |

The correlation between reading the template and emitting what the template requires is what the
pair shows, and it supports the original diagnosis. What it does **not** show is a rate, in either
direction — one capture per arm cannot establish one.

**The consequence for the entry's falsification is the same either way, and it is the one part of
the original text that survived.** "Re-run and assert the capture contains a `Read`" is
insufficient: a single draw cannot distinguish a fixed body from a lucky run, nor a regression
from an unlucky one. It must be K-of-N — this project's own standing rule for every live reading
(`docs/v8.7-constraint-teardown.md` governing record §2 item 3), which demotes even a K-of-5
result to a recorded observation rather than a gate.

999.88's Falsification paragraph was amended on this basis (quick task `260912-r23`): N ≥ 5 at the
current body, the same N against the body predating `956d033` for the before leg, pass condition
stated as a rate. `tests/reference-reads-v9.2.1/` freezes one draw of the before leg and this run
is one draw of the after leg. Backlog **999.89** owns the `reference_reads` census that is the
instrument for both.

**What this episode is evidence of, beyond the entry.** The false premise here was produced the
same way the project's dominant defect class is: a fact about the tree (the body is unchanged) was
carried forward from a census taken at an earlier commit rather than re-derived at the commit
being written about. The census was correct when taken at `3c3ed42` and wrong by the time it was
cited for `da59f3e`. That is `docs/PROCESS.md`'s stale-claim class exactly, reproduced in an
artifact written to analyse it.

---

# The run's full output, verbatim

Everything below is the agent's output as captured, unedited.

---

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | sync commit can't return until confirmation crosses link | none | n/a |
| C1 | 2 | every write gains ≥1 ~200 ms RTT | none | n/a |
| C1 | 3 | Boston writers pay too | none | n/a |
| C1 | 4 | cannot deliver low write latency to anyone | none | n/a |
| C1 | 5 | [2nd] link degradation stalls commits | A17 (no async fallback configured) | yes |
| C1 | 6 | [3rd] global write-latency/availability regression | none | n/a |
| C2 | 1 | great-circle RTT floor ≈157 ms | none (distance already GT-2?) | n/a |
| C2 | 2 | 201 ms exceeds floor by ~44 ms | none | n/a |
| C2 | 3 | no product can push penalty below ~150 ms | none | n/a |
| C3 | 1 | needs extension, app 2PC, or different DB | none | n/a |
| C3 | 2 | sync (C1 penalty) or async (visibility delay) | none | n/a |
| C3 | 3 | async lets both regions write same row | none | n/a |
| C3 | 4 | collisions settled by rule, e.g. newest timestamp | none | n/a |
| C3 | 5 | low latency or no lost/lagging writes, not both | none | n/a |
| C4 | 1 | write news travels no faster than signal | none | n/a |
| C4 | 2 | remote mutable copy is behind or makes writer wait | none | n/a |
| C4 | 3 | CDN escapes only for non-rewritten content | A2 | already present (A2) |
| C4 | 4 | if DB were immutable, proximity would work | none | n/a |
| C4 | 5 | DB accepts writes; 80% doesn't transfer | none | n/a |
| C5 | 1 | DB-only move puts every query on 200 ms link | A6 | already present (A6 / GT-10?) |
| C5 | 2 | N serial queries gain N×200 ms | none | n/a |
| C5 | 3 | DB-only move makes Sydney slower | none | n/a |
| C6 | 1 | 600 ms difference; server time cancels | A7 | already present (A7 / GT-14?) |
| C6 | 2 | per-RTT delta 175–220 ms | A14, A15 | yes |
| C6 | 3 | 2.7–3.4 RTTs, central 3.1 | none | n/a |
| C6 | 4 | ~3 serial client-to-app RTTs, no DB residual | A16 | yes |
| C6 | 5 | gap is on client-to-app leg | none | n/a |
| C7 | 1 | candidate sources: setup, serial calls, cohort server time | none | n/a |
| C7 | 2 | Resource Timing + Server-Timing separate sources | A18 | yes |
| C7 | 3 | instrumentation costs days | A18 | already present (A18) |
| C7 | 4 | measurement falsifies C6 first | none | n/a |
| C8 | 1 | Sydney node serves invoice omitting US change | A13 | yes |
| C8 | 2 | invoice collision overwritten, not surfaced | none | n/a |
| C8 | 3 | design produces forbidden stale/lost state | none | n/a |
| C9 | 1 | scope: extension, conflict-safe keys, DDL, failure model | A19 | yes |
| C9 | 2 | on-schedule sync design still has C1 penalty | none | n/a |
| C9 | 3 | budget fit is not the deciding question | none | n/a |
| C10 | 1 | app reads primary WAL location after write | A20 | yes |
| C10 | 2 | replica at/past that point replayed prior writes | none | n/a |
| C10 | 3 | gated read sees those writes | none | n/a |
| C10 | 4 | read-your-writes without sync replication | none | n/a |
| C10 | 5 | freshness vs others' writes costs a ~200 ms RTT | none | n/a |
| C10 | 6 | invoice reads go to primary; others local | none | n/a |
| C11 | 1 | weighted totals 110 > 91 > 24 | none | n/a |
| C11 | 2 | compliance and budget drive; no single weight flips | none | n/a |
| C11 | 3 | 85% read share enables local escalation | A10 | already present (A10) |
| C11 | 4 | recommend measure → edge + RTT reduction → escalate | none | n/a |
| C11 | 5 | [2nd] fewer RTTs help every region | none | n/a |
| C11 | 6 | [2nd] freed engineer-months cover the work | A18 | already present (A18) |
| C11 | 7 | [2nd] escalated writes still cross ocean | none | n/a |
| C11 | 8 | [3rd] escalation depends on batched writes | none | n/a |
| C11 | 9 | [3rd] primary-served invoice pages stay slower | none | n/a |

## §6→§4 closure ledger (process output)

```text
- "Do not build synchronous active-active; ... instrument ... edge TLS termination and batched API calls ... LSN-gated read replica only if a measured residual still misses the target" → chains C1, C3, C7, C11 ✓
- "The CDN worked because assets are immutable ... about three serial client-to-app round trips, a leg the database does not sit on" → chains C4, C6 ✓
- "Compliance-sensitive invoice reads stay on the us-east-1 primary ... edge termination with batching may remove only part of the gap" → chains C10, C11 ✓
- "Add a Server-Timing header ... points to query or tenant work" → chains C6, C7 ✓
- "Two engineers for four months is not the deciding question ..." → chains C1, C9 ✓
- "Sydney server time materially above Boston's ... provably immutable issued invoices would make replica-served invoice reads safe" → chains C4, C7, C8, C11 ✓
- "MEDIUM — the 'no' ... is HIGH ... recommended path rests on unverified GT-9?, GT-10?, GT-14?" → chains C1, C6 ✓
```

## Pre-mortem (Phase 5 process output)

**Plan A (your VP's plan) has already failed. What caused it?**
- Sydney p95 barely moved, because the app tier and connection handshakes were the gap.
- Boston write p95 went up by more than 200 ms.
- A problem on the trans-Pacific link froze commits in both regions.
- The move to a multi-master extension overran on sequences and schema changes.
- A last-update-wins overwrite changed an invoice, which became a compliance incident.

These group into four structural weaknesses:
1. Wrong leg of the request targeted (C5, C6).
2. Physics charged on every commit (C1, C2).
3. Inconsistency built into the design (C3, C8).
4. Scope (C9).

Plan change: reject Plan A.

**Plan B (the recommended plan) has already failed. What caused it?**
1. Sydney tenants turned out to hold much more data, so server time is part of the gap (GT-14? was wrong).
   - Mitigation: a measurement gate before any build, and a route to query work if server time dominates.
2. Connections were already kept alive, so edge termination saved less than one round trip (A11 overestimated).
   - Mitigation: measure the connect and TLS share first, and A/B test a Sydney synthetic probe through the edge before rolling out.
3. Batching needed a frontend rewrite that took longer than a quarter.
   - Mitigation: batch only the few interactions that contribute most to Sydney p95.

Accepted risk: escalating to a regional app tier may still be needed. Its compliant read design is already worked out in C10.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? |
|---|---|---|---|---|
| C1 | GT-3 (RTT) + GT-5 (sync waits) | yes | n/a | yes |
| C2 | GT-1 (fibre speed) + GT-2? (distance) + GT-3 (RTT) | yes | n/a | yes |
| C3 | C1 + GT-4 + GT-6 + GT-8 | yes | n/a | yes |
| C4 | GT-1 + GT-5 + GT-6 | yes | n/a | yes |
| C5 | GT-3 + GT-10? | yes | n/a | yes |
| C6 | GT-3 + GT-9? + GT-14? | yes | n/a | yes |
| C7 | C6 + GT-14? + GT-15? | yes | n/a | yes |
| C8 | C3 + GT-12? | yes | n/a | yes |
| C9 | C1 + C3 + GT-13? | yes | n/a | yes |
| C10 | GT-3 + GT-5 + GT-6 + GT-7 | yes | n/a | yes |
| C11 | C1 + C6 + C8 + C9 + C10 + GT-11? | yes | n/a | yes |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not build ... | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C3, C7, C11 |
| Key insight: CDN worked because immutable ... | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C4, C6 |
| Trade-offs acknowledged: invoice reads stay on primary ... | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C10, C11 |
| Measure first: Server-Timing + Resource Timing ... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C6, C7 |
| Two engineers for four months: not deciding ... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C9 |
| What would change the answer: server time / residual / immutable invoices | bold lead-in | yes | bold lead-in whose colon closes the bold span | C4, C7, C8, C11 |
| Confidence: MEDIUM ... | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C6 |

```text
Scan complete: 11 chain rows, one per section-4 chain block in order; 7 section-6 rows, one per construct in order — 7 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate verdict blocks (process output)

**Criterion 1: Identify Essence**
Quoted span: "Core problem: Will relocating database state to ap-southeast-2 under synchronous active-active replication remove the 600 ms Sydney–Boston p95 gap without violating the no-stale-invoice requirement, or does that gap live on a leg of the request this design cannot reach?"
Band: **Rigorous**
Justification: The Essence Statement is one sentence naming this problem's specific decision and gap, and each success criterion is a checkable verb + subject + outcome property of the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C6 | 2 | per-RTT delta 175–220 ms | A14, A15 | yes |"
Band: **Rigorous**
Justification: Every row uses the four-type scheme with the matching treatment and a token-plus-em-dash verdict; four assumptions are Discarded or Challenged; and the audit scan covers all 53 chain steps, adding the assumptions it surfaced (A13–A20) to the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-2, GT-9, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15; list carries `?` on exactly those eight; unsuffixed GT-1, GT-3, GT-4, GT-5, GT-6, GT-7, GT-8 each name a read location and each feeds a HIGH chain (C4, C1, C3, C1, C3/C4, C10, C3)"
Band: **Rigorous**
Justification: The enumeration matches the list, every unsuffixed ground truth names where it was read and feeds a HIGH chain, and the failure records name source and reason.

**Criterion 4: Reason Upward**
Quoted span: "Scan complete: 11 chain rows ... 0 chains malformed" plus, from section 5, "Why abandoned: it uses an analogy as evidence, and the premise it needs — immutability — is false for a database (chain C4)"
Band: **Rigorous**
Justification: All 11 chains conform and have clean dependencies, the five dead ends use the required three-part structure with specific reasons, and no analogy is used as evidence.

**Criterion 5: Validate**
Quoted span: "**Measure first:** ... (chains C6, C7)" — both cited chains are MEDIUM
Band: **Sound**
Justification: Every chain names its weakest link and every `?` input carries a caveat, but one Conclusion claim rests on no HIGH chain, so the overall rating is correctly MEDIUM and this criterion is not Rigorous.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "7 claims under R11, 0 excluded ... 0 claims untraced"; Key insight: "a copy of mutable data can only be stale or slow the writer ... a leg the database does not sit on"
Band: **Rigorous**
Justification: Every section 6 claim cites a section 4 chain, and the Key Insight is a finding the CDN analogy does not reach, not a restatement of the recommendation.

Gate result: no Absent scores and no Hand-wavy scores, so the gate passes.

---

## 1. Problem Essence

**Core problem:** Will relocating database state to ap-southeast-2 under synchronous active-active replication remove the 600 ms Sydney–Boston p95 gap without violating the no-stale-invoice requirement, or does that gap live on a leg of the request this design cannot reach?

**Success criteria:**
- The Conclusion states a yes/no verdict on the proposed synchronous active-active design.
- The Conclusion names the measurement to run first and which result selects which fix.
- The Conclusion states how compliance-sensitive invoice reads stay non-stale on the recommended path.
- The Conclusion states whether the 2-engineer × 4-month budget changes the verdict.
- The Conclusion states a confidence level and the findings that would change the answer.

## 2. Assumptions Table

Phase 2 used two techniques to find hidden assumptions:
- **Inversion.** The claim "active-active will cut Sydney latency ~80%" is guaranteed to fail if any of these hold:
  1. The gap is not on the app-to-database leg.
  2. The app tier stays in us-east-1.
  3. Writes wait on a 200 ms link.
  4. Compliance forces reads back to the primary.
  5. Conflicts rewrite invoice state.
  6. The team cannot finish in the budget.
- **Fishbone**, over the default categories:
  - Technology: handshakes, serial calls, query time.
  - Information: the p95 method and the unmeasured breakdown.
  - Environment: geography and tenant size.
  - Resources: 8 engineer-months.
  - Process: schema-change coordination.
  - People: reasoning by analogy.

The unverified preconditions and branches from both enter the table below as untested beliefs.

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1 Moving data closer cuts DB-backed latency by roughly the CDN's 80% | untested belief | Verify, or flag unverified | Discard — contradicted by C4: nearby copies avoid a consistency cost only for immutable content | GT-1, GT-5, GT-6 via chain C4 |
| A2 The CDN'd assets are versioned/immutable, so edge copies never need invalidating | convention | Challenge before use | Accept — the 80% gain implies cache hits, which versioned filenames make safe; that convention has no database counterpart | unverified — flagged (C4 hop 3); asset cache headers not inspected |
| A3 Core Postgres can run active-active multi-master | untested belief | Verify, or flag unverified | Discard — core Postgres offers no synchronous multimaster | GT-4 |
| A4 RTT between us-east-1 and ap-southeast-2 cannot fall below the propagation floor | physical law | Accept as ground-truth candidate | Accept — signal speed is bounded (GT-1); measured 201 ms (GT-3) | GT-1, GT-3; floor via GT-2? (C2, MEDIUM) |
| A5 Synchronous cross-region replication is compatible with low write latency | untested belief | Verify, or flag unverified | Discard — every commit waits on a ~200 ms confirmation | GT-3 + GT-5 via chain C1 |
| A6 The app tier is co-located with the primary in us-east-1 | untested belief | Verify, or flag unverified | Challenge — not stated in the prompt; inferred from the single-primary description | unverified — flagged (GT-10?) |
| A7 Server-side time is similar for Sydney and Boston interactions (fishbone: Environment/Technology) | untested belief | Verify, or flag unverified | Challenge — same servers, but tenant data volume is unknown | unverified — flagged (GT-14?) |
| A8 The 780/180 ms p95 figures compare like-for-like interactions (fishbone: Information) | untested belief | Verify, or flag unverified | Challenge — measurement method and interaction mix not inspected | unverified — flagged (GT-9?) |
| A9 Serving a stale invoice is a compliance violation | current constraint | Record expiry conditions | Accept — expires if the governing rule tolerates bounded staleness, or if issued invoices are immutable documents | unverified — flagged (GT-12?) |
| A10 85% reads by request count means ~85% of the latency users feel is on the read path | untested belief | Verify, or flag unverified | Challenge — share of requests is not share of latency; one slow write interaction can dominate what users feel | unverified — flagged (GT-11?; C11 hop 3) |
| A11 Terminating TCP/TLS at a Sydney edge (CloudFront / Global Accelerator) removes handshake round trips from the client path | untested belief | Verify, or flag unverified | Challenge — the GA doc confirms "static IP addresses are anycast from the AWS edge network" and routing "over the AWS global network", but not handshake termination or latency gains | unverified — flagged; Phase 3 failure record: `citation does not support the claim` |
| A12 Capacity is 2 engineers × 4 months | current constraint | Record expiry conditions | Accept — expires if headcount or deadline changes | unverified — flagged (GT-13?) |
| A13 Invoice state (payment status, credits, adjustments) can change after issue (inversion) | untested belief | Verify, or flag unverified | Challenge — if false, issued invoices are cacheable like assets | unverified — flagged (C8 hop 1) |
| A14 Boston clients reach us-east-1 in ~10–25 ms RTT | untested belief | Verify, or flag unverified | Accept — short metro-to-region distance; bracketed in C6 | unverified — flagged (C6 hop 2); surfaced by Assumption Audit |
| A15 Sydney clients reach us-east-1 in ~200–230 ms RTT (region RTT plus last mile) | untested belief | Verify, or flag unverified | Accept — GT-3 plus a last-mile allowance | unverified — flagged (C6 hop 2); surfaced by Assumption Audit |
| A16 The p95 tail on the long path is not dominated by packet loss/retransmits (fishbone: Technology) | untested belief | Verify, or flag unverified | Challenge — a retransmit at 200 ms RTT is expensive, so fewer round trips might explain the gap | unverified — flagged (C6 hop 4); surfaced by Assumption Audit |
| A17 The synchronous standby has no automatic async fallback, so commits block when the link fails | untested belief | Verify, or flag unverified | Accept — follows directly from GT-5's "will wait until confirmation is received" unless a fallback is configured | unverified — flagged (C1 hop 5); surfaced by Assumption Audit |
| A18 Browser Resource Timing and a Server-Timing header can be added in days | untested belief | Verify, or flag unverified | Accept — standard web mechanisms; effort not measured | unverified — flagged (C7 hops 2–3, C11 hop 6); surfaced by Assumption Audit |
| A19 Multi-master adds conflict-safe key/sequence and schema-change coordination work | untested belief | Verify, or flag unverified | Accept — follows from GT-4's "each server works independently"; size of the work unmeasured | unverified — flagged (C9 hop 1); surfaced by Assumption Audit |
| A20 A primary WAL location read after a session's commit is at or beyond that commit's record | untested belief | Verify, or flag unverified | Accept — GT-7 defines the write location; ordering at commit not read at source | unverified — flagged (C10 hop 1); surfaced by Assumption Audit |

## 3. Ground Truths

- **GT-1** Optical-fibre signals travel at about 200,000 km/s. Source: Wikipedia, "Optical fiber". Read at source: "a signal using optical fiber for communication will travel at around 200,000 kilometers per second"; core index "around 1.4475".
- **GT-2?** The great-circle distance from Sydney (−33.87, 151.21) to Ashburn, VA (39.04, −77.49) is 15,674 km. Unverified: computed by haversine in this analysis (output "great-circle km Sydney-Ashburn 15674"), but the coordinates came from recall, not a source.
- **GT-3** Measured RTT between us-east-1 and ap-southeast-2 is 201.34 ms. Source: CloudPing AWS Region Latency Matrix, https://www.cloudping.co/. Read at source: matrix figure "201.34ms", a point-in-time snapshot. Failure record: https://www.cloudping.co/grid returned HTTP 404.
- **GT-4** Core Postgres offers no synchronous multimaster replication. Source: PostgreSQL docs, "Comparison of Different Solutions". Read at source:
  - "PostgreSQL does not offer this type of replication, though PostgreSQL two-phase commit ... can be used to implement this in application code or middleware."
  - "Heavy write activity can cause excessive locking and commit delays."
  - Asynchronous multimaster: "each server works independently ... The conflicts can be resolved by users or conflict resolution rules."
- **GT-5** Synchronous replication makes every commit wait for the standby, and replayed WAL is visible to queries on the standby. Sources: PostgreSQL docs §26.2.8 and the `synchronous_commit` entry. Read at source:
  - "each commit of a write transaction will wait until confirmation is received that the commit has been written to the write-ahead log on disk of both the primary and standby server"
  - `remote_apply`: "applied it, so that it has become visible to queries on the standby(s) ... This will cause much larger commit delays"
- **GT-6** Streaming replication is asynchronous by default, so there is a delay before commits become visible on the standby. Source: PostgreSQL docs §26.2.5. Read at source: "Streaming replication is asynchronous by default ... there is a small delay between committing a transaction in the primary and the changes becoming visible in the standby ... typically under one second."
- **GT-7** Both the primary's WAL position and a replica's replayed position can be queried. Source: PostgreSQL docs, system administration functions. Read at source:
  - `pg_last_wal_replay_lsn()`: "Returns the last write-ahead log location that has been replayed during recovery"
  - `pg_current_wal_lsn()`: "Returns the current write-ahead log write location"
- **GT-8** Spock multi-master resolves conflicts by keeping the newest commit timestamp. Source: pgEdge Spock docs, conflicts page. Read at source:
  - "the version of data with newest commit timestamp is kept"
  - "Conflicts can arise if a node is subscribed to multiple providers, or when local writes happen on a subscriber node"
- **GT-9?** p95 page-interaction latency is 780 ms from Sydney and 180 ms from Boston. Unverified: reported by you; measurement method and sample not inspected.
- **GT-10?** The app tier runs in us-east-1 alongside the primary. Unverified: not stated explicitly; inferred.
- **GT-11?** About 85% of requests are reads, by count. Unverified: reported by you.
- **GT-12?** Serving an out-of-date invoice is a compliance violation. Unverified: reported by you; the governing rule's definition of "stale" was not read.
- **GT-13?** Budget is 2 engineers × 4 months, about 8 engineer-months. Unverified: reported by you.
- **GT-14?** Server-side and database time per interaction are similar for Sydney and Boston, and this breakdown has never been instrumented. Unverified: the similarity is plausible because both cohorts hit the same servers, but tenant data volume is unknown.
- **GT-15?** A new HTTPS connection needs a TCP round trip plus a TLS 1.3 round trip before the first response. Cited to RFC 8446 §2. Failure record: RFC opened, but the asserted one-round-trip wording was not located (`citation does not support the claim`).

**Irreducibility check (five-whys, reduce-to-primitives mode).** "A synchronous cross-region commit adds about 200 ms" breaks into three primitives:
- The commit waits for confirmation: definition, GT-5.
- The confirmation crosses the link: direct measurement, GT-3.
- Crossing time has a lower bound set by signal speed: physical law, GT-1.

All three are verified.

```text
?-marked: GT-2, GT-9, GT-10, GT-11, GT-12, GT-13, GT-14, GT-15 (8 of 15)
Read-at-source: GT-1 — Wikipedia "Optical fiber", "around 200,000 kilometers per second"
Read-at-source: GT-3 — cloudping.co matrix, "201.34ms"
Read-at-source: GT-4 — PG docs, Synchronous Multimaster Replication paragraph, quoted
Read-at-source: GT-5 — PG docs §26.2.8 and synchronous_commit remote_apply, quoted
Read-at-source: GT-6 — PG docs §26.2.5, quoted
Read-at-source: GT-7 — PG functions-admin, pg_last_wal_replay_lsn / pg_current_wal_lsn, quoted
Read-at-source: GT-8 — docs.pgedge.com spock_ext/conflicts, last_update_wins, quoted
```

## 4. Derivation Chains

### Conclusion C1: Synchronous cross-region replication adds at least one ~200 ms round trip to every commit, for every user

GT-3 (us-east-1↔ap-southeast-2 RTT 201.34 ms, CloudPing) + GT-5 (sync commit waits for standby confirmation, PG docs 26.2.8)
→ a synchronous commit cannot return to the client until the standby's confirmation has crossed the inter-region link
→ each write transaction's commit latency rises by at least one ~200 ms round trip over its intra-region value
→ Boston writers pay this too, because a us-east-1 commit waits on the ap-southeast-2 node exactly as a Sydney commit waits on us-east-1
→ "active-active with synchronous replication" across these two regions cannot deliver low write latency to any user
→[2nd] if the link degrades, commits wait on confirmations that do not arrive, tying write availability in both regions to the trans-Pacific link *[Assumes: A17]*
→[3rd] the project converts a Sydney latency complaint into a global write-latency and availability regression

**Confidence:** HIGH
Weakest link: hop 5 relies on A17 (no async fallback). It qualifies only the second-order availability effect, not the first-order latency conclusion.

### Conclusion C2: No technology can bring the cross-region commit penalty below roughly 150 ms (theoretical limit)

GT-1 (fibre ~200,000 km/s, Wikipedia) + GT-2? (Sydney–Ashburn great circle 15,674 km, computed) + GT-3 (measured RTT 201.34 ms, CloudPing)
→ the law-permitted round-trip floor on a great-circle fibre path is 2 × 15,674 km ÷ 200,000 km/s ≈ 157 ms
→ the measured 201 ms exceeds that floor by ~44 ms, the only headroom attributable to routing convention rather than physics
→ no replication product, protocol or configuration can push a cross-region synchronous commit penalty below ~150 ms

**Confidence:** MEDIUM
GT-2? uses coordinates from recall. Checking them against a gazetteer would raise this to HIGH. A ±10% distance error still leaves the floor above ~140 ms, so the conclusion holds either way. Weakest link: hop 1's distance input.

### Conclusion C3: An active-active Postgres across 200 ms can have low write latency or no lost or lagging writes, but not both

C1 (≥200 ms per sync commit) + GT-4 (core PG offers no synchronous multimaster) + GT-6 (async replication has commit-to-visibility delay) + GT-8 (Spock keeps newest commit timestamp on conflict)
→ active-active on this Postgres requires a third-party extension, application-level two-phase commit, or a different database, not a configuration change
→ every such design either confirms each write across the link, inheriting C1's penalty, or replicates asynchronously, inheriting a commit-to-visibility delay
→ the asynchronous variants let both regions accept writes to the same row during that delay
→ they settle such collisions by rule, for example keeping the version with the newest commit timestamp and discarding the other
→ an active-active Postgres across this link offers low write latency or no lost or lagging writes, but not both

**Confidence:** HIGH
Weakest link: hop 4 illustrates with Spock's documented rule. Other extensions use different rules, but GT-4 confirms that asynchronous multimaster always needs some resolution rule.

### Conclusion C4: The CDN analogy fails because a database is mutable, so the 80% asset result does not transfer

GT-1 (signal speed ~200,000 km/s) + GT-5 (sync: writer waits for the copy) + GT-6 (async: copy lags the writer)
→ news of a write reaches a distant copy no sooner than a signal can cross the distance
→ a copy of mutable data far from its writer is therefore either behind the writer or makes the writer wait
→ a CDN escapes that trade only for content that is not rewritten after publication *[Assumes: A2]*
→ if the database were immutable like versioned assets, proximity would cut its latency as the CDN did
→ the database accepts writes, so the premise fails and the 80% asset result does not transfer to it

**Confidence:** HIGH
Weakest link: A2, that the CDN'd assets are versioned. If they were not, the CDN result would be weaker evidence still, so the conclusion is unaffected.

### Conclusion C5: Moving only the database to Sydney makes Sydney slower

GT-3 (RTT 201.34 ms) + GT-10? (app tier in us-east-1)
→ relocating the database to ap-southeast-2 while the app tier stays in us-east-1 puts every app-to-database query on the ~200 ms link
→ an interaction issuing N serial queries gains roughly N × 200 ms for every user, Sydney included
→ moving only the data closer to Sydney users makes Sydney slower, not faster

**Confidence:** MEDIUM
GT-10? (app tier location) is unverified. Confirming from the deployment inventory that app servers run only in us-east-1 would raise this to HIGH. Weakest link: hop 1.

### Conclusion C6: The 600 ms gap is about three serial client-to-app round trips, not database time (estimate)

GT-3 (RTT 201.34 ms) + GT-9? (p95 780 ms vs 180 ms) + GT-14? (server time similar for both cohorts)
→ the target quantity is the 600 ms Sydney–Boston difference, from which shared server-side time cancels
→ each client round trip costs Sydney ~200–230 ms and Boston ~10–25 ms, a per-round-trip delta of 175–220 ms *[Assumes: A14, A15]*
→ 600 ms ÷ 220 ms per round trip = 2.7 and 600 ms ÷ 175 ms per round trip = 3.4 bound the count, central 600 ÷ 195 ≈ 3.1
→ both ends of the bracket name the same cause, about three serial client-to-app round trips with nothing left for database time *[Assumes: A16]*
→ the gap sits on the client-to-app leg, which only moving the client-facing endpoint or cutting round trips can shorten

**Confidence:** MEDIUM
Depends on GT-9? (the p95 figures) and GT-14? (similar server time). The C7 measurement would raise this to HIGH. Weakest link: GT-14?. If Sydney tenants are much larger, part of the 600 ms is server time.

### Conclusion C7: Instrumenting the breakdown is the first step, because it can disprove C6 in days

C6 (about three serial client-to-app round trips) + GT-14? (breakdown never instrumented) + GT-15? (new HTTPS connection costs TCP and TLS round trips)
→ the candidate sources of those round trips are connection setup, serial API calls, and server time that differs by cohort
→ browser Resource Timing phases for connect, TLS and time-to-first-byte plus a Server-Timing header on each response separate those sources per interaction *[Assumes: A18]*
→ that instrumentation costs days against a project scoped in months *[Assumes: A18]*
→ the measurement can falsify C6 before any architectural commitment, so it is the first step

**Confidence:** MEDIUM
Depends on GT-14? and GT-15? (handshake round-trip count). Reading RFC 8446's handshake figure directly and trialling the instrumentation on one interaction would raise this to HIGH. Weakest link: hop 2's effort assumption, A18.

### Conclusion C8: Low-latency active-active produces exactly the invoice state compliance forbids

C3 (active-active is slow or lagging) + GT-12? (stale invoice read is a compliance violation)
→ the low-latency variant of active-active lets a Sydney node serve an invoice that omits a committed US-side change *[Assumes: A13]*
→ a collision on an invoice row is resolved by overwrite rather than surfaced to anyone
→ the design produces, by construction, the stale or lost invoice state the requirement forbids

**Confidence:** MEDIUM
Depends on GT-12? (the compliance rule) and A13 (invoices change after issue). Reading the governing rule's staleness definition and confirming invoices can change after issue would raise this to HIGH. Weakest link: hop 1.

### Conclusion C9: The 2 × 4-month budget is not the deciding question

C1 (sync commit penalty) + C3 (extension or new database required) + GT-13? (8 engineer-months)
→ the project must deliver a replication extension or database change, conflict-safe keys, schema-change coordination and a new failure model within 8 engineer-months *[Assumes: A19]*
→ on-schedule completion of the synchronous design still yields C1's write penalty
→ fitting the budget is not the deciding question, because success on schedule does not reach the latency goal

**Confidence:** MEDIUM
Depends on GT-13? (budget) and A19 (size of the migration work). A scoped estimate of the extension migration would raise this to HIGH. Hop 2 rests on C1 (HIGH), so the verdict holds even if the budget figure is wrong. Weakest link: hop 1.

### Conclusion C10: LSN-gated routing keeps replica reads correct without synchronous replication; compliance-critical invoice reads still belong on the primary

GT-3 (RTT 201.34 ms) + GT-5 (replayed WAL is visible to standby queries) + GT-6 (async replica lags the primary) + GT-7 (primary WAL location and replica replay location are queryable)
→ an application can read the primary's WAL location after a write and compare it with a replica's replayed location *[Assumes: A20]*
→ a replica whose replayed location has reached that point has replayed every write committed before the location was read
→ a read gated on that comparison therefore sees those writes, because replayed WAL is visible to standby queries
→ that gate guarantees read-your-writes on an asynchronous replica without synchronous replication
→ freshness against other sessions' writes needs the primary's location at read time, which itself costs a ~200 ms round trip from Sydney
→ compliance-sensitive invoice reads from a Sydney app tier should go straight to the primary, since the gate would cost the same round trip, while other reads stay local

**Confidence:** HIGH
Weakest link: A20, that a WAL position read after commit is at or beyond that commit's record. Verify by reading the PostgreSQL WAL-internals documentation.

**Trade-off matrix.** Weights were fixed before any option was scored. Scores run 1–5, higher is better.

| Criterion (weight) | A: Sync active-active | B: Regional app tier + LSN-gated replica | D: Edge termination + round-trip reduction |
|---|---|---|---|
| Sydney latency reduction (5) | 1 → 5 | 4 → 20 | 3 → 15 |
| Compliance safety, no stale invoices (5) | 1 → 5 | 4 → 20 | 5 → 25 |
| Fits 8 engineer-months (4) | 1 → 4 | 3 → 12 | 5 → 20 |
| Low operational risk (4) | 1 → 4 | 3 → 12 | 5 → 20 |
| Reversibility (3) | 1 → 3 | 4 → 12 | 5 → 15 |
| No regression for other regions (3) | 1 → 3 | 5 → 15 | 5 → 15 |
| **Total (max 120)** | **24** | **91** | **110** |

Sensitivity check: D leads B by 19 points. Lowering any single weight D wins on (compliance, budget fit, risk, reversibility) to 1 costs D at most 6 points. Latency, the one criterion B wins, is already at the maximum weight. So no single weight change reverses first and second, and this is not a near-tie.

### Conclusion C11: Measure first, then edge termination and round-trip reduction, with a regional app tier as the measured escalation

C1 (sync commit penalty) + C6 (gap is client-to-app) + C8 (compliance conflict) + C9 (budget not deciding) + C10 (LSN-gated reads) + GT-11? (85% reads by count)
→ weighted totals: edge termination with round-trip reduction 110 > regional app tier with LSN-gated replica 91 > synchronous active-active 24, out of 120
→ compliance ×5 and fit within budget ×4 drive the ranking, and no single weight change on the 1–5 scale reverses first and second
→ the 85% read share is what would let most Sydney requests stay local if escalation to a regional app tier is needed *[Assumes: A10]*
→ recommend measuring first, then edge termination and round-trip reduction, holding the regional app tier as a measured escalation
→[2nd] cutting serial round trips also lowers latency for Boston and every other region
→[2nd] the engineer-months not spent on multi-master cover the measurement, edge change and batching work *[Assumes: A18]*
→[2nd] under escalation, Sydney write interactions still send each app-to-primary query across the ocean
→[3rd] escalation therefore depends on batched write paths, which the round-trip reduction work builds first
→[3rd] under escalation, invoice pages served from the primary stay slower in Sydney than replica-served pages

**Confidence:** MEDIUM
Depends on GT-11? (read share) plus the MEDIUM inputs C6, C8 and C9. Running the C7 measurement and confirming A11 (edge termination removes handshake round trips) with a Sydney synthetic probe would raise this to HIGH. Weakest link: the latency score of 3 for option D, which rests on A11. Second-order check: no extension step contradicts a ground truth.

## 5. Abandoned Reasoning

### Dead End: Extrapolating the CDN's 80% to the database
**What was tried:** Treating last year's asset result as evidence that data proximity gives a similar cut.
**Why abandoned:** it uses an analogy as evidence, and the premise it needs, immutability, is false for a database (chain C4).
**What it ruled out:** Any latency forecast for the database project that is derived from the CDN result.

### Dead End: Asynchronous active-active as a compromise
**What was tried:** Dropping "synchronous" to remove C1's per-commit penalty.
**Why abandoned:** it removes the write penalty but introduces lagging reads and overwrite conflict resolution, which contradicts GT-12? (C3, C8).
**What it ruled out:** Every multi-master variant under the current compliance rule.

### Dead End: A distributed SQL database "that does multi-region natively"
**What was tried:** Replacing Postgres with a globally consistent database.
**Why abandoned:** consistent cross-region writes are still bound by GT-1 and GT-3 (the ~150 ms floor in C2), and a database migration exceeds GT-13?. Product docs were not opened, so no product-specific claim is made.
**What it ruled out:** Choosing a different database as a way around physics.

### Dead End: Explaining the gap as N+1 app-to-database queries
**What was tried:** Attributing the 600 ms to chatty ORM queries.
**Why abandoned:** app and database are co-located (GT-10?), so per-query cost is the same for both cohorts and cancels out of the difference. The intermediate claim could not be established unless GT-14? fails.
**What it ruled out:** Database query tuning as the fix for the difference, though it may still help absolute latency.

### Dead End: A synchronous `remote_apply` replica in Sydney for fresh local reads
**What was tried:** Making the Sydney replica always current so invoice reads could be served locally.
**Why abandoned:** GT-5 states remote_apply "will cause much larger commit delays", which puts C1's penalty on every write.
**What it ruled out:** Buying read freshness with write latency.

## 6. Conclusion

**Recommended approach:** Do not build synchronous active-active; spend the first one to two weeks instrumenting where the 600 ms goes, then cut client round trips with edge TLS termination (CloudFront or Global Accelerator in front of the us-east-1 origin) and batched API calls, and move to an ap-southeast-2 app tier with an LSN-gated read replica only if a measured residual still misses the target (chains C1, C3, C7, C11).

**Key insight:** The CDN worked because assets are immutable, and a copy of mutable data can only be stale or slow the writer; separately, the 600 ms gap is the arithmetic signature of about three serial client-to-app round trips at ~200 ms each, a leg the database does not sit on, so moving the data attacks a leg that contributes almost nothing to the gap (chains C4, C6).

**Trade-offs acknowledged:** Compliance-sensitive invoice reads stay on the us-east-1 primary even under escalation, so those pages keep a ~200 ms-per-read cost for Sydney users, and edge termination with batching may remove only part of the gap (chains C10, C11).

**Measure first:** Add a Server-Timing header carrying app and database durations to every API response and collect browser Resource Timing (connect, TLS, time-to-first-byte, request waterfall) for Sydney and Boston sessions: connect-plus-TLS near one or two 200 ms round trips points to edge termination, three or more serial calls points to batching, and Sydney server time well above Boston's points to query or tenant work rather than database location (chains C6, C7).

**Two engineers for four months:** Budget is not the deciding question, because finishing the synchronous design on schedule still leaves every commit, Boston's included, at least ~200 ms slower (chains C1, C9).

**What would change the answer:** Sydney server time materially above Boston's would make this a query-performance problem in us-east-1; a residual above target after edge and batching work would trigger the regional app tier with LSN-gated replica reads; provably immutable issued invoices would make replica-served invoice reads safe (chains C4, C7, C8, C11).

**Confidence:** MEDIUM — the "no" to synchronous active-active is HIGH on physics and documented Postgres behaviour, while the recommended path rests on unverified GT-9?, GT-10? and GT-14? until the measurement runs (chains C1, C6).
