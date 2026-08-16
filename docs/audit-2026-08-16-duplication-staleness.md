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
| 1 — fix stale claims (S-1…S-8) | **DONE.** S-3/S-4/S-6/S-8 fixed during stream 5; S-1 and S-2 fixed here; **S-5 retracted** as a false finding (see below). Also fixed the v8.15 Self-Audit Gate rename, which had never reached the user-facing docs. |
| 2 — retire dead scripts | **DONE — 3 of 4 retired.** `check-sub-skill-routing.py`, `check-focused-output.py`, `check-inventory.py` (plus `tests/test_81_inventory.py`). `check-body-budget.py` **kept by decision**: TEARDOWN-01 deliberately preserved the reporter when it retired the gate, and the battery's `[INFO]` line is its live consumer — only its documentation footprint was pruned. |
| 3 — adjudicate 9 milestone docs | **DONE — 9 of 9 adjudicated, 0 deleted.** Three classes (governing record / frozen evidence / gate-pinned artifact); each verdict written as a banner in the document itself, summarised in a `docs/README.md` table. The estimate assumed pruning would follow; it should not — see below. |
| 4 — `tests/` archival decision | **DONE — decision is keep all 550, labelled; nothing deleted.** `tests/README.md` records the classification and `scripts/trace-tests-usage.py` re-derives it. The two-way pinned/archival split was replaced by three tiers, and §6's composition figures are corrected below. The stream-2 orphans are dispositioned in that README. **Original note, kept:** | stream 2 newly orphaned `tests/focused-output-catalog.md`, `tests/sub-skill-routing-catalog.md`, and the `focused-output-baseline-v*.md` / `sub-skill-routing-baseline-v*.md` sets — they were consumed only by the two retired shims. Several sit inside FROZEN-EVIDENCE's pathspec and must not be edited in place. They moved from live fixtures to archive of a retired tool; recorded here so they are not mistaken for still-live. |
| 5 — doc consolidation | **DONE.** All eight doc clusters consolidated; the ninth (the version stamp) is gated by stream 0. Per-cluster owners in §4. |
| 6 — extend SEMGATE (optional) | **DONE.** All three CAP-1 pairs locked: 6 catalog rows (S-A07…S-A12, co-fire + boundary control each) and 3 catalog-independent emulator assertions under SEMGATE-07. No phrase-table change was needed — each pair already resolved as intended, and the measurement came before the assertion. Proven by three injections, not by a passing first run. |

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

**Outturn against estimate.** Streams 0–2 and 5 are complete. Two estimates in §7 proved wrong in
opposite directions, both recorded rather than quietly adjusted:

- **Stream 2 was over-estimated.** Its "matrix re-tier + regeneration" cost rested on two rows
  being pinned by TRACE-03. Both rows carry an **empty `artifact_link`**, and only `artifact_link`
  is deep-resolved — so no re-tier was required to pass any gate.
- **Stream 2 was also under-estimated, for a reason the audit never saw.**
  `tests/test_65_doc_invariants.py` hard-pinned the two retired shims across six tests, and
  `deliverable_path` on one matrix row named a script about to be deleted. Retiring a shim means
  moving its regression guards onto the successor, not deleting them — that migration, not the
  deletion, was the actual work.

