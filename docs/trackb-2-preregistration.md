# Track B Pre-Registration (trackb-2) — Does the agent's own document beat an unaided answer?

**Id:** `trackb-2` · **Status:** LOCKED before any measurement run. Registered 2026-09-30.

**Supersedes** [`docs/trackb-preregistration.md`](trackb-preregistration.md) and its run
`tests/trackb-run-v9.13/`, per that document's own §6 ("Any subsequent run must cite this
document, state that it supersedes it, and say why").

**Why.** [`docs/trackb-transport-erratum.md`](trackb-transport-erratum.md) found that every
arm-T capture in `tests/trackb-run-v9.13/generations/` is the main session's *summary* of the
agent's analysis, not the agent's analysis — 0 of 6 output-contract sections and 0 `GT-`
identifiers across all ten captures, and dispatch itself undeterminable for 7 of the 10 cells.
The v9.13 `null` result therefore answered a narrower, unregistered question. This document
re-registers the comparison so that arm T is scored on the agent's own delivered document, with
dispatch recorded per cell from a stream-json transcript, under the same instrument and the same
decision threshold as before.

**Not the successor: `docs/emission-phase1-preregistration.md`.** That document's own text says
"Supersedes nothing" — it asks whether the agent's delivered document shows its derivations, a
different, mechanical question with no judge and no control arm. `docs/trackb-transport-erratum.md`
line 119 named it as the comparative successor; that line is wrong and is corrected in that
document's own erratum text (Task 1(b) of this run's plan). `trackb-2` is the comparative
successor.

**Binding:** this document fixes the hypothesis, the arms, the instrument, the analysis plan and
the decision threshold *before* any data exists under this id. Nothing below may be changed after
the first registered cell runs, except a pre-declared, dated pre-run amendment recorded under
§Pre-run amendments before that cell runs. A change after that requires a new pre-registration id.

---

## 1. Unchanged from `docs/trackb-preregistration.md`

