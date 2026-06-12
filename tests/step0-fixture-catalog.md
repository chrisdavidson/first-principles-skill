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
| S-P01 | run a pre-mortem on this launch — we are shipping the payments-rewrite service to all EU customers next Friday, replacing the legacy stripe integration, with no staged rollout | focused-pre-mortem | Fires `pre-mortem` trigger phrase. Technique: pre-mortem. Context added (Phase 74 FIX-01): names what is launching, who is affected, when, and a key constraint so the live agent can frame the already-failed counterfactual without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P02 | invert this claim: faster ships means better retention — our team ships every two weeks and we want to know when this assumption breaks down | focused-inversion | Fires `invert` trigger phrase. Technique: inversion. Context added (Phase 74 FIX-01): names the concrete team cadence and the question the inversion should answer, so the live agent can run the formal inversion rather than requesting context. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P03 | draw a fishbone diagram on the production incident — our checkout API returned 503 errors for 40 minutes starting 14:10 UTC yesterday, affecting all users; we have ruled out the database layer | focused-fishbone | Fires `fishbone` trigger phrase. Technique: fishbone. Context added (Phase 74 FIX-01): names the affected service, the error type, duration, scope, and one ruled-out cause branch so the live agent can enumerate cause categories without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P04 | do a five whys on this outage — our payment service API returned 500 errors for 12 minutes at 09:30 UTC on 2026-06-11; it recovered after a pod restart; 8k transactions were affected | focused-five-whys | Fires `five whys` trigger phrase. Technique: five-whys. Context added (Phase 74 FIX-01): names the symptom, timestamp, recovery event, and impact so the live agent has an observable starting symptom for the Why-chain without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P05 | build a trade-off analysis for these database options — we are choosing between PostgreSQL, MongoDB, and DynamoDB for a transactional e-commerce backend processing 500 writes/second at peak, with a 12-month managed-cloud budget of $3k/month | focused-trade-off | Fires `trade-off` trigger phrase. Technique: trade-off. Context added (Phase 74 FIX-01): names the candidate options, the workload characteristics, and the budget constraint so the live agent can build the weighted scoring matrix without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P06 | what are the second-order effects of shipping this feature this week — we are adding real-time inventory sync to our checkout flow, the feature is code-complete and tested in staging, and this week is a hard deadline because our biggest customer demos it Friday | focused-second-order | Fires `second-order` trigger phrase. Technique: second-order. Context added (Phase 74 FIX-01): names the feature, its current state, and the timeline constraint so the live agent can enumerate layered downstream effects without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-N01 | The plan looks solid and the team is excited, but I am nervous. Before we lock it in, I want to surface every way this could blow up. | full-composer | B-P12 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
| S-N02 | We are confident the data migration will go fine. I would rather figure out everything that would make it go wrong instead. | full-composer | B-P24 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
| S-N03 | I'm nervous about my Python script — it crashes on startup and I can't figure out why. Surface what could be wrong with my error handling. | full-composer | B-N1 / routing-battery-catalog.md — adjacent vocabulary (nervous) but no complete trigger phrase fires; debugging request outside scope. |
| S-N04 | We have a written plan to roll out the new authentication system across all teams next quarter. Before we lock the timeline, walk through how this could go badly — what failure modes should we prepare for? | full-composer | B-N2 / routing-battery-catalog.md — oblique prompt; no trigger phrase fires after D-02 normalization. |
| S-P07 | I am nervous about my plan for the launch | focused-pre-mortem | CR-01 falsifying fixture: fires the "nervous about (my the this) plan" alternation trigger that was silently dropped by the naive pipe-split parser. |
| S-P08 | walk through what would have caused this outage | focused-pre-mortem | CR-01 falsifying fixture: fires the "(walk run) through what would have caused" alternation trigger that was silently dropped by the naive pipe-split parser. |