- **Stream 4's estimate priced the wrong task.** "The decision is one commit; the cost is proving
  the 441 are unpinned (this audit's trace is reproducible)" assumed re-running the trace would
  confirm §6. It did not: the aggregate held and the composition did not, §6's pinned breakdown
  did not sum to its own headline, and a third tier had to be introduced. The estimate also
  assumed the trace was reproducible in the literal sense — it was a one-off run described in
  prose, so the re-run had to be rebuilt from scratch. It is now committed as
  `scripts/trace-tests-usage.py`, which is the part of stream 4 with a future.

- **Stream 3's estimate was right on cost and wrong on shape.** The 3–4 h and the "VAL-03 breaks
  on any bad link" risk both assumed adjudication would be followed by pruning. It was not:
  nine documents were classed and nine kept. The cost was in *proving* each standing — resolving
  matrix fields rather than counting greps, reading thirteen script comments to separate citation
  from dependency, and one remove-and-restore test — not in excising anything.

**Follow-up logged, not done.** Two shipped-content items each need a `shared/` edit, a regen and a
17-stamp version bump, so they belong to a release rather than to a documentation pass:

1. `shared/spine/tool-map.yml`'s phrase "the *inlined* fishbone procedure" — the wording that made
   S-8's wrong reading natural.
2. `shared/skills/first-principles-analysis/SKILL.md` still says "the validation rubric", the name
   v8.15 replaced with "Self-Audit Gate" precisely because two instruments shared it.

---

## 1. Headline

| Axis | Verdict |
|---|---|
| **Capability duplication (product surface — 14 skills)** | **Clean.** No redundant technique found. Overlap is real but deliberate and partly gated. |
| **Capability duplication (tooling — 23 scripts)** | **3 dead, retired** — ~40 KB of scripts plus `tests/test_81_inventory.py`; a 4th kept by decision. `check-routing.py` looked like a fifth and is not. |
| **Information duplication** | **Substantial.** 8 topic clusters restated across 3–7 of the 21 hand-maintained doc surfaces, plus one value (the version stamp) duplicated across 17 *files*. |
| **Stale information** | **Confirmed, concentrated** — worst offender was `CLAUDE.md`, which every session loads. **Closed in stream 1** (S-5 retracted as a false finding); the table below records each claim as found. |
| **Stale artifacts (`tests/`)** | **441 of 551 tracked files (80 %; 3.0 MB of 3.9 MB) are unpinned archive.** *Stream 4 re-measured this: the 441 holds, but 550 is the tracked count and the sizes were over-read (2.25 MB of 2.85 MB). More importantly the two-way split was wrong in kind — see the closure block in §6.* |

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

> **Closed (stream 6).** All three pairs are now locked, on the same two-layer contract as the
> original three: a catalog row plus a catalog-independent hardcoded literal in
> `check-step0-emulator.py`, so deleting the row cannot make the assertion vacuous. Six rows were
> added — each pair gets a co-fire row (both triggers fire; one winner) and a **boundary control**
> (neither trigger fires; `full-composer`), following the existing odd/even S-A convention.
>
> | Pair | Row | Winner | Locked by row order |
> |---|---|---|---|
> | fishbone ↔ five-whys | S-A07 / S-A08 | `focused-fishbone` | fishbone row 4 over five-whys row 5 |
> | theoretical-limit ↔ estimate | S-A09 / S-A10 | `focused-theoretical-limit` | row 2 over row 8 |
> | pre-mortem ↔ trade-off | S-A11 / S-A12 | `focused-pre-mortem` | row 1 over row 6 |
>
> **Measured before asserted, and nothing was reordered.** Each pair was classified first and the
> observed winner locked — honesty-not-score. All three already resolved the way the reference
> prose implies, so `shared/` was not touched and no version bump is involved. Had one disagreed,
> the finding would have been reported rather than fixed by reordering: the phrase table is
> shipped agent content, and changing it is a release, not an audit pass.
>
> **The pre-mortem ↔ trade-off pair is the one worth reading twice.** Its co-fire prompt fires
> **four** trade-off triggers against **one** pre-mortem trigger, and pre-mortem still wins —
> precedence is by row, not by trigger count. It is tempting to call that a defect, since
> pre-mortem's own prose says it is "not the right tool for evaluating options (use trade-off
> analysis)". It is not: that prose governs a reader choosing a technique for an options task,
> while the row order governs a prompt that opens with a flagship trigger, which is the documented
> D-05 flagship-first design already locked for inversion↔pre-mortem at S-A05. S-A12 is the
> control that keeps the claim honest — remove the pre-mortem trigger and the pair no longer
> resolves to pre-mortem.
>
> **Proven by injection, not by a passing first run.** Every new fixture passed immediately, which
> is the exact condition under which this project has twice shipped a gate that asserted nothing.
> Three injections against the live tree: (1) flipping `_SEMGATE07_TL_EST_EXPECTED` to the wrong
> technique → STEP0-08 RED naming S-A09; (2) editing the catalog's S-A11 prompt → the drift guard
> fires, distinctly from the classification assertion; (3) swapping the fishbone and five-whys
> rows in `shared/spine/SKILL-body.md` → S-A07 flips to `focused-five-whys` and both the catalog
> row and the hardcoded assertion fail. Each was restored and re-verified. Injection 3 is the one
> that matters: it proves the assertion locks the row order rather than merely restating it.
>
> **One thing it broke, and who did not catch it.** Six new rows tripped
> `test_step0_live_task1.py`'s frozen 35-row count (now 41). That guard lives in the
> **live-unwired** tier from stream 4 — a suite CI never runs — so on CI alone the count would
> have gone stale silently. The stream-4 finding demonstrating itself one commit later.
>
> **Scope note, recorded rather than resolved.** CAP-1 is apparatus-sourced, and the post-v8.11
> scope gate bars new instruments absent a use-journal entry or a real-output trigger. This
> extends an existing gate's coverage over pairs the audit had already documented rather than
> building a new instrument, and it was executed on the user's explicit instruction. Noted here so
> the tension is on the record; no findings document was produced, which is what the gate bars.

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
| `check-sub-skill-routing.py` | 5.7 K | no | no | **0** | **RETIRED** — self-declared deprecated shim; `check-routing-battery.py`'s header names it as replaced. |
| `check-inventory.py` | 27 K | no | no | **0** | **RETIRED** — parsed `.planning/milestones/vX.Y-REQUIREMENTS.md`, a corpus that exists locally but is git-ignored (absent from CI and a fresh clone) and superseded by `docs/requirements-traceability.md` under CANON-01. Its `--self-test` passes on inline fixtures, so it looks alive. Its "AUDIT-01..AUDIT-04 gate" docstring has no matching matrix rows. |
| `check-focused-output.py` | 7.8 K | no | no | **1** | **RETIRED.** The "pinned" verdict was wrong: the row's `artifact_link` is empty and only `artifact_link` is deep-resolved, so no re-tier was needed. Its `deliverable_path` did name the script, which is reported but never existence-checked — repointed at the successor so the matrix would not carry a dangling path. |
| `check-body-budget.py` | 9.5 K | no | yes (report-only) | **2** | **KEPT by decision.** TEARDOWN-01 retired the gate but deliberately preserved the reporter, and the battery's `[INFO]` line is a live consumer — deleting it would reverse a documented decision. Only its documentation footprint was pruned. |
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