The goalposts do not move. Every item below is a verbatim blockquote of the sentence(s) that
govern it in the superseded document — copy-paste, never paraphrased, never re-wrapped in a way
that changes a word (a normalised, whitespace-flexible comparison checks this mechanically; see
Task 1's `_c26_unchanged_is_verbatim` control). Commentary sits outside the blockquotes.

From §1:

> **H1.** For the same problem and the same underlying model, an analysis produced via
> the `first-principles` agent scores higher on the Track B Neutral Rubric
> (`docs/trackb-neutral-rubric.md`) than an answer produced without the plugin.
>
> **H0.** There is no detectable difference.
>
> A directional prediction is registered: if the plugin does anything, the effect should
> be largest on **Assumption Surfacing** and **Falsifiability**, because those are the
> behaviours its instructions most directly prescribe, and smallest on **Decision
> Usefulness**, which a strong unaided answer already delivers.

(Rubric criteria: Assumption Surfacing = C3, Falsifiability = C5, Decision Usefulness = C1.)

From §4:

> - **Prompts:** 10, fixed and published in `tests/trackb-catalog-v9.13.md` before the
>   run. Drawn across four domains (software, policy, science, personal/ethical) so a
>   single domain cannot carry the result. None is reused from any existing routing,
>   quality or Step-0 catalog — those prompts have shaped the agent body and would
>   favour arm T.

From §3:

> Scoring uses `docs/trackb-neutral-rubric.md`, authored for this run and frozen
> before it.

From §4:

> - **Runs per cell:** 1. Total generations = 10 × 2 × 1 = **20**.

From §4:

> - **Judges:** 2 independent blinded judges per document = **40** judgings. Two, not
>   one, because the existing harness's own stated limit is *"One judge per document,
>   not an inter-rater panel."* Inter-rater agreement is reported, never assumed.

From §4:

> - **Drift-control arm:** 20 documents re-judged in the same session = **20**
>   judgings, to measure this rubric's own same-run drift. See §5.

From §5:

> **Threshold for `cleared` — all three must hold:**
>
> 1. **Statistical:** a paired permutation test over the 10 prompt-level differences
>    returns *p* < 0.05 (two-tailed, 100,000 permutations, seed recorded in the
>    manifest).
> 2. **Larger than this instrument's own noise:** the observed mean difference exceeds
>    **twice the in-run measured judge drift**, where drift is the mean absolute
>    score change across the 20 re-judged documents in §4's drift-control arm. This
>    threshold is *self-calibrating* — it is computed from this run's own drift, not
>    from a number guessed in advance — which is deliberate, because the historical
>    +7/108 figure was measured on a different rubric and does not transfer.
> 3. **Not carried by one domain:** the effect holds in direction on at least three of
>    the four domains.

**Clarifying note, not a change:** the permutation test is enumerated exactly (2^10 sign
assignments), as the v9.13 code always did, so no seed is consumed by it. The seed recorded in
§4 below is the blinding shuffle's.

From §5:

> **Anything else is `null`.** `inconclusive` is reserved for a run that fails on
> mechanics (dispatch failures, unparseable scorelines above 10%), not for a
> disappointing result — a clean run that misses the threshold is `null`, not
> `inconclusive`, and may not be relabelled.

From §6:

> **Exactly one run.** No re-runs, no prompt substitutions, no "the harness misbehaved
> so we ran it again" without a recorded void and a fresh pre-registration id.

From §6:

> If the result is `null`, the comparative claim is **not published** — it is recorded
> in `docs/data/trackb-result.json` with `status: "null"` and reported internally. The
> Evidence Card then renders its standing disclaimer that no controlled comparison is
> published, which it already does today. This is enforced mechanically by
> `scripts/gen-evidence-card.py` controls C06 and C07, not by anyone's discipline.

From §2:

> **Model is pinned** for every invocation in both arms and recorded in the run
> manifest. A run spanning a model change is void and must be re-registered.

Pinned model for this run: `claude-sonnet-5`.

## 2. Changes, each with its justification

1. **Arm T invocation = the documented user path.** The prompt text is prefixed with the
   launcher skill's own slash form, `/first-principles:first-principles-analysis `, whose own
   procedure hands the request to the `first-principles:first-principles` agent, at repository
   HEAD `--plugin-dir <repo>/first-principles` (the answer-first body, commit `6c633199` or
   later — the run manifest records the exact HEAD sha and the sha256 of
   `first-principles/agents/first-principles.md`). Justified by the observed routing miss:
   `tests/emission-stage-a-v9.14/raw-attempt1/TB-05.jsonl` dispatched no agent at all on an
   undirected prompt (erratum §4a). The problem text after the prefix is byte-identical to arm
   C's. **Pre-declared fallback:** if the transport probe (§Transport probe) shows the slash
   form does not dispatch under `-p`, arm T instead uses the explicit frame "Use the
   first-principles:first-principles agent to analyse: `<prompt>`", recorded as a pre-run
   amendment before any registered cell. This document does not cite any unverified dispatch
   rate for either form.
2. **Arm T primary document = the agent's delivered file**, `.first-principles/analysis-*.md`
   from that cell's scratch working directory, scored whole (the `## Answer` block, the six
   named sections, and the process-output appendix). Dispatch is recorded per cell from the
   stream-json transcript. A cell with no dispatch, no delivered file, a delivered file failing
   the extraction-integrity check (below), a non-zero exit or a timeout is a mechanical failure:
   up to 3 attempts, every attempt frozen with its raw transcript and its reason, then the cell
   is void. A voided cell drops its prompt from the paired analysis. If voided cells exceed 10%
   of the 20 cells, status is `inconclusive` (mechanics), exactly like a dispatch-failure or
   unparseable-scoreline overrun above. A usage-limit stub is never counted as an attempt: the
   resumed run continues the same single run, and completed cells are never regenerated — so
   "exactly one run" holds across a pause. Retries are for mechanical causes only; content is
   never a retry cause beyond the contract-section extraction check.
3. **Secondary measure, reported and NOT gating.** Arm T's orchestrator final message — the last
   stream-json `result` event, not the earlier delegation stub (planner finding F5) — is also
   judged, 2 judges each, blinded in the same pool as the primary documents. It quantifies what a
   user sees without opening the delivered file. It never enters `evaluate()` and never affects
   `cleared`/`null`/`inconclusive`.
