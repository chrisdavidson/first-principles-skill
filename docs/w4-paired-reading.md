# The paired body comparison — the w4-paired reading

**A recorded reading with its N. Not a gate, and it may not become one.**
**Protocol:** [`docs/w4-paired-preregistration.md`](w4-paired-preregistration.md), registered
before any run, with one amendment made before any defect was read.
**Captures:** `tests/w4-paired/` (frozen) · **Re-derive:**
`python3 tests/w4-paired/run_paired.py reextract && python3 tests/w4-paired/run_paired.py read`

---

## The answer

[`docs/live-conformance-v9.14-reading.md`](live-conformance-v9.14-reading.md) found real defects
on two axes and could not say whether the body or the prompts produced them. Holding five prompts
fixed and running each three times on both bodies:

| Primary outcome (documents with ≥1 defect) | v9.0.0 | v9.12.0 | one-sided p | Pre-registered reading |
|---|---|---|---|---|
| **A1** — malformed chain block | 2 of 13 | 2 of 14 | 0.73 | **No difference detected at this N** |
| **A2** — nonconforming verdict cell | 9 of 13 | 8 of 14 | 0.40 | **No difference detected at this N** |

**Neither axis is attributable to the body at this N.** Both bodies produce both defects, at
rates the two arms cannot tell apart. By the pre-registration's §7, that closes W4's question for
both axes: the movement between the two frozen corpora is not evidence that v9.11 or v9.12
changed chain or verdict hygiene. It licenses no body edit and files no regression.

Block and cell rates point the same way — v9.0.0 is not the cleaner body:

| Reading | v9.0.0 | v9.12.0 |
|---|---|---|
| Malformed chain blocks | 9 / 85 | 2 / 77 |
| … of which a hop leads with a GT id | 1 of 9 | 1 of 2 |
| Nonconforming verdict cells | 47 / 203 | 28 / 215 |
| Untraced conclusion claims *(contracts differ — not interpreted)* | 16 / 78 | 11 / 98 |

## What else the run shows — reported, not decided

None of these is a pre-registered outcome, so none carries a verdict.

- **`Q-P2`'s wholesale vocabulary substitution did not recur.** Re-run three times on the very
  body that produced 31 nonconforming cells in the v9.0 corpus, `Q-P2` scored 2, 1 and 2. That
  single capture was run-level variance, which is what the
  [correction](live-conformance-v9.14-reading.md#correction-2026-09-26-the-pooled-verdict-rate-does-not-show-an-improvement)
  to the v9.14 reading inferred without being able to show.
- **Most of v9.0.0's malformed blocks are a different shape.** Seven of its nine sit in one
  document, six of those with the chain head wrapped in backticks; the other two sit inside a
  fenced block. Only one in each arm is a hop leading with a GT id — the rule the v9.14 reading's
  three flags broke.
- **Contract abandonment: v9.0.0 0 of 13 dispatched attempts, v9.12.0 3 of 17** (one-sided
  p = 0.17). In all three the agent was dispatched and reasoned at length but organised the
  document its own way — by technique (`## Five Whys`, `## Fishbone`), or by a numbered outline —
  instead of the six contract sections. Two were retried into readable documents; the third's
  retry was a routing miss, which is why `Q-P2.new.r2` is void. This is
  the same failure as the frozen `TB-08`, and it is **not** separated from noise here; it is the
  number worth measuring next, on its own protocol.
- **Routing misses are a harness confound, not a body property.** Six attempts were never
  dispatched: 4 on v9.0.0, 2 on v9.12.0, five of them on `PR-N1` ("our TLS setup"). The runner
  launches `claude -p` from this repository's root, and in each miss the main session grepped
  this repo for TLS configuration, found none, and answered directly. Three cells ended void —
  two v9.0.0, one v9.12.0. A future run of any "our X" prompt should start from an empty working
  directory.

## Limits

- **27 readable documents, five prompts, one model, today.** "No difference detected" is a
  statement about this N. A difference smaller than about three documents in fifteen would not
  show here.
- **Two points, not a trend.** v9.0.0 and v9.12.0 bracket several milestones.
- **Form, not quality.** Every figure counts artifacts.
  `docs/v8.7-correctness-spot-check.md` measured that conformance does not predict correctness.
- **Two hand-backs were rebuilt from the transcript** (`TB-06.new.r1`, `TB-06.new.r3`) under the
  pre-registration's Amendment 1. For `TB-06.new.r3` the streamed and rebuilt documents score
  identically on both primary axes.
- **A reading, never a gate** — `docs/v8.7-constraint-teardown.md` §2 item 3.

## Falsifiers

```sh
# 1. Every cell is re-derivable from raw/ under the fixed cell rule, and the reading
#    is what the tool emits.
python3 tests/w4-paired/run_paired.py reextract >/dev/null
python3 tests/w4-paired/run_paired.py read | grep -q 'A1 malformed chain block         old 2/13  new 2/14'
python3 tests/w4-paired/run_paired.py read | grep -q 'A2 nonconforming verdict cell    old 9/13  new 8/14'
python3 tests/w4-paired/run_paired.py read | grep -c 'no difference detected at this N' | grep -qx 2

# 2. Abandonment and routing misses are counted separately, with the published figures.
python3 tests/w4-paired/run_paired.py read | grep -q 'contract abandonment (void / dispatched attempts):  old 0/13  new 3/17'
python3 tests/w4-paired/run_paired.py read | grep -q 'routing misses (never dispatched / attempts):       old 4/17  new 2/19'

# 3. The captures have not been touched since they were frozen.
git diff --quiet HEAD -- tests/w4-paired
```
