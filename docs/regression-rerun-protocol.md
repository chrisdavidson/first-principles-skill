# Protocol — Do the body fixes resolve the example re-run's regressions?

**Id:** `regression-rerun` · **Registered:** 2026-09-29, before any run under this id.

The [example re-run](example-rerun-reading.md) found five regressions. One was a defect in a shipped
example (`estimate-fermi`), fixed directly in `ceb16c52`. The other four are agent behaviours;
branch `rerun-fixes` (`28f2bd9f`) adds one body rule for each. This run re-runs each affected
example **twice** on that body, with the same prompts and transport as the example re-run
(`tests/regression-rerun/run.py`), and scores each regression by a check fixed here.

| Regression | Example | Resolved when, in both runs |
|---|---|---|
| A combined figure landed below its inputs (4.4 × 1.1–1.2 reported as 4.3) | `science-engineering` | every figure a hop combines from others lands where its operation puts it — recomputed by hand for each combination in the chains |
| A success criterion foreclosed the hybrid option | `software-systems-2` | a split or hybrid of build and buy is explicitly evaluated as an option, and no success criterion requires exactly one option |
| Ids written `GT6`; an estimated tier shown as practice | `theoretical-limit-carnot` | no bare `GT` + digits id appears, and every current-practice or measured-performance figure is labelled measured, published design value, or estimate |
| Return and loan rate compared without a stated basis | `personal-general-2` | the expected return and the mortgage rate are each stated as nominal or real (and pre- or after-tax), and are compared on the same basis |

**Resolved:** a regression is resolved when both of its runs pass its check. **The fixes are
confirmed** when all four are resolved. A run that fails is reported with what it did, and the
rule it answers to is revised under a new id rather than re-scored.

A check that needs reading, not a pattern, is done by reading the document and recording the
evidence — the figure, the sentence, the label — in the reading, so it can be re-checked. One model,
two runs per example: a pass shows the rule working on these runs, not a rate.
