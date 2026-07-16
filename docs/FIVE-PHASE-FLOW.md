# The Five-Phase Flow

This diagram orients; the agent body (`first-principles/agents/first-principles.md`, sourced
from `shared/spine/SKILL-body.md`) is the authoritative spec. For the compact text form of the
same content see [METHODOLOGY-CHEATSHEET.md](METHODOLOGY-CHEATSHEET.md); for the system-level
generation-pipeline and measurement-stack diagrams see [COMPONENT-DIAGRAM.md](COMPONENT-DIAGRAM.md).

Scoped to `docs/` only — placement of this flow inside the agent body itself is byte-freeze,
permanently rejected scope.

```mermaid
flowchart LR
    STEP0["Step 0: Mode selection\n(technique phrase → focused;\notherwise → full-composer)"]

    ESSENCE["Phase 1: Identify Essence\n(Essence Statement)"]
    ASSUMPTIONS["Phase 2: Challenge Assumptions\n(Classified Assumptions Table)"]
    GROUNDTRUTHS["Phase 3: Establish Ground Truths\n(Ground Truths list)"]
    REASON["Phase 4: Reason Upward\n(Derivation Chains)"]
    VALIDATE["Phase 5: Validate\n(Signed-off analysis)"]
    RUBRIC["Validation Rubric gate\n(no conclusions until it clears)"]

    STEP0 --> ESSENCE
    ESSENCE --> ASSUMPTIONS
    ASSUMPTIONS --> GROUNDTRUTHS
    GROUNDTRUTHS --> REASON
    REASON --> VALIDATE
    VALIDATE --> RUBRIC

    subgraph techniques ["Companion techniques"]
        FISHBONE["Fishbone"]
        INVERSION["Inversion"]
        FIVEWHYS["Five Whys"]
        TRADEOFF["Trade-off"]
        SECONDORDER["Second-Order"]
        ESTIMATE["Estimate"]
        THEORETICALLIMIT["Theoretical Limit"]
        PREMORTEM["Pre-mortem"]
    end

    FISHBONE -->|"untested-belief rows"| ASSUMPTIONS
    INVERSION -->|"unverified preconditions"| ASSUMPTIONS
    FIVEWHYS -->|"causal root causes /\nreduced primitives"| GROUNDTRUTHS
    TRADEOFF -->|"derivation-chain step"| REASON
    SECONDORDER -->|"derivation-chain step"| REASON
    ESTIMATE -->|"derivation-chain step"| REASON
    THEORETICALLIMIT -->|"derivation-chain step"| REASON
    PREMORTEM -->|"weak-link flags"| VALIDATE

    REASON -.->|"second-order-contradiction rule:\nan extension step contradicting\na Ground Truth returns to Phase 2"| ASSUMPTIONS
```

## Legend

- **Solid edges** are hand-offs: a phase's named artifact becomes the entry condition for the
  next phase, or a companion technique's output feeds into the phase artifact it attaches to
  (e.g. Fishbone and Inversion feed rows into the Classified Assumptions Table).
- **The dotted edge** (Phase 4 → Phase 2) is the route-back: if a second-order extension step
  contradicts a Ground Truth, the conclusion returns to Phase 2 for re-challenging rather than
  proceeding to Phase 5 on a false premise.
- **The terminal rubric node** is a gate, not a hand-off: the Validation Rubric
  (`references/validation-rubric.md`) must clear before conclusions are presented — validate,
  fix, and repeat until every criterion passes.
