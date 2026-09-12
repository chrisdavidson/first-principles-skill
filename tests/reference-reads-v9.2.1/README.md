# v9.2.1 Reference-Reads Fixture — DEMO-TRIAGE Capture

**Recovered:** 2026-09-12. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `DEMO-TRIAGE.jsonl` is the raw capture; `DEMO-TRIAGE.md` is
its extracted analysis; `catalog.md` wraps the prompt that produced it; `defects.tsv` and
`baseline-defects.tsv` carry the detector readings taken against that analysis. All five, plus this
README, are committed as-is; any correction to this evidence is a fresh, separately-provenanced
capture, not a silent edit of this one.

## Origin run and chain of custody

Repo HEAD at freeze: `3c3ed42`. Plugin version at freeze: `9.2.1` (all 17 version stamps agree —
`check-version-stamps.py` PASS, per `DEMO-first-principles-ticket-triage.md`'s own Provenance
table).

The exact transport, copied verbatim from `DEMO-first-principles-ticket-triage.md` § Provenance:

```sh
ANTHROPIC_MODEL=claude-opus-5 python3 scripts/check-quality-harness.py \
    --probe DEMO-TRIAGE --catalog <scratch>/catalog.md \
    --plugin-dir first-principles --out <scratch>/out
```

`--probe` dispatches exactly one live generation through the harness's Plan-36-locked argv:

```
claude -p --plugin-dir <path> --no-session-persistence --output-format stream-json --verbose \
    --permission-mode bypassPermissions <prompt>
```

Model pinned `ANTHROPIC_MODEL=claude-opus-5`; `claude` CLI `2.1.268`; plugin surface
`--plugin-dir first-principles` — the working tree, not the installed cache (per
`memory/agent-testing-reads-plugin-cache.md`: invoking the agent through the in-session `Agent`
tool reads a frozen plugin cache, not the working tree — this run deliberately used the locked
CLI transport instead, for exactly that reason). One generation only; no judge invocation — this
is a demonstration capture, not a scored measurement.

Chain of custody:

1. The raw capture, extracted analysis, catalog wrapper, and both detector-reading `.tsv` files
   were produced by that transport into a session scratchpad at
   `/tmp/claude-1000/-home-chrisdavidson-Projects-first-principles-skill/5bcdecc2-8880-4870-a039-35c99aa721e6/scratchpad/fp-demo/`
   — a location subject to OS reaping, with no other copy anywhere.
2. The scratchpad nested the capture and analysis under an `out/` subdirectory and additionally
   carried a duplicate analysis under `analyses/DEMO-TRIAGE.md`. That `analyses/` copy was
   confirmed `cmp`-identical, byte for byte, to the `out/DEMO-TRIAGE.md` copy and was deliberately
   **not** frozen a second time — freezing the same bytes under two names would not add evidence,
   only a second byte-freeze obligation.
3. All five source files were flattened to this directory's root: `catalog.md` stays at the root
   (it was already there); `out/DEMO-TRIAGE.jsonl` → `DEMO-TRIAGE.jsonl`; `out/DEMO-TRIAGE.md` →
   `DEMO-TRIAGE.md`; `defects.tsv` and `baseline-defects.tsv` stay at the root (they were already
   there). This flattening follows the `tests/quality-provenance-v8.24/` precedent, which renamed a
   staged `analyses/run3-pr11.md` to `PR-P1.md` and documented the rename as deliberate rather than
   silent.

Chain-of-custody hashes, checkable rather than merely asserted — measured before the copy (source,
scratchpad) and re-measured after (frozen, this directory); both readings are identical for all
five files:

| File | sha256 |
|---|---|
| `catalog.md` | `51d277cf29223b0f557bb539099f9e359cb49ca3e87409b32c830770afc54575` |
| `DEMO-TRIAGE.jsonl` | `9b89317f4353c7b0edf0dc48ed5b65268c7aa92ec282110d638b59f4c1e6b92f` |
| `DEMO-TRIAGE.md` | `660109748ffc8ba53c7a818fcb38ee49258464f148fb9136994c9e3a271498dd` |
| `defects.tsv` | `532e8e1d45d96c777823af22130799c62f18f121a40853f68fde66d96326d195` |
| `baseline-defects.tsv` | `06d3be6873456a628979bb9dfb1743b454f40cbcd77a05cfb7b8eaeacaf3cc87` |

Each row above was verified via `cmp` returning exit 0 for the source→frozen pair, and via
`sha256sum` producing the identical digest on both the scratchpad original and the frozen copy —
not verified by size alone.

## Prompt

