# Protocol — Does the delivered analysis open with the Answer, in the wild?

**Id:** `answer-first` · **Registered:** 2026-09-29, before any `claude` call under this id.

**Body commit:** `6c633199` (`feat(agent): deliver the analysis answer-first — Answer, six
sections, process-output appendix`) — the commit that made the agent's delivered file open with
a `## Answer` block, keep the six contract sections unchanged and in order, and move every
process-output block to a trailing `## Appendix — process output` heading. Offline reader
controls (EMIT-STAGE-A's C21) and the runner/scorer below (`tests/answer-first/run.py`) were
committed at `257fc0be`, after the body commit and before this pre-registration.

## 1. What this confirms

The offline controls prove the mechanism reads correctly and that a mis-slice would be visible.
They do not show the body's own prescribed create/assemble commands survive a real, unscripted
`claude -p` run against a real prompt — a live agent narrates, dispatches sub-agents, and can
deviate from any written procedure. This run checks that on real prompts, once.

## 2. Prompts — `tests/trackb-catalog-v9.13.md`

Three prompts, one per domain, one run each, sequential:

| Prompt | Domain | Text |
|---|---|---|
| `TB-01` | software | Reason from the ground up about whether our team should replace our REST API with GraphQL. We have 9 client applications, 3 of them mobile, and our main complaint is that mobile screens need 4–6 round trips to render. Be rigorous and show your reasoning. |
| `TB-04` | policy | Analyse rigorously and from the ground up: a mid-sized city wants to cut commuter car journeys by 20% within three years, and is choosing between free public transit, congestion pricing, and building protected cycle lanes. What should determine the choice? |
| `TB-08` | science | Think this through carefully from fundamentals. A lab reports that a new catalyst raises the yield of their reaction from 62% to 71%, measured across three runs. What should be concluded, and what should not be? |

`TB-04` is also the specimen prompt EMIT-STAGE-A's live corpus (`tests/emission-stage-a-v9.14/`)
already carries, so this run's `TB-04` document can be compared against that prior capture on the
same prompt if a future reading wants to.

## 3. Transport

`claude -p --model claude-sonnet-5 --plugin-dir <repo>/first-principles --output-format
stream-json --verbose --permission-mode acceptEdits --allowedTools <ALLOWED_TOOLS>`, scratch cwd
outside the repository, one prompt per fresh subdirectory, sequential, session persistence ON
(the agent's own subagent transcript is captured, as every prior delivery-mechanics measurement
in this tree has done).

`ALLOWED_TOOLS` (`tests/answer-first/run.py`'s `ALLOWED_TOOLS` constant, amended — see §7):
`Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Bash(*)`.

**`bypassPermissions` is not used, and this is the one axis this transport differs from every
earlier delivery-mechanics capture in this tree** (`tests/delivery/`, `tests/delivery-fix-3/`,
`tests/delivery-fix-4/`, `tests/example-rerun/`, all of which ran with
`--permission-mode bypassPermissions` and no `--allowedTools`). Those captures needed only that
*a* transport delivered the file; this run also needs the permission surface a real installation
would actually grant, since D-G's own reasoning is that an allowlisted install must be able to run
the body's prescribed commands at all. `--allowedTools` here is what makes that a meaningful test
rather than an assumption.

The capture is the delivered `analysis-*.md` file collected from `<subdir>/.first-principles/`
after the run (`tests/answer-first/run.py`'s `_collect_all_files`, which copies every file in that
directory, not only `*.md`, so a leftover `.answer`/`.process`/`.tmp` side file is preserved as
evidence rather than silently swept).

## 4. Criteria (a)–(e) — the registered definitions, verbatim

Implemented in `tests/answer-first/run.py` as `criterion_a` … `criterion_e`; each is exercised
offline by the runner's own `--self-test` (S1–S6) before being trusted on a live document.

- **(a)** `qh._slice_sections(doc)` resolves (the six sections resolve in order, with no gap).
- **(b)** the first line outside fences matching `^## ` is exactly `## Answer`.
- **(c)** no heading before the `## 6. Conclusion` line matches
  `(?i)process output|assumption audit|adversarial pass|closure ledger|self-audit|techniques not applied|appendix`,
  and no line before it starts with `Techniques not applied` (optionally bolded).
- **(d)** the Answer body (from `## Answer` to the next heading) contains at least one `\bC\d+\b`
  token, and every such token is one section 4 cites (chain ids are compared normalised —
  `qh._normalize_chain_id` — so a bare `C1` citation matches a `### Conclusion C1: …` heading).
- **(e)** `len(answer_body.split()) <= 150`, the heading line excluded. (D-C sets the body's own
  authoring budget at 120 words; this criterion's ceiling is looser, matching the plan's stated
  live-criterion allowance.)

Alongside pass/fail, the reading records: total words, words before the `## 1.` heading, the
appendix's share of total words, any side file (`.answer`/`.process`/`.tmp`) left behind, and
whether every chain the Answer cites is also cited somewhere in section 6's own text.

## 5. Pass rule, void rules, and what a failure means

**Pass** = all 3 runs meet (a)–(e).

**A failing run is reported as a failure, not re-scored, and any revision to the body runs under
a new id.** This mirrors `docs/regression-rerun-protocol.md`'s own rule: a check that fails is not
softened by a second attempt at the same id.

**Void rules** (attempt-level, not scoring-level):

- **Usage-limit stub** → stop and resume later; not counted as an attempt.
- **Not dispatched** (the prompt did not route to the agent) → void, retry, at most 3 attempts
  per prompt.
- **A denied Bash command that names `.first-principles`** → void-permission: stop and report,
  do not retry silently. This is the one failure mode the transport probe (below) exists to catch
  *before* it can happen on a registered run.
- **`loaded_body` is not the working-tree plugin** (`tests/delivery-fix-3/run_fix3.py`'s own
  abort rule, reused here) → abort; the capture would not be testing this body.

## 6. What N=3 shows, and what it does not

**N=3 on one model shows the rule working on these three runs, not a rate.** This is not a K-of-5
noise-floor reading (`docs/v8.7-constraint-teardown.md` §2 item 3) and is not treated as one — it
is a pre-registered pass/fail confirmation on a named, small set of prompts, exactly as
`docs/regression-rerun-protocol.md` scores its own four regressions. A future run with more
prompts or repeats would need its own id.

## 7. Pre-run amendments

### 2026-09-29 — `ALLOWED_TOOLS` widened to `Bash(*)`; `--allowedTools` passed as one `=`-joined token

**Found by the transport probe** (`python3 tests/answer-first/run.py probe --cwd <scratch dir>`),
before any registered run.

**Finding 1 — the enumerated per-verb prefixes admit none of the body's own commands.** Live,
reproduced twice: the body's own create command
(`mkdir -p .first-principles && F=".first-principles/analysis-$(date -u +%Y%m%dT%H%M%SZ).md" &&
: > "$F" && …`), issued verbatim under `--allowedTools=Read,Glob,Grep,WebFetch,WebSearch,
Bash(mkdir:*),Bash(cat:*),Bash(printf:*),Bash(echo:*),Bash(date:*),Bash(grep:*),Bash(wc:*),
Bash(mv:*),Bash(rm:*),Bash(ls:*),Bash(head:*),Bash(sed:*)`, was denied both times with "Contains
shell syntax (string) that cannot be statically analyzed" — including once with the tool call's
own `dangerouslyDisableSandbox: true`, which did not change the verdict. Isolating the cause: a
compound `&&`-chained command with no variable assignment (`mkdir -p .first-principles &&
echo done`) is admitted by a single matching prefix (`Bash(mkdir:*)`); the same shape WITH a
shell variable capture-and-reuse (`F="…" && : > "$F" && echo "$F"`) is denied under that same
prefix. **Every step the body's delivery mechanics prescribe captures `F="<path>"` once and
re-references `"$F"` (or the caller substitutes a literal path for `<path>`) in every subsequent
Bash call** (`shared/spine/SKILL-body.md`, "Deliver the analysis as a file") — so no set of
narrower `Bash(<verb>:*)` prefixes can admit them; this is a property of Claude Code's own
static-analysis-based Bash permission engine reacting to shell variable assignment, not of which
verbs are or are not listed.

**Resolution.** `Bash(*)` was the narrowest change found that admits the affected commands.
Confirmed live, zero `permission_denials`: the create command alone, and a full
create → append → write-answer → assemble → idempotent-retry → check sequence run end to end.
`ALLOWED_TOOLS` is now `Read, Glob, Grep, WebFetch, WebSearch, Bash(*)` — one enumerated Bash-tool
entry (not the bare token `Bash`), under `--permission-mode acceptEdits` (never
`bypassPermissions`); the agent's own frontmatter `disallowedTools` (Write, Edit, Agent,
SendMessage, ListAgents) is unaffected by it and still applies. This does widen what the harness
grants relative to the narrower set originally registered above — recorded here rather than
smoothed over, since T-tg9-01's mitigation is now `acceptEdits` alone, not a per-verb allowlist,
and a real installation restricting Bash to specific verb prefixes would be unable to use this
agent's file-delivery mechanism at all, for the identical reason. That is a property of the
shipped body's command shape versus Claude Code's sandbox, out of this plan's scope to change,
and is recorded as a follow-up in the executing plan's SUMMARY rather than fixed here.

**Finding 2 — `--allowedTools` must be one `=`-joined token.** `--allowedTools <value>
<prompt>`, as two separate argv entries, is silently swallowed whole by the CLI's variadic
`<tools...>` arity — the prompt argument disappears into the tool list and the run fails with
`Error: Input must be provided either through stdin or as a prompt argument when using --print`.
Reproduced with both space- and comma-joined values as the wrongly-split two-entry form; resolved
by passing a single `--allowedTools=<comma-joined>` argv token instead. `tests/answer-first/
run.py`'s `live_argv` and `cmd_probe` were updated accordingly, and S7's self-test check was
updated to look for an `--allowedTools=` prefix rather than the flag and its value as two entries.

Both changes are committed together, before the first registered run.
