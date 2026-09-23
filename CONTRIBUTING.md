<!-- generated-by: gsd-doc-writer -->
# Contributing

Thank you for contributing to first-principles-skills. This project ships a Claude Code plugin as pure Markdown — no compiled artifacts, no build step. Contributions follow a `shared/` → sync → validate → PR loop.

## Before you start

- **Python ≥ 3.12 + PyYAML ≥ 6.0** are required to run sync and validation scripts.
- **Claude Code CLI** is required to run the routing battery and plugin validation.
- Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the source-of-truth vs. generated surface distinction — it is the single most important thing to know before making changes.

## The core rule

**Edit `shared/` only. Never edit `first-principles/` directly.**

The `first-principles/` tree is generated output. Every file in it carries a `<!-- GENERATED — DO NOT EDIT -->` marker. Direct edits will be overwritten on the next sync run and blocked by the pre-commit drift gate.

### The second rule: a claim about this tree needs a falsifier, not a grep

If your change states a **fact about this repository** — a count, a coverage claim, "every X does
Y", "no gate asserts Z" — `CLAUDE.md`'s [Claims and falsifiers](CLAUDE.md) section binds it, and it
binds any plan, plan-check or execution here. In short:

- Pair the claim with a command that **exits non-zero if the claim is false** — not one that
  confirms the sentence is present. `grep -c '<literal>' <file> == N` is a *presence check*; it
  passes happily while the sentence it pins is false.
- A reviewer re-derives the falsifier independently rather than re-running yours, because one
  written by the claim's author reproduces the author's blind spot.
- If a review finds one of your claims false, register it in `REGISTRY` in
  `scripts/check-retracted-claims.py` (gate **RETRACT-01**) **in the same change as the fix** —
  correcting it only where it was found leaves the copies.

This rule exists because v9.7.0 shipped the same false claim twice, three phases apart.

## Standard contribution loop

```sh
# 1. Edit files under shared/ — never first-principles/
python3 scripts/sync-content.py --write   # 2. regenerate the plugin tree
bash scripts/check-firewall-battery.sh    # 3. run every offline gate; expect FIREWALL: GREEN
git add -u && git commit -m "feat: <description>"
```

Step 3 is deliberately the whole battery rather than a list of individual scripts: a hand-picked
list omits gates added later and keeps naming ones that were retired. The loop is documented in
full, including the faster inner loop for iterating, in
[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md#standard-editing-loop).

## Setting up pre-commit hooks (recommended)

Install the hook so sync drift is caught before you push:

```sh
./scripts/install-hooks.sh
```

Five gates fire on `git commit`, in a fixed order, mirrored identically across
`.githooks/pre-commit` and `scripts/git-hooks/pre-commit`. See
[CLAUDE.md](CLAUDE.md#pre-commit-gates)'s `### Pre-commit gates` section and
[docs/CONFIGURATION.md](docs/CONFIGURATION.md#pre-commit-hooks) for the enumeration — the list is
not repeated here, following this file's own `## CI gates` discipline below. (A body-budget gate
used to run alongside the first of these; it was retired under TEARDOWN-01 and no longer fires.)

There is a second, mutually exclusive mechanism (`git config core.hooksPath .githooks`) — pick
one, never both. Full detail, including what `install-hooks.sh` does to an existing hook, is in
[docs/CONFIGURATION.md](docs/CONFIGURATION.md#pre-commit-hooks).

## What you can contribute

| Area | Where to edit |
|------|--------------|
| Agent methodology (phases 1–5) | `shared/agent/` and `shared/spine/SKILL-body.md` |
| Agent frontmatter (description, version, tools) | `shared/spine/SKILL.meta.yml` |
| Companion technique reference (Five Whys, fishbone, etc.) | `shared/references/<slug>.md` |
| Focused-mode skill stubs | `shared/skills/<slug>/SKILL.md` |
| Worked examples | `shared/examples/` |
| Validation scripts | `scripts/` |
| Routing catalogs | `tests/routing-catalog.md` (check-routing.py), `tests/routing-battery-catalog.md` (BATT-06), `tests/step0-fixture-catalog.md` (STEP0-06). **Check `tests/README.md`'s tier table first** — most of `tests/` is archive tier, read by nothing that runs, and several paths are frozen under FROZEN-EVIDENCE. `tests/sub-skill-routing-catalog.md` is archive: its consumers were retired at the 2026-08-16 audit |
| Documentation | `docs/` — register new pages in the `docs/README.md` nav; intra-docs links use bare filenames (no `docs/` prefix) |

## Key invariants

All PRs must preserve the invariants listed in
[docs/CONFIGURATION.md](docs/CONFIGURATION.md#key-invariants), which names the gate enforcing
each one. Most are caught automatically by the battery above; the two that are conventions
rather than gates are flagged there as such.

One rule that is easy to trip over, because it changed: the agent body's line count is **not**
an invariant. The 644-line gate was retired under TEARDOWN-01 and is now report-only.

**a guard guards the product; a guard is not itself guarded** — the chain
`999.27 → 999.28 → 999.30` is the measured justification. [docs/PROCESS.md](docs/PROCESS.md)
holds the full depth rule, the product/apparatus review split, and the rework cap; this file
cites it and does not restate its rules.

## CI gates

All PRs must pass the CI gates in `.github/workflows/validation.yml`. Before pushing, run the
whole offline set in one shot and check for a GREEN verdict:

```sh
bash scripts/check-firewall-battery.sh
```

The gate list itself is not repeated here — it changes, and a stale copy in a contributor-facing
file is worse than no copy. Two places carry it:

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#ci-and-pre-commit-gate-inventory) — the canonical
  inventory: every gate, its CI job, its script, and what it checks.
- [docs/TESTING.md](docs/TESTING.md) — how to run each one locally and interpret its output.

## Commit message format

Follow conventional commits:

```
feat: <description>
fix: <description>
refactor: <description>
docs: <description>
test: <description>
chore: <description>
```

## Submitting a PR

1. Fork the repository and create a branch from `master`.
2. Make your changes in `shared/`, run sync and all validation scripts locally.
3. Ensure all CI gates pass.
4. Open a PR against `master` with a clear description of what changed and why.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
