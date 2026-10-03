**Disclosed:** Missing inputs, analysis run best-effort: (1) whether the product is a medical device (inside the CSA guidance's scope) or drug/biologic; (2) whether your software-validation SOP already permits risk-based assurance; (3) how much scripted testing remains unexecuted and how much of it is high process risk. These are carried as GT-13?, GT-9? and GT-10?. Re-entry edge fired: the Self-Audit Gate's Fix/Repeat loop. Trigger: Criterion 3 scored Hand-wavy, and Criteria 1 and 4 scored Sound, on the first pass. What changed: the success criteria were rewritten, GT-4 was added to C1, and chain C8 was added.

## Answer

**Recommendation:** Do not switch the whole project now. Finish under the approved CSV plan by default. Move only the unexecuted remainder to CSA, at a documented boundary, when three things hold: the SOP permits it, the plan is amended first, and your own counts show a net saving (chain C5).

**Band (from §6):** MEDIUM (chain C5).

**Would change it:** Read your validation SOP and plan (chain C3). Risk-classify the remaining tests and count their effort (chain C4). Confirm the system is device production/QMS software (chain C7).

## 1. Problem Essence

**Core problem:** For the validation work on this in-flight project that has not yet been executed, which assurance method — finishing under the current scripted CSV plan, switching to the FDA's risk-based Computer Software Assurance (CSA) approach, or splitting at a defined boundary — produces evidence of fitness for intended use that is consistent with the firm's own approved procedures and defensible at inspection, at the lowest total risk and effort?

What triggered the analysis ("the team wants the new way; I think it is a bad move") is not the question. The question is not "is CSA good or bad" either: it is whether *changing method part-way through one project* costs or risks more than it saves, and under which conditions that flips.

**Success criteria:**

- The Conclusion names one default course of action for the unexecuted remainder of this project.
- The Conclusion states the conditions under which that default flips, each as a fact the user can check in their own documents or counts.
- The Conclusion states whether validation evidence already executed must be redone under each option.
- The Conclusion requires every CSA activity it permits to run under an approved, effective procedure and plan.
- The Conclusion points to a register of risks covering every option considered — including the status quo and a split — with a control per risk.
- The Conclusion may recommend a split or a conditional combination of methods; it is not required to pick "old way" or "new way".

## 2. Assumptions Table

Labels A-1 to A-19 are positional (row order) and are what the `[Assumes: A-N]` marks in section 4 refer to. Rows A-15 to A-19 were surfaced by the end-of-phase Assumption Audit (appendix).

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: The FDA requires scripted, step-by-step CSV test protocols for production and quality-system software | convention | Challenge before use | Discard — the regulation requires validation proportionate to risk; the guidance is nonbinding and permits alternative approaches (GT-1, GT-3) | FDA CSA guidance (Feb 2026), header and §V.A, read at source |
| A-2: CSA is a lower compliance bar ("less validation") | untested belief | Verify or flag | Discard — the requirement is unchanged; CSA changes the evidence method and record content, not the obligation (GT-3, GT-7) | CSA guidance §V.A.6, read at source |
| A-3: Switching mid-flight invalidates scripted tests already executed | untested belief | Verify or flag | Discard — scripted testing is itself a CSA assurance activity and the recommended rigor for high process risk (GT-6) | CSA guidance §V.A.4, read at source |
| A-4: The firm's current SOPs and the approved validation plan prescribe scripted CSV and do not yet permit CSA methods | current constraint | Record expiry conditions | Challenge — load-bearing; expires when the software-validation SOP is revised to permit risk-based assurance and the project plan is amended under change control | unverified — flagged (GT-9?) |
| A-5: The system is production or quality-management-system software for medical devices (inside CSA guidance scope) | untested belief | Verify or flag | Challenge — if the firm is drug/biologic (21 CFR 211) or the software is a device software function, the CSA guidance does not directly apply (GT-2) | unverified — flagged (GT-13?) |
| A-6: FDA investigators will treat CSA-style records (unscripted testing, digital evidence) with suspicion | untested belief | Verify or flag | Challenge — undercut by the guidance being final and aligned to the QMSR (GT-1, GT-4); individual investigator practice is not verifiable here | unverified — flagged; no chain rests on it |
| A-7: The team is trained and competent in process-risk determination and unscripted testing | untested belief | Verify or flag | Challenge — the switch's execution risk rests on it | unverified — flagged; priced as a trade-off score |
| A-8: Switching would save meaningful effort on the remaining scope | untested belief | Verify or flag | Challenge — true only in proportion to the remaining scope that is not high process risk (GT-5, GT-10?) | unverified — flagged (GT-10?) |
| A-9: A validation package mixing scripted and unscripted methods is inherently non-compliant | convention | Challenge before use | Discard — the guidance names a hybrid of scripted and unscripted testing and lets the method be chosen per feature (GT-6) | CSA guidance §V.A.4, read at source |
| A-10: The QMSR/ISO 13485 requires a documented procedure for validating QMS software, which the firm must follow | current constraint | Record expiry conditions | Accept — expires only with a regulation change; until then deviating from one's own validation procedure is a nonconformance regardless of method | ISO 13485 text not opened — flagged (GT-11?) |
| A-11: A change of validation method mid-project must go through a plan amendment under document/change control | convention | Challenge before use | Accept — survives challenge: it follows from A-10 and from the record needing an approved conclusion (GT-7) | derived from GT-7 and GT-11? |
| A-12: Part 11 applies to electronic validation evidence | current constraint | Record expiry conditions | Accept — expires only with a regulation change; Part 11 generally applies to records needed to evidence validation, and validation enforcement discretion does not cover QMS software validation (GT-8) | CSA guidance §V.B, read at source |
| A-13: The user's position — "switching is a bad move" — is correct as stated | untested belief | Verify or flag | Challenge — it is the subject of the analysis; section 4 shows it is conditionally right (C5) | tested in C5 |
| A-14: Supporting software (tools not directly used in production/QMS) can be assured by vendor records and installation/configuration evidence | current constraint | Record expiry conditions | Accept — current FDA recommendation; expires if the guidance is superseded (GT-12) | CSA guidance §V.A.5, read at source |
| A-15: The executed CSV package already holds requirement-to-test traceability, so a retrospective risk determination can be mapped onto it | untested belief | Verify or flag | Challenge — if absent, the bridging document must build it; the endpoint of C2 survives either way | unverified — surfaced by the Assumption Audit |
| A-16: Unscripted testing reduces execution-plus-documentation effort on a not-high-risk feature by roughly 50–80% versus a full scripted protocol | untested belief | Verify or flag | Challenge — an estimate, not a measurement; used only to bracket C4 | unverified — surfaced by the Assumption Audit |
| A-17: The one-off cost of a mid-flight switch (plan amendment, retrospective risk assessment, training, SOP update if needed) is roughly 10–40 person-days | untested belief | Verify or flag | Challenge — an estimate; used only to bracket C4 | unverified — surfaced by the Assumption Audit |
| A-18: Changes made to the system after go-live are assured under whichever validation procedure is effective at the time of the change | convention | Challenge before use | Accept — follows from change control under the effective procedure and the guidance's treatment of changes across the life cycle (GT-1) | CSA guidance §III, read at source |
| A-19: The firm will revise its software-validation SOP to QMSR/ISO 13485 terms in any case, independent of this project | untested belief | Verify or flag | Challenge — plausible because the QMSR has applied since February 2026 (GT-4) but not verified for this firm; if the SOP is already revised, C3's gate is already open | unverified — surfaced by the Assumption Audit |
## 3. Ground Truths

- **GT-1** The FDA's CSA guidance is final (February 2026, superseding the final version of September 24, 2025), contains nonbinding recommendations, and states "You can use an alternative approach if it satisfies the requirements of the applicable statutes and regulations"; it applies the risk-based approach of the existing Software Validation guidance, which covers managing changes across the life cycle — source: FDA, *Computer Software Assurance for Production and Quality Management System Software* (fda.gov guidance page and PDF media/188844); read-at-source: guidance page issue date and "supersedes" statement; PDF header (nonbinding statement) and §III Scope. Published regulatory text.
- **GT-2** The guidance's scope is computers or automated data processing systems used as part of production or the quality management system for medical devices; it "does not provide recommendations for the design and development verification or validation requirements for device software functions" — source: CSA guidance; read-at-source: §III Scope. Published regulatory text.
- **GT-3** Under ISO 13485 subclauses 4.1.6, 7.5.6 and 7.6 as incorporated by the QMSR, "the specific approach and activities associated with software validation and revalidation are required to be proportionate to the risk associated with the use of the software" — source: CSA guidance; read-at-source: §V.A.1, paragraph beginning "As described in Subclauses 4.1.6, 7.5.6, and 7.6". Published regulatory text (the standard itself was not opened; the guidance's statement of it was).
- **GT-4** The QMSR took effect February 2, 2026 and incorporates ISO 13485:2016 by reference; FDA discontinued the QSIT inspection technique on that date and now inspects under Compliance Program 7382.850 — source: FDA QMSR web page; read-at-source: "The rule is effective February 2, 2026…" and the QSIT discontinuation paragraph. Published regulatory text.
- **GT-5** A software feature, function or operation is "high process risk" when its failure to perform as intended may result in a quality problem that foreseeably compromises safety; CAPA routing, complaint tracking, change-control and procedure-management automation and data-management functions are given as generally not high process risk — source: CSA guidance; read-at-source: §V.A.2. Published regulatory text.
- **GT-6** For high process risk features the guidance points to scripted testing or a hybrid of scripted and unscripted testing; for not-high-risk features, unscripted methods (scenario, error-guessing, exploratory); and it says these are "not exclusive to those categories" — source: CSA guidance; read-at-source: §V.A.4, paragraph beginning "In general, FDA recommends that manufacturers apply principles of risk-based testing". Published regulatory text.
- **GT-7** FDA recommends the record include the intended use, the result of the risk-based analysis, a description of testing, issues found, a conclusion statement of acceptability, who performed it and when, and review/approval when appropriate; documentation "need not include more evidence than necessary" — source: CSA guidance; read-at-source: §V.A.6 "Establishing the Appropriate Record". Published regulatory text.
- **GT-8** Part 11 generally applies to electronic records needed to evidence required validation, and Part 11 validation enforcement discretion "expressly does not apply" to validation of production/QMS software under ISO 13485 — source: CSA guidance; read-at-source: §V.B. Published regulatory text.
- **GT-9?** The firm's current software-validation SOP and the project's approved validation plan prescribe scripted CSV and do not yet permit CSA methods — unverified: a fact about the user's quality system, not stated in the request.
- **GT-10?** The fraction of the project's remaining, unexecuted test scope that is not high process risk — unverified: depends on the system and its intended uses, not stated in the request.
- **GT-11?** ISO 13485:2016 subclause 4.1.6 requires the organization to document procedures for validating the application of computer software used in the QMS — unverified: the standard is a paid document and was not opened; GT-3 confirms the subclause's risk-proportionality, not its wording on documented procedures.
- **GT-12** Supporting software can often be assured by leveraging vendor evaluation and validation records, installation or configuration, "such that additional assurance activities (e.g., scripted or unscripted testing) may be unnecessary" — source: CSA guidance; read-at-source: §V.A.5. Published regulatory text.
- **GT-13?** The project's system is medical-device production/QMS software (inside GT-2's scope) rather than drug/biologic GMP software or a device software function — unverified: the request says only "regulated by the FDA".

**Provenance summary:**

```text
?-marked: GT-9?, GT-10?, GT-11?, GT-13? (4 of 13)
Read-at-source: GT-1 — FDA guidance page + PDF header and §III; GT-2 — §III; GT-3 — §V.A.1; GT-4 — FDA QMSR page; GT-5 — §V.A.2; GT-6 — §V.A.4; GT-7 — §V.A.6; GT-8 — §V.B; GT-12 — §V.A.5
```

Phase 3 failure record: GT-11? — ISO 13485:2016 not opened: paywalled standard; the CSA guidance quotes its risk-proportionality requirement (GT-3) but not its documented-procedure wording. GT-9?, GT-10?, GT-13? cite no external source; they are facts about the user's own system and quality system, and only the user can supply them.
## 4. Derivation Chains

### Conclusion C1: CSV and CSA are two evidence methods for one unchanged obligation

GT-1 (alternative approaches permitted, guidance nonbinding) + GT-3 (validation must be proportionate to risk) + GT-4 (QMSR in force, incorporating ISO 13485) + GT-7 (what the record must show)
→ the regulation fixes the outcome — risk-proportionate evidence that the software is fit for its intended use — and leaves the test method open
→ scripted CSV and risk-based CSA are two ways of producing that one required evidence
→ choosing between them on this project is a decision about execution risk and effort, not about the level of compliance

**Pre-check:** head GT-1, GT-3, GT-4, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input is read at source (CSA guidance header, §III, §V.A.1, §V.A.6; FDA QMSR page); each hop is a deduction from the line above; the rival "CSA is a lower compliance bar" is ruled out by GT-3 and GT-7 in section 5, Dead End 1 (chain C1).

### Conclusion C2: Evidence already executed carries over; a switch needs a mapping, not re-execution

GT-6 (scripted testing is a CSA method, hybrids named) + GT-7 (record contents) + C1 (HIGH, method open)
→ an executed, approved scripted protocol already supplies the testing description, issues, conclusion, performer and date that the CSA record asks for
→ the one CSA record element it may lack is an explicit per-feature process-risk determination *[Assumes: A-15]*
→ a switch therefore requires a retrospective risk-determination mapping onto executed tests, not their re-execution

**Pre-check:** head GT-6, GT-7, C1 (HIGH) · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** HIGH — A-15 is priced: if the executed package lacks requirement-to-test traceability, the mapping document must build it, which raises the one-off switch cost B used in C4 but still requires no re-execution, so the endpoint stands; the rival "a package must use one method throughout" is ruled out by GT-6 in section 5, Dead End 2.

### Conclusion C3: No CSA activity may run until the firm's own procedure and plan permit it

GT-11? (ISO 13485 requires a documented software-validation procedure) + GT-9? (current SOP and plan prescribe scripted CSV) + GT-7 (record needs an approved conclusion)
→ an assurance activity performed by a method the effective SOP and approved plan do not permit is a deviation from the firm's own procedure
→ that deviation is a nonconformance regardless of whether FDA would accept the method itself
→ a switch is admissible only once the SOP permits risk-based assurance and the plan is amended under change control, before the first CSA activity is executed

**Pre-check:** head GT-11?, GT-9?, GT-7 · ?-marked: GT-11?, GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-11? is removed as a cause by reading ISO 13485:2016 subclause 4.1.6; GT-9? is removed by reading the firm's current software-validation SOP and the project's approved validation plan. If the SOP already permits risk-based assurance, the gate reduces to a plan amendment. The rival "FDA endorses CSA, so the team may start now" is ruled out in section 5, Dead End 3.

### Conclusion C4: A switch pays back only when R × f × r exceeds the one-off switch cost B

GT-5 (definition of high process risk) + GT-6 (high-risk features keep scripted or hybrid rigor) + GT-10? (share of remaining scope that is not high risk)
→ any effort saving from switching accrues only on remaining, unexecuted features that are not high process risk
→ net saving equals R × f × r minus B, with R the remaining scripted effort in person-days, f the not-high share, r the per-feature effort reduction and B the one-off switch cost
→ illustrative bracket: at f = 0.5 and r = 0.65, breakeven R is B ÷ 0.325, about 31 to 123 person-days for B between 10 and 40 *[Assumes: A-16, A-17]*
→ at the conservative end (f = 0.3, r = 0.5) breakeven R is about 67 to 267 person-days
→ at the aggressive end (f = 0.8, r = 0.8) breakeven R is about 16 to 63 person-days
→ a remaining scripted effort under about 16 person-days cannot pay back a switch at any bracketed value
→ the decision rule is to measure R, f and B on this project and switch the remainder only if R × f × r exceeds B

**Pre-check:** head GT-5, GT-6, GT-10? · ?-marked: GT-10? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-10? is removed by classifying every remaining unexecuted test case as high or not high process risk under GT-5's definition. A-16 and A-17 are priced: they set only the illustrative bracket; if either is wrong the bracket moves but the endpoint — measure R, f and B and compare — stands. Rival "a fixed breakeven number can be stated" is abandoned in section 5, Dead End 6.

### Conclusion C5: Finish under the approved CSV plan by default; switch the remainder at a documented boundary only when C3's gate is open and C4's rule shows a net saving

GT-1 (method open) + GT-6 (hybrids named) + GT-9? (SOP state) + GT-10? (not-high share) + C2 (HIGH, evidence carries over) + C3 (MEDIUM, procedure gate)
→ must-have knock-out: any option that executes CSA activities before C3's gate is open is not viable, so the switching options are viable only conditionally
→ weighted totals with weights locked before scoring: O1 finish under CSV = 78, O3 boundary switch = 78, O4 pause-then-switch = 67, O2 immediate full re-plan = 53
→ the exact tie resolves to O1 because O3's decisive effort score rests on GT-10? and O1's scores rest on read ground truths
→ the flip test shows a ±1 change on any of five criteria moves the winner to O3, so the generic comparison is a near-tie that only project facts can break
→ finish under CSV unless the gate in C3 is open and C4's rule shows a net saving, in which case switch only the unexecuted remainder at a documented boundary

**Pre-check:** head GT-1, GT-6, GT-9?, GT-10?, C2 (HIGH), C3 (MEDIUM) · ?-marked: GT-9?, GT-10? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-9? (read the SOP and plan) and GT-10? (risk-classify the remaining tests); C3 is MEDIUM. The near-tie between O1 and O3 is not a live rival: the endpoint states the observation that selects between them. O2 and O4 are ruled out in section 5, Dead Ends 4 and 5. Full matrix, anchors and flip test are in the appendix.

### Conclusion C6: Finishing under CSV defers this system's CSA benefit rather than forfeiting it

C5 (MEDIUM, default recommendation) + GT-1 (risk-based approach covers changes across the life cycle) + GT-4 (QMSR in force, new inspection program)
→[2nd] time lens: after go-live every change is assured under the procedure then effective, so a system finished under CSV moves to CSA at its first change *[Assumes: A-18]*
→[2nd] time lens: the CSA saving forgone by O1 is bounded to the remaining pre-go-live scope
→[2nd] actor lens: a team overruled on method may execute the remaining scripts as box-ticking, degrading the very evidence O1 is chosen to protect
→[2nd] actor lens: managers told CSA saves money will read O1 as resistance unless the deferral and C4's rule are shown to them
→[2nd] actor lens: investigators now inspect against the QMSR, which incorporates ISO 13485's risk-proportionate validation
→[3rd] the firm's SOP revision is therefore a QMSR-driven task, so its cost belongs outside B in C4's comparison *[Assumes: A-19]*

**Pre-check:** head C5 (MEDIUM), GT-1, GT-4 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C5 (MEDIUM). The rival "O1 locks the system into CSV for life" is ruled out in section 5, Dead End 7. A-18 is priced: if post-go-live changes stayed under CSV, the deferral claim weakens but the endpoint about SOP cost does not depend on it. A-19 is priced: if the SOP is already revised, C3's gate is already open and B is smaller still, so the endpoint stands. The box-ticking effect works against success criterion 1 (record quality) and is carried as a risk (R9) in C7. No effect contradicts a ground truth.

### Conclusion C7: The risks of the transition are execution risks with known controls, concentrated in five failure classes

C1 (HIGH, obligation unchanged) + C2 (HIGH, evidence carries over) + C3 (MEDIUM, procedure gate) + GT-5 (risk definition) + GT-8 (Part 11 on evidence) + GT-13? (system inside CSA scope)
→ because the obligation is unchanged and executed evidence carries over, the transition does not raise regulatory-level risk from CSA itself
→ the risks concentrate in procedure/plan mismatch, process-risk misclassification, thin records, uncontrolled digital evidence and scope misapplication
→ each has a named control in the register below, so a switch made through the gate is a manageable change rather than a compliance gamble

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), GT-5, GT-8, GT-13? · ?-marked: GT-13? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: C3 is MEDIUM, and GT-13? is removed by confirming the system is medical-device production or QMS software and not drug/biologic GMP software or a device software function. Rival "the switch is a compliance gamble" is ruled out by C1 and C2 (section 5, Dead End 1).

