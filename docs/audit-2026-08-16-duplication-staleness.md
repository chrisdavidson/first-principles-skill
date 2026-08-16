# Audit: capability duplication & stale information

Audit date: **2026-08-16**. Repo state audited: `caef7a0`, working tree clean.

Method: tracked-file inventory; cross-surface claim comparison; script-reference mapping
(CI workflow, `check-firewall-battery.sh`, docs, and `docs/data/matrix.json` artifact links);
and a runtime `sys.addaudithook` open-trace of all ten offline gate self-tests to determine
which `tests/**` artifacts are actually read rather than merely named.

## Remediation status

The audit's findings are recorded below as found. This block tracks what has since been acted on;
the §7 effort table keeps its original estimates so the forecast stays auditable against the outturn.

| Stream | Status |
|---|---|
| 0 — version-stamp equality assertion | **DONE.** `scripts/check-version-stamps.py` (VERSION-01), wired into CI and the offline battery (16 → 17 gates). Proven by fault injection on the live tree, not only on fixtures. |
| 1 — fix stale claims (S-1…S-6) | **Partly done as a side effect of stream 5** — see the table below. S-1 and S-2 remain, and both are larger than a wording fix. |
| 2 — retire 4 dead scripts | Open. |
| 3 — adjudicate 9 milestone docs | Open. |
| 4 — `tests/` archival decision | Open. |
| 5 — doc consolidation | **DONE.** All eight doc clusters consolidated; the ninth (the version stamp) is gated by stream 0. Per-cluster owners in §4. |
| 6 — extend SEMGATE (optional) | Open. |

**Stale claims fixed while consolidating**, none of which were the point of the exercise — each
was found because merging two copies forced a comparison:

| Claim | Where | Was |
|---|---|---|
| S-3 skill count | `CLAUDE.md`, `ARCHITECTURE.md` | "the thirteen companion skills live under `first-principles/skills/`" — 14 directories do |
| S-4 accretion | `README.md` ×3 | "Eleven companion skills … has since grown to thirteen"; same shape for examples |
| S-6 index gap | `docs/README.md` | `whole-system-remeasure-verdict.md` unlisted |
| S-8 (new) | 6 surfaces | `{{TOOL:slug}}` documented backwards — see below |
| Body budget | `CONTRIBUTING.md` ×2 | "must stay under 644 lines" listed as an invariant PRs must preserve; gate retired under TEARDOWN-01 |
| Gate counts | `CONTRIBUTING.md`, `CONFIGURATION.md` | "twelve CI gates" / "all 12 CI gates" — 14, and stale before VERSION-01 |
| QUAL-01 in CI | `CLAUDE.md` | listed under "all gates run in `validation.yml`"; it is battery-only |
| Battery count | `CLAUDE.md` | 16/16 → 17/17 |
| Version badge | `README.md` | hardcoded `8.0.0` while shipping `8.17.1`; now a tag-reading badge that cannot go stale |
| Plugin README | `first-principles/README.md` | described v3.0.0: "plugin contents removed", six tools, six examples, no skills directory |

**Still open, and deliberately so.** S-1 (`CLAUDE.md` is ~9 milestones behind) and S-2 (two
competing coverage headlines) are not wording fixes: S-1 needs a judgement about which of ten
milestones' facts still matter to a session, and S-2 needs a decision about whether
`v8.0-final-closure.md` may keep calling a superseded number "final". Both belong to stream 1
proper.

---

## 1. Headline

| Axis | Verdict |
|---|---|
| **Capability duplication (product surface — 14 skills)** | **Clean.** No redundant technique found. Overlap is real but deliberate and partly gated. |
| **Capability duplication (tooling — 23 scripts)** | **3 confirmed dead/duplicate, 1 needs adjudication.** ~80 KB of code. |
| **Information duplication** | **Substantial.** 8 topic clusters restated across 3–7 of the 21 hand-maintained doc surfaces, plus one value (the version stamp) duplicated across 17 *files*. |
| **Stale information** | **Confirmed, concentrated.** Worst offender is `CLAUDE.md` (loaded every session, ~9 milestones behind). |
| **Stale artifacts (`tests/`)** | **441 of 551 tracked files (80 %; 3.0 MB of 3.9 MB) are unpinned archive.** |

