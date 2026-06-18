# Component Diagram

Two Mermaid diagrams at file/script node granularity: the **generation pipeline** and the
**measurement stack**. Each shows what reads what and what generates what. See also the
narrative in [DATA-FLOW.md](DATA-FLOW.md) and the canonical architecture reference in
[ARCHITECTURE.md](ARCHITECTURE.md).

---

## Diagram 1 — Generation pipeline

Source files in `shared/` flow through `scripts/sync-content.py` to produce the committed
`first-principles/` plugin tree, which is then verified by CI and pre-commit gates.
The non-obvious edges are the token-substitution reads: `{{TOOL:slug}}` pulls the
`## Procedure` section from `shared/references/<slug>.md` into the agent body; `{{PROCEDURE:slug}}`
pulls the full body of the same reference file into each focused-mode skill stub.

```mermaid
flowchart LR
    subgraph shared ["shared/ (canonical source — edit here)"]
        BODY["shared/spine/SKILL-body.md\n(contains {{TOOL:slug}} tokens)"]
        META["shared/spine/SKILL.meta.yml\n(agent frontmatter)"]
        TOOLMAP["shared/spine/tool-map.yml\n(slug → inline name map)"]
        REFS["shared/references/&lt;slug&gt;.md\n(eleven companion references)"]
        SKILLS["shared/skills/&lt;slug&gt;/SKILL.md\n(contains {{PROCEDURE:slug}} tokens)"]
    end

    SYNC["scripts/sync-content.py\n(--write regenerates; --check detects drift)"]

    subgraph generated ["first-principles/ (generated — never hand-edit)"]
        AGENT["first-principles/agents/first-principles.md\n(assembled orchestrating agent)"]
        REFS_OUT["first-principles/agents/references/\n(verbatim copies of shared/references/ + spine refs + examples/)"]
        SKILLS_OUT["first-principles/skills/&lt;slug&gt;/SKILL.md\n(generated focused-mode stubs)"]
    end

    subgraph gates ["CI and pre-commit gates"]
        DUAL04["DUAL-04\nsync-content.py --check\n(CI + pre-commit sync-drift gate)"]
        GATE01["GATE-01\ncheck-agent.py\n(agent structural checks)"]
        VAL01["VAL-01\nclaude plugin validate\n(plugin schema validity)"]
        BATT06["BATT-06\ncheck-routing-battery.py --self-test\n(anti-masking sentinels)"]
    end

    REFS -->|"{{TOOL:slug}} → ## Procedure section"| BODY
    REFS -->|"{{PROCEDURE:slug}} → full body"| SKILLS

    SYNC -->|"reads"| META
    SYNC -->|"reads"| BODY
    SYNC -->|"reads"| TOOLMAP
    SYNC -->|"reads"| REFS
    SYNC -->|"reads"| SKILLS

    SYNC -->|"generates"| AGENT
    SYNC -->|"generates"| REFS_OUT
    SYNC -->|"generates"| SKILLS_OUT

    AGENT -->|"reads"| DUAL04
    SKILLS_OUT -->|"reads"| DUAL04
    AGENT -->|"reads"| GATE01
    AGENT -->|"reads"| VAL01
    SKILLS_OUT -->|"reads"| VAL01
    AGENT -->|"reads"| BATT06
```

For the full 13-gate inventory (VAL-01 through TRACE-03 plus the two pre-commit gates) see
[ARCHITECTURE.md#ci-and-pre-commit-gate-inventory](ARCHITECTURE.md#ci-and-pre-commit-gate-inventory).
For the token-substitution mechanics see
[ARCHITECTURE.md#token-substitution](ARCHITECTURE.md#token-substitution).

---

## Diagram 2 — Measurement stack

`scripts/_battery_core.py` is the shared core. The scripts that sit above it exercise
different layers of routing and Step 0 correctness. `check-step0-emulator.py` reads the
phrase-detection table directly from the canonical source — the key cross-subsystem edge
connecting the measurement stack back to `shared/`.

```mermaid
flowchart LR
    SKILLBODY["shared/spine/SKILL-body.md\n(phrase detection rules table)"]

    CORE["scripts/_battery_core.py\n(MIN_HEADER_HITS=2, _COMPOSER_FOCUS_CEILING=4;\nself_test_boundary() — BATT-06 sentinels:\nRR-95-01, RR-95-02, RR-77-08, RR-80-01 emulator layer)"]

    BATT["scripts/check-routing-battery.py\n(BATT-06: merged dual-signal battery;\n--self-test is CI gate)"]
    ROUTING["scripts/check-routing.py\n(DELEGATE/NO-DELEGATE battery;\ndeveloper tool — not in CI)"]

    EMU["scripts/check-step0-emulator.py\n(STEP0-08: offline phrase-detection\nclassifier; --self-test is CI gate)"]
    LIVE["scripts/check-step0-live.py\n(STEP0-06: live MODE classification\nvia bypass channel; --self-test is CI gate)"]

    TRACE["scripts/check-traceability.py\n(TRACE-03: matrix emitter + gate;\n--self-test is CI gate)"]
    MATRIX["docs/requirements-matrix.md\n(generated 206-row capability matrix)"]
    TRACEABILITY["docs/requirements-traceability.md\n(active residuals; 121/85/0/206)"]

    SKILLBODY -->|"reads phrase table"| EMU

    CORE -->|"imports"| BATT
    CORE -->|"imports"| ROUTING

    BATT -->|"self-test (BATT-06)"| CORE
    ROUTING -->|"reads catalog"| BATT

    TRACE -->|"emits"| MATRIX
    TRACE -->|"reads"| TRACEABILITY
```

For residual ownership details (which gate owns which RR-NN residual) see
[MEASUREMENT-MAP.md#residual-ownership](MEASUREMENT-MAP.md#residual-ownership).
For the anti-masking invariants and constant values see
[ARCHITECTURE.md#measurement-subsystem](ARCHITECTURE.md#measurement-subsystem).

---

## See also

- [ARCHITECTURE.md#generation-pipeline](ARCHITECTURE.md#generation-pipeline) — canonical assembly steps narrative
- [ARCHITECTURE.md#measurement-subsystem](ARCHITECTURE.md#measurement-subsystem) — measurement inventory at altitude
- [DATA-FLOW.md](DATA-FLOW.md) — narrative data-flow trace (Stage 1 through Stage 5)
- [MEASUREMENT-MAP.md](MEASUREMENT-MAP.md) — residual-ownership map (gate → RR-NN)
