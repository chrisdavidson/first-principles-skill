# Step 0 Fixture Catalog

## Purpose

This is the fixture catalog for the offline Step 0 emulator
(`scripts/check-step0-emulator.py`). Each row specifies a prompt,
the expected `MODE` that the phrase-detection classifier should
produce for that prompt, and traceability notes.

The emulator loads this catalog at `--self-test` time and asserts
that every row's `Expected MODE` matches the classifier output.

**ID scheme:** `S-P` prefix = positive fixture (fires a focused technique);
`S-N` prefix = negative fixture (expected `full-composer`). The `S-`
prefix avoids collision with the merged routing battery's `B-` and
`F-` row IDs in `tests/routing-battery-catalog.md`.

## Run Command

```bash
python3 scripts/check-step0-emulator.py --self-test
```

## Anti-Regression Warning

> Do not re-expect the four canonical negative rows as focused-technique —
> they are canonical oblique prompts (P12/P24/N1/N2) whose
> `full-composer` expectation is confirmed by live Python execution
> after D-02 normalization. Do not add slash-invocation prompts as
> positives — D-08 requires natural-language trigger phrases only.

---

## Catalog

| ID | Prompt | Expected MODE | Notes |
|---|--------|--------------|-------|
| S-P01 | run a pre-mortem on this launch | focused-pre-mortem | Fires `pre-mortem` trigger phrase. Technique: pre-mortem. |
| S-P02 | invert this claim: faster ships means better retention | focused-inversion | Fires `invert this claim` trigger phrase. Technique: inversion. |
| S-P03 | draw a fishbone diagram on the production incident | focused-fishbone | Fires `fishbone` trigger phrase. Technique: fishbone. |
| S-P04 | do a five whys on this outage | focused-five-whys | Fires `five whys` trigger phrase. Technique: five-whys. |
| S-P05 | build a trade-off analysis for these database options | focused-trade-off | Fires `trade-off` trigger phrase. Technique: trade-off. |
| S-P06 | what are the second-order effects of shipping this feature this week? | focused-second-order | Fires `second-order` trigger phrase. Technique: second-order. |
| S-N01 | The plan looks solid and the team is excited, but I am nervous. Before we lock it in, I want to surface every way this could blow up. | full-composer | B-P12 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
| S-N02 | We are confident the data migration will go fine. I would rather figure out everything that would make it go wrong instead. | full-composer | B-P24 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
| S-N03 | I'm nervous about my Python script — it crashes on startup and I can't figure out why. Surface what could be wrong with my error handling. | full-composer | B-N1 / routing-battery-catalog.md — adjacent vocabulary (nervous) but no complete trigger phrase fires; debugging request outside scope. |
| S-N04 | We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for? | full-composer | B-N2 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
