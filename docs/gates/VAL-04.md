# VAL-04: No 4-gram collision across skill descriptions.

<!-- GENERATED:FACTS -->
## Facts

- `derived_counts` (1 entries): `ngram_width`=4
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-trigger-collisions.py --self-test && python3 scripts/check-trigger-collisions.py
```

CI job: `check-trigger-collisions`
<!-- END GENERATED:HOW-TO-RUN -->