### Conclusion C8: Under CSA the remaining work's rigor is re-allocated toward safety-relevant features, never removed from them

GT-2 (scope: production/QMS software, not device software functions) + GT-5 (high process risk definition) + GT-8 (Part 11 applies to validation evidence) + GT-12 (supporting software via vendor and configuration evidence)
→ inside the guidance's scope, the rigor a remaining feature needs is set by whether its failure could foreseeably compromise safety
→ that rigor has a floor wherever electronic evidence is relied on, because Part 11 controls apply to it
→ effort can fall only on not-high-risk and supporting features, where vendor and configuration evidence may replace testing
→ a CSA remainder re-allocates effort from low-risk and supporting features toward safety-relevant ones under a fixed evidence-integrity floor

**Pre-check:** head GT-2, GT-5, GT-8, GT-12 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input is read at source (CSA guidance §III, §V.A.2, §V.B, §V.A.5); each hop is a deduction from the line above; the rival "CSA reduces rigor across the board" is ruled out by GT-5 and GT-8 in section 5, Dead End 1. Whether this system is inside the guidance's scope at all is GT-13?, carried on C7, not an input here: C8 states what holds inside the scope (chain C8).

**Risk register (supports C7) — every option's risks, with controls** (O1 finish under CSV; O2 immediate full switch with re-plan; O3 boundary switch of the unexecuted remainder; O4 pause, revise, then switch):