Estimated remediation: **13–20 h** for the staleness-only pass (streams 0–4),
**24–39 h** for everything including doc consolidation. Full breakdown in §7.

---

## 2. Capability duplication — product surface

14 skill directories: 13 companion skills + the `first-principles-analysis` launcher; plus the
composer agent. Each `shared/references/<slug>.md` opens with a distinct "When to reach for
this" scope, and several disambiguate their neighbour explicitly in prose
(`fishbone` → "breadth across the cause space, not depth into one chain";
`pre-mortem` → "not the right tool for evaluating options (use trade-off analysis)").

The project has already *acted* on overlap once: `decompose` was merged into `five-whys`
(Phase 110), and its triggers were absorbed rather than duplicated.

Three overlap pairs are formally locked by the SEMGATE-07 block in
`scripts/check-step0-emulator.py:915` and by rows S-A01–S-A06 in `tests/step0-fixture-catalog.md`:

| Pair | Intended winner | Locked by |
|---|---|---|
| absorbed-decompose ↔ five-whys (intra-merge) | `focused-five-whys` | S-A01 / S-A02 |
| theoretical-limit ↔ inversion | `focused-theoretical-limit` (row order) | S-A03 / S-A04 |
| inversion ↔ pre-mortem | `focused-pre-mortem` (row order) | S-A05 / S-A06 |

