# Live-output conformance — the v9.14 reading

**A recorded reading with its N. Not a gate, and it may not become one.**
Emission rates are K-of-N live observations, and
[`docs/v8.7-constraint-teardown.md`](v8.7-constraint-teardown.md) §2 item 3 bars those from
gating. `EMIT-STAGE-A`'s control C19 fails if `cmd_conformance` ever acquires a failing exit
code.

**Corpus:** `tests/emission-stage-a-v9.14/documents/` (frozen) · **Detector:**
`check-quality-harness.detect_defects`, the same instrument the v9.0 surface uses
**Re-derive:** `python3 scripts/check-emission-stage-a.py conformance --out-dir tests/emission-stage-a-v9.14`

---

## Why this exists

Every analysis-quality gate in this repository reads one of three layers: the **shipped prose**
(`shared/`, `first-principles/`), the **frozen exemplars**, or its **own fixtures**. None reads
what the agent actually produced at runtime. The apparatus is enforced one layer away from where
quality happens.

That was tolerable while no live corpus existed. One does now, and it has defects.

## The reading

**N = 9 scored, 1 unreadable.**

| Reading | Numerator / denominator | Rate |
|---|---|---|
| Untraced conclusion claims | 3 / 61 | **4.9%** |
| Malformed chain blocks | 3 / 49 | **6.1%** |
| Nonconforming verdict cells | 17 / 120 | **14.2%** |

### The unreadable document is the point, not a footnote

`TB-08` raises `SectionResolutionError` — it carries 2 of 6 section headings and no traceable
identifiers. It was **dispatched and it reasoned well**: it separates the given facts from the
causal story, challenges baseline comparability, and states what three runs cannot establish. It
simply did not emit the contract.

**Every rate above is therefore conditional on readability.** An unreadable document contributes
to no numerator and no denominator, so a run that abandons the output contract *entirely* leaves
the population rather than lowering any rate. Contract-emission reliability and conformance are
two different numbers, and only the second is a rate. Control C18 fails if unreadable documents
stop being counted.

**The first is now published as a rate too:** contract-emission reliability on the v9.12.0 body
is 24 of 28 dispatched attempts across this corpus and the w4-paired run, against 22 of 22 on
older bodies — see [`docs/abandonment-phase0-reading.md`](abandonment-phase0-reading.md). Every
abandonment there is a run that used no tools at all.

## Against the older corpus

`tests/live-conformance-v9.0/` predates v9.11's EMIT-01..03 work on verdict-cell emission shape.

| Reading | v9.0 (n=8) | v9.14 (n=9) |
|---|---|---|
| Nonconforming verdict cells | 33/153 = 21.6% | **17/120 = 14.2%** |
| … excluding each corpus's largest single contributor | 2/122 = 1.6% (`Q-P2` out) | **10/103 = 9.7%** (`TB-06` out) |
| Documents with ≥1 nonconforming verdict cell | 3 of 8 | **6 of 9** |
| Untraced conclusion claims | 0.0% | **4.9%** |
| Malformed chain blocks | 0.0% | **6.1%** |

**This is directional and nothing more.** Different prompts, different corpora, n≈9 per side, one
run each, no control arm and no pairing.

### Correction (2026-09-26): the pooled verdict rate does not show an improvement

As first published, this section read the pooled 21.6% → 14.2% as the verdict reading moving the
right way, and as consistent with v9.11's EMIT-01..03 landing at runtime. **Withdrawn.** One
document carries the whole of that movement:

- **`Q-P2` holds 31 of v9.0's 33 nonconforming cells** — every Verdict cell it wrote. Take it out
  and v9.0 reads 2/122 = 1.6%. The same leave-one-out on v9.14 (its largest contributor, `TB-06`,
  7 of 17) leaves 9.7%. **The direction reverses.** Counted per document rather than per cell,
  it reverses too: 3 of 8 documents carried a nonconforming cell in v9.0, 6 of 9 in v9.14.
- **The failures are not the same defect.** `Q-P2` substituted its own vocabulary wholesale
  (`Accepted as a modelling convention`, `Verified approximately true`). Every one of v9.14's 17
  still leads with a prescribed token and fails on what follows it — a qualifier before the
  em-dash (`Accept, narrowly —`, `Discard as stated —`) or no em-dash rationale at all. That is
  the shape of v9.0's *other* two failures (`PR-N1`, `PR-N2`), now more frequent.
- **EMIT-01..03 do not target either shape.** They prescribe the Self-Audit Gate's heading, the
  em-dash-not-colon separator, and the assumptions table's five columns. No v9.14 failure is a
  colon separator.

So the pooled rate was a one-document artefact, and the defensible reading is the reverse: on
these corpora, token-plus-qualifier drift is **more** frequent after v9.11 than before, and
nothing here attributes that to any change. It joins the other two adverse readings as a
**question**, not a regression finding. The honest test for all three is a paired re-run on
identical prompts, which neither corpus can supply.

Read the 0.0% figures with particular care: a detector that fires 3 times on one corpus and 0 on
another may be reading a genuine difference or a difference in document shape.

## Adjudicating the six flagged items (W4 Phase A, offline)

Before spending on a re-run, each untraced claim and malformed chain block the detector flagged
was read against the rule in `shared/spine/references/output-template.md` it is scored under,
and that rule was checked at `v9.0.0` to see whether both corpora were written against it.