**S-5 — RETRACTED. Not a finding.** ~~`docs/adoption-telemetry.csv` appears abandoned.~~

The file is **already local-only by an explicit, recorded decision** — untracked and gitignored at
commit `de08ffb` (2026-07-28, "chore: keep adoption telemetry local-only"), whose message states
the reasoning in full: adoption stopped being a graded surface at v8.8 (personal/portfolio tool,
not a distribution play), the populating script `scripts/snapshot-traffic.sh` was removed in the
same technical-debt audit, and the file was deliberately kept on disk while no longer being
published. `.gitignore:15-17` carries the same rationale as a comment. So the decision *is*
recorded in the tracked tree, and the file is not a stale artifact but a deliberate one.

**Why the audit got this wrong — a method defect worth keeping.** The finding came from reading
`ls docs/`, which lists the working directory, while every other check in this audit ran against
`git ls-files`. The completeness sweep that verified each `docs/` file was indexed in
`docs/README.md` iterated the *tracked* list, so it never examined this file and never flagged the
mismatch. An untracked file sitting in a tracked directory is invisible to a tracked-file
inventory and conspicuous to a directory listing; mixing the two sources produced a finding about
a file that was not in the audit's own scope. **Fix on sight anywhere else in this document:
`ls` is not `git ls-files`.**

Acting on this would have deleted a local file git could not restore.

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

