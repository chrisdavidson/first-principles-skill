# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Version stamps move in lockstep.** Plugin installs are version-gated, not content-gated,
so every release bumps all 17 stamps together — the 14 `shared/skills/*/SKILL.md` sources
(13 companion skills plus the `first-principles-analysis` launcher),
`shared/spine/SKILL.meta.yml`, `.claude-plugin/marketplace.json`, and
`first-principles/.claude-plugin/plugin.json`. A body edit without a bump never reaches an
installed session.

## [Unreleased]

## [8.17.4] — 2026-08-17

Closes the second-hop residual v8.17.3 named and deferred. **Overturns DEC-A.**

### Fixed

- **The agent's reference siblings are now anchored to each other.** v8.17.3 fixed the first hop
  (agent body → `references/validation-rubric.md`) and left 16 links *between* files in
  `first-principles/agents/references/` bare — 4 `-detail.md` pointers plus 12 cross-technique
  links (`](pre-mortem.md)`, `](inversion.md)`, `](trade-off.md)`, `](five-whys.md)`). So an
  agent that successfully opened `five-whys.md` and followed its pointer to `five-whys-detail.md`
  failed at the second hop in exactly the way the first hop used to. All 16 now carry the
  `${CLAUDE_PLUGIN_ROOT}/agents/references/` prefix. With the four `-detail.md` files and the
  three spine references carrying zero relative links, the agent-side reference graph is now
  clean end to end.

- **`shared/references/*.md` deliberately keeps the bare form.** The rewrite lives at the
  emission layer (`_absolutise_agent_ref_links()` in `sync-content.py`), not in the source,
  because those same 16 links also feed the skill stubs — where the correct target is a
  different path. Skill stubs are byte-unchanged by this release.

### Changed

- **DEC-A is overturned, deliberately and by name.** DEC-A held that an agent reference sibling
  must keep its bare pointer because it lands in the same directory as its detail file. That
  reasoning was true of the filesystem and false of the reader: a model opens these files with
  the *session* working directory in force, so "same directory" never applied to it.
  GATE-02-v8.5's (g) assertion is inverted to match — anchored exactly once, bare **zero** times.

- **GATE-02-v8.5 gained a directory-wide bare-target sweep.** The per-slug loop only ever visited
  the four `SLUGS_WITH_DETAIL` pointers; the 12 cross-technique links lived in files it never
  named, so a per-slug assertion could not have caught them and could not catch a future one. The
  sweep asserts the property that actually matters — no emitted agent reference file carries a
  bare markdown target — and fails loudly if it matches zero files rather than reporting a
  vacuous clean.

- **An unrecognised bare `.md` target now raises.** The allowed-target set is derived from
  `TOOLS` / `SLUGS_WITH_DETAIL` / `SPINE_REFERENCES` rather than hand-maintained. A bare link to
  something not emitted into that directory is a typo: passing it through would leave the
  same-class bug alive with no signal, and anchoring it blindly would mint a broken absolute
  path.

### Scope of the claim on this surface — narrower than the agent body's

The documented substitution table covers **"Skill and agent content"** — the registered
component content the harness itself loads. These reference siblings are **not** registered
components; they are plain files the model opens with Read, and the docs are **silent** on
whether placeholders are substituted inside them (checked 2026-08-17 against
`code.claude.com`'s plugins-reference and skills pages; the env var is also not exported to an
agent's Bash). The token is used here because it is **self-describing and inference-resolvable**
— the model reached the file via an already-expanded absolute path, so
`${CLAUDE_PLUGIN_ROOT}/agents/references/x.md` is trivially recoverable, whereas a bare `x.md`
requires reconstructing the directory from nothing. This is a strictly better pointer, not a
guaranteed-substituted one. v8.17.3's substitution claim applies to the agent body and is not
restated here.

### Still open

The **12 cross-technique links reaching the skill stubs** (`](five-whys.md)` in
`skills/fishbone/SKILL.md`) remain broken, and this is not the same defect wearing a different
hat. Those break because they point at a *wrong path* inside a resolution mechanism that works —
a slash-invoked skill does resolve against its own directory — whereas the agent surface had no
resolution at all. The correct target is genuinely undecided (`D-02`): the peer skill stub at
`${CLAUDE_PLUGIN_ROOT}/skills/five-whys/SKILL.md`, or the same content on the agent surface at
`${CLAUDE_PLUGIN_ROOT}/agents/references/five-whys.md`. Those are not interchangeable, so the
choice is a decision, not a sweep.

Also still owed, unchanged from 8.17.3: **no live run has verified the Self-Audit Gate now
fires.**

Battery: 17/17 GREEN. Three fault injections: a broken anchored link on the sibling glob (VAL-03
reports it), an unrecognised bare target (emission raises), and the rewrite call removed
(GATE-02's sweep names `inversion.md` and `second-order.md` — files the per-slug loop never
visits).

## [8.17.3] — 2026-08-16

Fixes the reason the agent could not open its own Self-Audit Gate.

### Fixed

- **Agent-body reference links are now plugin-root-anchored.** Every `references/…` link the
  agent body carried was file-relative. An agent body is read with the *session* working
  directory in force — not the directory the agent file lives in — so
  `references/validation-rubric.md` resolved against the user's project, where it does not
  exist, and the read failed. All 25 of the agent body's reference links (21 in
  `shared/spine/SKILL-body.md` plus the four `-detail.md` pointers `sync-content.py` emits onto
  the agent surface) now carry the `${CLAUDE_PLUGIN_ROOT}/agents/references/` prefix, which
  Claude Code substitutes in agent and skill content wherever it appears. This reaches the
  Self-Audit Gate, the output template, the assumption taxonomy, the fourteen worked examples,
  and the four on-demand detail appendices.

  The live v8.14.0 run against the Umesh Bhatt article is the observation behind this: zero
  `Band:` / `Rigorous` / `Hand-wavy` markers across 533k characters — the Phase 5 gate never
  fired. Absolutising the link removes one of that failure's two documented causes (the other,
  a name collision with a user-requested rubric, was addressed at 8.15.0). **It is not proof the
  gate now fires** — no live run has been taken since; that measurement is still owed.