| # | Risk | Options exposed | Basis | Control |
|---|------|-----------------|-------|---------|
| R1 | CSA activities executed before the SOP and plan permit them — a self-inflicted procedural nonconformance | O2 high; O3, O4 only if the gate is skipped | C3 | SOP permits risk-based assurance and plan amendment approved before the first CSA activity |
| R2 | A safety-relevant feature misclassified as not high process risk and tested only unscripted | O2, O3, O4 | GT-5, GT-6 | Documented per-feature risk determination with QA approval; when uncertain, classify high |
| R3 | Unscripted-test records missing intended use, risk result, issues or conclusion | O2, O3, O4 | GT-7 | Record template carrying every GT-7 element; reviewer checks against it |
| R4 | System logs, audit trails or screenshots used as evidence without Part 11 controls | All options using digital evidence | GT-8 | Confirm the evidence-holding system's Part 11 controls before relying on it |
| R5 | CSA guidance applied outside its scope (drug/biologic GMP software, or device software functions) | O2, O3, O4 | GT-2, GT-13? | Confirm scope first; outside it, follow the procedures that apply to that product type |
| R6 | A two-method package with no stated boundary or rationale reads as incoherent at inspection | O3 | C2, GT-7 | Plan amendment naming the boundary, the reason, and the risk mapping onto executed tests |
| R7 | Executed scripted evidence re-documented or re-run needlessly | O2 | C2 | Keep it; map it |
| R8 | Re-planning, training and SOP work delay go-live | O2, O4 high; O3 medium | C4, C5 | Switch only where C4's rule shows a net saving |
| R9 | Team overruled on method executes the remaining scripts as box-ticking | O1 | C6 | Explain the deferral; make post-go-live changes the team's first CSA work |
| R10 | An untrained team performs unscripted testing poorly | O2, O3, O4 | A-7 | Training and an experienced reviewer; start on not-high-risk features |
| R11 | Management books savings that do not materialise on a mostly high-risk remainder | O2, O3 | C4 | Show R, f and B before committing |
| R12 | Supporting software over-tested when vendor records would suffice | All, once the SOP permits it | GT-12 | Leverage vendor evaluation and installation/configuration evidence |
## 5. Abandoned Reasoning

