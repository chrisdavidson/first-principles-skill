# Real-use dispatch findings — the agent is not reached by its own trigger phrases

> **Status: findings-only. No milestone is scoped from this record.** It reports a real-use
> observation, a re-run, and a full live routing-battery pass — three sources that agree the agent
> is not being dispatched. What it has **no control arm** for is *attribution*: nothing here
> establishes when the boundary broke or why. Under this project's own pairing discipline that is
> not enough to name a cause, and the record says so rather than implying otherwise.

> **Evidence class: author-auditable, not reader-auditable.** The document that prompted this
> check is real client work living outside this repository. Every figure below about *the tool's
> behaviour* is stated plainly and is checkable from the captures named in Provenance; nothing
> about the *client's business* is reproduced here, under the content rule in
> [use-journal.md](use-journal.md). The external project is referred to without a label — the
> `project-*` labels are assigned in first-use order in the private key, and this record
> deliberately does not guess which one applies.

> **A second dated observation of this finding is pre-registered.** Its outcome table is committed before the run, in [v8.14-delivery-verification.md](v8.14-delivery-verification.md) §3. This pointer records that the pre-registration exists; it records no result.

## What was asked

The author ran a first-principles analysis on a real external work problem, saved the output,
and asked whether it had been executed correctly against this project's testing apparatus.

## What was found

Four findings. The first and fourth are load-bearing and mutually corroborating — one from real
use, one from the tracked instrument. The third is the one most likely to outlive this record.

**Headline:** the agent is loaded and is not reached. Two real dispatch attempts produced
**zero** `Task` calls, and a full live routing battery returns **`BATTERY: FAIL`, P 1/13,
N 20/20** — a perfect negative arm alongside a near-total positive-arm failure, which locates the
defect in delegation firing rather than in routing generally.

### Finding 1 — the agent was loaded and never dispatched

A fresh headless run was issued against **current 8.6.0** code, on the same problem, with the
same source material available on disk:

- The `system/init` roster **contained** `first-principles:first-principles`. The agent was
  loaded and available.
- The prompt opened with **two of the agent description's verbatim documented trigger phrases**
  — the "analyze from first principles" and "challenge assumptions" forms the description names
  explicitly.
- The run completed `subtype=success` in **31 turns** and **27 tool calls**
  (Bash ×1, Read ×7, WebFetch ×16, WebSearch ×3, ToolSearch ×1).
- **Zero `Task` dispatches. Zero `task_notification` events.**

The main agent performed the entire analysis inline. This is the signature of **RR-130-01**, the
main-routing inline-answer regression recorded as diagnosed and fixed in v7.12.

**The originating real run failed the same way, and this is observed rather than inferred.** The
session transcript that produced the original document was located and read directly. It records
**10 Read, 3 Bash, 1 Write, and zero `Task` / Agent-tool calls** — the single Write being the
analysis file itself, which confirms session identity. The author's prompt carried two documented
trigger phrases in natural language. So the dispatch failure is **n = 2**: once in genuine
unobserved use, once under deliberate re-run, on different plugin surfaces.

This matters for attribution in one specific direction. The private label key's reconstruction of
the 13 prior real runs across four external projects records them as **full-composer runs via the
Agent tool** — i.e. dispatch demonstrably worked on this project's real traffic before today.
That reconstruction is metadata assembled after the fact and is not equivalent to the direct
transcript reading above, so it is reported as **suggestive, not established**: it is a reason to
suspect a change rather than a longstanding condition, and it is explicitly not a control arm.

**The stale-install confound is eliminated.** The author's plugin surface was pinned to a much
older generation at the time the original document was produced, which is a real defect in its own
right but does not explain the document's shape: the older generation's own output template
mandates the **identical six sections in the identical order**. The fresh run above was issued
against current code with the current agent loaded, and reproduced the behaviour independently.

### Finding 2 — neither document satisfies the output contract

The D-18 mechanical defect detector (`check-quality-harness.py --detect-defects`, the QUAL-01
instrument) **raises `SectionResolutionError` on both documents** and scores neither. That is the
detector behaving as designed — a document the parser cannot read must fail loudly rather than
report zero defects.

A structural scan of the same two documents:

| | original | fresh 8.6.0 re-run |
|---|---:|---:|
| canonical sections present (of 6) | **1** | **0** |
| distinct `GT-N` identifiers | 6 | 0 |
| chains in `GT-N + GT-M →` form | 0 | 0 |
| `Confidence:` / HIGH-MEDIUM-LOW | 0 | 0 |
| four-type classification vocabulary | 0 | 0 |
| Accept / Challenge / Discard verdicts | 0 | 0 |
| honest-depth escape valve | 0 | 0 |

The re-run's only arrows are prose arrows; it has no derivation chains. The original at least
carried stable `GT-N` identifiers with specific citations. **The current-code re-run therefore
conforms *less* than the document that prompted the check.**

### Finding 3 — conformance fell and substance rose

The re-run is the weaker document by every contract measure above and the stronger document on
substance: it produced a materially larger set of typed findings, marked each claim's source
class explicitly, and — unprompted — identified a factual citation error in the external
project's own reference material.

