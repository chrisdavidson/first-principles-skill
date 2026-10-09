# Pre-Registration — Does the shell-sourced pointer stop the wrong delivery path?

**Id:** `pointer-fix` · **Registered:** 2026-10-08, before any run under this id.
**Origin:** [`skip-paired-reading.md`](skip-paired-reading.md) — the current body's final
pointer named a location the shell never wrote in 3 of 9 runs (0 of 9 on v9.13.0).

## 1. The defect and the fix

**Mechanism, read from the transcripts.** Every delivery command prints a relative path
(`.first-principles/report-<UTC>.md`). In its final message the agent rewrites those as absolute
paths it builds itself; the directory it chose (`/home/…/Projects/first-principles-skill`) was
never printed by any command — it is the scratch working directory's *name*
(`…-home-chrisdavidson-Projects-first-principles-skill-…`) decoded into a path. One run noticed
the files were not there and abandoned the file handoff; another issued a `Read` of the
invented path. Step 9 of *Deliver the analysis as a file* asked for "the path" of each file
without saying where it must come from.

**Fix (`shared/spine/SKILL-body.md`, step 9).** The final message's paths come from the shell:
one Bash call prints `"$(pwd -P)/<path>"` for every path steps 1 and 5–8 printed, and the
message copies each line verbatim; the agent may not write a path no command printed, nor
derive a directory from the session's environment, a directory's name or a project it
believes the analysis concerns. Body under test: the generated agent file with sha256 prefix
`edd03cf41a680a39`, exported outside the repository.

## 2. Design

All 14 worked-example prompts (`tests/example-rerun-2/prompts.json`, verbatim), one run each, on
the fixed body, through `tests/example-rerun-2/run_examples.py`'s transport unchanged
(`claude-sonnet-5`, CLI 2.1.289, persistence on, routing misses retried at most twice). The
working directory is the same scratch directory **whose name triggered the defect** — the
stress condition is kept, not removed.

## 3. Instrument — `tests/pointer-fix/run_pointer.py read`

For each run that delivered a file, every path token naming a `.first-principles/` file is taken
from **all of the agent's own assistant text and every `Read` it issues** (strict: an earlier
wrong pointer or a `Read` of an invented location counts even if the last message is right).
A token is **wrong** if it is absolute but not under `<run cwd>/.first-principles/`, or names a
file no command printed and the capture does not hold. **Calibrated before any run** on the two
existing captures: it flags exactly the four runs read by hand as wrong — `skip-paired`
`decompose-irreducibility.new.r1`, `personal-general-2.new.r1`, `product-business.new.r1`, and
`example-rerun-2` `estimate-fermi` — and no other run. Baseline on the unfixed current body:
**4 wrong of 23** file-delivering runs (≈17%).

## 4. Verdict, fixed in advance

The fix is **verified** when both hold:

- **no run has a wrong pointer** (0 of the file-delivering runs); and
- in **at least 12 of 14** runs, every path the pointer names is absolute and correct (the
  fix's positive instruction followed, not merely the defect absent).

At the baseline rate, 0 wrong in 14 has probability ≈ 0.07 by chance; the second condition is
what separates a followed instruction from luck. If either fails, the fix is not verified and is
revised before any release. Skips (no file) are reported and excluded from both denominators.

## 5. What this cannot establish

One run per example, one model, print mode. The worked examples' recommendations are not
re-judged here — that was `example-rerun-2`.

## Amendment 1 — registered 2026-10-09, before any run under it

**Why.** §4's second condition counts runs whose every path is absolute and correct, and §4
excludes skips from its denominators. Four of the first thirteen runs skipped the procedure
before the delivery step (`decompose-irreducibility`, `product-business`,
`science-engineering-2`, `self-application`) — the agent never reached step 9, so they carry
no information about the pointer — which leaves at most ten file runs and makes "at least 12"
unreachable for a reason unrelated to the fix. Written while the fourteenth run
(`theoretical-limit-carnot`) was still generating; the first thirteen results were known.

**Added runs.** Each example whose registered run skipped is re-run, same body, transport and
working directory, recorded as `<name>.supp1`, then `<name>.supp2` only if `supp1` also skipped.
No further attempts.

**Verdict, replacing §4.** The fix is **verified** when both hold over every file-delivering run,
registered and added:

- **no run has a wrong pointer**; and
- **at least 12 runs have every path absolute and correct, and at most one file run does not.**

A run that shortens or relativises a printed path without naming a wrong location counts against
the second condition, not the first. If either fails, step 9 is revised and a fresh registered
re-run decides.