> **Closed (stream 3), and the binary in the question was wrong.** All nine were adjudicated and
> **none deleted**. "Governing record or historical narrative?" admits no answer for five of them:
> a document can be neither authority nor disposable narrative but *frozen evidence* — a
> measurement, true of its date and of nothing later, that live artifacts cite for provenance.
> Three classes were needed:
>
> | Class | Documents |
> |---|---|
> | **Governing record** — decision still in force | `v8.7-constraint-teardown`, `v8.5-byte-freeze-relaxation`, `v8.14-delivery-verification` |
> | **Frozen evidence** — measurement, cited for provenance | `whole-system-remeasure-verdict`, `v8.7-quality-baseline-freeze`, `v8.6-quality-ab-experiment`, `v8.6-live-remeasure-verdict` |
> | **Gate-pinned artifact** — a gate resolves the file itself | `gen-01-rearch-milestone` |
> | **Split** — governing for its dispositions, superseded for its figures | `v8.0-final-closure` |
>
> Each verdict is written **into the document**, not only into an index, because the failure this
> stream exists to prevent — a document asserting terminal authority over a figure that has since
> moved — is exactly what happens when the warning lives somewhere the reader is not. A summary
> table sits in `docs/README.md` for navigation; the banners are the load-bearing part.
>
> **Three things the adjudication established that the audit had wrong or had not checked:**
>
> 1. **"Is it gate-pinned?" is confounded, and the confound had to be removed before the question
>    meant anything.** Removing *any* of the nine fails VAL-03, because `docs/README.md` links all
>    nine — that measures the index, not the document. The documented prune convention (demote the
>    index link to backticks) clears it. So the discriminating question is narrower: **does a gate
>    resolve the file itself, independent of the index link?** For eight of the nine, no.
> 2. **`gen-01-rearch-milestone.md` is the one exception.** It is set as `artifact_link` on
>    TRACE-03 self-test fixture (9) and is deep-resolved; removing it makes
>    `check-traceability.py --self-test` exit 1 with `artifact file not found`. Verified by
>    removal, then restored — not by grep, for the reason §3 records twice.
> 3. **`whole-system-remeasure-verdict.md` looks pinned and is not.** Thirteen matrix rows name
>    it, but as one `deliverable_path` (the RECON-01 row, authored at `check-traceability.py:872`;
>    reported, never existence-checked) and twelve `gap_rationale` prose mentions. Confirmed the
>    same way as gen-01 and with the same grade of proof: with the file moved away, TRACE-03
>    `--self-test` exits **0** and the battery's only failure is VAL-03. Same field-level
>    distinction that made §3's original `check-focused-output.py` verdict wrong.
> 4. **Every remaining `scripts/` mention is a provenance comment, not a dependency.** All script
>    references to the other seven — across `_battery_core.py`, `check-step0-live.py`,
>    `sync-content.py`, `check-quality-harness.py`, `check-body-budget.py`,
>    `check-firewall-battery.sh`, `check-traceability.py` and both pre-commit hooks — were read
>    line by line rather than counted. None existence-check a file; several *cite* one as the
>    authority for a live behaviour, which is a reason to keep the document but not a gate.
>
> **A per-file sweep nearly shipped a false claim here, which is the DETECT-05 lesson recurring.**
> The first pass read script mentions for five of the seven non-pinned documents in one loop and
> left `whole-system-remeasure-verdict` out of it — the one document whose banner made the
> strongest negative claim ("no gate fails if it disappears"). A loop proves every *file in the
> loop* was seen, not every *claim-site*. The omission was caught in review, the three lines were
> read, the removal test was run — and the claim turned out to be **wrong as originally written**:
> VAL-03 does fail, for the index reason above. Recorded rather than quietly corrected, because
> the near-miss is the finding.
>
> **`v8.14-delivery-verification.md` is the case against pruning by reference count.** It has the
> fewest inbound references of the nine (two, both from the index) and is the least prunable on
> merit: it is the published form of a pre-registered STOP that still governs Phases 189–191 and
> GREENMEAN-01's WON'T-DO scope, with both pre-registrations committed before their evidence.
> Deleting it on a grep count would have destroyed the artifact the project's honesty posture
> exists to protect.
>
> **One refuted-figure check, done by reading rather than grepping.** `v8.7-quality-baseline-freeze`
> is the only one of the nine carrying figures the v8.13 DETECT-05 detector fix reversed, and it
> already carries the corrections inline at the point of use (rows 1–2 of the sweep's §3a table).
> Its banner points at them, since a correction 128 lines in is invisible to someone quoting the
> summary. No uncorrected reversal was found in the other eight.

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

> **Closed (stream 4). Decision: keep all 550 tracked files, labelled; nothing deleted.**
> The classification lives in [`tests/README.md`](../tests/README.md) and is re-derived, not
> asserted, by `scripts/trace-tests-usage.py` — a manual tool of the same standing as
> `check-traceability.py emit`. §6's own claim of reproducibility is what made re-running it the
> first task; the re-run agreed on the aggregate and disagreed on almost everything else.
>
> **The aggregate reproduces. The composition does not, and §6 does not sum to itself.**
> Two separate facts, stated separately because the coincidence is misleading:
>
> - **Aggregate agrees.** 441 archive against 441 — but partly by luck: this count runs against
>   550 tracked files, not 551 (stream 2 deleted `tests/test_81_inventory.py`), and it moves 7
>   pytest suites *out* of archive that §6 had counted *in*.
> - **Composition disagrees, and §6's pinned breakdown never added up.** As written it lists
>   56 captures + 24 quality-fixtures + 16 quality-baseline + 6 step0-baseline + 4 catalogs =
>   **106**, under a headline of 110. Measured: **55** captures, **24** quality-fixtures, **16**
>   quality-baseline, **1** quality-probe, **3** catalogs opened at runtime, plus 2 files pinned
>   only by `artifact_link` — 102 gate-pinned. **Zero** `step0-baseline-v*.md` files are opened by
>   any gate; §6's 6 came from counting matrix `deliverable_path` entries, which are reported and
>   never existence-checked. Same field-level error as §3 and as stream 3's finding 3.
>
> **Two tiers were not enough, and the missing one is the finding.** Splitting only
> pinned/archival hid **7 pytest suites carrying 123 assertions that no CI job runs** — CI runs
> pytest on exactly one path, `scripts/check-links_anchors_test.py`. §6 classed them as archive,
> which is the more comfortable of the two available wrong answers: they are live tests with no
> automation behind them, including the retirement guards stream 2 migrated into
> `test_65_doc_invariants.py` one commit earlier. A third tier, **live-unwired**, now names them.
> Wiring them into CI is logged as follow-up, not done here — classification was the remit.
>
> **The audit's own excerpt caveat is wrong, and the way it is wrong is instructive.**
> `_battery_core.py` does **not** embed capture excerpts as string literals; every
> `_load_excerpt_v*` helper calls `Path.read_text()` at runtime. The real trap is the opposite
> shape: a loader passed as a *function object* inside a sentinel tuple
> (`..., _load_excerpt_v74, ...`) is invisible to `grep '_load_excerpt_v74('`, so a live
> generation reads as dead code. This nearly shipped here — the grep said no call site, the
> runtime trace showed five v7.4 files being read, and the trace was right. Measured result:
> **8 of 12 capture generations (164 files) are read by nothing**, which is a runtime observation,
> not an inference about loaders.
>
> **`FROZEN-EVIDENCE` does not protect against deletion**, contrary to the reading its name
> invites. It is `git diff --quiet` over a pathspec: it catches uncommitted worktree edits to
> frozen files, and a committed `git rm` passes it clean.
>
> **A VAL-03 blind spot, found while checking this closure's own two links.** `_check_docs_file`
> skips any link target beginning with `../` — its docstring says so — so parent-relative links
> out of `docs/` are counted by no gate. There are five in the tree. Four resolve; the fifth,
> `docs/requirements-traceability.md:249`, pointed at `../.planning/PROJECT.md`, which is
> **gitignored and untracked** — dead in a fresh clone, and directly contradicting the
> `docs/history/` line two rows above it in the same list, which is deliberately backticked rather
> than linked for exactly that reason. Demoted to backticks here. The gate gap is recorded, not
> closed: teaching VAL-03 to resolve `../` targets is a change to a gate's behaviour and belongs
> to a milestone, not to an audit remediation pass.
>
> **Stream-2 orphans dispositioned.** All six are in the archive tier. The two baseline sets sit
> inside the `FROZEN-EVIDENCE` pathspec, so the battery now protects the frozen evidence of a
> retired tool — **both entries are kept deliberately**: retiring a tool does not unfreeze what it
> measured, and dropping them would make those files editable in place, reducing protection to
> tidy a list.

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