| Item | What was flagged | Rule, and whether `v9.0.0` carried it | Verdict |
|---|---|---|---|
| `TB-02` C2 | `→ GT-2's real pricing shows…` as the second hop | §4: *a hop must not begin with a `GT-N` identifier* — yes | **Real positive** |
| `TB-10` C1 | `→ GT-5 and GT-7? show…` as the second hop | same — yes | **Real positive** |
| `TB-10` C3 | `→ GT-6 shows…` as the second hop | same — yes | **Real positive** |
| `TB-04` | `**Key sources read at source for this analysis:**` + seven links | §6: any bold colon lead-in is a claim — yes | Rule-literal only: a bibliography, not an assertion |
| `TB-07` | `**Trade-offs acknowledged:**` ending `no chain — flagged assumption only` | §6: a marked caveat *still scores untraced*, by design — yes | Disclosed gap, scored as the template intends |
| `TB-09` | `**Confidence:**` naming `GT-7?` but no chain | §6: `**Confidence:**` must cite a chain — **no**, added after `v9.0.0` | Real against the current rule; not comparable |

**The malformed-chain reading survives adjudication.** All three blocks become well-formed when
the only change is that the offending hop no longer *leads* with the GT id — the cause is that
one rule, which both bodies carried. v9.0: 0 of 64 blocks; v9.14: 3 of 49.

**The untraced reading does not survive as a regression signal.** One item is a bibliography,
one is the template's own disclosure marker working as designed, and the third breaks a rule the
older body was never given: `v9.0.0` listed three prescribed lead-ins, not four, and only 1 of
v9.0's Confidence lines was even shaped to be read as a claim, against 9 of v9.14's.

Real positives therefore stand on two axes — leading-GT hops and verdict qualifier drift — and
neither corpus can say whether they come from the body or from the prompts. That is what the
paired re-run pre-registered in [`docs/w4-paired-preregistration.md`](w4-paired-preregistration.md)
exists to answer.

**Answered, 2026-09-27: not the body, at this N.** Five prompts, three repeats, both bodies —
malformed chain blocks 2 of 13 documents (v9.0.0) vs 2 of 14 (v9.12.0), nonconforming verdict
cells 9 of 13 vs 8 of 14, both *no difference detected at this N* under the pre-registered rule.
Both bodies produce both defects. See [`docs/w4-paired-reading.md`](w4-paired-reading.md).

## Limits

- **One run per prompt, one model.** Within-arm variance is uncontrolled; this repository has
  measured swings of up to 3 band points on an identical prompt.
- **Nothing here says the analyses are good.** Every figure counts artifacts.
  `docs/v8.7-correctness-spot-check.md` measured that conformance does not predict correctness,
  and that applies to every number on this page.
- **The reading is deterministic only because the corpus is frozen.** Re-running the *agent* would
  not reproduce it. That is precisely why it may not gate.
- **No comparison against working without the agent.** `docs/EVIDENCE.md` keeps its standing
  disclaimer.

## Falsifiers

```sh
# 1. The published figures are what the tool emits — not hand-typed.
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q '3/61'
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q '17/120'

# 2. N is 9 scored and 1 unreadable, and the unreadable one is named.
python3 scripts/check-emission-stage-a.py conformance \
    --out-dir tests/emission-stage-a-v9.14 | grep -q "N = 9 scored, 1 unreadable \['TB-08'\]"

# 3. The reading is not a gate: it exits 0 on a corpus carrying defects.
python3 scripts/check-emission-stage-a.py conformance --out-dir tests/emission-stage-a-v9.14

# 4. The controls that keep 1-3 true are registered and pass.
python3 scripts/check-emission-stage-a.py --self-test

# 5. The correction's figures: exits 1 if Q-P2 does not hold 31 of v9.0's 33,
#    if either leave-one-out figure or the per-document counts differ, or if any
#    v9.14 failing cell does not lead with a prescribed token.
python3 - <<'EOF'
import importlib.util, sys, glob, os, re
spec = importlib.util.spec_from_file_location('qh', 'scripts/check-quality-harness.py')
q = importlib.util.module_from_spec(spec); sys.modules['qh'] = q; spec.loader.exec_module(q)
def read(pat):
    out = {}
    for f in sorted(glob.glob(pat)):
        n = os.path.basename(f)[:-3]
        if n == 'README' or n.endswith('.orchestrator'): continue
        try: out[n] = q.detect_defects(open(f).read(), n)
        except Exception: pass
    return out
a = read('tests/live-conformance-v9.0/*.md')
b = read('tests/emission-stage-a-v9.14/documents/*.md')
tot = lambda d, s=(): tuple(sum(r[k] for n, r in d.items() if n not in s)
                            for k in ('nonconforming_verdict_cells', 'verdict_cells'))
docs = lambda d: (sum(r['nonconforming_verdict_cells'] > 0 for r in d.values()), len(d))
tok = re.compile(r'^\**\s*(Accept|Challenge|Discard)\b')
sys.exit(0 if all([
    tot(a) == (33, 153), a['Q-P2']['nonconforming_verdict_cells'] == 31,
    tot(a, {'Q-P2'}) == (2, 122), tot(b, {'TB-06'}) == (10, 103),
    docs(a) == (3, 8), docs(b) == (6, 9),
    all(tok.match(x) for r in b.values() for x in r['_nonconforming_verdict_text']),
]) else 1)
EOF
```
