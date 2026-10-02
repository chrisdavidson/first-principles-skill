# Persona-view fixtures (v9.18)

Five hand-written persona views used by `scripts/check-persona-view.py`'s `--self-test` and by
its CLI-mode smoke checks. Every fixture cites only facts, ids and numbers that its named source
analysis already carries — none is derived from a user's private analysis (D-08).

## Provenance

| Fixture | Role | Source |
|---------|------|--------|
| `product-business-2-decision-owner.md` | Decision Owner | `shared/examples/product-business-2.md` |
| `product-business-2-operator.md` | Operator | `shared/examples/product-business-2.md` |
| `product-business-2-risk.md` | Risk | `shared/examples/product-business-2.md` |
| `product-business-2-skeptic.md` | Skeptic | `shared/examples/product-business-2.md` |
| `personal-general-risk.md` | Risk | `shared/examples/personal-general.md` |

Both sources are shipped worked examples under `shared/examples/`, the same corpus every other
checker in this repo (`check-report-figures.py`, `check-summary-block.py`) reads as fixture
material. Neither fixture here, nor any file in this directory, is derived from `.first-principles/`
or from any analysis a user ran against their own problem — a persona view of a live, private
analysis is never checked into this repository.

## D-08 falsifier

`product-business-2-decision-owner.md` cites `GT-5?` — the one `?`-marked (unverified) ground
truth product-business-2.md declares. Replacing that citation with `GT-6` (a ground truth the
source does not declare at all) must make `check-persona-view.py` fail with exactly `PV-ID`;
replacing it with `GT-5` (dropping the `?`, which claims the ground truth is verified when §3
declares it is not) must also fail with exactly `PV-ID`. Both are exercised as the `M-ID` and
`M-AGREE` must-fail controls in `scripts/check-persona-view.py --self-test`.

## Hand-written, not generated

Every fixture here is hand-written directly against the persona contract
(`shared/spine/references/persona-views.md`): the exact five-line header, the role's word band,
and the citation grammar. None is copied from, or post-processed from, the output of a live
`first-principles` run.
