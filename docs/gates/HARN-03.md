# HARN-03: Focused-mode parity: stub surface, agent surface and cross-surface parity-token set equality, with the D-12 anchor-control ratchet.

<!-- GENERATED:FACTS -->
## Facts

- `locked_constants` (2 entries): `expected_stub_count`=13, `launcher_slug`='first-principles-analysis'
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
classification, not a restatement of the label.

**(a) What moved.** `_check_stub_surface` gained a presence assertion (`_HANDOFF_CANDIDATE_TAIL`,
exactly once in every non-launcher stub) and an absence assertion (`_HANDOFF_EXEMPT_SLOT`, in no
stub, launcher included), under a new check id in the same function, each with a control in the
gate's existing self-test. Both constants clear the D-12 anchor-control ratchet by ordinary
reference — see this page's own generated `disclosed_bounds_anchors` field above rather than a
restated value here; neither joined it. This page's Facts region does not move, because HARN-03
publishes no control count.

**(b) Why that is REACH under `docs/PROCESS.md` § "REACH is not LEVEL".** The subject of both new
assertions is product text a model reads at the end of every focused run — where its output goes
next and what that output is — never another guard's correctness. No check, CI job or battery
registration was added; an existing check's own reach widened over the same class of prose it
already polices.

**(c) The action a future contributor loses.** Letting a stub's hand-copied tail drift from the
others, dropping its no-cited-source clause, or routing its output back into the Input Contract's
`Known ground truths` slot now fails HARN-03 by name. The tail is hand-copied across every stub
rather than generated from a token — a token would reach into `scripts/sync-content.py` and
DUAL-04, outside this milestone's scope — so the per-stub exactly-once presence assertion is
itself the drift guard.

**(d) What it does not reach, stated as bounds.** Both literals are exact wording, so a reworded
tail or a reworded routing line escapes them; the check reads the generated stubs, whose agreement
with `shared/` is DUAL-04's job, not this determination's; and presence is checkable while
obedience is not — no gate here verifies that a run actually hands its output over as described.

**(e) This section itself.** Writing it adds no check, no CI job, no battery gate and no
`--self-test` control asserting that a determination exists on this page, so it is not the
meta-guard regress `docs/PROCESS.md` § "The depth rule" caps. Promoting this page into
`NARRATIVE_ENTRIES` so the section survives regeneration is a single-member change to the
generator's own configuration, not a guard.

**(f) Pointer.** The `_HANDOFF_CANDIDATE_TAIL` / `_HANDOFF_EXEMPT_SLOT` comment block in
`scripts/check-focused-parity.py` points at this section by name and restates none of it.
