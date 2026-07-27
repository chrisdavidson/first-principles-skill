# Dispatch remediation plan — restoring a reliable path to the agent

> **Input document.** This is a plan, not a findings record. Its evidence base is
> [real-use-dispatch-findings.md](real-use-dispatch-findings.md); nothing here re-derives those
> figures. It is written to be consumed as milestone scope — each phase below carries a goal, a
> pre-registered acceptance criterion, and an explicit branch condition.

> **⚠ Phase 1a has been executed and the branch is decided. Read this before scoping any phase
> below.** [dispatch-attribution-findings.md](dispatch-attribution-findings.md) returns
> **`RUNTIME-WIDE`**: a freshly-authored control agent in an unrelated domain also failed to
> dispatch (0 of 3), alongside a paired first-principles reference (0 of 1). The defect is not
> agent-specific and **no change to this repository can fix it**.
>
> Consequently: **Phases 2a, 2b and 3 are void**, and **Phase 1b should not be run** — it would
> test old versions against a runtime that does not dispatch a new control agent either, spending
> ~200 live invocations to confirm a foregone conclusion. The phases below are preserved as
> written, for the record of what was planned and why it was set aside.

> **Status as of 2026-07-27 — the plan is discharged.**
>
> | Phase | State |
> |---|---|
> | 1 · Attribution (`DISPATCH-01`) | **Done** — task 1a executed, verdict `RUNTIME-WIDE` |
> | 1b · Historical bisect | **Will-not-run** — uninformative under the verdict |
> | 1c · P12 discriminator ladder | **Open** — the one remaining probe into what still routes |
> | 2a · In-repo regression (`DISPATCH-02`) | **Void** — assumes a repository-side cause |
> | 2b · Description re-engineering (`DISPATCH-03`) | **Void** — same |
> | 3 · Verification (`DISPATCH-04`) | **Void as written**; its real-use criterion was met by Phase 4's end-to-end check |
> | 4 · Deliberate invocation path (`DISPATCH-05`) | **Done** — `/first-principles-analysis`, commit `c2a7365` |
> | 5 · Silent-staleness hole (`DISPATCH-06`) | **Done** — documentation only |
>
> Phase 4 landed smaller than specified: explicit dispatch through the Task tool was found to
> still work, so the launcher delegates to the existing agent instead of duplicating the
> methodology and its 22-file reference tree. Its open design question — whether the entry point
> should be `disable-model-invocation: true` — resolved affirmative.
>
> **One item is open that this plan did not anticipate.** On the launcher's verified output the
> D-18 detector flags 16/16 verdict cells nonconforming and 4/4 chain blocks malformed, while the
> chains inspect as conformant to the template's prescribed shape. Detector over-strictness and
> systematic formatting variance are both live explanations and neither is established. See
> [dispatch-attribution-findings.md](dispatch-attribution-findings.md).

## Scope correction, before anything else

**The harness is not broken.** `check-routing.py` passed its own `--self-test` (15 fixtures) and
then correctly reported a real defect it was built to catch. Treating this as a harness problem
would fix the thermometer.

What is broken is **delegation firing**: the agent is loaded, is addressed in its own documented
trigger vocabulary, and is not reached. `BATTERY: FAIL`, P **1/13**, N **20/20**. The perfect
negative arm is the load-bearing detail — routing machinery works and correctly withholds the
agent from all twenty off-topic prompts. Only the positive path is dead.

**The deeper problem this exposes.** The agent is delegation-only; the thirteen companion skills
are `disable-model-invocation: true`, slash-only. If delegation does not fire, **the agent has no
reliable invocation path at all**. That is a product-level defect, not a routing tuning issue, and
Phase 4 exists because a fix that restores 11/13 still leaves the agent reachable only by a
mechanism that has now failed silently for an unknown period.

## Non-negotiables

Carried from this project's own governing records. A phase that violates one of these is wrong
even if it produces a green number.

1. **Pre-register every threshold before measuring.** The v8.7 lesson. Post-hoc rules are labelled
   post-hoc or they are not used.
