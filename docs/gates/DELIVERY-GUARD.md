# DELIVERY-GUARD: The plugin's one piece of executable code — the SubagentStop delivery guard in `first-principles/hooks/` that refuses the agent's stop, at most twice, until its analysis file is assembled and its reader report exists (backlog 999.196) — is wired and decides right.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (35): `P1-live-wiring`, `P2-guard-self-test`, `P3-corpus-verdicts`, `M1-matcher-renamed`, `M2-command-path-missing`, `M3-second-subagentstop-entry`, `M4-guard-always-allows`, `M5-guard-always-blocks`, `M6-corpus-floor`, `P4-survivor-blocked`, `M7-survivor-check-stubbed`, `A01-plain-replace`, `A02-unmatched-refuses`, `A03-duplicate-refuses`, `A04-h3-scope`, `A05-fence-ignored`, `A06-last-wins`, `A07-chained`, `A08-extent-sibling`, `A09-level-mismatch-refuses`, `A10-unclosed-fence-refuses`, `A11-withdraw-recovers`, `A12-withdraw-unmatched-warns`, `A13-idempotent`, `A14-identity-captures`, `A22-malformed-then-withdraw-assembles`, `A23-malformed-alone-refuses`, `A24-unclosed-fence-recovery`, `M8-fence-test-dropped`, `M9-duplicate-refusal-removed`, `M11-withdraw-skip-removed`, `M12-unmatched-refusal-removed`, `M13-deferred-validation-ignores-withdraw`, `M14-unmatched-withdraw-refuses`, `M15-unmatched-withdraw-survives`
- `control_count`: `35`
- `registered_surfaces` (2): `first-principles/hooks/delivery-guard.py`, `first-principles/hooks/hooks.json`
- `disclosed_bounds_anchors` (3): `decides delivery from the file on disk, never from the analysis's quality`, `blocks at most twice per run, then lets the stop through`, `whether a blocked agent then delivers is a live reading, never gated`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-delivery-guard.py --self-test
```

CI job: `check-delivery-guard`
<!-- END GENERATED:HOW-TO-RUN -->
