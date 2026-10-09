# The shell-sourced delivery pointer — the pointer-fix reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/pointer-fix-preregistration.md`](pointer-fix-preregistration.md) and its
Amendment 1, both registered before the runs they govern. **Captures:** `tests/pointer-fix/`
(frozen). **Re-derive:** `python3 tests/pointer-fix/run_pointer.py read`

---

## The answer in one paragraph

**The fix is verified.** With step 9 of *Deliver the analysis as a file* requiring the final
message's paths to be printed by the shell and copied verbatim, **no run named a location the
shell did not write: 0 of 14 file-delivering runs**, against 4 of 23 on the unfixed body. In
**13 of 14** every path was absolute and correct; the fourteenth named correct locations but
shortened three of them to relative paths. Every run used the same scratch working directory
whose name produced the defect, so the trigger was present throughout. Both Amendment 1
conditions hold: no wrong pointer, and at least 12 runs all-correct with at most one not.

## Result

| | Unfixed body (calibration) | Fixed body |
|---|---|---|
| File-delivering runs | 23 (`example-rerun-2` 14, `skip-paired` new arm 9) | 14 (10 registered + 4 under Amendment 1) |
| Runs naming a wrong location | **4** | **0** |
| Every path absolute and correct | 11 | **13** |
| Correct locations, some shortened or relative | 7 | 1 (`science-engineering`) |
| Pointer names no path | 1 | 0 |

At the unfixed rate (≈17%), 0 wrong in 14 has probability ≈ 0.07 by chance; the 13-of-14
compliance with the positive instruction is what distinguishes a followed rule from luck. The
instrument's calibration — it flags exactly the four runs read by hand as wrong on the unfixed
captures, and no other run — is in the pre-registration's §3.

**Two runs read by hand, not left to the instrument.** `science-engineering-2.supp1` names a
single path because it wrote only the working file and skipped the report steps (5–8): a partial
delivery, not a pointer error, and the one path it names is correct. `self-application.supp1`
explored this repository again (its prompt concerns this project's own agent file, and the
scratch path encodes the repository's name), which contaminates its content but not its pointer:
all seven paths name the run's own working directory.

## Skips — a separate, still-open defect

Four of the fourteen registered runs skipped the procedure before reaching step 9 and were
replaced under Amendment 1 (each delivered on its first re-run). They carry no information about
the pointer and are not caused by this fix — the unfixed body skipped 3 of 14 in `example-rerun-2`
and the same examples recur. Their modes, read from the transcripts:

- **The agent invokes a skill and loses its procedure.** `science-engineering-2` called the
  slash-only `first-principles-analysis` launcher, which it cannot invoke, then told the user to
  run `/first-principles-analysis` themselves; `self-application` invoked an unrelated user-level
  skill (`claude-api`). In `example-rerun-2`, `decompose-irreducibility` opened with a call to a
  skill that does not exist. The agent's `disallowedTools` does not exclude `Skill`.
- **The agent answers without the procedure.** `product-business` made no tool call at all (as
  it did in `example-rerun-2`); `decompose-irreducibility` answered from web searches alone.

This is filed as a known issue, not fixed here: excluding `Skill` changes the agent's frontmatter,
whose exact `disallowedTools` list GATE-01 pins, and the zero-tool mode has no mechanism yet.

## What limits this reading

One run per example (four examples twice), one model (`claude-sonnet-5`), one CLI version
(2.1.289), print mode, one working directory. Amendment 1 was written with the first thirteen
results known; it changed which runs count, not what a run must do to pass. The worked examples'
content is not re-judged here.