- **Skill stubs deliberately keep the file-relative form.** A slash-invoked skill is resolved by
  the harness against its own skill directory, so `references/<slug>-detail.md` already works
  there. `_rewrite_detail_link()` in `sync-content.py` now takes a per-surface prefix
  (`AGENT_REF_PREFIX`) instead of one hardcoded form.

**Known residual — this fixes the first hop, not the whole chain.** The agent's own reference
siblings under `first-principles/agents/references/` still carry 16 file-relative links between
each other (`](pre-mortem.md)`, `](five-whys-detail.md)`, and so on). Those resolve correctly
*within that directory* but not from a session working directory, so an agent that successfully
opens `${CLAUDE_PLUGIN_ROOT}/agents/references/five-whys.md` and then follows its pointer to
`five-whys-detail.md` fails in exactly the way this release fixes one level up. Left alone
deliberately: it is outside the agent body, and the bare form there is a DEC'd invariant
(DEC-A) that GATE-02-v8.5 actively asserts, so changing it is a separate, gated decision rather
than a tail of this one. The Self-Audit Gate, output template, assumption taxonomy and worked
examples are all reached in one hop from the body and are therefore unaffected by this residual.

### Changed

- **VAL-03 resolves `${CLAUDE_PLUGIN_ROOT}` rather than skipping it.** The cheap accommodation
  would have been to skip the unfamiliar prefix the way `http://` is skipped — which would have
  dropped the entire agent body out of link checking while `check-links.py` still printed PASS.
  `_resolve_link` maps the token onto `first-principles/` instead, so every absolutised link is
  still validated, and validated against the path the agent will actually open. Section 8 of the
  `--self-test` pins this with a positive assertion, a non-vacuity check that the rubric really
  is there, and a negative control; both a repointed target and a reversion-to-skip were
  fault-injected and caught.
- **GATE-02-v8.5 asserts the two assembly surfaces separately.** The drift guard previously
  expected one rewritten pointer form on both the agent body and the skill stub. It now expects
  the plugin-root-anchored form on the agent body — *and zero file-relative fallbacks there* —
  and the file-relative form on the stub.

Battery: 17/17 GREEN.

## [8.17.2] — 2026-08-16