**Finding CAP-1 (enhancement, not a defect).** Three further plausible overlap pairs are
disambiguated only in reference prose, with no SEMGATE row and no phrase-table precedence lock:
`five-whys ↔ fishbone`, `estimate ↔ theoretical-limit`, `pre-mortem ↔ trade-off`. VAL-04 is
structurally blind to these (it scans skill *descriptions*, never the Step 0 phrase table — the
emulator's own comment says so). A row-order change could silently flip any of them.

**Finding CAP-2 (by design, worth stating).** The 8 technique skills nest *inside* the 5 phase
skills — `inversion.md` says "use inversion during Phase 2 (Challenge Assumptions)",
`second-order.md` says "after Phase 4, before Phase 5". So `challenge-assumptions` ↔ `inversion`
is containment, not redundancy. No action.

**Finding CAP-3 (zero-cost duplication).** Each technique procedure exists twice in the generated
tree — as an agent reference sibling (a verbatim copy) and inside the focused-mode skill stub (via
`{{PROCEDURE:slug}}`). Both are generated from the single `shared/references/<slug>.md` source and
drift-gated by DUAL-04. **Remediation cost: zero.** Do not price it as work.

*Corrected during stream 5:* this finding originally said "three times", counting the agent body
via `{{TOOL:slug}}`. That was the same error as S-8 below — `{{TOOL:slug}}` substitutes a name,
not a procedure. The audit inherited the mistake from the documents it was auditing, which is
itself evidence for how far that claim had propagated.

---

## 3. Capability duplication — tooling

Traceability pinning was checked for each candidate — `docs/data/matrix.json` artifact links are
deep-resolved by TRACE-03, so a script named there cannot simply be deleted.

| Script | Size | In CI | In battery | Matrix rows | Verdict |
|---|---|---|---|---|---|
| `check-sub-skill-routing.py` | 5.7 K | no | no | **0** | **Dead, clean removal** — self-declared deprecated shim; `check-routing-battery.py`'s header names it as replaced. |
| `check-inventory.py` | 27 K | no | no | **0** | **Dead input corpus, clean removal** — parses `.planning/milestones/vX.Y-REQUIREMENTS.md`, a tree that is git-ignored and superseded by `docs/requirements-traceability.md` under CANON-01. Its `--self-test` passes on inline fixtures, so it looks alive. Its "AUDIT-01..AUDIT-04 gate" docstring has no matching matrix rows. |
| `check-focused-output.py` | 7.8 K | no | no | **1** | **Dead but pinned** — deprecated shim, but retiring it means re-tiering its matrix row and regenerating `docs/data/matrix.json` (a tracked file). |
| `check-body-budget.py` | 9.5 K | no | yes (report-only) | **2** | **Retired gate still shipping** — the 644-line budget was torn down under TEARDOWN-01. Keeping it as a reporter is defensible; its 15-place documentation footprint is not. Same matrix re-tier cost. |
| `check-routing.py` | 35 K | no | yes | **15** | **Keep.** Both it and the battery carry a "boundary" signal, but they differ (main-agent DELEGATE/NO-DELEGATE vs. sub-skill boundary) and the battery's header names only the *other two* scripts as replaced. 15 matrix rows depend on it. |
| `run-live-monitoring.sh` | 1.6 K | no | no | pinned | **Keep** — a TRACE-03 assertion (`GEN-02-RUNBOOK`) checks it exists. |

So Stream 2 splits: two clean deletions, and two that additionally require a matrix re-tier +
`check-traceability.py emit` regeneration, which dirties tracked `docs/data/matrix.json`.
Removing all four also removes a combined 34-reference documentation footprint.

---

## 4. Information duplication — 8 hand-maintained clusters

21 surfaces carry the project's prose: root `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`,
`first-principles/README.md`, and 17 files in `docs/` (~4,400 lines excluding the generated matrix).

| Topic | Restated on | Surfaces | Status |
|---|---|---|---|
| **Version stamp** (files, not docs) | 14 × `shared/skills/*/SKILL.md`, `shared/spine/SKILL.meta.yml`, `.claude-plugin/marketplace.json`, `first-principles/.claude-plugin/plugin.json` | **17** | **gated — VERSION-01** |
| CI gate inventory | `CLAUDE.md`, `CONTRIBUTING.md`, `docs/CONFIGURATION.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/DATA-FLOW.md`, `docs/COMPONENT-DIAGRAM.md` | **7** | **done** — owner `docs/ARCHITECTURE.md` (inventory) + `docs/TESTING.md` (run-detail) |
| Sync pipeline / token substitution | `CLAUDE.md`, `ARCHITECTURE`, `CONFIGURATION`, `DATA-FLOW`, `DEVELOPMENT`, `COMPONENT-DIAGRAM` | **6** | **done** — owner `docs/ARCHITECTURE.md`; surfaced S-8 |
| Methodology / 5 phases | `README.md`, `METHODOLOGY-CHEATSHEET`, `FIVE-PHASE-FLOW`, `ARCHITECTURE`, `first-principles/README.md` | **5** | **done** — README trimmed to its front-door pitch; cheatsheet kept as a distinct genre |
| Measurement stack | `CLAUDE.md`, `TESTING`, `MEASUREMENT-MAP`, `testing-agents-headlessly`, `live-monitoring-runbook` | **5** | **done** — owner `docs/MEASUREMENT-MAP.md` |
| Key invariants | `CLAUDE.md`, `CONTRIBUTING`, `CONFIGURATION`, `ARCHITECTURE` | **4** | **done** — owner `docs/CONFIGURATION.md`, each invariant paired with its gate |
| Install instructions | `README.md`, `GETTING-STARTED`, `DEVELOPMENT`, `first-principles/README.md` | **4** | **done** — owner `docs/GETTING-STARTED.md`; plugin README rewritten self-contained |
| Pre-commit hook setup | `CLAUDE.md`, `CONTRIBUTING`, `CONFIGURATION`, `DEVELOPMENT` | **4** | **done** — owner `docs/CONFIGURATION.md` |
| Contribution / editing loop | `CONTRIBUTING`, `DEVELOPMENT`, `ONBOARDING` | **3** | **done** — owner `docs/DEVELOPMENT.md`; both copies now call the battery |

**Consolidation rules applied in stream 5.** One owner per topic holds the full statement; every
other surface keeps a one-line orientation plus a link. Three exceptions, each for a reason that
would otherwise make the consolidation harmful:

- **`CLAUDE.md` is not hollowed out.** It appears in 7 of these clusters, so a naive
  one-owner rule points at gutting it — but its job is to make a *session* competent without
  opening 17 documents. It keeps its operational content (commands, gate list, invariants) and is
  deduplicated against *itself* and made accurate instead.
- **`first-principles/README.md` stays self-contained**, with absolute GitHub URLs rather than
  relative links. It ships inside the plugin, where `docs/` and the repo root do not exist — the
  defect fixed in v8.17.1.
- **Merge the union, not the intersection.** Where copies had diverged, the surviving owner
  absorbs every distinct claim before the others are trimmed. No gate reads doc prose, so nothing
  would catch a fact dropped along with its duplicate.

This is the duplication that actually costs — every gate change is a 7-file edit, and nothing
gates the consistency. It is also the mechanism behind every staleness finding in §5.

**The version stamp is the one duplication with a production consequence, not just a maintenance
cost.** CHANGELOG's preamble states all 17 stamps move in lockstep because plugin installs are
version-gated, not content-gated — a body edit without a bump never reaches an installed session,
and a missed bump at v8.14 left the update path inert. All 17 currently read `8.17.1`, so the
convention is being honoured. But **no gate asserts they are equal**: `sync-content.py` copies
`metadata.version` through per-file rather than propagating from one source (it only re-quotes the
value, `sync-content.py:97`), and `CONFIGURATION.md`'s "Version string invariant" is a *format*
check (double-quoted YAML string), not an equality check. `grep -riE 'lockstep|stamps together'`
across `scripts/`, `.github/workflows/`, and both hook paths returned nothing.

> **Closed (stream 0).** `scripts/check-version-stamps.py` — gate **VERSION-01** — now discovers
> every hand-maintained stamp by glob and asserts they are all equal. It is wired into
> `.github/workflows/validation.yml` and `scripts/check-firewall-battery.sh` (battery 16 → 17).
> The count is *reported*, never asserted: hardcoding "17" would recreate exactly the drift this
> gate exists to catch, so a new skill is picked up automatically and a new skill missing its
> stamp fails on presence instead. Verified by fault injection against the **live** tree — a
> lagging skill stamp, a lagging manifest, and an unquoted YAML stamp are each caught and the
> tree restored — not only against fixtures, since a fixture-only proof does not show the gate
> is wired to anything real.

Structural duplicates worth collapsing outright: `ONBOARDING.md` (112 L) is a worked instance of
`DEVELOPMENT.md`'s "standard editing loop"; `COMPONENT-DIAGRAM.md` (118 L) diagrams what
`DATA-FLOW.md` (104 L) narrates; `CONTRIBUTING.md` (115 L) is a subset of `DEVELOPMENT.md` (230 L).

---

## 5. Stale information — confirmed instances

**S-1 — `CLAUDE.md` is ~9 milestones behind (highest impact).** It names milestones only up to
v8.8; the shipped plugin is **8.17.1**. It is loaded into every session, so its drift propagates
into work rather than sitting on a page. `docs/README.md` covers through v8.14, also behind.

**S-2 — two conflicting coverage headlines, both presented as authoritative.**
`CLAUDE.md:179` carries `133 reproducible / 96 audit-only / 0 gap / 229 total`;
`CLAUDE.md:182` carries `126 / 88 / 0 / 214`. The second matches
`docs/requirements-traceability.md:7`, `docs/MEASUREMENT-MAP.md:40`, and the real artifacts
(`docs/data/matrix.json` = 214 rows). The first survives because
`docs/v8.0-final-closure.md:61` still calls it the **"final coverage headline"** — a document
frozen at v8.0 asserting terminal authority over a figure that has moved twice since.
Cleanest single finding in the audit.

**S-3 — skill-count claim is incomplete in one place.** `CLAUDE.md:117` says "The thirteen
companion skills live under `first-principles/skills/<slug>/SKILL.md`". True as far as it goes,
but **14 directories live there** — the 13 companions plus the `first-principles-analysis`
launcher, which the sentence silently omits. `CHANGELOG.md` and `docs/GETTING-STARTED.md:96` both
state the full picture, so this is localized, not systemic.

**S-4 — accreted-patch staleness in `README.md` (a *class*, not one instance).**
Lines 79, 80 and 108 still say "Eleven companion skills" / "Eleven domain-spread worked examples"
/ "eleven companion-tool slash-only skills", each followed by a retrofit clause
("The skill surface has since grown to thirteen — `estimate` in v7.2…"). Three separate patches
rather than one rewrite. Where this pattern appears, assume more of it.

**S-5 — `docs/adoption-telemetry.csv` appears abandoned.** Two rows, last dated 2026-07-27, never
extended. One inbound reference, from a test document. Confirm against whatever recorded the
project's shift to a personal/portfolio tool before removing — that decision is not in the tracked
tree as far as this audit found.

**S-6 — `docs/whole-system-remeasure-verdict.md` is unindexed.** It is the only tracked `docs/`
file missing from the `docs/README.md` index — a v7.11 verdict that survived the 2026-08-16
prune of 34 historical documents without being re-listed.

**S-8 — the `{{TOOL:slug}}` mechanism was documented backwards on six of seven surfaces
(found during stream 5, cluster 2; now fixed).** `CLAUDE.md`, `ARCHITECTURE.md` (twice, plus a
downstream claim), `DATA-FLOW.md`, `COMPONENT-DIAGRAM.md` and `ONBOARDING.md` all stated that
`{{TOOL:slug}}` is replaced by the `## Procedure` section of `shared/references/<slug>.md`,
"inlining the companion technique procedures directly into the agent body". It does not.
`_expand()` in `sync-content.py:316` substitutes the phrase held under that slug's `agent` key in
`shared/spine/tool-map.yml` — `{{TOOL:fishbone}}` becomes the string "the inlined fishbone
procedure". It is a **naming** token. The procedures are never inlined: searching the generated
agent body for any technique's actual procedure steps returns nothing, and the body's
`## Companion tools` summaries are hand-written in `SKILL-body.md`.

Only `CONFIGURATION.md` had it right, and its correctness was invisible because five louder
copies disagreed with it. This is the clearest demonstration of the cost in §4: the duplication
did not merely risk drift, it actively buried the correct copy. A contributor following
`ONBOARDING.md`'s walkthrough would have edited `shared/references/five-whys.md`, looked in the
agent body for their change, and not found it.

The substituted phrase itself — "the *inlined* fishbone procedure" — is what makes the wrong
reading so natural, and it is shipped agent content rather than documentation. **Left alone
deliberately:** changing it means editing `shared/`, regenerating, and bumping all 17 version
stamps, which is product surface and outside a documentation consolidation. Logged here as
follow-up work.

**S-7 — nine milestone-verdict documents remain in `docs/`** (~1,600 lines):
`gen-01-rearch-milestone`, `whole-system-remeasure-verdict`, `v8.0-final-closure`,
`v8.5-byte-freeze-relaxation`, `v8.6-live-remeasure-verdict`, `v8.6-quality-ab-experiment`,
`v8.7-constraint-teardown`, `v8.7-quality-baseline-freeze`, `v8.14-delivery-verification`.
**Not bulk-prunable** — `v8.7-constraint-teardown.md` is cited normatively by `CLAUDE.md` as the
governing record for TEARDOWN-01/03 and the K-of-5 demotion rule. Needs per-document adjudication:
governing record, or historical narrative?

---

## 6. Stale artifacts — `tests/` is 80 % archive

Measured by tracing every `open()` during all ten offline gate self-tests, plus every `tests/`
path referenced from `docs/data/matrix.json` (TRACE-03 deep-resolves artifact links).

| | Files | Bytes |
|---|---|---|
| **Pinned** (read at runtime by a gate, or a matrix artifact link) | **110** | ~0.9 MB |
| **Archival** (tracked, never read by any gate) | **441** (80 %) | **3.0 MB** |
| Total tracked under `tests/` | 551 | 3.9 MB |

Pinned breakdown: 56 `step0-captures` (v7.11 / v8.5 / v8.6 — consumed by the BATT-06 sentinels),
24 `quality-fixtures-v8.7`, 16 `quality-baseline-v8.7*`, 6 `step0-baseline`, plus 4 catalogs.

Archival breakdown: **330 `step0-captures`** across 8 frozen version directories
(v5.2 → v8.6, unreferenced generations), 58 `quality-baseline` analyses/judgments,
9 `routing-baseline`, 7 `step0-baseline`, 5 `defrobust-v8.11`, and 8 `tests/test_*.py`
phase-invariant suites — CI runs pytest on exactly one file, `scripts/check-links_anchors_test.py`,
so none of the `tests/test_*.py` are CI-executed.

Two constraints on any cleanup: the repo has already filter-repo'd 237 `tests/**.jsonl` once
(2026-07-28, all SHAs rewritten), and the frozen `step0-baseline-v*.md` set is what makes every
prior measurement comparable. Treat this as *which subset is pinned*, not *can we delete* —
and note that `_battery_core.py` embeds capture excerpts as **string literals** (11
`_load_excerpt_v*` generations), so a capture can be load-bearing by provenance while its
filename appears nowhere in code. That is a diff-review question, not a grep question.

---

## 7. Effort estimate

Sequenced so each stream de-risks the next. Assumes one experienced person, full battery re-run
(16 gates) after each stream.

| # | Stream | Effort | Risk | Notes |
|---|---|---|---|---|
| 0 | **Add a version-stamp equality assertion** (§4) | **1 h** | Low | Best value/effort ratio in the audit; the only duplication here with a shipped-product failure mode. |
| 1 | **Fix stale claims** (S-1 … S-6) | **3–5 h** | Low | Mechanical once each number is verified against its artifact. S-2 needs a decision on which doc owns the headline. |
| 2 | **Retire dead scripts** (4) | **4–6 h** | Low / Medium | Two are clean deletions (`check-sub-skill-routing`, `check-inventory`). Two more (`check-focused-output`, `check-body-budget`) also need a matrix re-tier + `emit` regeneration, which dirties tracked `docs/data/matrix.json`. `check-routing.py` stays. |
| 3 | **Adjudicate the 9 milestone docs** (S-7) | **3–4 h** | Medium | Each must be classed governing-record vs. narrative; `CLAUDE.md` cites at least two normatively. VAL-03 breaks on any bad link. |
| 4 | **`tests/` archival decision** | **2–4 h** | Medium | The decision is one commit; the cost is proving the 441 are unpinned (this audit's trace is reproducible) and re-running the battery. Excerpt-provenance caveat above applies. |
| 5 | **Doc consolidation** (9 clusters, §4) | **8–14 h** | Medium | One owner per topic, others become links. Highest ongoing payoff, largest churn. Every excision must survive `check-links.py`. |
| 6 | *(optional)* **Extend SEMGATE to 3 more overlap pairs** (CAP-1) | **3–5 h** | Low | Enhancement, not a defect. Adds catalog rows + hardcoded assertions in the emulator. |
| | **Staleness-only pass (0–4)** | **13–20 h** | | |
| | **Everything (0–6)** | **24–39 h** | | |

**Recommended order if time is limited:** stream 0 plus S-1/S-2/S-3 (≈3 h) buys the most —
the version assertion closes a shipped-product failure mode, and the three claim fixes stop
`CLAUDE.md` from misleading every session that loads it. Stream 5 is the only one that stops the
drift recurring; everything else treats symptoms of it.

**Do not price:** the `{{TOOL:}}` / `{{PROCEDURE:}}` triplication (generated, DUAL-04-gated) or
the 13-skill technique surface (no redundancy found).
