# Persona-view fixtures (v9.18)

Five hand-written persona views used by `scripts/check-persona-view.py`'s `--self-test` and by
its CLI-mode smoke checks. Every fixture cites only facts, ids and numbers that its named source
analysis already carries — none is derived from a user's private analysis (D-08).

Each fixture is in the Phase 87 memo format (D-11): the nine-line memo header (title line, blank,
the To/Re/Basis/Band blockquote block, blank, the provenance sentence, blank), then exactly five
single-line prose paragraphs separated by blank lines — an `In brief:` paragraph first, then one
paragraph per the role's fixed `**Questions (in order):**` list from
`shared/spine/references/persona-views.md`, in order. The questions themselves are never printed;
no bullets, bold labels or headings appear in the body.

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
(`shared/spine/references/persona-views.md`): the exact nine-line memo header, the `In brief:`
paragraph, the role's fixed question list answered in order as prose paragraphs, the role's word
band, and the citation grammar. None is copied from, or post-processed from, the output of a live
`first-principles` run — with the one exception named below.

## Frozen pre-87 must-fail fixture

`pre87-product-business-2-decision-owner.md` is a byte copy of the persona example shipped at
commit `87e9d0ac` (`shared/persona-examples/product-business-2-decision-owner.md`), itself a real
`/first-principles:persona` run against `shared/examples/product-business-2.md` rendered as
`analysis-20260101T000001Z.md`. It was frozen before Phase 87 re-derived that example under the
new voice rule. It is the one file in this directory that is not hand-written, and it is never
edited. It exists so PERSONA-GATE can show it fails for PV-DIRECTIVE: it opens "Decide to build
the reporting rewrite this quarter..." and repeats several consecutive words of §6's own
`**Recommended approach:**` line — the restated-recommendation shape the voice rule now bars. It
keeps its original pre-memo five-line header by design: it is a byte-frozen copy and is never
rewritten to the Phase 87 memo shape, including this plan's own revision of that shape.