This is a **fresh, real-use instance of the finding v8.7 identified as the one that outlives it:
rubric conformance does not predict correctness.** That finding was previously established only
on harness-generated analyses of harness-chosen problems. It now has an instance from outside
the apparatus, in the opposite direction from the one the apparatus was built to detect.

### Finding 4 — the routing battery agrees: `BATTERY: FAIL`, P 1/13, N 20/20

Before this pass returned, the record pre-registered the two readings it could produce, so that the
interpretation was fixed in advance rather than chosen once the number was visible: either the
battery would also score low on P-cases — the two instruments agreeing, a live routing defect in
the agent — or it would clear its 11/13 threshold while real use scored zero dispatches, which
would have meant the battery exercises a path real invocation does not take and that a green
routing gate is uninformative about live behaviour. **It resolves to the first: the two
instruments agree.**

A full live pass of `check-routing.py` against the tracked catalog, on the same tree:

| Arm | Score | Threshold | Verdict |
|---|---:|---:|---|
| P-cases (expect `DELEGATE`) | **1 / 13** | ≥ 11 | **FAIL** |
| N-cases (expect `NO-DELEGATE`) | **20 / 20** | ≥ 18 | PASS |

`check-routing.py --self-test` passes (15 fixtures) before the live pass, so the detection logic
is sound independently of the live numbers.

**The failure is specific, not general.** A perfect N-arm rules out a broadly broken router — the
routing machinery works, and correctly withholds the agent from all twenty off-topic prompts. What
fails is delegation firing at all. Twelve of thirteen P-prompts failed, including those built
directly from the agent description's own trigger vocabulary — the "analyze from first principles",
"challenge the assumptions", "decompose this problem into its foundations" and "stress-test the
reasoning" forms.

**The one prompt that routed is the self-application case** — P12, which asks the agent to reason
about whether first-principles reasoning is itself reliable. P1 carries the same
"analyze from first principles" trigger in the same natural mid-sentence position and did **not**
route. Trigger-phrase presence therefore does not discriminate between the two outcomes, and one
observation cannot establish what does. This is recorded as the open thread, not as a mechanism.

**What this changes about the apparatus.** The battery reproduces what happens in real use rather
than exercising a path real invocation does not take. That is the better of the two outcomes for
the measurement apparatus and the worse one for the agent: the routing boundary five milestones of
instrumentation assumed was working is broken, and the instrument was capable of saying so all
along.

**Caveats on this figure.** `--repeat 1` — a single pass, where standard practice for a live
catalog run in this project is aggregate K-of-N across repeats. The margin is ten below threshold,
far outside the ±3 P-prompt swing documented for this harness, so it is reported as a **strong
signal rather than a hard figure**; a `--repeat 5 --min-pass 3` confirmation has not been run.
Note also that `--priority positives` reorders the catalog rather than filtering it, so this pass
covered all 33 prompts.

## What this record does not establish

Stated explicitly, because the project's characteristic failure mode is promoting an observation
into a measured harness and then spending milestones measuring the harness:

- **No control arm exists.** Both v8.12 verdicts carry a re-coded control precisely because
  incidence without a control cannot be attributed. Nothing here is paired. The **attribution of
  the dispatch failure is unknown** — it is not established as new, as a regression, or as
  caused by any particular change. The evidence establishes *that* the boundary is broken now,
  not *when* it broke or *why*.
- **Everything here is same-day.** The two real dispatch attempts and the battery pass share a
  date, a model generation, and a machine. They are three sources, not three independent samples.
- **The battery pass is `--repeat 1`.** Standard practice for a live catalog run here is
  aggregate K-of-N across repeats; a `--repeat 5 --min-pass 3` confirmation has not been run.
- **The P12 exception is unexplained.** One prompt routed and twelve did not, and the record
  offers no mechanism for the difference — only the observation that trigger-phrase presence does
  not account for it.
- **It does not establish that a fix is warranted.** A fix needs its own trigger and its own
  pre-registered success criterion. That said, this is the first finding in several milestones
  whose trigger is neither prior milestone paperwork, an altitude check, nor evidence about the
  measurement apparatus — the three channels the standing scope gate has exhausted.

## Provenance

- Re-run transport: `claude -p --output-format stream-json --verbose`, the Plan-36-locked
  transport, with `--plugin-dir` pointed at this repository's plugin root.
- `--permission-mode bypassPermissions` was used so the headless session could read the external
  source material without an interactive prompt. The run was read-only in effect — 27 calls, no
  writes — and the agent's own frontmatter disallows Write and Edit regardless. Recorded because
  it is a deviation from an unattended-safe default, not because it changed the result.
- Battery: `check-routing.py --catalog tests/routing-catalog.md --priority positives --repeat 1
  --min-pass 1`, run against the live tree. `--priority` reorders rather than filters, so all 33
  catalog prompts were covered. Per-prompt captures and `verdict.txt` were written to a `/tmp`
  output directory and are not committed.
- Captures live under the session scratchpad in `/tmp` and are **not** committed. Per the standing
  privacy constraint, no part of the external corpus entered this repository.
- Install-surface note: the plugin cache copies a **version-pinned snapshot**, and both
  `claude plugin marketplace update` and `claude plugin update` are version-gated rather than
  content-gated. A repository edit without a version bump never reaches a session. This is the
  mechanism behind the stale surface named in Finding 1.
