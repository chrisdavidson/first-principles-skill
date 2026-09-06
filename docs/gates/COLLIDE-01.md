# COLLIDE-01: Dual-install name-collision scan: no skill/agent name collisions between the plugin and monolith install surfaces.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (2): `first-principles`, `first-principles-thinking`
- `disclosed_bounds_anchors` (1): `vacuous-when-monolith-absent`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-install-collisions.py --self-test && python3 scripts/check-install-collisions.py
```

CI job: `check-install-collisions`
<!-- END GENERATED:HOW-TO-RUN -->