### Dead End: 1 — "CSA is a lower compliance bar, so switching lowers our compliance"

**What was tried:** Treating the choice as old-strict versus new-lenient, so that switching trades compliance for speed.

**Why abandoned:** Contradicted by GT-3 (validation proportionate to risk is required either way) and GT-7 (CSA still expects intended use, risk result, testing description, issues, an approved conclusion, performer and date). The obligation does not move; only the method does (C1). GT-5 and GT-8 also show that rigor is redistributed by process risk under a fixed Part 11 evidence floor, not lowered (C8).

**What it ruled out:** Arguing against the switch on the grounds that CSA is "less validation", and arguing for it on the grounds that it is "less work across the board". Both misread the guidance.

### Dead End: 2 — "A validation package must use one method throughout, so a mid-flight switch means redoing what is done"

**What was tried:** Assuming method consistency is required inside one package, which would make the executed scripted work sunk cost.

**Why abandoned:** GT-6 names a hybrid of scripted and unscripted testing and lets the method be chosen per feature; scripted testing is itself a CSA method. C2 shows executed tests need a risk mapping, not re-execution.

**What it ruled out:** Treating executed work as lost under a switch, and treating a two-method package as inherently non-compliant (it needs a stated boundary — R6 — not uniformity).

### Dead End: 3 — "FDA has endorsed CSA, so the team can start working the new way now"

**What was tried:** Reading the final guidance as permission that overrides the firm's current procedure and approved plan.

**Why abandoned:** GT-1 shows the guidance is nonbinding; it permits an approach, it does not amend the firm's SOP. Executing outside one's own approved procedure is a nonconformance whatever the method's merits (C3).

**What it ruled out:** Any switch that begins before the SOP permits risk-based assurance and the plan is amended (risk R1).

### Dead End: 4 — Option O2 — switch everything now and re-plan the whole package to CSA

**What was tried:** Scoring an immediate, complete switch, including re-documenting executed work in CSA form.

**Why abandoned:** Lowest weighted total (53 against 78 for O1 and O3) in C5's trade-off; it pays re-planning cost on work C2 shows already carries over, and it fails C3's must-have unless the SOP is already revised.

**What it ruled out:** The "go fully to the new way now" reading of the team's proposal.

### Dead End: 5 — Option O4 — pause execution, revise the SOP, train, then switch

**What was tried:** Stopping the project until the quality system and team are ready, then running O3.

**Why abandoned:** 67 against 78 in C5; it adds O3's switching cost plus a schedule stop, without evidence advantage over O3, because O3 already requires the gate to be open before any CSA activity.

**What it ruled out:** Halting the in-flight project as a way to "do the transition properly".

### Dead End: 6 — Stating one breakeven number for when a switch pays

**What was tried:** Computing a single person-day threshold above which switching is worth it.

