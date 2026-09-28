# Pre-Registration — Does file handoff deliver the whole analysis?

**Id:** `delivery-fix-3` · **Registered:** 2026-09-28, before any run under this id.
**Chosen by the user** over three alternatives, after v1 and v2 failed.

## 1. Why a file

v1 and v2 both failed for one reason ([v2 §4](delivery-fix-2-preregistration.md)): a long
document the agent writes a second time is **regenerated, not copied** — v2's re-send came back
with sections 20-50% shorter and three missing, after little re-reasoning. So no fix that makes the
agent re-send its document can preserve fidelity. v3 (`0b673878` on branch `delivery-fix`)
removes the second writing: the agent appends its deliverable to
`.first-principles/analysis-<UTC>.md`, **one section per Bash call** — each call its own output
budget, each section written once — and its final message becomes a short pointer that the caller
follows. If the file cannot be written, it falls back to the document as its final message and
says so. `Write` and `Edit` stay disallowed.

## 2. Design

- **Body:** `0b673878`. **Prompts:** `TB-02`, `TB-03`, `TB-04`, `TB-06` — the four whose runs
  lost sections — 3 repeats each, **12 runs**. **Transport and capture:** as `delivery` (empty
  working directory, persistence on, the agent's own transcript kept); after each run the file is
  moved out of the working directory into `raw/<run>.files/`, leaving it empty for the next.
- **Retries:** a routing miss is retried, at most twice.

## 3. Definitions — `tests/delivery-fix-3/run_fix3.py`

- **Complete:** the file carries all 6 contract sections.
- **Verbatim:** the file's text equals the concatenation of the heredoc payloads the agent issued
  (whitespace-normalised) — nothing in the file was written other than as first written.
- **Read:** the main session issued a `Read` (or a `Bash` read) naming the file.
- **Delivered:** complete **and** verbatim **and** read.

## 4. Success rule, fixed now

**Operational** if **every** scored run is *delivered*. **Not operational** if any is not.
Reported, not decided: cut-off events (`stop_reason=max_tokens`) and how each was handled; the
fallback; the pointer message's length; the words the main session received from its read.

## 5. What this cannot establish

- **Twelve runs, four prompts, print mode.** In an interactive session the reader is the same main
  session; whether it then shows the user the whole file is outside this measurement.
- **A file in the working directory is a side effect,** accepted by the user's choice.
- **Verbatim-to-appends is not verbatim-to-intent:** it proves nothing was rewritten between writing
  and delivery, not that each section was complete when first written.

## 6. Amendment 1 — `delivery-fix-3b`, registered mid-run for the runs not yet observed

**What happened.** Of the first 4 scored runs, 3 were *delivered* and `TB-03.r1` was not — on one
criterion only. Its file carried all six sections and the main session read it, but its text did
not equal the concatenated appends, because **the agent revised its own file in place** during its
self-audit: it inserted a missing assumption row (A17) with `sed -i`, rewrote one Conclusion line,
and corrected verdict cells (`Unresolved —` → `Challenge —`) into the prescribed vocabulary. The
file ended longer than the appends (8,349 against 8,082 words). Nothing was regenerated or lost.
§3's *verbatim* was written to catch regeneration, and did not anticipate deliberate revision.

**The v3 verdict stands as registered.** By §4, `TB-03.r1` makes v3 **not operational** under
`delivery-fix-3`, and that is how it is reported. This amendment does not re-score it.

**`delivery-fix-3b`, prospective only.** It scores **only the runs whose result is not yet in
`tests/delivery-fix-3/cells.json` at this amendment's commit** — the four already scored are
excluded (`TB-02.r1`, `TB-02.r2`, `TB-02.r3`, `TB-03.r1`). It replaces *verbatim* with
**provenance**: replay every Bash command the agent issued against the file, in order, on an empty
copy; the result must equal the delivered file byte for byte, so every byte came from the agent's
own recorded writes — appends and in-place edits alike — and nothing entered or left the file any
other way. Replay refuses any command whose verbs are not a listed file-and-text set, and such a
run fails. Tamper controls, run before this amendment: a one-character change, a removed last
section and an appended line each make the replay **not** match.

**Success rule for `delivery-fix-3b`:** every run it scores is complete (6 sections), read by the
main session, and provenance-true; **at least 6** such runs; if fewer than 6 unobserved runs remain
when `delivery-fix-3` ends, the same four prompts are run again until 6 are scored.
