# Onboarding: Making a Change

This guide is a contributor on-ramp. It walks you through a single end-to-end "make a change" cycle so you can see exactly how an edit travels from canonical source to shipped, gated plugin artifact.

**The one rule:** edit files under `shared/` only. The `first-principles/` tree is generated output — every file in it carries a `<!-- GENERATED — DO NOT EDIT -->` marker and will be overwritten on the next sync run. See [DEVELOPMENT.md#core-rule-edit-shared-only](DEVELOPMENT.md#core-rule-edit-shared-only) for the rationale.

---

## Prerequisites

- Python ≥ 3.12 + PyYAML ≥ 6.0 (or `uv` — see [GETTING-STARTED.md#prerequisites](GETTING-STARTED.md#prerequisites))
- Git

---

## End-to-end walkthrough: editing `shared/references/five-whys.md`

This example uses `shared/references/five-whys.md` — a stable companion-technique reference that feeds directly into both the orchestrating agent body and the focused-mode five-whys skill. It is a good representative target because one small prose edit propagates to two distinct generated files, making the sync pipeline concrete and observable.

### Step 1 — Make a small edit in `shared/`

Open `shared/references/five-whys.md`. This file contains the canonical procedure for the Five Whys technique. Make a small, reversible change — for example, add one clarifying sentence to the end of the `## Procedure` section or the `## Failure modes` section.

This file is never edited in the generated tree. If you tried to edit `first-principles/agents/first-principles.md` or `first-principles/skills/five-whys/SKILL.md` directly, those edits would be silently overwritten the next time sync runs.

### Step 2 — Regenerate the generated tree

```sh
python3 scripts/sync-content.py --write
```

This command reads all canonical source files under `shared/` and regenerates the entire `first-principles/agents/` tree and all `first-principles/skills/*/SKILL.md` stubs. For your `five-whys.md` edit specifically, the sync pipeline carries the change through two paths:

- **Agent body (`first-principles/agents/first-principles.md`)** — the agent body template in `shared/spine/SKILL-body.md` contains a `{{TOOL:five-whys}}` token. The sync script resolves this by extracting the `## Procedure` section from `shared/references/five-whys.md` and inlining it directly into the generated agent body. Your edit to that section appears in the inlined procedure at the corresponding location.

- **Focused-mode skill stub (`first-principles/skills/five-whys/SKILL.md`)** — the source stub at `shared/skills/five-whys/SKILL.md` contains a `{{PROCEDURE:five-whys}}` token. The sync script resolves this by copying the full body of `shared/references/five-whys.md` (from `## When to reach for this` onward) into the generated skill file.

Both generated files carry a `<!-- GENERATED — DO NOT EDIT -->` marker. They are git-tracked so changes to them are visible in `git diff`, but the content is always derived from `shared/` — never hand-authored.

### Step 3 — Confirm the generated tree updated

Run `git diff` to see the change in both generated targets:

```sh
git diff first-principles/agents/first-principles.md
git diff first-principles/skills/five-whys/SKILL.md
```

The diff should show your edit propagated through both token-substitution paths. The `<!-- GENERATED — DO NOT EDIT -->` marker is present in both files — unchanged, as always.

### Step 4 — Run the validation scripts

Two checks are required before committing. A minimal inline recap:

```sh
python3 scripts/sync-content.py --check   # DUAL-04: verify no drift between shared/ and generated tree
python3 scripts/check-agent.py            # GATE-01: structural integrity of the assembled agent
```

`sync-content.py --check` exits 0 if `shared/` and the generated tree are in sync, exits 1 on any drift. `check-agent.py` validates frontmatter schema, required fields, version format, and description constraints.

For the full per-gate run-detail (how to run each CI gate and interpret results), see [TESTING.md#ci-gates--operational-run-detail](TESTING.md#ci-gates--operational-run-detail). For the complete validation-script inventory, see [DEVELOPMENT.md#validation-scripts](DEVELOPMENT.md#validation-scripts).

### Step 5 — Watch the gates react: what happens when sync drifts

The DUAL-04 sync-drift gate fires in two places:

1. **Pre-commit** — the sync-drift gate runs on every `git commit` (when a hook mechanism is installed). If you commit without running `--write` first, or if you hand-edit a file in `first-principles/` and try to commit, the gate detects the mismatch between `shared/` and the generated tree and blocks the commit with an exit-1 error.

2. **CI (DUAL-04)** — the same check runs in `.github/workflows/validation.yml` on every push/PR to master:

   ```sh
   python3 scripts/sync-content.py --check
   ```

   A PR cannot merge if this gate fails.

**How to reproduce the gate failing:** edit any file in `first-principles/` directly (e.g., add a space to a line in `first-principles/agents/first-principles.md`), then run:

```sh
python3 scripts/sync-content.py --check
```

You will see exit 1 and a diff showing the divergence. To fix: run `--write` to regenerate from `shared/`, then verify with `--check`. This is exactly what the pre-commit gate and DUAL-04 enforce automatically.

For the two mutually-exclusive pre-commit install paths (`install-hooks.sh` vs `core.hooksPath .githooks`), see [DEVELOPMENT.md#pre-commit-hooks](DEVELOPMENT.md#pre-commit-hooks) — install one of the two; do not enable both.

For DUAL-04 run-detail (the exact command the pre-commit sync-drift gate runs), see [TESTING.md#sync-drift-gate](TESTING.md#sync-drift-gate).

### Step 6 — Commit

Once all gates pass, stage and commit. Example:

```sh
git add shared/references/five-whys.md first-principles/agents/first-principles.md first-principles/skills/five-whys/SKILL.md
git commit -m "docs: clarify five-whys procedure"
```

Follow the conventional commits format; for conventions and the full commit-message guide, see [DEVELOPMENT.md#commit-conventions](DEVELOPMENT.md#commit-conventions).

---

## Where to go next

| Document | What it covers |
|----------|---------------|
| [DATA-FLOW.md](DATA-FLOW.md) | The same pipeline you just walked through, as a system trace: every stage from `shared/` source edit to shipped, gated plugin artifact |
| [MEASUREMENT-MAP.md](MEASUREMENT-MAP.md) | The layered test stack and which gate owns which residual |
| [COMPONENT-DIAGRAM.md](COMPONENT-DIAGRAM.md) | Mermaid diagrams of the generation pipeline and measurement stack — what reads what and what generates what |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Full contributor workflow: editing loop, validation-script inventory, pre-commit hook setup, key invariants |
| [TESTING.md](TESTING.md) | How to run every CI gate and the two pre-commit gates, including offline `--self-test` modes |
| [GETTING-STARTED.md](GETTING-STARTED.md) | Install, invoke the agent, companion skills |