**Why abandoned:** The threshold depends on GT-10? (the not-high-risk share of remaining work) and on two estimates (A-16, A-17) that only the project can measure; the bracket spans about 16 to 267 person-days (C4).

**What it ruled out:** Quoting a generic threshold. C4 keeps the rule (compare R × f × r with B) and leaves the numbers to the project's own counts.
### Dead End: 7 — "Finishing under CSV locks this system into the old way for its whole life"

**What was tried:** Treating O1 as forfeiting CSA's benefit for this system permanently, which would weigh against it.

**Why abandoned:** GT-1 places changes across the life cycle under the risk-based approach, and A-18 records that post-go-live changes are assured under the procedure then effective; C6 shows the benefit is deferred to the first change, not lost.

**What it ruled out:** Counting the whole future maintenance saving of CSA against O1; only the pre-go-live remainder is at stake.

## 6. Conclusion

**Recommended approach:** Do not switch the whole in-flight project now; finish it under its approved CSV plan by default, and move only the unexecuted remainder to CSA, at a documented boundary, if the firm's SOP already permits risk-based assurance, the plan is amended before any CSA activity, and the project's own counts show R × f × r exceeding the switch cost B (chain C5).

**Key insight:** CSV and CSA are two methods for one unchanged obligation, so the danger is not CSA itself but changing method mid-stream outside your own approved procedure (chain C1). Your objection is right about an uncontrolled switch and wrong if it rests on CSA being riskier or weaker (chain C3).

**Trade-offs acknowledged:** Finishing under CSV gives up savings on not-high-risk remaining features, but defers them rather than forfeiting them: the system moves to CSA at its first post-go-live change, and the SOP revision is a QMSR-driven task anyway (chain C6). The default is a near-tie that a ±1 weight change flips, so the project facts below decide it (chain C5).

**What decides it, and what holds either way:**

- Confirm the system is medical-device production or quality-system software, inside the CSA guidance's scope (chain C7).
- Read the current software-validation SOP and approved plan to see whether risk-based assurance is permitted (chain C3).
- Classify every remaining unexecuted test case as high or not high process risk, and count its scripted effort (chain C4).
- Executed scripted evidence is kept and mapped to a risk determination, never re-run because of a switch (chain C2).
- If the remainder does move to CSA, its rigor shifts toward safety-relevant features under a Part 11 evidence floor rather than falling everywhere (chain C8).
- Whichever option is chosen, the twelve risks in C7's register each carry a named control (chain C7).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM), C8 (HIGH) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C3, C4, C5, C6 and C7 are rated MEDIUM; the decision turns on the firm's SOP state, the not-high-risk share of remaining work and the system's scope, carried in those chains, and establishing those three facts would remove them as causes of the downgrade (chain C5).
## Appendix — process output

## Trade-off procedure output (process output)

## Options

- **O1 — status quo:** finish all remaining work under the approved CSV plan; adopt CSA for new projects and for this system's post-go-live changes.
- **O2 — immediate full switch:** start working the CSA way now on all remaining work and re-plan the whole package, including re-documenting executed work, in CSA form.
- **O3 — composite boundary switch:** keep executed evidence; once the SOP permits it, amend the plan, risk-classify remaining features, keep high-risk ones scripted or hybrid, test not-high ones unscripted, and map a retrospective risk determination onto executed tests (C2).
- **O4 — pause-then-switch:** halt execution until the SOP is revised and the team trained, then run O3.

Must-have M1 (C3): no CSA activity is executed before the SOP permits it and the plan is amended. O2, O3 and O4 are viable only conditionally on M1; O1 is always viable. Scoring below assumes M1 can be met; if it cannot before the remaining work is due, O2–O4 are knocked out and O1 wins by default.

## Criteria & Weights

Locked before scoring. Higher is always better.

| Criterion | Weight | 1 means | 5 means |
|---|---|---|---|
| Inspection defensibility / package coherence | 5 | method changed with no approved rationale; records incomplete | one approved plan governs every activity; every GT-7 record element present |
| Schedule to go-live | 4 | adds a stop or re-plan of more than a month | no added planning or training lead time |
| Remaining effort | 3 | re-work of executed tests plus full scripted remainder | only the minimum risk-proportionate effort on what remains |
| Execution risk (low risk scores high) | 4 | team executes an untrained method on safety-relevant features | team executes a method it has run before under existing templates |
| Organisational learning / future value | 2 | no CSA capability built | CSA procedure, templates and experience in place after the project |
| Defect-finding effectiveness on remaining scope | 3 | tests confined to pre-written steps on all features | exploratory/scenario testing applied where failures are likely, scripted where risk demands |

## Scoring

| Option | Defensibility ×5 | Schedule ×4 | Effort ×3 | Execution ×4 | Learning ×2 | Defect-finding ×3 | Total |
|---|---|---|---|---|---|---|---|
| O1 | 5 = 25 (GT-1, GT-7) | 4 = 16 (no re-plan) | 2 = 6 (full scripted remainder) | 5 = 20 (known method) | 1 = 2 | 3 = 9 (GT-6) | **78** |
| O2 | 3 = 15 (R6, R7) | 1 = 4 | 2 = 6 (C2: re-work offsets saving) | 2 = 8 (A-7) | 4 = 8 | 4 = 12 (GT-6) | **53** |
| O3 | 4 = 20 (GT-6, C2, needs R6 control) | 3 = 12 (amendment, mapping, training) | 4 = 12 (GT-10?) | 3 = 12 (A-7) | 5 = 10 | 4 = 12 (GT-6) | **78** |
| O4 | 4 = 20 | 1 = 4 (stop) | 3 = 9 (GT-10?) | 3 = 12 | 5 = 10 | 4 = 12 | **67** |

Execution and learning scores are preferences informed by A-7, not ground truths; they are marked as such.

## Recommendation