2. **No single-run verdicts.** Live catalog runs are read as aggregate K-of-N. The current 1/13 is
   a strong signal, not yet a citable figure.
3. **K-of-5 is an observation, not a gate** (governing record §2 item 3). A phase records it; a
   phase may not be gated on it.
4. **Edit `shared/` only.** Never the generated tree. `sync-content.py --write`, then the
   sync-drift gate.
5. **Do not promote an observation into a new instrument.** This project's characteristic failure
   is building a harness and then spending milestones measuring the harness. No new detector, no
   new CI gate, unless a phase below names one explicitly and justifies it.
6. **Honesty-not-score (D-01).** A documented honest count beats a green number.
7. **The 16/16 offline firewall battery must stay green** (`scripts/check-firewall-battery.sh`).

## The open question everything hinges on

**Is the cause inside this repository or outside it?**

Nothing measured so far answers this. There is no control arm. Two facts point in opposite
directions and neither settles it:

- The private label key's reconstruction records 13 prior real runs across four external projects
  as full-composer dispatches via the Agent tool, the most recent on 2026-07-25 — suggesting
  dispatch worked recently. That is after-the-fact metadata, not a transcript reading.
- The agent's description is already maximally directive (`ALWAYS delegate…`, `Do not perform
  inline analysis for these`) and still fails on twelve of thirteen prompts — which is not what a
  weak-description failure usually looks like.

Phase 1 exists solely to answer this, because **the correct fix differs completely by branch** and
committing to a fix first would be guessing.

---

## Phase 1 — Attribution (`DISPATCH-01`)

**Goal.** Determine whether the dispatch failure originates in this repository, in the agent's
description shape, or in the runtime — before any fix is attempted.

**Why first.** This is the missing control arm. Every remaining phase branches on its result.

### Tasks

**1a — Runtime control: does *any* agent auto-delegate right now?**
Author a throwaway minimal plugin containing one agent with a short, unambiguous description in a
domain the first-principles agent does not claim (e.g. "converts currency"). Issue three prompts
that should obviously route to it. This is the sharpest available discriminator:

- Minimal agent **routes** → delegation works in this runtime; the problem is specific to this
  agent. Continue to 1b.
- Minimal agent **does not route** → delegation is broken runtime-wide and **no repository change
  can fix it**. Jump to Phase 4; Phases 2 and 3 are void.

**1b — Historical control: bisect by plugin version, not by reading diffs.**
The generated tree is committed at every tag, so old agents are directly runnable:

```sh
git archive v7.13 | tar -x -C /tmp/fp-v713
python3 scripts/check-routing.py --catalog tests/routing-catalog.md \
    --plugin-dir /tmp/fp-v713/first-principles --repeat 3 --min-pass 2 --out /tmp/routing-v713