Closes all six streams of the 2026-08-16 duplication-and-staleness audit (PR #8).

**Agent and skill content are byte-unchanged from 8.17.1.** `shared/` was not touched by this
release, so the assembled agent body and all fourteen skill stubs are identical. The only shipped
change inside the plugin is `first-principles/README.md`, which had still described v3.0.0. The
version moves because installs are version-gated, not content-gated — a stamp that does not
advance is a change that never reaches a session. Do not read a behaviour difference into this
bump; there is none to read.

### Added

- **SEMGATE now locks all six documented technique-overlap pairs, not three.** The audit's CAP-1
  finding was that `fishbone ↔ five-whys`, `theoretical-limit ↔ estimate` and
  `pre-mortem ↔ trade-off` were disambiguated only in reference prose — no catalog row, no
  precedence lock — so a Step 0 phrase-table reorder could silently flip any of them, and VAL-04
  is structurally blind to that axis. Six rows added to `tests/step0-fixture-catalog.md`
  (S-A07…S-A12: a co-fire row and a `full-composer` boundary control per pair) plus three
  catalog-independent assertions in `check-step0-emulator.py`, so deleting a row cannot make the
  assertion vacuous. Each pair was **measured before it was asserted** and all three already
  resolved as intended, so no phrase table was reordered and no version bump is involved.
  Proven by three injections against the live tree — a wrong expected value, a drifted catalog
  prompt, and a fishbone/five-whys row swap that flips S-A07 — because every new fixture passing
  on the first run is how a vacuous gate looks.
- **VERSION-01 gate — the stamp-lockstep rule above is now enforced.**
  `scripts/check-version-stamps.py` discovers every hand-maintained version stamp by glob and
  asserts they all carry the same value. Until now nothing checked this: `sync-content.py` copies
  `metadata.version` through per-file rather than propagating one source of truth, and the
  documented "version string invariant" checks a stamp's *format*, not its agreement with the
  others — so a single missed stamp shipped an inert update with every gate green, which is what
  happened at v8.14. Wired into `.github/workflows/validation.yml` and
  `scripts/check-firewall-battery.sh`; battery composition moves 16 → 17. The stamp count is
  reported, never asserted, so adding a skill does not require editing the gate.

### Removed

- **Three retired scripts**, none of which had a live consumer:
  `scripts/check-sub-skill-routing.py` and `scripts/check-focused-output.py` (deprecated thin
  shims — `check-routing-battery.py` had already replaced both, and its own header said so), and
  `scripts/check-inventory.py` (a requirement-ID auditor whose input corpus,
  `.planning/milestones/*-REQUIREMENTS.md`, is gitignored and superseded by
  `docs/requirements-traceability.md` under CANON-01; no requirement in the traceability surface
  referenced its AUDIT-01..04 IDs). `tests/test_81_inventory.py` went with the last of these,
  having loaded it by hard path.
- `scripts/check-body-budget.py` was **kept**, deliberately. TEARDOWN-01 retired the body-budget
  gate but preserved the reporter, and the firewall battery's untallied `[INFO]` line still
  consumes it. Only its documentation footprint was pruned.
- **Guards migrated, not dropped.** `tests/test_65_doc_invariants.py` had pinned the two shims
  across six tests — their self-tests, the boundary p-threshold default of 2, the catalog dry-run
  parse, and a `CLAUDE.md` mention. Each invariant moved onto `check-routing-battery.py` under its
  namespaced `--boundary-*` / `--focused-*` flags, plus a new guard asserting the three retired
  scripts do not reappear. Two of the old tests would have kept passing vacuously: one was
  satisfied by the sentence *recording* the retirement, and one pinned flag spelling rather than
  the threshold values it existed to protect.
- The `v3.8/EVAL-01` matrix row named `check-focused-output.py` as its `deliverable_path`. That
  field is reported but never existence-resolved (only `artifact_link` is), so a dangling path
  would have failed silently — it is repointed at the successor with the substitution recorded,
  and `docs/requirements-matrix.md` / `docs/data/matrix.json` regenerated. Row count unchanged
  at 214.

### Changed

- **`tests/` is classified, and nothing is deleted.** 550 tracked files sorted into three tiers —
  **102 gate-pinned** (opened at runtime by an offline gate, or `artifact_link`-resolved),
  **7 live-unwired**, **441 archive** — recorded in a new `tests/README.md` with the decision and
  its reasoning. The audit's two-way pinned/archival split was the wrong shape: it hid the middle
  tier. Re-running its trace reproduced the 441 aggregate but disagreed on the composition, and
  its pinned breakdown never summed to its own headline (56 + 24 + 16 + 6 + 4 = 106, under a
  headline of 110). Zero `step0-baseline-v*.md` files are opened by any gate; the audit's six came
  from counting `deliverable_path` entries, which are reported and never existence-checked.
- **`scripts/trace-tests-usage.py`** — new manual reporting tool that re-derives that
  classification by tracing `open` events under `sys.addaudithook` while each gate runs. The audit
  called its own trace reproducible while it existed only as prose; this makes the claim literal.
- **7 pytest suites carrying 123 assertions are run by no CI job** — CI runs pytest on exactly one
  path, `scripts/check-links_anchors_test.py`. Among them are the retirement guards migrated into
  `test_65_doc_invariants.py` one commit earlier. Named as a tier rather than silently reclassed;
  wiring them into CI is logged as follow-up.
- **The nine surviving milestone documents in `docs/` are adjudicated, and none deleted.** They
  had survived the 2026-08-16 prune as an undifferentiated block, with nothing distinguishing a
  rule still in force from a measurement true only of its date. Each now opens with a **Standing**
  banner giving its class and its live dependents; `docs/README.md` carries the summary table. The
  audit posed it as "governing record or historical narrative?" — that binary fits four of them.
  Five are neither: *frozen evidence*, cited for provenance by live artifacts while asserting
  nothing current. A third class covers `gen-01-rearch-milestone.md`, the only one of the nine a
  gate resolves (TRACE-03 fixture (9) deep-resolves its `artifact_link`; verified by removing the
  file and watching `--self-test` exit 1). "Gate-pinned" first had to be disentangled from an
  index artefact: removing *any* of the nine fails VAL-03 because `docs/README.md` links all
  nine, which measures the index rather than the document. The verdicts live in the documents rather than only in
  an index because the failure being closed — `v8.0-final-closure.md` calling a moved figure
  "final" — persisted exactly because its warning sat in `CLAUDE.md` instead.
- **`v8.14-delivery-verification.md` is the case against pruning by reference count.** Fewest
  inbound references of the nine, and least prunable on merit: it is the published form of a
  pre-registered STOP still governing Phases 189–191 and GREENMEAN-01's WON'T-DO scope.
- **`first-principles/README.md` rewritten.** The shipped plugin README still described v3.0.0 —
  a "plugin contents removed" banner, six companion tools, six worked examples, and no mention of
  the `skills/` directory. It now describes what the plugin actually ships (8 technique references
  with 4 detail siblings, 3 spine references, 14 worked examples, 14 slash-invocable skills), each
  count verified against the tree. Its outbound links stay absolute, and the file now says why, so
  the v8.17.1 defect is not reintroduced by a later tidy-up. **This is shipped content: it reaches
  installed users only on the next version bump.**
- Repo documentation consolidated onto one owner per topic, and a set of stale claims corrected
  along the way — including a mechanism that six documents had backwards (`{{TOOL:slug}}`
  substitutes a *name*, not a procedure, so the technique procedures are not inlined into the
  agent body). Full record in
  [`docs/audit-2026-08-16-duplication-staleness.md`](docs/audit-2026-08-16-duplication-staleness.md).
- **The Self-Audit Gate rename reached the user-facing docs.** 8.15.0 renamed the Validation
  Rubric to the Self-Audit Gate because two instruments shared one name, but the change stopped at
  the agent surface: `README.md` (×4), `docs/ARCHITECTURE.md` and `docs/METHODOLOGY-CHEATSHEET.md`
  kept the old name — the exact collision the rename existed to remove. The file is still
  `validation-rubric.md`. One occurrence remains in shipped content
  (`shared/skills/first-principles-analysis/SKILL.md`) and is logged as follow-up, since changing
  it requires a regen and a version bump.
- The coverage headline now has one authoritative home. Three surfaces asserted the superseded
  v8.0 figure (133/96/0/229) as current against the real 126/88/0/214;
  `docs/requirements-traceability.md` is the single source, and `docs/v8.0-final-closure.md` keeps
  its numbers unedited with a superseded-by note, since it is the record of what v8.0 measured.

## [8.17.1] - 2026-08-16

### Fixed

- **Links in shipped plugin content escaped the plugin root.** Four relative links pointed
  above `first-principles/` with `../` — one in the agent body
  (`agents/first-principles.md` → `../../docs/testing-agents-headlessly.md`) and three in
  `first-principles/README.md` (→ `../README.md`, `../CHANGELOG.md` ×2). Inside the repo they
  resolved, so no gate caught them: `check-links.py` validates the repo tree, where the
  targets exist. For anyone who installs the plugin standalone — the normal case, since
  `docs/` and the repo root are never delivered — all four were dead. Each is now an absolute
  URL into the GitHub repo, which resolves from either surface. The agent body carries no
  other outbound link, and no `../` link remains anywhere in `shared/` or `first-principles/`.

A patch release, not a minor: this fixes a defect and opens no milestone. It is the project's
first patch version — every prior release was milestone-numbered `X.Y.0`. All 17 version
stamps moved in lockstep per the note above, because without the bump the fix would never
reach an installed session.

Non-shipping change in the same window: `docs/` was pruned of 34 historical milestone
documents (61 tracked entries → 27, −898 KB). Removed files remain in git history; see the
**Retrieving removed documents** note at the top of `docs/README.md`.

## [8.17.0] - 2026-08-16

Fixes the defect recorded below: the `?`-count is now **enumerated by ID** rather than asserted
as an integer, and the Self-Audit Gate checks the enumeration against the Ground Truths list
instead of quoting it.

### Changed

- **Phase 3 exit criterion now requires an enumeration, not a count** (`shared/spine/SKILL-body.md`).
  Write `?-marked: GT-2, GT-5, GT-9, GT-14 (4 of 22)` — the list, not the number. **A stated
  integer no longer satisfies the criterion**, on the grounds that an integer cannot be checked
  against the list it summarizes and an enumeration can, by inspection. Where a count accompanies
  an enumeration and the two disagree, **the enumeration governs.**
- **Output template's provenance summary** updated to the same form, with a worked example
  (`shared/spine/references/output-template.md` §3).
- **Self-Audit Gate Criterion 3 now verifies rather than quotes** (`shared/spine/references/validation-rubric.md`).
  Explicit instruction added: *"Check the enumeration, do not quote it."* Quoting the analysis's
  own provenance summary as the satisfying span does not discharge the criterion — that verifies a
  summary was written, not that it is correct. The gate must read the Ground Truths list, collect
  the IDs actually carrying `?`, compare, and cite the comparison.
- **Band ladder retightened for this criterion.** A bare count with otherwise-correct suffixes now
  bands **Sound** rather than Rigorous. **An enumeration that disagrees with the list bands
  Hand-wavy** — a mismatch understates unverified inputs in the direction that flatters the
  analysis, and unlike a bare count it was checkable, so it is a stronger failure than never
  enumerating at all.

### Known defect (fixed above; retained for the record)

The defect this release fixes, as originally recorded:

#### The `?`-count exit criterion was satisfied in form and failed in substance

v8.16.0's Phase 3 exit criterion requires the count of `?`-marked ground truths to be stated
explicitly. **Across every draft observed in post-release testing, a count was stated and none
was correct.** Three runs against the same prompt — two turn budgets, both agent versions:

| Draft | Stated | Actual |
|---|---|---|
| full-composer, `maxTurns: 60`, base | 24 of 41 | **31 of 41** |
| same run, consolidated after revision | 17 of 45 *(while enumerating 20 IDs)* | **21 of 57** |
| full-composer, `maxTurns: 30` | 17 of 22 *("the unsuffixed five")* | **15 of 22** *(seven unsuffixed)* |

The consolidated draft is the sharpest case: it reports the same quantity **three different ways
inside one document** — a header figure, an enumeration of a different length, and an actual
suffix count that matches neither.

**Self-Audit Gate Criterion 3 passes all three.** It quotes the stated count as its satisfying
span rather than recomputing it, so the gate verifies *that a count was stated*, not *that it is
correct*. In the `maxTurns: 30` draft the Gate quotes `"Count of ?-marked ground truths: 17 of
22"` verbatim and bands the criterion **Sound**.

**Why this one is worth fixing before the others.** Every other Gate criterion is a judgement
call — whether an essence statement is specific enough, whether a chain has a genuine
intermediate. This one is arithmetic over a document the agent has already written, and it is
the criterion the provenance discipline leans on hardest: the count is the summary statistic a
reader uses to calibrate the whole analysis. A wrong count understates unverified inputs by up
to seven ground truths, in the direction that flatters the analysis.

**Fix, implemented in this release:** derive the count rather than assert it — the `?`-marked IDs
are enumerated, and the Gate checks the enumeration against the Ground Truths list rather than
quoting the stated number. An enumeration is checkable by inspection; a bare integer is not.

*Not a regression: the criterion was new in 8.16.0 and never reported a correct figure in the
one release it shipped in.*

## [8.16.0] - 2026-08-16

Source-provenance discipline for ground truths. Both changes come from the same observed
failure: a fabricated figure carried a well-formed citation to a real paper that did not
contain it, propagated into a HIGH-confidence derivation chain, and reached the conclusion.
A citation being *present* passed every check the agent had.

### Added

- **Source-provenance labels on every ground truth** (Phase 3, `shared/spine/SKILL-body.md`).
  One test decides the label: *did this analysis read the asserted figure or wording in the
  cited source?* Three values — `read-at-source` (no suffix), `reported-by-delegate` (`?`
  required), `unverified` (`?` required). Provenance is scored on what the analysis did, never
  on who supplied the claim: a well-formed citation from a capable sub-agent is
  `reported-by-delegate` until someone opens the source.
- **Delegate-reported ground-truth form** in `shared/spine/references/output-template.md` §3,
  alongside the existing verified and unverified forms, plus a required provenance summary.
- **Provenance check** prepended to Criterion 3 of the Self-Audit Gate, applied before banding.

### Changed

- **The `?` suffix is now the default rather than the exception.** It is dropped only when a
  read-at-source location can be named. A delegate report counts as read-at-source only when it
  quotes the source's own wording and that quote was checked.
- **Phase 3 exit criterion** now requires the count of `?`-marked ground truths to be stated
  *and* every unsuffixed ground truth feeding a HIGH-confidence chain to name where its figure
  was read. A bare count of zero no longer satisfies the criterion — the named read-locations
  are the auditable part.
- **Self-Audit Gate Criterion 3 band ladder retightened.** An unsuffixed, unread ground truth
  feeding a HIGH-confidence chain now bands at **Hand-wavy**; it previously banded at **Sound**,
  which is precisely the defect above passing at a tolerated level. The MEDIUM/LOW-confidence
  case stays at Sound, so the ladder still discriminates.

### Note

The binary `GT-N` / `GT-N?` notation is deliberately unchanged. Provenance layers on top of it
rather than introducing a third symbol, so D-07, the exact-tie tiebreak, the MEDIUM/LOW
confidence rule, and all four Criterion 3 bands keep working without re-verification.

## [8.15.0] - 2026-08-16

Findings from the first real-world audit of the shipped agent — a full-composer run against a
Medium article, reconstructed from the raw subagent transcript rather than from the written
output.

### Added

- **"Turn discipline" section** in the agent body, placed before Step 0. Prescriptive rather
  than prohibitive on purpose: the observed run reached for `Monitor` first and fell back to
  `sleep` loops anyway, so the text names the alternative — dispatched work notifies on
  completion, so stop and wait for the notification rather than polling.
- **Carry-forward rule for regenerated analyses.** The observed run emitted three complete
  full-length analyses and each rewrite silently lost artifacts: the Essence Statement was
  present in drafts 1 and 2 and absent from the deliverable, and `GT-N?` marks decayed 13 → 2 →
  0 while a fabricated figure's usage rose 0 → 6 → 8. A rewrite is now a revision — confirm
  every named artifact survives or is explicitly retired.
- **Honest-failure clause.** If the closure ledger or the gate could not run, say so at the top
  of the response, naming which. A stated omission is recoverable; a silent one is not.

### Changed

- **`maxTurns` raised 30 → 60.** The observed run used 32 assistant turns against a cap of 30,
  with roughly 9 spent on tool-schema fetches and seven consecutive busy-wait loops polling for
  dispatched sub-agents. The Fix/Repeat loop runs last and is therefore what gets dropped when
  the budget runs out — and it was.
- **The Validation Rubric is renamed the Self-Audit Gate.** The request asked for "a validation
  rubric scoring the article's argument"; the agent produced one and let it stand in for its own
  gate, which never ran. Two different instruments shared a name. The disambiguation lives in
  `SKILL-body.md`, not only in the reference file, because the whole failure was that the linked
  file never got opened: the gate scores *this analysis's* structure, a subject-matter rubric is
  a separate deliverable, and both must appear.
- `docs/CONFIGURATION.md` and `docs/FIVE-PHASE-FLOW.md` updated in the same commit so no tracked
  prose asserts the old value or the old name. `docs/CONFIGURATION.md` also carried a
  pre-existing stale `metadata.version` of `"8.0.0"`.

### Note

The file path `references/validation-rubric.md` is deliberately unchanged despite the rename —
`check-quality-harness.py` copies it *by name* into the QUAL-01 frozen packet and asserts on the
entry list, `check-traceability.py` pins it as a `deliverable_path`, and `sync-content.py` keys
its INLINE list on the slug. The frozen quality baseline records the rubric by path only, so
retitling does not affect pre/post comparability.

## Earlier releases (1.0 – 8.14)

This changelog was not maintained between 3.8.0 and 8.15.0. The entries below are
**reconstructed from the annotated git tags** and carry only each release's headline — no
Added/Changed/Fixed decomposition, because that detail was never recorded here and inventing it
would misrepresent the record. **For any release below, the annotated tag body is the
authoritative account** (`git show <tag>`). Releases **3.0.0 through 3.8.0 are omitted from this
table** — they already carry full hand-written entries further down.

Note also that the repository history was rewritten on 2026-07-28 (removal of `docs/history/`
and 237 raw test captures), so commit SHAs referenced in material predating that date are stale;
tag names remain valid.

| Tag | Date | Headline |
|---|---|---|
| `v8.14-greenmean` | 2026-07-29 | v8.14 GREENMEAN-01 — the milestone that stopped itself |
| `v8.14` | 2026-07-29 | Builder Retirement & Traceability Reconciliation |
| `v8.13` | 2026-07-28 | DETECTFIX-01 — Correct the Inverted D-18 Defect Checks |
| `v8.12` | 2026-07-26 | REALREAD-01 — First Read of Real Work Output |
| `v8.11` | 2026-07-24 | DEFROBUST-01 — D-03 Definition-Robustness Test |
| `v8.10` | 2026-07-24 | CORRECTGATE-01 — A Correctness Instrument for the DIVERGE Class |
| `v8.9` | 2026-07-24 | DIAGNOSE-01 — Diagnose the Failed §6→§4 Contract Fix |
| `v8.8` | 2026-07-23 | Technical-Debt Clean-Up & Framing Correction |
| `v8.7` | 2026-07-23 | Analysis Correctness, Constraint Teardown & Output-Contract Integrity |
| `v8.6` | 2026-07-21 | Agent-Body Procedure Compression |
| `v8.5` | 2026-07-20 | Context Optimization: Execute the Reference-File Split |
| `v8.4` | 2026-07-19 | Implementation-Readiness Evaluation |
| `v8.3` | 2026-07-18 | Technique & Context-Length Optimization Evaluation |
| `v8.2` | 2026-07-18 | Deep Investigation of the 19 Not-Approved Grok Items |
| `v8.1` | 2026-07-16 | Grok Recommendations Review & Selective Implementation |
| `v8.0` | 2026-07-06 | Final Release (project wrapped) |
| `v7.13` | 2026-07-02 | Live Re-Measure — RR-130-01 Fix + Step 0 Residuals |
| `v7.12` | 2026-06-30 | Diagnose & Fix RR-130-01 (Main-Routing Inline-Answering Regression) |
| `v7.11` | 2026-06-30 | Live Re-Measure of the Whole System |
| `v7.10` | 2026-06-28 | Evaluate Gaps & Technical Debt Misaligning Agent Goals |
| `v7.9` | 2026-06-27 | Close the 5-Fix Over-Routing Fishbone (Fix #3 / Fix #4 / Fix #5) |
| `v7.8` | 2026-06-25 | Step 0 Over-Routing Precision — Negative-Match Guard & Stay-in-Composer Default |
| `v7.7` | 2026-06-24 | Fix the S-P01/S-P03 Step 0 Under-Routing Regressions |
| `v7.6` | 2026-06-23 | Validate the Merge — Live 8-Technique Step 0 Re-Baseline |
| `v7.5` | 2026-06-21 | Execute the decompose→five-whys Merge |
| `v7.4` | 2026-06-20 | Measure the Expansion — Live 9-Technique Step 0 Re-Baseline |
| `v7.3` | 2026-06-20 | Introduce Tier-1 Rigor — the theoretical-limit Skill |
| `v7.2` | 2026-06-19 | Introduce Tier-1 Rigor — the estimate Skill |
| `v7.1` | 2026-06-19 | Introduce Tier-1 Rigor — the decompose Skill |
| `v7.0` | 2026-06-18 | Documentation Refresh & System-Connection Docs |
| `v6.4` | 2026-06-17 | Resolve v6.3 Carry-Forward Residuals (RR-92-01 / RR-92-02) |
| `v6.3` | 2026-06-16 | GEN-01 Step 0 Classifier Rearchitecture |
| `v6.2` | 2026-06-15 | Close the Last Two Documented Gaps |
| `v6.1` | 2026-06-15 | Close Actionable Traceability Gaps |
| `v6.0` | 2026-06-14 | Requirements & Traceability Alignment |
| `v5.3` | 2026-06-14 | Live S-P Routing — Close Remaining Detector Residuals |
| `v5.2` | 2026-06-13 | Live S-P Routing Fix |
| `v5.1` | 2026-06-12 | Step 0 Live Detector Closure |
| `v5.0` | 2026-06-12 | Step 0 Measurement Harness |
| `v4.3` | 2026-06-11 | Unified Routing/Output Battery |
| `v4.2` | 2026-06-10 | Sub-Skill Battery Fixture Correction |
| `v4.1` | 2026-06-06 | Builder Auto-Install Flag |
| `v4.0` | 2026-06-04 | Programmatic Skill/Agent Builder |
| `v3.13` | 2026-06-03 | Routing Catalog v3.2 Content Coverage |
| `v3.12` | 2026-05-30 | Phase-Level Slash Commands |
| `v3.11` | 2026-05-29 | P8 Routing Forward Monitoring |
| `v3.10` | 2026-05-29 | Phase 46 Convention Closure |
| `v3.9` | 2026-05-29 | P8 Routing Fix + Phase 45 Convention Restoration |
| `v2.0` | 2026-05-22 | Collection-of-Skills Plugin |
| `v2.0.0` | 2026-05-21 | Collection-of-Skills Plugin (dual-publish) |
| `v1.2` | 2026-05-20 | Forward Consequence-Tracing Tools (Inversion + Second-Order Thinking) |
| `v1.1` | 2026-05-19 | Ishikawa (Fishbone) Diagram Tool |
| `v1.0` | 2026-05-18 | Enhanced Skill |

---

The 3.0.0 – 3.8.0 entries below are the original hand-written records, kept verbatim.

## [3.8.0] - 2026-05-28

### Added

- `scripts/check-focused-output.py` — verifies that agent analysis outputs stay focused on first-principles methodology (not off-topic delegation); includes `--self-test` fixture battery and a LOAD-BEARING Probe 3 sanity feed.
- `scripts/check-sub-skill-routing.py` — verifies that companion-tool invocations (`/first-principles:fishbone` etc.) are correctly routed to the named sub-skill rather than delegated to the main agent.
- Sub-skill routing catalog at `tests/sub-skill-routing-catalog.md` (P12, P24, N1, N2 prompts).
- Sub-skill routing baseline at `tests/sub-skill-routing-baseline-v3.8.md`.
- Focused-output baseline at `tests/focused-output-baseline-v3.8.md`.
- Six namespaced companion-tool skills under `first-principles/skills/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}/` — standalone slash-only skills (`/first-principles:<name>`) for direct invocation of individual techniques without triggering the full agent. Each has `disable-model-invocation: true`.
- `generate_skill_stub` in `scripts/sync-content.py` with six corresponding `shared/skills/` sources; skill stubs are now generated alongside the agent surface.
- `GENERATED` marker prepended to every byte-identical emission in the generated agent tree so code reviewers can skip the `shared/`↔`first-principles/` mirror.
- `.reviewignore` at repo root declaring the generated mirror as review-skippable.

### Fixed

- Signal A routing-envelope override now takes priority over composer-structure cardinality classifier, fixing false sub-skill delegation on routing prompts that carry both signals.
- `_extract_assistant_text` tightened to top-level assistant entries only, preventing nested tool-result text from inflating detection scores.
- Sibling-shared boilerplate in six technique-skill descriptions reworded to eliminate ~60 false-positive 4-gram collisions that blocked `check-trigger-collisions.py` on CI push.
- `sync-content.py` docstrings on three verbatim-copy generators corrected — they previously claimed "NO marker expansion, NO edits" after the GENERATED marker prepend was added.
- Agent marker's primary canonical source now named as a navigable path (`shared/spine/SKILL-body.md`) instead of freeform prose.

## [3.7.0] - 2026-05-27

### Added

- Mandatory Assumption Audit protocol in the validation rubric (`shared/spine/references/validation-rubric.md`): exhaustive enumeration of assumptions by scanning each derivation-chain step, replacing the prior opportunistic-listing approach.
- `[Assumes: X]` annotations on derivation-chain steps in `science-engineering-2.md` worked example.
- Assumption Audit section in `software-systems.md` worked example.
- Routing baseline v3.7 at `tests/routing-baseline-v3.7.md` — BATTERY PASS: P 10/10, N 17/17.

### Changed

- Validation rubric Criteria 1, 2, and 4 Rigorous descriptors rewritten with structural/observable tests instead of subjective phrases ("withstand inspection by a skeptic").
- Validation rubric Criteria 5 and 6 Rigorous descriptors: modal verbs removed; compliance is now detectable from output structure alone.

## [3.6.0] - 2026-05-26

### Added

- Two new routing catalog prompts: P9 (chemistry/first-principles of reaction kinetics) and P10 (earth science/continental drift).
- Two new N-case catalog rows: N16 and N17 (science-lookup questions that should NOT delegate).
- Routing mini-catalog v3.6 fixture at `tests/routing-mini-catalog-v3.6.md` (P9, P10, N16, N17).
- Routing baseline v3.6 at `tests/routing-baseline-v3.6.md` — BATTERY PASS: P 8/10, N 17/17.

### Changed

- Battery thresholds rescaled to P ≥ 8/10 and N ≥ 15/17 to match the expanded 10P/17N catalog.

## [3.5.0] - 2026-05-25

### Added

- P3+P7 mini-battery catalog fixture at `tests/routing-mini-catalog-p3p7.md` for fast-iteration confirmation before running the full battery.
- P7-targeted paraphrases added to agent description: question-form (`"Is our reasoning sound..."`), back-reference (`"evaluate whether a claim..."`), and evaluate-whether variants.
- Routing baseline v3.5 at `tests/routing-baseline-v3.5.md` — BATTERY PASS: P 6/8, N 15/15.

### Fixed

- P3 routing fragility: prompt mid-sentence rewritten to eliminate structural embedding that suppressed delegation.
- P7 routing fragility: vocabulary gap closed — agent description now covers the "evaluate whether" and question-form trigger shapes that P7 exercises.

## [3.4.0] - 2026-05-25

### Added

- `--repeat` and `--min-pass` flags on `check-routing.py` enabling K-of-N aggregation: run each prompt N times, require K passes — reduces false FAIL/PASS verdicts from single-run non-determinism.
- K>N guard and K-of-N self-test fixtures in the battery runner.
- Rerun-to-stability methodology documented in `docs/testing-agents-headlessly.md` (Section 10).
- Routing baseline v3.4 at `tests/routing-baseline-v3.4.md` — canonical best-of-3: P 6/8, N 15/15.

## [3.3.0] - 2026-05-25

### Added

- `scripts/check-body-budget.py` — checks generated agent body against the ~500-line target; includes `--self-test`.
- `scripts/git-hooks/pre-commit` — combined body-budget + sync-drift gate; blocks commits that would push the agent body over budget or leave `shared/` and the generated agent tree out of sync.
- `scripts/install-hooks.sh` — idempotent installer that symlinks the above hook into `.git/hooks/pre-commit` (preserves any existing hook as `.bak` on first run).
- `scripts/smoke-test-hook.sh` — end-to-end smoke test for the pre-commit hook.
- `.githooks/pre-commit` extended with body-budget gate (for contributors using the `core.hooksPath` opt-in path).
- Contributor setup documentation in README.md for both hook opt-in paths.

## [3.2.0] - 2026-05-24

### Added

- `shared/spine/references/assumption-taxonomy.md` — canonical classification guide for the five assumption types used in Phase 2 (physical law, engineering constraint, current constraint, convention, untested belief); emitted to `first-principles/agents/references/assumption-taxonomy.md`.
- Phase 2 cross-reference from assumption-taxonomy to the agent body.
- Self-application worked example (`shared/examples/self-application.md`) — first-principles analysis applied to a live design decision about the agent itself (body length vs. scope).
- Four second-pass worked examples covering distinct reasoning shapes not present in the original six:
  - `software-systems-2.md` — Build vs. Buy (authentication service); capability-cost-risk trade-off shape.
  - `product-business-2.md` — Feature prioritization under a binding engineering-capacity constraint.
  - `personal-general-2.md` — Mortgage paydown vs. index investment; quantitative expected-value chain.
  - `science-engineering-2.md` — In-service mechanical component failure analysis; diagnostic/backward-reasoning shape.
- Worked Examples navigation subsection added to the agent spine.
- All five new examples synced to the generated agent surface.

### Changed

- Spine appendices (assumption taxonomy, output template, validation rubric) extracted out of the inlined agent body into on-demand reference files, reducing recurring token cost per invocation.

## [3.1.0] - 2026-05-23

### Added

- `scripts/check-routing.py` — headless routing battery: issues each catalog prompt through `claude -p --output-format stream-json`, scores DELEGATE / NO-DELEGATE from the event stream, and exits non-zero if P-case or N-case thresholds are not met.
- `tests/routing-catalog.md` — initial routing test catalog: 8 P-cases (should delegate) and 15 N-cases (should NOT delegate), with per-prompt annotations and pass thresholds.
- `docs/testing-agents-headlessly.md` — documents the stream-json methodology, two-signal detection rule, jq extraction strategies, and `--permission-mode bypassPermissions` requirement for reproducible headless agent testing.
- Routing baseline v3.1 recorded in `tests/routing-catalog.md`.

### Fixed

- Agent description scope-line tightened to explicitly exclude performance optimization, debugging, and general Q&A — closes a class of false-positive delegations where the agent was invoked for routine coding tasks.

## [3.0.0] - 2026-05-23

### Removed

- Standalone monolith skill at `first-principles-thinking/`. Users who copied this to `~/.claude/skills/` should remove that local copy manually:
  `rm -rf ~/.claude/skills/first-principles-thinking`
- 7 namespaced plugin skills at `first-principles/skills/{thinking,five-whys,pre-mortem,trade-off,fishbone,inversion,second-order}/`. The Phase 26 forwarding language ("still installable") is superseded — these surfaces no longer exist.

### Added

- First-principles agent surface at `first-principles/agents/first-principles.md` (initially shipped Phase 23 in the v3.0-alpha series; now the sole installable interface).
- 6 on-demand companion-tool reference siblings under `first-principles/agents/references/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}.md`.
- 6 worked-example siblings under `first-principles/agents/references/examples/` (migrated from the deleted monolith examples directory).

### Upgrade path

- Install: `claude --plugin-dir ./first-principles` for dev, or via the marketplace (`/plugin marketplace add chrisdavidson/first-principles-skill` then `/plugin install first-principles@first-principles-skill`).
- Invoke: `@agent-first-principles:first-principles` (auto-routing) or `/first-principles:first-principles` (explicit).
- If you previously copied `first-principles-thinking/` into `~/.claude/skills/`, delete that local copy manually — Claude Code does not auto-remove it.

### Reference

- Per-technique deep procedures now ship as agent-loaded reference files (`first-principles/agents/references/`).
- The 5-phase methodology text formerly carried by the monolith body is inlined in the agent body itself.