4. **Length** is reported as the registered covariate (words per arm, mean/median/min/max); no
   normalisation is applied to either arm.
5. **Arm C's transport is made symmetric with arm T**: stream-json capture, the same
   `ALLOWED_TOOLS`, `acceptEdits`, a fresh scratch working directory outside the repository, and
   `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0`. The only manipulated variable across the two arms is
   the plugin; the control is not denied any tool arm T has.
6. **Plugin isolation (new).** Planner finding F3 measured that the `first-principles` plugin is
   installed and enabled at user scope on the run machine, so an unisolated arm C would silently
   load the very agent it is supposed to be the control for. Every generation and judge call
   therefore passes `--settings` with an inline JSON object setting `enabledPlugins` to `false`
   for both `first-principles@first-principles-skill` and `bm@buildomator` (confirmed, read-only,
   against the exact schema key `~/.claude/settings.json` already uses on this machine).
   Pre-declared fallback if that does not isolate arm C: `--setting-sources project,local`. Every
   attempt aborts if arm C's init event lists a first-principles plugin or the
   `first-principles:first-principles` agent is ever dispatched inside it, or if arm T's init
   event lists any first-principles path other than the repository's own
   `<repo>/first-principles`. Whether v9.13's arm C loaded the installed plugin is
   **undeterminable** — plain `-p` records no init event — and is stated as such, not assumed
   either way.
7. **Judges** use the same `JUDGE_PROMPT` and the same packet-blinding mechanism as v9.13
   (`--permission-mode acceptEdits --allowedTools=Read,Glob,Grep`, the isolation settings, cwd =
   the blinded packet, never `bypassPermissions`). The passive-non-exposure blinding bound
   restated unchanged below.
8. **Format tell — disclosed, not stripped.** Arm T's scored document is the agent's own
   contract-structured delivered file: a `## Answer` block, the six named sections, `GT-` ids,
   and a trailing process-output appendix. That makes arm T identifiable by its format with near
   certainty — a stronger tell than v9.13's registered length/structure confound, because
   v9.13's scored arm-T text was an orchestrator summary carrying none of that structure.
   Therefore a `cleared` result on this run cannot separate reasoning quality from a format or
   halo effect, and any published result must carry that caveat. The non-gating secondary score
   of arm T's orchestrator final message (item 3, less structured) is reported alongside as
   partial context, not part of the threshold. Markers are deliberately not stripped from the
   scored document, because stripping them would change the document the product actually
   delivers — the thing under test, not a proxy for it. The pinned sentence carrying this
   disclosure, present verbatim in the run record and on any cleared card render:

   > The scored arm-T document is identifiable by its format with near certainty, so this
   > result cannot separate reasoning quality from a format or halo effect.

   This limit is carried into §5 (What this run cannot establish) below.

**Blinding, restated from §4 of the superseded document.** Judges receive a packet of exactly
two files — the anonymised analysis and the rubric — outside the repository. Arm labels are
stripped; filenames are opaque shuffled ids; the key is held outside the judge's packet. The bound
on that blinding is *passive non-exposure, not unreachability*: a judge subprocess retains
filesystem access and could in principle locate the key, exactly as the superseded document
disclosed; not tightened here.

## 3. Extraction integrity (superseding the v9.13 fault class)

Every capture is checked before it reaches a judge. In addition to the two v9.13 checks
(rubric-contamination, and a 120-word implausibility floor), an arm-T capture must also carry at
least 4 of the agent's 6 output-contract sections (Problem Essence, Assumptions Table, Ground
Truths, Derivation Chains, Abandoned Reasoning, Conclusion). This closes the exact fault the
erratum names: a 282-699-word orchestrator summary passes the two v9.13 checks but carries none
of the contract, and is now rejected. A control-arm capture is never subject to this fourth
check — the control is unaided and would never carry the contract, so applying it there would
void every control cell and destroy the comparison it protects.

## 4. Sample

- 20 generations (10 prompts × 2 arms × 1 run per cell).
- 40 primary judgings (2 judges × 20 primary documents).
- 20 in-run drift re-judgings (1 per primary document).
- 20 secondary judgings (2 judges × 10 arm-T orchestrator messages, non-gating).
- **Total live invocations: 100** (excludes retries and the two transport-probe calls below).
  The primary 80 are unchanged from v9.13's own count.