O1 and O3 tie at 78. Deterministic tiebreak: O3's decisive effort score rests on GT-10?, O1's on read ground truths, so O1 is the default. **Flip test:** the smallest change that flips the winner is ±1 on any of five criteria — effort 3→4 (O3 82 vs O1 80), learning 2→3 (83 vs 79), execution 4→3 (75 vs 73), schedule 4→3 (75 vs 74), defensibility 5→4 (74 vs 73). Only defect-finding 3→2 leaves O1 ahead (75 vs 74). This is a near-tie: the generic comparison cannot decide between O1 and O3, and the project facts in C3 and C4 must. O2 and O4 trail by 25 and 11 and no single ±1 move lifts either to the top.

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | regulation fixes outcome, leaves method open | no | n/a |
| C1 | 2 | CSV and CSA are two ways to one evidence | no | n/a |
| C1 | 3 | decision is execution risk/effort, not compliance level | no | n/a |
| C2 | 1 | executed protocol supplies most CSA record elements | no | n/a |
| C2 | 2 | may lack per-feature risk determination | yes — executed package has traceability (A-15) | yes — A-15 |
| C2 | 3 | switch needs mapping, not re-execution | no | n/a |
| C3 | 1 | activity outside SOP/plan is a deviation | no (A-10, A-11 already in table) | n/a |
| C3 | 2 | deviation is a nonconformance regardless of method | no | n/a |
| C3 | 3 | switch admissible only after SOP + amendment | no | n/a |
| C4 | 1 | savings accrue only on not-high-risk remainder | no | n/a |
| C4 | 2 | net saving = R × f × r − B | no | n/a |
| C4 | 3 | central bracket 31–123 person-days | yes — effort reduction r (A-16), switch cost B (A-17) | yes — A-16, A-17 |
| C4 | 4 | conservative bracket 67–267 | no (same A-16, A-17) | n/a |
| C4 | 5 | aggressive bracket 16–63 | no (same A-16, A-17) | n/a |
| C4 | 6 | under ~16 person-days never pays back | no (same A-16, A-17) | n/a |
| C4 | 7 | measure R, f, B and compare | no | n/a |
| C5 | 1 | must-have knock-out from C3 | no | n/a |
| C5 | 2 | weighted totals | no (A-7 already in table) | n/a |
| C5 | 3 | tiebreak to O1 | no | n/a |
| C5 | 4 | flip test: near-tie | no | n/a |
| C5 | 5 | conditional recommendation | no | n/a |
| C6 | 1 | post-go-live changes assured under effective procedure | yes — A-18 | yes — A-18 |
| C6 | 2 | forgone saving bounded to pre-go-live scope | no | n/a |
| C6 | 3 | overruled team box-ticks scripts | no | n/a |
| C6 | 4 | management reads O1 as resistance | no | n/a |
| C6 | 5 | investigators inspect against QMSR | no | n/a |
| C6 | 6 | SOP revision is QMSR-driven, outside B | yes — firm revises SOP anyway (A-19) | yes — A-19 |
| C7 | 1 | no regulatory-level risk from CSA itself | no | n/a |
| C7 | 2 | risks concentrate in five classes | no | n/a |
| C7 | 3 | each class has a named control | no | n/a |
| C8 | 1 | rigor set by safety-relevance of failure | no | n/a |
| C8 | 2 | Part 11 floor on electronic evidence | no (A-12 already in table) | n/a |
| C8 | 3 | effort falls only on not-high and supporting features | no (A-14 already in table) | n/a |
| C8 | 4 | CSA re-allocates effort under a fixed floor | no | n/a |

Techniques not applied:
- theoretical-limit (Phase 1) — not applicable — the essence is a method-choice question with no figure that could be a convention masquerading as a physical bound
- theoretical-limit (Phase 4) — not applicable — no conclusion needs a law-permitted ceiling; the limiting quantities (R, f, B) are project counts, not physical limits
- inversion (Phase 2) — not applicable — the assumption set was enumerated directly against the guidance's scope, record and testing requirements, and failure enumeration is carried by the Phase 5 pre-mortem on the recommendation
- fishbone (Phase 2) — not applicable — the question is not multi-causal diagnosis of an observed effect; the risk space is enumerated in C7's register
- five-whys (Phase 3) — not applicable — the ground truths are direct quotations of regulatory text or facts about the user's own system, already at definition level

## Adversarial pass (process output)

**Recompute:** C4 — 0.5 × 0.65 = 0.325; 10 ÷ 0.325 = 30.8 and 40 ÷ 0.325 = 123.1 (stated 31–123 ✓); 0.3 × 0.5 = 0.15; 10 ÷ 0.15 = 66.7 and 40 ÷ 0.15 = 266.7 (stated 67–267 ✓); 0.8 × 0.8 = 0.64; 10 ÷ 0.64 = 15.6 and 40 ÷ 0.64 = 62.5 (stated 16–63 ✓). Each breakeven rises as f × r falls, as division requires. C5 — O1 25+16+6+20+2+9 = 78 ✓; O2 15+4+6+8+8+12 = 53 ✓; O3 20+12+12+12+10+12 = 78 ✓; O4 20+4+9+12+10+12 = 67 ✓; flip-test pairs recomputed in the trade-off output ✓. Every chain traced to named ground truths or upstream chains; no hop failed.

**Sensitivity:** The ground truth whose falsity flips the recommendation is GT-10? (`?`-marked): if most of the remaining unexecuted scope is not high process risk and large, O3 overtakes O1; if most is high risk, the switch saves little. GT-9? is the gate: if the SOP does not permit CSA, the switching options are not available at all. Neither can be verified without the user's own documents; both are named on the C3, C5 and §6 confidence lines as MEDIUM causes. Weakest link per chain: C1 — none outstanding; C2 — hop 2 (A-15, priced); C3 — head inputs GT-11?, GT-9?; C4 — hop 3 bracket values (A-16, A-17, priced); C5 — effort scores resting on GT-10?; C6 — hop 6 (A-19, priced); C7 — GT-13? scope.

**Rival:** Headline rival 1 — "never switch; CSA is the riskier way" — ruled out by GT-3 and GT-7 (section 5, Dead End 1). Headline rival 2 — "switch everything now" — ruled out by C3 and C5 (Dead Ends 3 and 4). Intermediate chains: C1 → Dead End 1; C2 → Dead End 2; C3 → Dead End 3; C4 → Dead End 6; C5 → Dead Ends 4 and 5 (O3 is absorbed into the endpoint as its condition, not left live); C6 → Dead End 7; C7 → Dead End 1; C8 (added in the Fix step) → Dead End 1, rival "CSA reduces rigor across the board". C8's weakest link: none outstanding inside scope; scope itself is GT-13? on C7.

**Premise:** It is April 2027. The recommendation — finish under CSV by default, switch the remainder at a documented boundary only when the gate is open and the numbers favour it — has already failed badly. What caused it?

**Causes:** (validation lead) the near-tie was settled by whoever argued loudest rather than by measuring R, f and B; (validation lead) the risk mapping onto executed tests was never written, so the two-method package had no bridge. (test team) told to finish the old way, the team signed scripts without reading the steps and a defect shipped; (test team) some members ran unscripted checks informally and the findings never entered the record. (QA/regulatory) the plan amendment was approved but the SOP revision's effective date came later, so CSA records predate the procedure permitting them; (QA/regulatory) a hurried risk classification put an automated acceptance-inspection function in "not high" and it was tested only exploratorily. (management, who pays) the measured switch saving was optimistic, the switch was taken and go-live slipped; (management) the user's caution was read as obstruction and an immediate full switch was imposed. (FDA investigator) asked why the SOP says risk-based but this system's package is fully scripted with no rationale, and got none; (investigator) evidence relied on system logs whose Part 11 controls were never confirmed. (vendor) vendor validation records were leveraged without a purchasing-control evaluation of the vendor. (scope) the product turned out to be drug-led GMP software and the CSA device guidance was cited as authority.

