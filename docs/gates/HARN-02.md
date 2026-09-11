# HARN-02: Observe->Perceive re-entry edges: a Criterion 1 Absent verdict routes back to Phase 1, every re-entry edge is bounded to one re-perception pass, and a fired edge is recorded.

<!-- GENERATED:FACTS -->
## Facts

- `checked_files` (4): `shared/agent/input-contract.md`, `shared/spine/SKILL-body.md`, `shared/spine/SKILL.meta.yml`, `shared/spine/references/validation-rubric.md`
- `control_ids` (39): `N1`, `N10`, `N11`, `N12`, `N13`, `N14`, `N15`, `N16`, `N17`, `N18`, `N19`, `N2`, `N20`, `N21`, `N22`, `N23`, `N24`, `N25`, `N26`, `N27`, `N28`, `N29`, `N3`, `N30`, `N31`, `N32`, `N33`, `N34`, `N35`, `N36`, `N37`, `N38`, `N39`, `N4`, `N5`, `N6`, `N7`, `N8`, `N9`
- `control_count`: `39`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-loop-closure.py --self-test
```

CI job: `check-loop-closure`
<!-- END GENERATED:HOW-TO-RUN -->

## REACH-or-LEVEL determination (v9.2.0, GUARD-01, GUARD-03)

`_check_input_contract_text` is an existing HARN-02 check that already reads
`shared/agent/input-contract.md` and already asserts presence literals on that file's prose. This
determination is written in the CONF-SURFACE precedent's voice — the argument for the classification,
not a restatement of the label.

**(a) What moved.** `_check_input_contract_text` gained a presence assertion (`_CANDIDATE_ENTRY`) and
an absence assertion (`_SUPERSEDED_EXEMPTION`) on the same file's Input Contract bullet, each with a
negative control in the gate's existing self-test. No file was added to what this check reads — see
this page's own generated `checked_files` field above rather than a restated value here.

**(b) Why that is REACH under `docs/PROCESS.md` § "REACH is not LEVEL".** The subject of both new
assertions is product text a model reads — the bullet that decides how a supplied fact enters the
analysis — never another guard's correctness. No check, CI job or battery registration was added; an
existing check's own reach widened over the same file it already governs.

**(c) The action a future contributor loses.** Rewriting the bullet so a supplied fact no longer
enters Phase 2 as a candidate now fails HARN-02 by name, and so does re-adding the superseded
exemption clause beside the new wording. The absence half exists because the defect this bullet
carried survived as coexistence — the exemption clause outlived later edits that each wrote the
correct rule somewhere else without removing it — and a presence literal alone cannot see
coexistence: it stays green whether the old clause sits beside the new wording or not.

**(d) What it does not reach, stated as bounds.** The absence pin matches the exact superseded
wording only; a reworded exemption carrying the same meaning would pass it. The gate reads the
`shared/` source and never the emitted agent body — whether they agree is DUAL-04's job, not this
determination's. And presence is checkable while obedience is not: no gate here verifies that a run
actually follows the bullet it reads.

**(e) This section itself.** Writing it adds no check, no CI job, no battery gate and no
`--self-test` control asserting that a determination exists on this page, so it is not the
meta-guard regress `docs/PROCESS.md` § "The depth rule" caps. Promoting this page into
`NARRATIVE_ENTRIES` so the section survives regeneration is a single-member change to the
generator's own configuration, not a guard.

**(f) Pointer.** The `_CANDIDATE_ENTRY` / `_SUPERSEDED_EXEMPTION` comment block in
`scripts/check-loop-closure.py` points at this section by name and restates none of it.