`catalog.md` in this directory wraps the scenario prompt authored for this demonstration (see
`DEMO-first-principles-ticket-triage.md` § "The scenario" for the full authored text and its
stated intent). The scenario was built to exercise three specific parts of the methodology, not
to be merely realistic; it is not drawn from any committed catalog elsewhere in this repo.

## Metadata

| | |
|---|---|
| Capture size (`DEMO-TRIAGE.jsonl`) | 259,463 bytes |
| JSONL line count | 66 |
| Decoded object count | 66 |
| Extracted analysis (`DEMO-TRIAGE.md`) | 28,420 bytes |
| Terminal event | `result` / `success` |

Every number above was re-derived directly from this frozen directory's own files in this phase's
own execution session, not carried over from an earlier reading.

## Per-event census

`tool_use` breakdown, re-derived from the frozen `DEMO-TRIAGE.jsonl` by walking every
`type == "assistant"` event's `message.content[]` for `block["type"] == "tool_use"`:

| Tool | Count |
|---|---|
| WebFetch | 3 |
| Agent | 1 |
| Skill | 1 |
| ToolSearch | 1 |
| Bash | 1 |

**`Read`, `Grep` and `Glob` each occur zero times in this capture.** This is the whole point of the
fixture: during this run, `output-template.md` — along with every other reference file the agent
body's `references/` tree carries — was opened zero times, because nothing in the run's tool_use
stream is a `Read`, `Grep`, or `Glob` call at all.

## What this fixture is evidence for

This is the *before* reading for backlog 999.88 / review finding R1 — the finding that the agent
body carries exactly one read imperative directed at a named file (the Phase 3 evidence-acquisition
step, `shared/spine/SKILL-body.md:145`), and that `output-template.md` itself carries no imperative
instructing the agent to open it. This capture is the live demonstration of that gap: a run that
exercised the methodology end to end opened zero reference files of any kind.

The *after* reading — re-running an equivalent capture once this phase's product edit lands, to
measure whether the read-imperative count moved the observed behavior — is **not** taken here. It
belongs to backlog 999.89, filed by this phase to own the `reference_reads` census this fixture's
own read-zero result motivates.

## On the two root-level review documents

`REVIEW-agent-improvement-opportunities.md` and `DEMO-first-principles-ticket-triage.md` — the two
files that named this run, discussed its findings, and supplied the Provenance table this README
quotes from — are both **untracked and volatile**: neither is committed to this repository, and
either may be edited, moved, or deleted outside of this phase's own record. `.planning/ROADMAP.md`
§ *Phase 999.88* carries the transcription of record for what those two documents said. Note that
`.planning/` is itself gitignored in this repository (`commit_docs: false`), so that transcription
is not a tracked surface either — this README and the five frozen capture files in this directory
are the only tracked, durable record of this run and its provenance.

## Why registering this path is not a new gate (D-03)

FROZEN-EVIDENCE (`scripts/check-firewall-battery.sh`) is an inline check whose
`TOTAL=$((TOTAL + 1))` line fires exactly once, unconditionally, regardless of how many entries
`_FROZEN_PATHS` carries — the increment is not inside any loop over the array. Registering this
directory's path as one more `_FROZEN_PATHS` entry therefore does not add a new battery member: the
battery's total gate count and CI job count are unaffected by this registration. For the current
battery/CI population figures, see `CLAUDE.md`'s generated gate table — this README deliberately
states no bare digit of its own for that population, per `docs/PROCESS.md` §2's standing constraint
on moving counts (a digit copied here would go stale the next time either total moves, exactly the
defect class the rest of this repository's apparatus exists to prevent).

## Frozen-evidence discipline

`catalog.md`, `DEMO-TRIAGE.jsonl`, `DEMO-TRIAGE.md`, `defects.tsv`, `baseline-defects.tsv`, and this
README are committed as-is and never regenerated or hand-edited to match a later result. This
directory is registered in `scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array, so an
uncommitted edit to any of these tracked files turns the battery RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet HEAD` over the registered pathspec, plus a separate
untracked-files sweep. It catches an edit to a file already tracked at HEAD, and it catches an
untracked file appearing inside the directory — but a committed `git rm` of one of these files
passes it clean. It is tamper-evidence for modification, not a deletion guard. Any change to this
fixture's committed contents, including removal, must be reviewed in-diff like any other commit;
nothing here enforces that automatically.

## A note on the absolute donor-machine path

Nothing in this fixture's own files embeds an absolute path from the donor machine that produced
it (unlike `tests/quality-provenance-v8.24/`'s two `Read` targets) — this run's tool_use census
carries no `Read` calls at all. If a future capture of the same shape does carry such paths, the
precedent instruction stands: they are frozen fixture content, a property of the machine that
produced the capture, not of any machine that later reads this file, and must not be "fixed" to
match a local path.
