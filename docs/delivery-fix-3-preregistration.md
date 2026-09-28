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
