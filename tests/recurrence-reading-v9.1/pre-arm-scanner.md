# Recurrence reading: pre-arm, scanner arm

**Timing:** pre-arm (taken immediately before the first release act of v9.1.0, per D-27-11 —
the tree with plans 27-01/27-02/27-03 landed, before plan 27-05's stamp bump)
**Arm:** scanner
**Reader id:** n/a (the scanner arm has no human reader — see `protocol.md` `## Two instruments,
never summed`)
**Commit sha read:** `33fe35b157a8fdf283d4d9fe89f3194845bea480`

**Instruments run, in this order** (all four from `scripts/gen-gate-docs.py`, in-process,
exactly as `cmd_check()` runs them — see `how derived` per row for the exact call):

1. `run_literal_scan()` (its non-exempt hits, via `literal_scan_problems(run_literal_scan())`)
2. `narrative_restatement_problems()` (the `'finding'`-class subset it already returns)
3. `detail_page_containment_problems()` over the four registered containment surfaces
   (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/gates/*.md`), replicating
   `cmd_check()`'s own per-surface loop (same `marker_pairs`/`check_spelled_out` derivation)
4. `chain_terminus_problems()` over the same four surfaces, same loop

**Result: every instrument reads clean.** This scanner-arm reading is exactly what
`python3 scripts/gen-gate-docs.py --check` reports at this commit (`harvested 22/22 expected
script-backed entries`, exit 0, zero `DRIFT:` lines) — a legitimate outcome for the scanner arm
per `protocol.md`'s own note that this convergence is expected here and is only a defect if the
*prose* arm reduces to it.

| # | file:line | claimed value | live generated value | how derived | tier | fence class | distinct claim |
|---|-----------|----------------|-----------------------|-------------|------|-------------|-----------------|

**Totals this file:** 0 sites / 0 distinct claims.

## Reproduction

```python
import sys, importlib.util
spec = importlib.util.spec_from_file_location("ggd", "scripts/gen-gate-docs.py")
ggd = importlib.util.module_from_spec(spec)
sys.modules["ggd"] = ggd
spec.loader.exec_module(ggd)

literal_read = ggd.run_literal_scan()
literal_problems = ggd.literal_scan_problems(literal_read)          # []

nrp = ggd.narrative_restatement_problems()                          # []

pass1 = ggd.generate_all()
_named_containment_paths = {
    ggd.CLAUDE_MD: "CLAUDE.md",
    ggd.ARCHITECTURE_MD: "docs/ARCHITECTURE.md",
    ggd.TESTING_MD: "docs/TESTING.md",
}
_surface_check_spelled_out = {s.key: s.check_spelled_out for s in ggd._CONTAINMENT_SURFACES}
_surface_terminus_policy = {s.key: s.terminus_policy for s in ggd._CONTAINMENT_SURFACES}
containment_problems, terminus_problems, reached = [], [], set()
for path, generated in pass1.items():
    if path in _named_containment_paths:
        surface_key = _named_containment_paths[path]
        if surface_key not in _surface_check_spelled_out:
            continue
        rel, check_spelled_out = surface_key, _surface_check_spelled_out[surface_key]
    elif ggd.DETAIL_PAGE_DIR in path.parents:
        surface_key = "docs/gates/*.md"
        rel = str(path.relative_to(ggd.REPO_ROOT))
        check_spelled_out = path.stem not in ggd.NARRATIVE_ENTRIES
    else:
        continue
    reached.add(surface_key)
    marker_pairs = ggd._generated_marker_pairs_for(rel)
    containment_problems += ggd.detail_page_containment_problems(
        rel, generated, marker_pairs=marker_pairs, check_spelled_out=check_spelled_out
    )
    terminus_problems += ggd.chain_terminus_problems(
        rel, generated, marker_pairs=marker_pairs,
        terminus_policy=_surface_terminus_policy[surface_key],
    )
# literal_problems == [], nrp == [], containment_problems == [], terminus_problems == []
# reached == {'CLAUDE.md', 'docs/ARCHITECTURE.md', 'docs/TESTING.md', 'docs/gates/*.md'}
```

Confirmed independently by `python3 scripts/gen-gate-docs.py --check` (exit 0, no `DRIFT:`
line) and `python3 scripts/gen-gate-docs.py --self-test` (`SELF-TEST PASS — 112 controls run`)
at this same commit. `git diff f189c99 -- scripts/gen-gate-docs.py` (phase base to this commit)
is empty — no detector was widened, patched or parameterised to produce this reading.
