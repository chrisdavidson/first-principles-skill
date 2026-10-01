# agent-router decisions

Every checkpoint the agent-router-fp hooks recorded, from `/home/chrisdavidson/Projects/agent-router/integrations/first-principles/runs/structured-summary-live/state/audit`.
`(main)` = the main session, `(in agent)` = inside first-principles:first-principles.

## Counts per example

| example | checkpoints | Agent (main) -> skipped: own tool | Bash (in agent) -> skipped: does not fit: exact-calc | Bash (in agent) -> skipped: skip pattern | prompt -> skipped: skip pattern |
|---|---|---|---|---|---|
| composed-inversion-second-order | 18 | 1 | 1 | 15 | 1 |
| decompose-irreducibility | 20 | 1 | 1 | 17 | 1 |
| estimate-fermi | 16 | 1 | 2 | 12 | 1 |
| ishikawa-fishbone | 23 | 1 | 1 | 20 | 1 |
| personal-general | 26 | 1 | 9 | 15 | 1 |
| personal-general-2 | 17 | 1 | 4 | 11 | 1 |
| product-business | 24 | 1 | 4 | 18 | 1 |
| product-business-2 | 21 | 1 | 2 | 17 | 1 |
| science-engineering | 34 | 1 | 4 | 28 | 1 |
| science-engineering-2 | 15 | 1 | 1 | 12 | 1 |
| self-application | 44 | 1 | 20 | 22 | 1 |
| software-systems | 18 | 1 | 3 | 13 | 1 |
| software-systems-2 | 16 | 1 |  | 14 | 1 |
| theoretical-limit-carnot | 32 | 1 | 17 | 13 | 1 |
| **total** | **324** | **14** | **69** | **227** | **14** |

## Every checkpoint

### composed-inversion-second-order

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Evaluate this cl…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |

### decompose-irreducibility

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Evaluate this cl…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 4 | Bash (in agent) | skipped |  |  | skip pattern |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |

### estimate-fermi

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Estimate this qu…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |

### ishikawa-fishbone

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Northbrook Analy…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |

### personal-general

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis A software engin…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 8 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 9 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 10 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 11 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 12 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |
| 24 | Bash (in agent) | skipped |  |  | skip pattern |
| 25 | Bash (in agent) | skipped |  |  | skip pattern |
| 26 | Bash (in agent) | skipped |  |  | skip pattern |

### personal-general-2

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis A household hold…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |

### product-business

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Does this B2B Sa…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |
| 24 | Bash (in agent) | skipped |  |  | skip pattern |

### product-business-2

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Given that one e…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |

### science-engineering

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Given a fixed si…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |
| 24 | Bash (in agent) | skipped |  |  | skip pattern |
| 25 | Bash (in agent) | skipped |  |  | skip pattern |
| 26 | Bash (in agent) | skipped |  |  | skip pattern |
| 27 | Bash (in agent) | skipped |  |  | skip pattern |
| 28 | Bash (in agent) | skipped |  |  | skip pattern |
| 29 | Bash (in agent) | skipped |  |  | skip pattern |
| 30 | Bash (in agent) | skipped |  |  | skip pattern |
| 31 | Bash (in agent) | skipped |  |  | skip pattern |
| 32 | Bash (in agent) | skipped |  |  | skip pattern |
| 33 | Bash (in agent) | skipped |  |  | skip pattern |
| 34 | Bash (in agent) | skipped |  |  | skip pattern |

### science-engineering-2

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis A 1.5 MW upwind …” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |

### self-application

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis The single-agent…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 8 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 9 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 10 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 11 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 12 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 13 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 14 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 15 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 16 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 17 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 18 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 19 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 20 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 21 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |
| 24 | Bash (in agent) | skipped |  |  | skip pattern |
| 25 | Bash (in agent) | skipped |  |  | skip pattern |
| 26 | Bash (in agent) | skipped |  |  | skip pattern |
| 27 | Bash (in agent) | skipped |  |  | skip pattern |
| 28 | Bash (in agent) | skipped |  |  | skip pattern |
| 29 | Bash (in agent) | skipped |  |  | skip pattern |
| 30 | Bash (in agent) | skipped |  |  | skip pattern |
| 31 | Bash (in agent) | skipped |  |  | skip pattern |
| 32 | Bash (in agent) | skipped |  |  | skip pattern |
| 33 | Bash (in agent) | skipped |  |  | skip pattern |
| 34 | Bash (in agent) | skipped |  |  | skip pattern |
| 35 | Bash (in agent) | skipped |  |  | skip pattern |
| 36 | Bash (in agent) | skipped |  |  | skip pattern |
| 37 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 38 | Bash (in agent) | skipped |  |  | skip pattern |
| 39 | Bash (in agent) | skipped |  |  | skip pattern |
| 40 | Bash (in agent) | skipped |  |  | skip pattern |
| 41 | Bash (in agent) | skipped |  |  | skip pattern |
| 42 | Bash (in agent) | skipped |  |  | skip pattern |
| 43 | Bash (in agent) | skipped |  |  | skip pattern |
| 44 | Bash (in agent) | skipped |  |  | skip pattern |

### software-systems

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis A 6-year-old e-c…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |
| 17 | Bash (in agent) | skipped |  |  | skip pattern |
| 18 | Bash (in agent) | skipped |  |  | skip pattern |

### software-systems-2

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis A 7-person engin…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | skip pattern |
| 4 | Bash (in agent) | skipped |  |  | skip pattern |
| 5 | Bash (in agent) | skipped |  |  | skip pattern |
| 6 | Bash (in agent) | skipped |  |  | skip pattern |
| 7 | Bash (in agent) | skipped |  |  | skip pattern |
| 8 | Bash (in agent) | skipped |  |  | skip pattern |
| 9 | Bash (in agent) | skipped |  |  | skip pattern |
| 10 | Bash (in agent) | skipped |  |  | skip pattern |
| 11 | Bash (in agent) | skipped |  |  | skip pattern |
| 12 | Bash (in agent) | skipped |  |  | skip pattern |
| 13 | Bash (in agent) | skipped |  |  | skip pattern |
| 14 | Bash (in agent) | skipped |  |  | skip pattern |
| 15 | Bash (in agent) | skipped |  |  | skip pattern |
| 16 | Bash (in agent) | skipped |  |  | skip pattern |

### theoretical-limit-carnot

| # | where | action | entry | p | reason / call |
|---|---|---|---|---|---|
| 1 | prompt | skipped |  |  | skip pattern · “/first-principles:first-principles-analysis Find the law-per…” |
| 2 | Agent (main) | skipped |  |  | own tool |
| 3 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 4 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 5 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 6 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 7 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 8 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 9 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 10 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 11 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 12 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 13 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 14 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 15 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 16 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 17 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 18 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 19 | Bash (in agent) | skipped |  |  | skip pattern |
| 20 | Bash (in agent) | skipped |  |  | skip pattern |
| 21 | Bash (in agent) | skipped |  |  | skip pattern |
| 22 | Bash (in agent) | skipped |  |  | skip pattern |
| 23 | Bash (in agent) | skipped |  |  | skip pattern |
| 24 | Bash (in agent) | skipped |  |  | skip pattern |
| 25 | Bash (in agent) | skipped |  |  | skip pattern |
| 26 | Bash (in agent) | skipped |  |  | does not fit: exact-calc |
| 27 | Bash (in agent) | skipped |  |  | skip pattern |
| 28 | Bash (in agent) | skipped |  |  | skip pattern |
| 29 | Bash (in agent) | skipped |  |  | skip pattern |
| 30 | Bash (in agent) | skipped |  |  | skip pattern |
| 31 | Bash (in agent) | skipped |  |  | skip pattern |
| 32 | Bash (in agent) | skipped |  |  | skip pattern |

