# DELIVERY-GUARD: The plugin's one piece of executable code — the SubagentStop delivery guard in `first-principles/hooks/` that refuses the agent's stop, at most twice, until its analysis file is assembled and its reader report exists (backlog 999.196) — is wired and decides right.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (9): `P1-live-wiring`, `P2-guard-self-test`, `P3-corpus-verdicts`, `M1-matcher-renamed`, `M2-command-path-missing`, `M3-second-subagentstop-entry`, `M4-guard-always-allows`, `M5-guard-always-blocks`, `M6-corpus-floor`
- `control_count`: `9`
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