```

Run **v7.13** (the last milestone where routing was recorded RESOLVED), **v8.0**, **v8.6**, and
**HEAD**, all inside one session window so the runtime is held constant.

- An old version scores **≥ 11/13** today → the cause is **in-repo**, between that tag and HEAD.
  Go to Phase 2a.
- **All** versions score ≤ 3/13 today, including v7.13 → the cause is **external** to the
  repository; the description was never the variable. Go to Phase 2b.

**1c — Discriminator probe: why did P12 route when P1 did not?**
P12 (self-application: *"…whether first-principles reasoning itself is a reliable method"*) is the
only prompt that routed. P1 carries the same `analyze from first principles` trigger in the same
mid-sentence position and did not. Construct a small ladder of variants between P1 and P12 —
double trigger mention, meta framing, explicit method naming — and find which single edit flips
routing.

### Pre-registered acceptance criteria

- 1a returns a definite ROUTES / DOES-NOT-ROUTE with n ≥ 3.
- 1b produces a per-version P-score table, all runs inside one session window, `--repeat 3
  --min-pass 2`.
- 1c names **at least one** minimal edit that flips a non-routing prompt to routing, **or**
  records that no such edit was found — a null result here is a real result and is recorded, not
  retried until it yields.
- **The phase passes on producing the attribution verdict, not on the verdict being convenient.**
  `EXTERNAL` is a passing outcome.

**Artifacts.** `docs/dispatch-attribution-findings.md` — per-version table, the 1a control, the
1c ladder, and one of three verdicts: `IN-REPO` / `DESCRIPTION-SHAPED` / `EXTERNAL`.

**Risks.** ~200+ live invocations; budget a long window. Routing is non-deterministic, so a
single-version anomaly must not be over-read — the decision rule is on the table as a whole.

---

## Phase 2a — In-repo regression (`DISPATCH-02`) · *only if Phase 1 returns IN-REPO*

**Goal.** Locate the change that broke delegation and reverse its effect.

### Tasks

- Bisect between the last-good and first-bad tags from 1b, running a **shortened** P-only catalog
  at each step (the full 33-prompt battery is too slow to bisect on).
- Confirm the identified change by reverting it in `shared/` alone and re-measuring.
- `sync-content.py --write`; sync-drift gate must pass.

### Pre-registered acceptance criteria

- The offending change is named at commit granularity.
- With the fix applied: **P ≥ 11/13 and N ≥ 18/20**, `--repeat 5 --min-pass 3`.
- The N-arm must not regress below 18/20 — a fix that restores delegation by making the agent
  greedy is a failure, not a success. This is the anti-Goodhart clause and it is pre-registered.
- 16/16 offline firewall battery stays green.

---

## Phase 2b — Description re-engineering (`DISPATCH-03`) · *only if Phase 1 returns DESCRIPTION-SHAPED or EXTERNAL-but-recoverable*

**Goal.** Find a description shape that the current runtime actually routes on.

**Why this is a real possibility.** The current description is ~1,000 characters and front-loads a
capability summary before its trigger list. If the routing model weights early tokens or dilutes on
length, the most directive sentence in the description may simply be arriving too late. Phase 1c's
ladder is the evidence that would support or kill this.

### Tasks

- Derive 3–4 candidate descriptions from the 1c ladder — e.g. trigger-phrases-first ordering, a
  short high-signal variant, an explicit-domain variant.
- Measure each against the full catalog, one session window, `--repeat 3 --min-pass 2`.
- Adopt the winner in `shared/spine/SKILL.meta.yml`; regenerate.

### Pre-registered acceptance criteria

- Winner scores **P ≥ 11/13 and N ≥ 18/20** at `--repeat 5 --min-pass 3`.
- **N-arm floor of 18/20 is a hard gate**, checked before the P-arm improvement is credited.
- VAL-04 (4-gram trigger collisions) and VAL-05 (description budget) pass.
- If no candidate clears both arms, the phase records **NO-CANDIDATE-CLEARS** and routes to
  Phase 4. That is a passing outcome for the phase.

---

## Phase 3 — Verification (`DISPATCH-04`)

**Goal.** Confirm the fix holds on the surface that actually matters — real use, not the catalog.

**Why separate.** The catalog is the instrument the fix was tuned against. Verifying only there
risks confirming the tuning rather than the fix.

### Tasks

- Full battery, `--repeat 5 --min-pass 3`, fresh session.
- **A real-use re-run**: re-issue the original real prompt from the findings record through the
  fixed plugin and confirm a `Task` dispatch appears in the transcript.
- Run the resulting output through `check-quality-harness.py --detect-defects` and record whether
  the six-section contract now resolves.

### Pre-registered acceptance criteria

- Battery: P ≥ 11/13, N ≥ 18/20 at K-of-5.
- Real-use re-run: **≥ 1 `Task` dispatch observed in the transcript.** This is the criterion that
  matters; the battery number alone does not close this milestone.
- The detector result is **recorded, not gated** — a document that now parses is evidence the
  agent ran, but Finding 3 established that conformance does not predict correctness, so it must
  not become a quality claim.

---

## Phase 4 — A deliberate invocation path (`DISPATCH-05`)

**Goal.** Ensure the agent is reachable by a mechanism that cannot fail silently — regardless of
whether Phases 2–3 succeeded.

**Why this phase is unconditional.** Even a successful fix leaves the agent reachable only through
model-mediated routing, which has now demonstrably failed for an unknown period with no signal to
the user. If Phase 1 returns `EXTERNAL`, this phase is the *entire* remedy.

### Tasks

- Add an explicit slash entry point that invokes the full five-phase composer directly, alongside
  the thirteen focused skills. Delegation stays as the convenience path; the slash command becomes
  the guaranteed one.
- Verify no name collision (`check-install-collisions.py`), no 4-gram collision (VAL-04), and that
  the description budget still clears (VAL-05).
- Update `GETTING-STARTED.md` and `METHODOLOGY-CHEATSHEET.md`, which currently document delegation
  as the way to reach the agent.

### Pre-registered acceptance criteria

- The slash command invokes the composer and produces the six-section output, verified once
  end-to-end.
- COLLIDE-01, VAL-04, VAL-05 pass; 16/16 firewall battery green.
- Docs no longer describe delegation as the sole path.

**Open design question for the phase to settle, not this plan:** whether the new entry point
should be `disable-model-invocation: true` like the other thirteen. Making it model-invocable
creates a second routing surface with the same failure mode; making it slash-only guarantees
reachability but means the agent never fires automatically. This is a genuine trade-off and should
be decided with the Phase 1 verdict in hand.

---

## Phase 5 — Close the silent-staleness hole (`DISPATCH-06`)

**Goal.** Make it impossible for a session to run months-old plugin code without any signal.

**Why it belongs here.** The install surface that produced the original document was pinned to a
generation five months old. That did not cause the dispatch failure — the fresh 8.6.0 re-run
reproduced it — but it is a real defect found in the same investigation, and it delayed diagnosis
by supplying a plausible wrong explanation.

### Tasks

- Document the mechanism in `DEVELOPMENT.md`: `claude plugin install` copies a **version-pinned
  snapshot**; both `marketplace update` and `plugin update` are **version-gated, not
  content-gated**; a repo edit without a version bump never reaches a session.
- Document the `~/.claude/skills/<name>` symlink install as the supported development path — it
  loads as `<name>@skills-dir` with no cache copy and no version pin. Note that the marketplace
  cache has a GC that reaps orphaned directories, so a symlink placed *inside the cache* does not
  survive.
- Recommend recording the loaded plugin version in any future live-measurement record, so a stale
  surface is visible in the artifact rather than discovered afterwards.

### Pre-registered acceptance criteria

- `DEVELOPMENT.md` states the version-gating behaviour and the supported dev-install path.
- No new script, no new gate. **This phase is documentation only** — per non-negotiable 5.

---

## Decision tree

```text
Phase 1 (attribution)
├─ 1a minimal agent does NOT route  ──────────────► Phase 4 + Phase 5   (2a/2b/3 void)
├─ 1b an old version scores ≥ 11/13 ──────────────► Phase 2a → 3 → 4 → 5
└─ 1b all versions ≤ 3/13, 1a minimal DOES route ─► Phase 2b → 3 → 4 → 5
                                                     └─ if NO-CANDIDATE-CLEARS → Phase 4 + 5
```

## Explicitly out of scope

- **Any change to the six-section output contract or the rubric.** The conformance failures in
  Findings 2 and 3 are downstream of the agent not running. Touching the contract before the agent
  is reachable would be fixing a symptom, and Finding 3 is direct evidence that conformance is not
  the quality lever.
- **A new CI gate for routing.** Routing needs a live session and cannot run in CI. Milestone-close
  is the right cadence, by a human, as an observation.
- **Re-opening `CGATE-BUILD-01`** — WON'T-DO stands.
- **Any fix to the quality harness or the D-18 detector.** Both behaved correctly throughout.

## First action

Phase 1, task **1a** — the minimal-agent control. It is the cheapest task in the plan, needs three
prompts, and it alone can void two of the five phases.