- Blinding seed: `20260929`.

## 5. Transport probe (pre-declared, not scored)

Before the registered run: one arm-C isolation probe (a trivial prompt, "Reply with the single
word OK.") and one arm-T slash-form probe on a problem **not** in the catalog, each terminated as
soon as dispatch (or the final result) is observed. Outputs are kept under
`tests/trackb-run-v9.15/probe/`. If either probe fails, the pre-declared fallback in §2 items 1
or 6 is adopted, recorded below as a pre-run amendment, and the constant is updated in the code
before any registered cell runs. No amendment is made after the first registered cell.

## Pre-run amendments

None as of registration.

### Mid-run mechanics correction, 2026-09-30

Not a protocol, sample, threshold or invocation change — nothing decision-relevant in §§1-6
above moves. Recorded here because it is a dated, mechanics-only correction discovered mid-run,
and the log for that is this section, not a silent code edit.

**What happened.** During generation, `TB-01-C` attempt 1 completed as a genuine, complete
answer (`is_error: false`, a non-empty final `result` text, no API error) discussing GraphQL vs
REST trade-offs, including its own prose mention of "rate limiting" concerns. `is_limit_stub()`'s
regex fallback — a tail-of-stdout scan for `usage limit|rate limit` combined with the absence of
`parent_tool_use_id` — misfired on that prose: arm C never carries `parent_tool_use_id` (it has
no subagent thread at all), so the fallback's second guard was trivially satisfied and the
answer's own words tripped the first. The capture was wrongly renamed to
`TB-01-C.a1.limit-stub.jsonl` and the run paused (exit 3) as if a genuine usage limit had been
hit.

**Fix.** `is_limit_stub()` now checks the stream's final `result` event FIRST: if `is_error` is
true or `api_error_status == 429`, it is a stub (the genuine detector, unchanged in substance —
confirmed against the real frozen 429 specimen, `TB-06-T.a1.limit-stub.jsonl`); if `is_error` is
false and `result` is non-empty, it is never a stub, regardless of its wording. The tail-regex
fallback now runs only when no final `result` event exists at all (a genuinely truncated or
killed capture) or one with `is_error` false and an empty `result`. A new self-test control
(`C27`) pins both directions plus a mutation leg (flipping `is_error` on the good fixture must
flip the verdict), so the fix cannot regress silently.

**Disposition of the affected cell.** `TB-01-C` attempt 1 was not re-generated: the existing
capture is a genuine, complete, unaided answer to the byte-identical prompt, and discarding it
in favour of a fresh generation would burn a second live call for no reason and would not make
the record any more honest. It is adopted as `TB-01-C`'s scored attempt 1: the raw capture is
restored to its ordinary name (`TB-01-C.a1.jsonl`, dropping the erroneous `.limit-stub` middle
segment) and `cells.json` records `outcome: "scored"` with a `reclassified_by` note pointing at
this amendment, rather than being silently overwritten as if the misclassification never
happened.

## 6. What this run cannot establish, whatever it returns

Carried from §8 of the superseded document, with one bullet replaced (the invocation described
there no longer applies):

- **Not a general quality claim.** Ten prompts is a spread across four domains, not a domain
  sample.
- **Not a claim about ordinary use.** Arm T is dispatched via the documented slash-launcher form,
  not an undirected prompt. Whether an ordinary user prompt reaches the agent at all is a
  separate, known-unreliable question measured elsewhere.
- **Not a correctness claim.** The rubric scores the quality of the reasoning as presented. It
  does not re-derive the analysis's arithmetic — that was done once, by hand, on six documents
  (`docs/v8.7-correctness-spot-check.md`), and its finding that conformance does not predict
  correctness applies to this rubric too until someone measures otherwise.
- **Not transferable to another model.** The model is pinned; the result is about that model.
- **Not separable from a format/halo effect.** Per §2 item 8, a `cleared` result cannot
  distinguish reasoning quality from arm T's document being identifiable by its own contract
  structure.
