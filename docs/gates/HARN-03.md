# HARN-03: Focused-mode parity: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet.

<!-- GENERATED:FACTS -->
## Facts

- `locked_constants` (3 entries): `expected_stub_count`, `launcher_slug`, `non_technique_slugs`
- `registered_surfaces` (3): `cross-surface  # derived agreement between the two above`, `first-principles/agents/first-principles.md  # agent surface`, `first-principles/skills  # stub surface`
- `disclosed_bounds_anchors` (1): `_WS`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-focused-parity.py --self-test
```

CI job: `check-focused-parity`
<!-- END GENERATED:HOW-TO-RUN -->

## REACH-or-LEVEL determination (v9.2.0, GUARD-02, GUARD-03)

`_check_stub_surface` is an existing HARN-03 check that already walks every emitted focused stub
and already anchors the closing handoff's placement through `_CLOSING_HANDOFF_ANCHOR`. This
determination is written in the CONF-SURFACE precedent's voice — the argument for the
classification, not a restatement of the label. **v9.2.1 (HAND-04, D-29-P2) narrowed and extended
clause (a) below in place; it is not a second determination.**

**(a) What moved.** `_check_stub_surface` carries more literal assertions on the closing-handoff
text than it once did: a presence assertion (`_HANDOFF_CANDIDATE_TAIL`) narrowed at
HAND-01..04/D-29-P2 from every non-launcher stub to only the unclassified-facts stubs — the roster
`_HANDOFF_ROUTED_SLUGS` names the stubs this assertion now excludes because their own routing
clause targets a phase other than Phase 2; a further presence assertion added at the same
narrowing (`_HANDOFF_NO_SOURCE_CLAUSE`, exactly once, asserted across every non-launcher stub
including the ones the candidate-tail assertion now excludes, since every focused run carries this
provenance clause regardless of where its output routes); and an absence assertion
(`_HANDOFF_EXEMPT_SLOT`, in no stub, launcher included), unchanged since v9.2.0. Each has its own
control in the gate's self-test (the narrowed `_HANDOFF_CANDIDATE_TAIL` loop: g8, targeting a
derived unclassified-facts slug; `_HANDOFF_NO_SOURCE_CLAUSE`: g6, repointed from
`_HANDOFF_CANDIDATE_TAIL` onto the new literal and deliberately kept on its existing
`identify-essence` target, since g6's bare id-existence is cited GUARD-02 evidence;
`_HANDOFF_EXEMPT_SLOT`: g7, unchanged). Every constant here and the roster
clear the D-12 anchor-control ratchet by ordinary reference — see this page's own generated
`disclosed_bounds_anchors` field above rather than a restated value here; none joined it. This
page's Facts region does not move, because HARN-03 publishes no control count.

**(b) Why that is REACH under `docs/PROCESS.md` § "REACH is not LEVEL".** The subject of these
assertions is product text a model reads at the end of every focused run — where its output goes
next and what that output is — never another guard's correctness. No check, CI job or battery
registration was added; an existing check's own reach widened over the same class of prose it
already polices.

**(c) The action a future contributor loses.** Letting one of the unclassified-facts stubs'
hand-copied candidate tail drift from the others, dropping any non-launcher stub's no-cited-source
clause, or routing any stub's output back into the Input Contract's `Known ground truths` slot
fails HARN-03 by name. The tail is hand-copied across every stub rather than generated from a
token — a token would reach into `scripts/sync-content.py` and DUAL-04, outside this milestone's
scope — so the per-stub exactly-once presence assertion is itself the drift guard. **What this
does not yet cover, since v9.2.1:** the routed stubs' own routing clauses carry no per-stub drift
guard of their own — see (d).

**(d) What it does not reach, stated as bounds.** Every literal here is exact wording, so a
reworded tail, a reworded provenance clause, or a reworded routing line escapes them; the check
reads the generated stubs, whose agreement with `shared/` is DUAL-04's job, not this
determination's; and presence is checkable while obedience is not — no gate here verifies that a
run actually hands its output over as described. **New bound, v9.2.1 (HAND-01..04, D-29-P2):** the
routed stubs' own routing clauses — `identify-essence`'s Input Contract framing,
`reason-upward`'s Phase 5 chains, `validate`'s Phase 5 verdict — carry no presence-literal
assertion of their own; HARN-03 asserts only that each still carries the shared no-cited-source
clause, never that its own routing text is present, unchanged, or correctly worded. Phase 30's
GUARD-04 four-class partition is this bound's named owner.

**(e) This section itself.** Writing it adds no check, no CI job, no battery gate and no
`--self-test` control asserting that a determination exists on this page, so it is not the
meta-guard regress `docs/PROCESS.md` § "The depth rule" caps. Promoting this page into
`NARRATIVE_ENTRIES` so the section survives regeneration is a single-member change to the
generator's own configuration, not a guard.

**(f) Pointer.** The `_HANDOFF_CANDIDATE_TAIL` / `_HANDOFF_EXEMPT_SLOT` / `_HANDOFF_NO_SOURCE_CLAUSE`
/ `_HANDOFF_ROUTED_SLUGS` comment blocks in `scripts/check-focused-parity.py` point at this section
by name and restate none of it.

## Non-technique exemption (PSKILL-03)

**What qualifies.** An emitted skill qualifies for `NON_TECHNIQUE_SLUGS` only if its body carries
neither `## When to reach for this` (the inlined-procedure anchor) nor `## Focused-mode validation`
(`_STUB_SECTION_HEADING`) — the two headings every technique stub carries and a non-technique skill
does not. The launcher is the set's only member today.

**Why it exists.** A persona companion skill (D-06, PSKILL-03) reads an already-finished analysis
and renders one of its views; it runs no inlined procedure and emits no focused-mode validation
section, so without an exemption HARN-03's stub-surface checks (Stub-1..13) would treat it as a
broken technique stub rather than recognising it as a different kind of skill entirely.

**How Stub-14 polices it.** Stub-14 runs over every slug named in the exemption set and fails if
either of two things is true: the slug has no emitted stub at all (an exemption cannot be vacuous),
or the slug's emitted body carries one of the two technique markers above (an exemption cannot
silence a real technique). The self-test drives both branches directly — a must-fail control per
technique slug widens the set by exactly that slug and asserts Stub-14 fires naming it, and a
further control widens it with a nonexistent slug and asserts Stub-14 fires for the absent-stub
reason — plus a positive control proving the default set (the launcher alone) produces zero Stub-14
failures.

**Mutate-run-restore observation (plan 85-01, SC2 falsifier).** A throwaway copy of
`scripts/check-focused-parity.py` with `NON_TECHNIQUE_SLUGS` widened to also name the `validate`
technique was run live and then deleted:

```sh
python3 scripts/_tmp_harn03_mut.py
```

The run exited non-zero and its output named both `Stub-14` and `validate` — the exemption-widening
mutation was rejected for its own stated reason, not merely for a sibling check's.