**Clusters:**
- K1 Procedure sequencing — SOP effective date, plan amendment and first CSA activity out of order (C3, GT-9?, R1, R6). Triage: fatal (self-inflicted inspection observation).
- K2 Process-risk misclassification — a safety-relevant function tested too lightly (GT-5, GT-6, R2). Triage: fatal (product-quality escape).
- K3 People and incentives — box-ticking under O1, shadow testing, management override, near-tie settled by argument (C5, C6, R9, R11). Triage: costly but survivable.
- K4 Evidence integrity — Part 11 on digital evidence and vendor records without purchasing controls (GT-8, GT-12, R4, R12). Triage: costly but survivable.
- K5 Wrong regulatory frame — CSA guidance applied outside its scope (GT-2, GT-13?, R5). Triage: fatal to the analysis's applicability.

**Disposition:**
- K1 — plan change: a written gate checklist, signed by QA, requiring SOP effective date ≤ plan-amendment approval ≤ first CSA activity. Tripwire: any unscripted test record dated before amendment approval; seen by the QA reviewer at each record review.
- K2 — plan change: per-feature risk determinations approved jointly by QA and the process owner, defaulting to high when uncertain and checked against GT-5's example list. Tripwire: any not-high classification of a function matching a GT-5 high-risk example; seen at the risk-determination approval.
- K3 — accepted risk with named mitigation: show the team and management C4's measured numbers and C6's deferral before deciding; the decision is taken on those numbers, recorded with them. Tripwire: script-execution rate rising sharply with zero deviations raised (rubber-stamp signal), or test findings appearing in chat/email but not in records; watched weekly by the validation lead.
- K4 — accepted risk with named mitigation: confirm Part 11 controls of every system whose logs serve as evidence, and a purchasing-control evaluation of every vendor whose records are leveraged, before relying on them. Tripwire: an evidence citation to a system not on the validated-systems list; seen at record review.
- K5 — plan change: confirming scope is the first action (§6, chain C7). Tripwire: product classification not yet confirmed when the plan amendment is drafted; seen by the user.

**Falsification:** The conclusion is false if, with the SOP permitting CSA and the project's own counts showing R × f × r above B, a boundary switch still produced a slower go-live or weaker inspection outcome than finishing under CSV; or if the firm is outside the CSA guidance's scope, in which case C1's premise does not carry over as stated.

## §6→§4 closure ledger (process output)

- "Do not switch the whole in-flight project now; finish it under its approved CSV plan by default … switch cost B" → chain C5 ✓
- "CSV and CSA are two methods for one unchanged obligation … outside your own approved procedure" → chain C1 ✓ (second sentence → chain C3 ✓)
- "Finishing under CSV gives up savings … defers them … QMSR-driven task anyway" → chain C6 ✓ (near-tie sentence → chain C5 ✓)
- "Confirm the system is medical-device production or quality-system software …" → chain C7 ✓
- "Read the current software-validation SOP and approved plan …" → chain C3 ✓
- "Classify every remaining unexecuted test case … count its scripted effort" → chain C4 ✓
- "Executed scripted evidence is kept and mapped … never re-run because of a switch" → chain C2 ✓
- "Whichever option is chosen, the twelve risks in C7's register each carry a named control" → chain C7 ✓
- "If the remainder does move to CSA, its rigor shifts toward safety-relevant features under a Part 11 evidence floor" → chain C8 ✓ (added in the Fix step)
- "Pre-check: head C1 (HIGH) … Inputs ceiling: MEDIUM" → chains C1–C8 ✓
- "Confidence: MEDIUM — C3, C4, C5, C6 and C7 are rated MEDIUM …" → chain C5 ✓

No claim cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-1 + GT-3 + GT-4 + GT-7 | unreached | R9/R10 at hop 3 — beyond the mechanical check's two-hop reach | yes | HIGH | yes | none |
| C2 | GT-6 + GT-7 + C1 | unreached | R9/R10 at hop 3 — beyond the mechanical check's two-hop reach | yes | HIGH | yes | none |
| C3 | GT-11? + GT-9? + GT-7 | unreached | R9/R10 at hop 3 — beyond the mechanical check's two-hop reach | yes | MEDIUM | yes | none |
| C4 | GT-5 + GT-6 + GT-10? | unreached | R9/R10 at hops 3–7 — beyond the mechanical check's two-hop reach | yes | MEDIUM | yes | none |
| C5 | GT-1 + GT-6 + GT-9? + GT-10? + C2 + C3 | unreached | R9/R10 at hops 3–5 — beyond the mechanical check's two-hop reach | yes | MEDIUM | yes | none |
| C6 | C5 + GT-1 + GT-4 | unreached | R9/R10 at hops 3–6 — beyond the mechanical check's two-hop reach | yes | MEDIUM | yes | none |
| C7 | C1 + C2 + C3 + GT-5 + GT-8 + GT-13? | unreached | R9/R10 at hop 3 — beyond the mechanical check's two-hop reach | yes | MEDIUM | yes | none |
| C8 | GT-2 + GT-5 + GT-8 + GT-12 | unreached | R9/R10 at hops 3–4 — beyond the mechanical check's two-hop reach | yes | HIGH | yes | Fix/Repeat |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not switch whole project now … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5 |
| Key insight: two methods for one obligation … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1, C3 |
| Trade-offs acknowledged: defers savings; near-tie … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C6, C5 |
| What decides it, and what holds either way: | bold lead-in | no | a section-intro label whose colon-terminated span is the whole line and which carries no citation of its own | n/a |
| Confirm the system is in CSA scope | list item | yes | list item that closes its own sentence and runs past forty characters | C7 |
| Read the SOP and approved plan | list item | yes | list item that closes its own sentence and runs past forty characters | C3 |
| Classify remaining tests by process risk | list item | yes | list item that closes its own sentence and runs past forty characters | C4 |
| Executed evidence kept and mapped | list item | yes | list item that closes its own sentence and runs past forty characters | C2 |
| Twelve risks each carry a control | list item | yes | list item that closes its own sentence and runs past forty characters | C7 |
| CSA remainder shifts rigor toward safety-relevant features | list item | yes | list item that closes its own sentence and runs past forty characters | C8 |
| Pre-check: head C1 … Inputs ceiling MEDIUM | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C1–C8 |
| Confidence: MEDIUM … | bold lead-in | yes | a bold lead-in whose colon closes the bold span | C5 |

