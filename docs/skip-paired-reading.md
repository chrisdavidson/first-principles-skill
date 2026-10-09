# Procedure skips, current body vs v9.13.0 — the skip-paired reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/skip-paired-preregistration.md`](skip-paired-preregistration.md), registered
before any run. **Captures:** `tests/skip-paired/` — each run's stream, the agent's own transcript,
the delivered files and `cells.json`. **Re-derive:** `python3 tests/skip-paired/run_paired.py read`

---

## The answer in one paragraph

**The skip rate did not reproduce.** On the three prompts whose
[example-rerun-2](example-rerun-2-reading.md) runs skipped the procedure, 18 paired runs gave
**v9.13.0 0 of 9 skips and the current body 1 of 9** (Fisher one-sided p = 0.50). Every one of the
18 runs delivered its six-section file; the single skip by the registered definition is a current-body
run that delivered the file but never read the output template. The 3-of-14 full skips that
prompted this test are therefore not shown to be a property of the current body — on the same
prompts and transport they did not recur once in nine runs. What the test did turn up instead is a
**delivery-pointer defect specific to the current body** (below).

## Result, as registered

| | v9.13.0 (`old`) | `2628e725` (`new`) |
|---|---|---|
| Runs dispatched | 9 | 9 |
| No file under `.first-principles/` | 0 | 0 |
| No `Read` of `output-template.md` | 0 | 1 (`decompose-irreducibility.new.r2`) |
| **Skips** (either condition, §3) | **0 of 9** | **1 of 9** |
| Routing misses retried | 0 | 0 |

Per prompt, every cell delivered a file; the one template-read miss read the rubric and the summary
schema and wrote a complete file. Fisher one-sided p (new > old) = 0.50. As the pre-registration
stated, N = 9 per arm cannot carry a verdict on a small difference; it does bound a large one —
the 3-of-14 rate seen in example-rerun-2 would predict about 2 full skips in 9, and none occurred
on either arm.

**Against example-rerun-2.** There, the registered runs of these three prompts all skipped on the
current body (no file; one made no tool call), and their supplementary runs all delivered. Here,
nine more current-body runs of the same prompts all delivered. Across the twelve current-body runs
of these prompts since, 12 delivered a file. The three skips are best read as an episode the
current data cannot attribute — not to the body, which is the only thing this design can test.

## What the test turned up that it was not looking for

- **A wrong delivery pointer, current body only: 3 of 9 against 0 of 9** (Fisher one-sided
  p ≈ 0.10; with example-rerun-2's `estimate-fermi`, four current-body runs in all). The final
  message names the reports under an absolute path inside this repository
  (`/home/…/Projects/first-principles-skill/.first-principles/…`) although every file was written in
  the run's own working directory; one run then tried to `Read` that path, got "File does not
  exist", and listed the repository's own `.first-principles/` directory. Nothing was written to the
  repository. The likely mechanism: the current body's step 9 (*Deliver the analysis as a file*)
  asks the final message for "the path" of each report, figure, guide and index without saying to
  repeat it as the delivery commands printed it, and the agent absolutises the relative
  `.first-principles/…` path by decoding the scratch working directory's name, which encodes the
  repository's path. v9.13.0's shorter pointer step never did. In ordinary use the working
  directory is the reader's own project and a guessed absolute path would usually be right, so the
  field impact is unmeasured; the fix — print each path exactly as the command that created it
  printed it, or resolve it with `realpath` — is a body change and is not made here.
- **One run read its own example.** `personal-general-2.new.r3` read the plugin's shipped copy of the
  worked example for the same problem (`references/examples/personal-general-2.md`) before writing.
  It is the plugin's own reference tree, not the repository, so it is not contamination in this
  test's sense — but it means a live run can model its answer on the curated example, which any
  future example comparison should check for.

## What limits this reading

Nine runs per arm, three prompts, one model (`claude-sonnet-5`), one CLI version (2.1.289), print
mode, one afternoon. The v9.13.0 arm carries the confound the pre-registration names (its reference
tree under `agents/` registers extra agent types). The design attributes a difference to a body as a
whole, and found none to attribute on the registered outcome.
