# FROZEN-EVIDENCE: Frozen baselines and captures are unmodified relative to HEAD, plus an untracked-files sweep over the same paths.

<!-- GENERATED:FACTS -->
## Facts

This gate carries no `--describe`-derived facts (no script backs it).
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
git diff --quiet HEAD -- "${_FROZEN_PATHS[@]}"
```

CI job: — (not a CI job)
<!-- END GENERATED:HOW-TO-RUN -->
