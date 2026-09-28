# File handoff — the delivery-fix-3 reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/delivery-fix-3-preregistration.md`](delivery-fix-3-preregistration.md) and its
Amendment 1 (`delivery-fix-3b`). **Captures:** `tests/delivery-fix-3/` (frozen) — each run's
stream, the agent's own transcript, and the delivered file. **Re-derive:**
`python3 tests/delivery-fix-3/run_fix3.py read`

---

## The verdicts, as registered

| Registration | Result | Verdict |
|---|---|---|
| `delivery-fix-3` — complete, verbatim to the appends, read | 6 of 12 | **not operational** |
| `delivery-fix-3b` — complete, provenance-true, read; the 8 runs unobserved at its registration | 5 of 8 | **not operational** |

Neither registration's bar was met, and this reading does not say otherwise.

## What the runs show

| | Result |
|---|---|
| Output-limit cut-offs | **0 of 12** — against 6 of 20 before the fix, 5 of which lost sections |
| Runs where the agent used the file | 10 of 12 |
| … delivered complete (6 sections) and read by the caller | **10 of 10** |
| … every byte replayed from the agent's own recorded writes | 9 of 10; the tenth unverifiable (below) |
| File length | 7,719 to 10,147 words — longer than the pre-fix documents, none condensed |
| Runs that ignored the rule | 2 of 12 |

**Where the file handoff was followed, truncation did not occur and no analysis lost anything.**
Appending one section per call keeps every message far below the output limit, so no cut-off
happened at all, and the caller read each file whole.

**The failures are of two kinds, and neither is lost fidelity:**

- **The rule was ignored (`TB-04.r1`, `TB-04.r2`).** No file, no template read either; `TB-04.r2`
  made no tool calls at all — the one-shot shape of the earlier abandonment work. Both returned
  their document as the final message, and both happened not to be cut off, so what was written
  arrived: 4,739 words with 6 sections, and 3,223 words with 5. **This is the residual risk:** a
  run that skips the procedure *and* runs past the output limit would still lose its opening.
- **The agent revised its own file (`TB-03.r1`, `TB-03.r3`, `TB-06.r2`, `TB-06.r3`).** That fails
  v3's *verbatim*, which was written to catch regeneration and did not anticipate revision. Three
  edited in place during self-audit — inserting missing assumption rows and correcting verdict
  cells into the prescribed vocabulary with `sed -i` and `awk` (`TB-03.r1`, `TB-06.r3`), or with a
  Python script (`TB-06.r2`). `TB-03.r3` instead **restarted**: five appends (2,539 words), then it
  truncated the file and rewrote it in eight (7,750 words). That is a second writing, but it
  replaced a partial draft rather than condensing a finished one — position by position the rewrite
  is at least as long (233→233, 564→636, 1,196→1,212, 149→552, 397→785). Three of the four replay
  byte for byte from the agent's own recorded commands; `TB-06.r2`'s Python edit is one 3b's
  registered replay refuses to execute, so its provenance is unverified rather than violated.

## Limits

- **Twelve runs, four prompts, print mode, one model.**
- **Compliance is the open question,** at 10 of 12. Two misses on one prompt is too few to rate.
- **Provenance proves nothing was rewritten between writing and delivery,** not that each section
  was complete when first written.
- **A file in the working directory is a side effect** the user accepted when choosing this fix.

## Falsifiers

```sh
python3 tests/delivery-fix-3/run_fix3.py --self-test
python3 tests/delivery-fix-3/run_fix3.py read | grep -q 'delivered 6/12   runs with a cut-off 0'
python3 tests/delivery-fix-3/run_fix3.py read | grep -q "recorded writes (appends and in-place edits): 9/12"
python3 tests/delivery-fix-3/run_fix3.py read | grep -q 'VERDICT  NOT OPERATIONAL'
git diff --quiet HEAD -- tests/delivery-fix-3
```
