# Scratch demo catalog — one row

One-row scratch catalog for a `--probe` demonstration run. Not a committed fixture.

| ID | Prompt | Notes |
|---|---|---|
| DEMO-TRIAGE | Our support organization runs an LLM ticket-triage job over 1.2 million tickets a month. Today every ticket goes through a single Claude Opus call averaging 2,400 input tokens and 600 output tokens, and our finance lead says the line item is now the second-largest thing in the platform budget. Our staff engineer wants to move to Claude Haiku and issue three independent calls per ticket, taking the majority answer, arguing that three cheap votes will come out both cheaper and more accurate than one expensive call because self-consistency voting recovers most of the gap between model tiers. We measured Opus at 94 percent agreement with human triagers on a 500-ticket sample; we have never measured Haiku. The migration needs one engineer for three weeks, and a mis-triaged ticket lands in the wrong queue and adds about 9 hours to first response. Should we make the switch? | Demonstration scenario. Contains one externally verifiable class of fact (published per-token model pricing), one embedded false premise (majority voting "recovers most of the gap"), and one unmeasured quantity the decision depends on (Haiku accuracy). Carries no Step 0 technique trigger phrase. |