```text
Scan complete: 8 chain rows, one per section-4 chain block in order; 12 section-6 rows, one per construct in order — 11 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Sound · Criterion 2 Rigorous · Criterion 3 Hand-wavy · Criterion 4 Sound · Criterion 5 Rigorous · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 findings acted on by the Fix step: Criterion 1 — success criteria described project records, not properties of the Conclusion; Criterion 3 — unsuffixed GT-4, GT-5 and GT-8 fed only MEDIUM chains, and GT-2 and GT-12 fed no chain (the latter also noted under Criterion 4). Fix: success criteria rewritten as Conclusion properties; GT-4 added to C1's head; chain C8 (HIGH) added consuming GT-2, GT-5, GT-8 and GT-12, with a §6 list item citing it; Assumption Audit, closure ledger, self-audit scan and adversarial record rows re-run for the change.

**Criterion 1: Identify Essence**
Quoted span: "The Conclusion states the conditions under which that default flips, each as a fact the user can check in their own documents or counts."
Band: **Rigorous**
Justification: The essence is one sentence naming the method choice for the unexecuted remainder (not the triggering disagreement), and each success criterion is now a verb–subject–outcome test on the Conclusion section, including the explicit allowance for a split answer.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C4 | 3 | central bracket 31–123 person-days | yes — effort reduction r (A-16), switch cost B (A-17) | yes — A-16, A-17 |"
Band: **Rigorous**
Justification: Every row uses one of the four types with its prescribed treatment and an em-dash verdict, several assumptions are challenged or discarded, unverified ones read "unverified — flagged", and the Assumption Audit covers every chain step including C8's and records A-15 to A-19 back into the table.

**Criterion 3: Establish Ground Truths**
Quoted span: "enumerated GT-9?, GT-10?, GT-11?, GT-13?; the list carries ? on exactly those four, and each unsuffixed GT (GT-1, 2, 3, 4, 5, 6, 7, 8, 12) now feeds C1, C2 or C8, all HIGH, with a named read location"
Band: **Rigorous**
Justification: IDs are stable, the enumeration matches the suffixed entries on inspection, GT-11?'s Phase 3 failure record names the paywalled standard, and after the Fix every unsuffixed ground truth with a reachable source feeds at least one HIGH chain.

**Criterion 4: Reason Upward**
Quoted span: "| C8 | GT-2 + GT-5 + GT-8 + GT-12 | unreached | R9/R10 at hops 3–4 — beyond the mechanical check's two-hop reach | yes | HIGH | yes | Fix/Repeat |"
Band: **Sound**
Justification: Every conclusion has one arrow-led chain with intermediates, dependencies are clean, dead ends use the three-part structure, arithmetic recomputes, and no analogy is used as evidence — but every chain carries hops beyond the mechanical check's reach, so form conformance at those positions rests on inspection, recorded as `unreached` rather than claimed.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — C3, C4, C5, C6 and C7 are rated MEDIUM; the decision turns on the firm's SOP state, the not-high-risk share of remaining work and the system's scope"
Band: **Rigorous**
Justification: Each chain's band matches its axes (HIGH only where every input is read at source and assumptions are priced, MEDIUM where a `?` input or MEDIUM chain sits on the head), the Conclusion equals its weakest contributing chain, and the adversarial record carries recompute, sensitivity, rivals, a past-tense premise, stakeholder causes, clusters citing chain/GT ids, dispositions with tripwires, and falsification.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| CSA remainder shifts rigor toward safety-relevant features | list item | yes | list item that closes its own sentence and runs past forty characters | C8 |"
Band: **Rigorous**
Justification: All eleven §6 claims cite a §4 chain with none untraced, and the Key Insight — that the risk lies in changing method outside one's own approved procedure, not in CSA itself — is a finding that reasoning by "old way versus new way" does not reach, not a restatement of the recommendation.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-2",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-4",
      "type": "current constraint",
      "verdict": "Challenge"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-7",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-10",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-11",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-12",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-14",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-15",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-16",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-17",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-18",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-19",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": false
    },
    {
      "id": "GT-10",
      "read_at_source": false
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": true
    },
    {
      "id": "GT-13",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-3",
        "GT-4",
        "GT-7"
      ]
    },
    {
      "id": "C2",
      "confidence": "HIGH",
      "rests_on": [
        "GT-6",
        "GT-7",
        "C1"
      ]
    },
    {
      "id": "C3",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-11?",
        "GT-9?",
        "GT-7"
      ]
    },
    {
      "id": "C4",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-5",
        "GT-6",
        "GT-10?"
      ]
    },
    {
      "id": "C5",
      "confidence": "MEDIUM",
      "rests_on": [
        "GT-1",
        "GT-6",
        "GT-9?",
        "GT-10?",
        "C2",
        "C3"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C5",
        "GT-1",
        "GT-4"
      ]
    },
    {
      "id": "C7",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "GT-5",
        "GT-8",
        "GT-13?"
      ]
    },
    {
      "id": "C8",
      "confidence": "HIGH",
      "rests_on": [
        "GT-2",
        "GT-5",
        "GT-8",
        "GT-12"
      ]
    }
  ],
  "dead_ends": [
    "1 — \"CSA is a lower compliance bar, so switching lowers our compliance\"",
    "2 — \"A validation package must use one method throughout, so a mid-flight switch means redoing what is done\"",
    "3 — \"FDA has endorsed CSA, so the team can start working the new way now\"",
    "4 — Option O2 — switch everything now and re-plan the whole package to CSA",
    "5 — Option O4 — pause execution, revise the SOP, train, then switch",
    "6 — Stating one breakeven number for when a switch pays",
    "7 — \"Finishing under CSV locks this system into the old way for its whole life\""
  ],
  "techniques": {
    "applied": [
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "the essence is a method-choice question with no figure that could be a convention masquerading as a physical bound"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion needs a law-permitted ceiling; the limiting quantities (R, f, B) are project counts, not physical limits"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the assumption set was enumerated directly against the guidance's scope, record and testing requirements, and failure enumeration is carried by the Phase 5 pre-mortem on the recommendation"
      },
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the question is not multi-causal diagnosis of an observed effect; the risk space is enumerated in C7's register"
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "the ground truths are direct quotations of regulatory text or facts about the user's own system, already at definition level"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Rigorous",
          "Hand-wavy",
          "Sound",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 3 scored Hand-wavy and Criteria 1 and 4 Sound on the first pass."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Do not switch the whole in-flight project now; finish it under its approved CSV plan by default, and move only the unexecuted remainder to CSA, at a documented boundary, if the firm's SOP already permits risk-based assurance, the plan is amended before any CSA activity, and the project's own counts show R × f × r exceeding the switch cost B (chain C5).",
    "confidence": "MEDIUM",
    "rests_on": [
      "C1",
      "C2",
      "C3",
      "C4",
      "C5",
      "C6",
      "C7",
      "C8"
    ]
  }
}
```
