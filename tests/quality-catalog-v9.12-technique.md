# Quality Harness Prompt Catalog — v9.12, technique coverage

## Purpose

This is a **second, additive** prompt catalog for `scripts/check-quality-harness.py`, read via
`--catalog` exactly as `tests/quality-catalog-v8.7.md` is. It does not replace that catalog and it
is not comparable to it: the prompts here are different prompts, so a reading taken from this
catalog may never be set against a `tests/quality-baseline-v8.7*` figure. The v8.7 catalog is a
`_FROZEN_PATHS` entry precisely because the baselines that generate from it are a matched pair, and
it was left byte-unchanged by the work that authored this file.

**The gap this closes.** `.planning/AGENT-EVAL-3GEN-2026-09-24.md` ran one prompt
(`FP-ETHICS-R`, transplant-allocation ethics) byte-identical across three tree generations, and its
§7 states the limit plainly: *"One prompt is not a domain sample, and it exercises neither
theoretical-limit nor five-whys, so two of v9.10.0's four technique workstreams are untested
here."* Its §5 recorded `TIGHT-02 three-tier bracket: 0/5` and then had to explain **in prose**
that an ethics/allocation problem has no governing physical bound, so theoretical-limit correctly
did not fire. A zero that means *the technique declined* and a zero that means *the technique fired
and ignored its prescription* are the same number. The three rows below are prompts on which the
untested techniques have a reason to fire, so a zero taken here carries information the ethics
prompt's zero could not.

Each prompt is worded as a decision a person is actually facing, with enough concrete numbers that
the agent can reason rather than ask for context — the posture `tests/quality-catalog-v8.7.md` and
`tests/step0-fixture-catalog.md` both take. Each contains no technique name and fires no Step 0
trigger phrase (confirmed against `scripts/check-step0-emulator.py --prompt`), so each reaches the
full six-section composer rather than a focused technique stub. Each is off-catalog against
`tests/routing-catalog.md`, `tests/step0-fixture-catalog.md`, `tests/routing-battery-catalog.md`
and `tests/quality-catalog-v8.7.md`.

**Reading the result.** Adoption is scored by `scripts/score-technique-adoption.py`, which reports
one of three values per workstream per capture — `n/a — technique not invoked`, `absent — invoked,
prescription not followed`, or `present`. Detecting invocation separately from
prescription-adherence is the whole reason that tool exists: it encodes the distinction §5 had to
resolve by hand.

**Secondary reading, not this catalog's objective.** These prompts are also expected to produce
derivation chains with three or more hops. Backlog 999.168 closed the `unreached` mis-routing on
both surfaces but recorded its **frequency as unmeasured**, and `unreached` binds via R9/R10 at
positions beyond the second hop. Deep chains are the condition under which that frequency becomes
observable at all. Record any such observation as a secondary finding with its own N; this catalog
was not authored to settle it.

**Deliberately not a gate, and this omission is not an oversight.** Nothing here is registered in
`scripts/check-firewall-battery.sh` and neither this catalog nor its scorer has a CI job. Two
binding reasons, both of which survive a later reader's urge to "fix" the omission:

1. `docs/v8.7-constraint-teardown.md` §2 item 3 bars a K-of-N live result from gating a phase. The
   measured evidence is the S-P04 vector swinging 2/5 → 0/5 → 2/5 with no source change to the
   technique it measures. At N=5, noise equals effect. A live reading from this catalog is a
   recorded observation stated with its N, never a verdict.
2. REG-GUARD asserts that every battery-registered gate has a matching CI job, and the battery
   tally is generated arithmetic rather than a hand-swept number. Registering the scorer's own
   offline `--self-test` would be defensible on its merits, but it would move that tally, and it
   was out of scope for the task that authored these files.

## Run Command

```bash
mkdir -p /tmp/qt-probe
python3 scripts/check-quality-harness.py --probe QT-P1 \
    --catalog tests/quality-catalog-v9.12-technique.md \
    --plugin-dir first-principles \
    --out /tmp/qt-probe
```

Captures belong outside `tests/` — FROZEN-EVIDENCE sweeps that tree for untracked files. Score a
capture directory with:

```bash
python3 scripts/score-technique-adoption.py --captures /tmp/qt-probe
```

## Catalog

| ID | Prompt | Notes |
|---|---|---|
| QT-P1 | Our reverse-osmosis desalination plant currently uses 3.8 kilowatt-hours of electricity per cubic metre of fresh water at 45 percent recovery from Gulf seawater at 45,000 ppm salinity. A vendor is quoting 14 million dollars for a new membrane train plus energy-recovery devices, claiming it will bring us to 2.9 kilowatt-hours per cubic metre. We produce 95,000 cubic metres a day and pay 7.2 cents per kilowatt-hour. The plant is 11 years old and our board wants a decision before the next capital cycle closes in eight weeks. Should we buy the upgrade? | Desalination membrane-train upgrade decision — authored to give **theoretical-limit** (TIGHT-02, the three-tier bracket) a reason to fire. Separation work has a hard thermodynamic floor set by the free energy of mixing, so a law-permitted bound exists to derive and a real gap exists to bracket, and the vendor's quoted figure is plausible-but-checkable against it. **This catalog deliberately pins no expected bound value** — what is measured is whether the technique fires and brackets, not whether it reproduces a number asserted here. Classifies `full-composer` on the offline Step 0 emulator; no technique name; off-catalog against `tests/routing-catalog.md`, `tests/step0-fixture-catalog.md`, `tests/routing-battery-catalog.md` and `tests/quality-catalog-v8.7.md`. |
| QT-P2 | Our checkout service has gone down seven times in the last five months. Each incident was closed with a different immediate fix: a connection-pool size bump, a retry added to the payment gateway call, a cache TTL change, two separate hotfixes to the same inventory lock, a load-balancer timeout increase, and one rollback. Mean time to recovery is 34 minutes and each outage costs us roughly 40,000 dollars in abandoned carts. The on-call team of four is burning out and wants to stop paging. Engineering leadership is asking for a plan by the end of next sprint. What should we actually do here? | Recurring-outage remediation decision — authored to give **five-whys** (TECH-01, the counterfactual test) a reason to fire. A symptom that recurs, each recurrence closed by a different surface fix, is the shape a causal pass exists for; the two hotfixes to the *same* inventory lock are the deliberate tell that no pass went past the immediate cause. Classifies `full-composer`; no technique name; off-catalog against the three routing/Step-0 catalogs and `tests/quality-catalog-v8.7.md`. |
| QT-P3 | We run a developer API on a flat 49-dollar-a-month plan used by 6,400 accounts. The top 3 percent of accounts generate 61 percent of our total call volume, and our infrastructure bill has grown from 78,000 to 214,000 dollars a month over 18 months. Finance wants to introduce metered pricing above 50,000 calls a month, which would reprice about 190 accounts, 40 of which are on annual contracts renewing over the next two quarters. Two of our three largest competitors are still flat-rate. Our docs, SDKs and four community tutorials all state the flat price. Should we introduce metered pricing next quarter? | API repricing decision — authored to exercise **second-order** (TECH-05, the actor/time lens) harder than the ethics prompt did, where the lens vocabulary appeared in only two of five runs. Distinct parties respond on distinct timescales: heavy accounts immediately, contracted accounts at renewal, competitors over a pricing cycle, and the community authors of now-stale tutorials never. That divergence is what the actor and time lenses are coverage checks for. Classifies `full-composer`; no technique name; off-catalog against the three routing/Step-0 catalogs and `tests/quality-catalog-v8.7.md`. |
