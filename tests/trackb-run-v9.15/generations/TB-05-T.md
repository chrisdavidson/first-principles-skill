## Answer

**Recommendation:** Expect a bare "publish training data sources" hiring-AI rule to produce vague, categorical vendor disclosures rather than itemized data accounting (chain C1), and expect that disclosure — however complete — to be logically incapable of revealing discriminatory bias, since bias is a property of outcome/feature statistics that source-naming doesn't convey (chain C2); the closest real-world analogue shows this class of mandate gets ≈5% real compliance, self-selected toward favorable results (chain C3). Net effect: real compliance costs and modest secondary transparency value, not the anti-discrimination outcome usually cited to justify it.

**Band (from §6):** LOW

**Would change it:** The actual statutory/implementing-rule text of a specific proposal (resolving whether it mandates a granular, outcome-linked schema and real enforcement — chains C1, C3); a working primary-source citation for the Title VII disparate-impact standard behind chain C2 (its EEOC and eCFR citations were unreachable); and post-enactment compliance data for the specific rule, analogous to the LL144 field study behind chains C3/C4.
## 1. Problem Essence

**Core problem:** When a national regulator requires every AI system used in hiring to publish its training-data sources, what concrete institutional and behavioral responses actually follow, and does the resulting information regime give the regulator (or anyone else) the ability to detect or reduce discriminatory bias in hiring AI — the aim such rules are consistently justified by?

**Success criteria:**
1. The analysis names the specific compliance behavior the rule would most plausibly produce (not merely "firms will comply" or "firms will resist"), grounded in how comparable real-world disclosure mandates have actually been satisfied.
2. The analysis states, independent of compliance rates, whether the disclosed information (training-data *sources*) is logically capable of revealing discriminatory bias, and shows the reasoning rather than asserting it.
3. The analysis accounts for at least one real-world precedent of a structurally similar "publish X about your hiring AI" mandate and uses its observed outcome as evidence, not analogy.
4. The analysis states explicitly what would have to be true about the rule's actual design (schema, verification, enforcement) for it to achieve the stated aim, so a reader can judge any real proposal against those conditions rather than against this analysis's default reading alone.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A1: "Publish training data sources" means publicly naming/categorizing the datasets, data types, or data providers used to train the model — distinct from publishing the raw training data, publishing bias-audit/outcome results, or publishing model internals. | convention | Explicitly challenge before use — the prompt's phrasing admits at least three readings; state which is adopted and note how the conclusion would change under the others. | Accept — em-dash: adopted as the working interpretation because it is the plain reading of "publish...sources," and because the two closest real regulatory analogues (GT-1, GT-5) both require a summary/name-level posting rather than raw-data release, evidencing this is the reading regulators actually draft toward. | Cross-checked against GT-1, GT-5; alternate reading (raw-data publication) explored and abandoned — see §5 Dead End 3. |
| A2: The obligated party (AI vendor/developer vs. employer/deployer) is unspecified in the prompt; this analysis assumes an employer/deployer-facing public-posting obligation, the pattern of the closest same-type analogue (GT-1), while noting a developer-facing version (GT-5's pattern) behaves somewhat differently. | untested belief | Verify, or flag as unverified — the prompt gives no obligated-party detail, so this is a modeling choice, not a fact. | Challenge — em-dash: flagged; both variants are carried through the chains rather than picking one silently. | Unverified — flagged; no chain rests on this choice alone (C1–C4 hold under either obligated party). |
| A3: The rule's stated aim, as with every real-world analogue found, is to enable detection/prevention of discriminatory hiring bias and to enable public/regulatory scrutiny of hiring AI — this is the operative definition of "achieve what it is aimed at" used throughout this analysis. | convention | Explicitly challenge before use — the prompt does not state an aim; this is inferred from the consistent stated purpose of every comparable real rule located. | Accept — em-dash: consistent across GT-1 (bias-audit framing), GT-4 (EEOC disparate-impact framing), and GT-5 (which explicitly names bias/data-diversity assessment as one of several purposes, alongside copyright/privacy). | Cross-checked against GT-1, GT-4, GT-5; scope-limited in §6 if the regulator's actual stated aim is primarily something else (e.g., copyright). |
| A4: Firms have a standing legal and competitive incentive (trade-secret protection, client confidentiality, litigation exposure) to satisfy a "publish your sources" duty with vague/categorical rather than granular disclosure. | current constraint | Record expiry conditions — this constraint lifts if the statute itself defines a mandatory minimum specificity that defeats trade-secret-based vagueness. | Accept — em-dash: expires only if a specific granular schema is legally mandated (see A6); not expired under the generic reading this analysis addresses. | Unverified — flagged; supported by GT-6's observed outcome under the one real analogue with a dedicated template process. |
| A5: The new national regulator's enforcement design/resourcing for this mandate resembles existing complaint-driven, low-audit-staff disclosure regimes (GT-1's pattern) rather than a heavily resourced, systematic-verification regime. | current constraint | Record expiry conditions — this is a default assumption in the absence of stated detail; it expires once a specific proposal's enforcement budget, audit mechanism, and penalty structure are known. | Accept — em-dash: default reading of a generic "requires...to publish" proposal, which names a disclosure duty but no enforcement mechanism. | Unverified — flagged; drives chain C3's confidence band directly. |
| A6: The rule's implementing regulations do not themselves prescribe a specific granular, outcome-linked disclosure schema (this is what "as commonly proposed" means throughout this analysis). | current constraint | Record expiry conditions — expires the moment an actual implementing rule with a granular schema is published; the conclusion is explicitly scoped to the generic reading. | Accept — em-dash: matches the prompt's generic phrasing; the one real analogue with a template (GT-5/GT-6) still produced a banded, non-itemized schema. | Unverified — flagged. |
| A7 [surfaced by inversion, §2 procedure]: No independent verification/audit mechanism accompanies the disclosure mandate. | untested belief | Verify, or flag as unverified. | Challenge — em-dash: assumed absent by default given the prompt's generic phrasing; load-bearing for chain C3. | Unverified — flagged. |
| A8 [surfaced by inversion]: The required disclosure format does not itself mandate outcome/statistical bias information, only source identity. | untested belief | Verify, or flag as unverified. | Challenge — em-dash: this is A6 restated at the schema level; load-bearing for chains C1 and C2. | Unverified — flagged; cross-referenced to A6. |
| A9 [surfaced by inversion]: No private right of action or dedicated enforcement funding ties disclosure to consequences. | untested belief | Verify, or flag as unverified. | Challenge — em-dash: assumed absent by default; load-bearing for chain C3 (contrast with Colorado's AG-only enforcement, which this constraint resembles). | Unverified — flagged. |
| A10 [surfaced by inversion]: No accessible aggregation/search layer exists for job seekers, researchers, or journalists to use the disclosures at scale. | untested belief | Verify, or flag as unverified. | Challenge — em-dash: assumed absent by default; load-bearing for chain C3's second-order extension. | Unverified — flagged; the empirical analogue (GT-2) measured exactly this gap directly (17–19 pages, 30 minutes per search). |

**Inversion procedure applied (Phase 2):** Claim challenged: "Requiring publication of training-data sources will enable meaningful detection/prevention of hiring discrimination" (A3 operationalized). Inverted: "...will NOT enable meaningful detection/prevention...". Failure-guaranteeing conditions enumerated: (1) the regulator lacks resources/authority to verify disclosures or compel completeness [→A5/A9]; (2) the disclosed information (source names) is definitionally insufficient to reveal discriminatory statistics [→A8, see GT-7/GT-8]; (3) firms have strong incentive to disclose only vague/categorical information [→A4]; (4) no mechanism connects the disclosure to an actual remedy [→A9]; (5) job seekers/researchers lack practical means to use the published information even if complete [→A10]. Necessary preconditions for the rule to achieve A3's aim, all tagged **load-bearing** (the conclusion does not survive their being false): (a) enforceable verification mechanism exists [A7]; (b) disclosure format ties to outcome-relevant statistics, not just naming [A8]; (c) legally mandated minimum specificity defeats trade-secret-based vagueness [A4's negation]; (d) an actionable remedy/monitoring pathway links disclosure to consequences [A9]; (e) accessible aggregation/search exists for end users [A10]. All five are carried into the table above as untested beliefs (A7–A10, plus A4/A6) and assumed absent by default given the prompt's generic phrasing — this default, not a claim that no real proposal could include them, is what chains C1–C3 are scoped to.

## 3. Ground Truths

- **GT-1** NYC Local Law 144 (effective July 5, 2023) requires a covered employer/employment agency using an automated employment decision tool (AEDT) to obtain an independent bias audit within the year prior to use and to publicly "post a summary of the results of the bias audit," plus give candidates advance notice — it does not require publication of the underlying training data or a list of training-data sources. — source: NYC Department of Consumer and Worker Protection, AEDT page (nyc.gov/site/dca/about/automated-employment-decision-tools.page); read-at-source: page text quoting the posting duty as "Post a summary of the results of the bias audit."
- **GT-2** A 2024 field study of 267 NYC employers with open job listings found only 14 (≈5%) had publicly posted a required bias-audit report and only 12 (≈4%) had posted the required candidate notice; only 11 employers posted both; the researchers term this pattern "null compliance" — the absence of a disclosure cannot be distinguished from the tool being out of scope. — source: Wang et al., "Null Compliance: NYC Local Law 144 and the Challenges of Algorithm Accountability," arxiv.org/html/2406.01399v1, corroborated by Consumer Reports' Digital Lab summary (innovation.consumerreports.org); read-at-source: both pages fetched directly and quoted ("Out of 267 employers... only 14 audit reports (5%) and 12 notices (4%)").
- **GT-3** Among the bias-audit reports that were publicly posted under GT-1's regime, roughly 96% reported impact ratios at or above the EEOC's four-fifths (0.8) threshold — i.e., showed no statistical adverse impact — a pattern the researchers attribute to selective, litigation-avoidant disclosure rather than to AEDTs being uniformly unbiased. — source: same arxiv paper as GT-2; read-at-source: "96% of published audit reports showed impact ratios above the 0.8 threshold."
- **GT-4?** Under Title VII, algorithmic hiring tools are treated as "selection procedures"; disparate/adverse impact is assessed by comparing selection rates across protected groups, using the "four-fifths rule" (a group's selection rate below 80% of the highest group's rate) as a rule-of-thumb screening threshold under the 1979 Uniform Guidelines on Employee Selection Procedures — i.e., the operative legal test is a comparison of outcome statistics, not an inquiry into which organizations supplied the training data. — cited to: EEOC technical guidance ("Select Issues: Assessing Adverse Impact...") and 29 CFR 1607; reported-by-delegate: law-firm summaries (Mayer Brown, Ogletree) returned by WebSearch — cited sources not opened successfully by this analysis (see Phase 3 failure records below).
- **GT-5** EU AI Act Article 53(1)(d) requires providers of general-purpose AI (GPAI) models to "draw up and make publicly available a sufficiently detailed summary about the content used for training," per a template issued by the EU AI Office — the closest existing real-world regulatory analogue to "publish your AI's training-data sources," though it applies to GPAI model providers, not specifically to hiring-AI deployers (hiring/recruitment AI is separately classified "high-risk" under Annex III with documentation obligations owed to regulators, not the public). — source: artificialintelligenceact.eu, Article 53 page; read-at-source: exact text quoted, "draw up and make publicly available a sufficiently detailed summary about the content used for training of the general-purpose AI model."
- **GT-6?** The template actually adopted by the EU Commission's AI Office for GT-5's disclosure requirement (released July 24, 2025) asks for training-data size in bands, a data-acquisition cutoff date, and yes/no flags per data-source category — a categorical/banded disclosure format, not an itemized list of specific datasets or data providers. — cited to: European Commission AI Office training-content-summary template coverage; reported-by-delegate: WebSearch synthesis of secondary reporting (cadeproject.org, securiti.ai) — the template document itself was not opened by this analysis.
- **GT-7** Detecting discriminatory bias in a hiring algorithm's training data or outputs requires examining the statistical relationship between input features/labels and protected-class membership, or comparing group selection rates (per GT-4's definition of disparate impact) — a property of the data's composition and labeling, not of which named organizations or platforms supplied it. — source: definitional entailment of GT-4 via reduce-to-primitives decomposition (see below); no separate external citation required beyond GT-4.
- **GT-8** Because of GT-7, two systems can disclose an identical list of named training-data sources while having materially different bias profiles (depending on filtering, labeling, weighting, and modeling choices), and two systems can disclose different sources while having identical bias profiles — a list of source names is therefore not, by itself, informative about the presence or degree of discriminatory bias. — source: logical corollary of GT-7; no separate external citation required.
- **GT-9?** Hiring-AI training data commonly includes an employer's own historical applicant and hiring records containing personally identifiable information about real, identifiable people; a 2024 UK ICO audit of recruitment-AI vendors and developers found compliance problems with purpose limitation and data minimization specifically in this data flow (candidate data reused to improve vendor products beyond the original service purpose). — cited to: UK Information Commissioner's Office, "AI in Recruitment" outcomes report; reported-by-delegate: WebSearch synthesis referencing the ICO report — the report itself was not opened by this analysis.

**Reduce-to-primitives decomposition (Phase 3, producing GT-7/GT-8):** Claim tested: "Publishing a hiring AI's training-data sources would let someone detect whether it is discriminatory." Immediate constituents: (i) what "discriminatory" means under the applicable legal/statistical test, and (ii) what information a "source name" conveys. (i) reduces to GT-4's definition (a comparison of group outcome/selection-rate statistics) — irreducible, verified (with the `?` caveat on GT-4's own citation). (ii) reduces to the definition of a data source as an origin/provenance label, which carries no logical entailment about the demographic composition, labeling, or filtering applied to what came from it — irreducible by definition, needs no external citation. Since the parent claim's truth requires (ii) to entail (i), and it demonstrably does not (a source name is a superset descriptor with no fixed relationship to within-set demographic statistics), the parent claim is **false as a general claim** and GT-7/GT-8 record the verified negative.

**Provenance summary:** `?`-marked: GT-4, GT-6, GT-9 (3 of 9). Read-at-source: GT-1 — nyc.gov DCWP AEDT page, posting-duty clause quoted verbatim; GT-2 — arxiv.org/html/2406.01399v1, compliance-count sentence quoted verbatim; GT-3 — same paper, impact-ratio sentence quoted verbatim; GT-5 — artificialintelligenceact.eu Article 53, statutory clause quoted verbatim.

**Phase 3 failure records:**
1. GT-4 — attempted read of `https://www.eeoc.gov/select-issues-assessing-adverse-impact-software-algorithms-and-artificial-intelligence-used`: unreachable, HTTP 404 Not Found.
2. GT-4 — attempted read of `https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XIV/part-1607` (29 CFR 1607, the Uniform Guidelines' codified four-fifths-rule text): unreachable, server returned a 302 redirect to a bot-block/"unblock" interstitial rather than the regulation text.

## 4. Derivation Chains

### Conclusion C1: Absent a mandated granular schema, the rule would most plausibly be satisfied through categorical, low-specificity disclosures rather than itemized data-source accounting

GT-5 (EU Art 53(1)(d) text: "sufficiently detailed summary") + GT-6? (actual EU template: banded, categorical, not itemized)
→ even the most directly comparable real-world "publish what your AI was trained on" mandate, backed by a dedicated EU regulatory template-drafting process, resolved into banded categorical disclosure rather than an itemized, source-by-source accounting
→ this outcome is consistent with regulated entities converging on the least specific disclosure that satisfies a "publish your sources" duty when trade-secret, competitive, and legal-exposure concerns are present *[Assumes: A4]*
→ a national "publish training data sources" rule for hiring AI that does not itself prescribe a granular schema would most plausibly be satisfied the same way — for example "internal applicant records," "a licensed third-party resume database," "publicly available profile data" — rather than an itemized accounting of the actual datasets used *[Assumes: A6]*

**Pre-check:** head GT-5, GT-6? · ?-marked: GT-6? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes short. Inputs: GT-6? is reported-by-delegate (the EU Commission's own template document was not opened directly); verification path: fetch the AI Office's published template PDF directly and confirm the banded/categorical field structure. Rivals: a live, unsettled rival — the specific new national statute could itself prescribe a granular, itemized schema unlike EU Art 53's principles-based approach — nothing in this analysis rules that out; what would settle it is the actual statutory/implementing-rule text of a real proposal, which does not yet exist for this hypothetical.

### Conclusion C2: Training-data-source disclosure, however complete and accurate, is not logically capable of revealing discriminatory bias

GT-4? (Title VII disparate impact = comparative selection-rate/four-fifths test) + GT-7 (bias detection requires outcome/feature-label statistics) + GT-8 (source names do not convey those statistics)
→ the legal and technical definition of hiring discrimination centers on differential selection/outcome rates across protected groups, a property of how data is filtered, labeled, and modeled
→ a list of "training data sources," however accurate, is decoupled from that property: identical source lists can accompany opposite bias profiles, and different source lists can accompany identical bias profiles
→ source-of-training-data disclosure is not, by itself, a mechanism capable of detecting or preventing discriminatory hiring outcomes; at most it is a precondition for a separate, much larger investigation (for example, obtaining the actual data for statistical analysis) that a bare "publish your sources" duty does not itself provide

**Pre-check:** head GT-4?, GT-7, GT-8 · ?-marked: GT-4? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — Inputs axis short: GT-4? rests on secondary legal summaries after two direct-read attempts failed (EEOC page 404, eCFR redirect-blocked; see Phase 3 failure records in §3); verification path: locate a current, working citation to 29 CFR 1607.4(D) or an EEOC guidance mirror and confirm the four-fifths-rule/selection-rate definition of disparate impact. Inference and Rivals axes are clean: both hops follow by deduction from GT-7/GT-8's definitional content, and the strongest rival to this chain's endpoint — that a *named* source could itself be a bias red flag when that exact source has independently documented demographic skew — is ruled out for the general/default case addressed here by GT-9 (most hiring-AI training data is idiosyncratic employer-specific historical data, not a standardized public dataset with pre-existing bias literature attached); see §5 Dead End 2.

### Conclusion C3: Real-world compliance with this class of hiring-AI transparency mandate has been low and self-selected, and the proposed rule would predictably reproduce that pattern

GT-1 (LL144's public bias-audit-summary posting duty) + GT-2 (only ≈5%/4% of covered employers actually post) + GT-3 (96% of what is posted shows favorable results)
→ LL144 is the closest existing analogue to a mandatory "publish information about your hiring AI" duty, already carrying real statutory force since 2023
→ despite that force, only about one in twenty covered employers actually posts the required disclosure
→ of the few disclosures that do appear, the overwhelming majority report favorable results, consistent with employers self-selecting what to publish rather than the mandate compelling comprehensive reporting
→ compliance and information quality under this class of mandate are therefore driven by self-selection and litigation-avoidance, not by the disclosure duty itself
→[2nd] employers and vendors route a "publish training data sources" duty to compliance counsel as a litigation/PR risk-management task rather than treating it as a substantive audit for job seekers to use *[Assumes: A5, A7, A9]*
→[3rd] the people the rule is meant to inform — job seekers, researchers, enforcement staff — are the people least likely to encounter complete, findable disclosures, and the disclosure standardizes over repeated compliance cycles into a boilerplate artifact that signals compliance without increasing what any of them can actually learn *[Assumes: A10]*
→ a bare "publish training data sources" mandate modeled on this same disclosure-only structure would predictably reproduce this low, self-selected, low-utility compliance pattern rather than the robust public information resource its stated aim (A3) presumes

**Pre-check:** head GT-1, GT-2, GT-3 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** LOW — two axes short despite clean Inputs. Inference: the 2nd/3rd-order extension and the endpoint both rest on A5/A7/A9/A10 (that the new rule's enforcement design resembles LL144's rather than a stronger model); if A5/A9 fail — i.e., the new regulator funds systematic verification and a private right of action — this chain's endpoint does not survive unchanged, so the premise is not yet priced to HIGH. Verification path: the actual enforcement budget, audit mechanism, and penalty structure of a real proposal once drafted. Rivals: a live, unsettled rival — a differently designed enforcement regime could avoid this pattern entirely — is not ruled out by this analysis (only the narrower "reputational deterrence alone suffices" rival is ruled out; see §5 Dead End 1); what would settle it is post-enactment compliance data for the specific rule, analogous to the LL144 field study behind GT-2/GT-3.

### Conclusion C4: The same pressure that keeps this class of rule at the category-name level is itself part of why it cannot also serve as a precise bias-detection instrument

GT-9? (hiring-AI training data commonly contains real applicants' PII; ICO found purpose-limitation/minimization problems) + GT-1 (the closest real analogue requires a summary/audit posting, not raw-data release)
→ both regulatory patterns examined in this analysis (GT-1's audit-summary posting and GT-5's banded training-content summary) require a summary/name-level posting rather than raw training-data release, which is the pattern most consistent with avoiding a collision between "make training data inspectable" and data-protection law's purpose-limitation and minimization principles
→ staying at the category-name level, as C1 concludes this rule most likely would, sidesteps that collision, but only by giving up exactly the outcome/feature-level detail C2 shows bias detection actually needs
→ the two goals commonly bundled together under "AI hiring transparency" — protecting the privacy of the real people in the training data, and producing bias-diagnostic information — pull the disclosure's required specificity in opposite directions, so a single "publish your sources" duty cannot cleanly serve both

**Pre-check:** head GT-9?, GT-1 · ?-marked: GT-9? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — two axes short. Inputs: GT-9? is reported-by-delegate (the ICO report itself was not opened); verification path: fetch the ICO "AI in Recruitment" outcomes report directly and confirm the purpose-limitation/minimization finding. Rivals: a live, unsettled rival — a rule could require anonymized or aggregated (rather than raw or fully categorical) data-composition disclosure, potentially serving both privacy and bias-diagnostic goals at once — this analysis did not evaluate that design and does not rule it out; it is outside the scope of "the rule as commonly proposed" (A1, A6) this analysis addresses.

## 5. Abandoned Reasoning

### Dead End: Reputational-deterrence rival to C3

**What was tried:** Considered whether public naming alone, without independent enforcement, would deter poor data/hiring practices through reputational or market pressure, making the rule effective even at low measured compliance.

**Why abandoned:** The closest empirical analogue (GT-2, GT-3) shows reputational pressure did not drive compliance up under a legally comparable disclosure duty — only ≈5% of covered employers posted the required disclosure — and the researchers attribute what little disclosure occurs to litigation-avoidant self-selection, not reputational competition. The mechanism is directly contradicted by C3's evidence rather than merely unsupported.

**What it ruled out:** A "sunlight alone is enough" design theory for this specific instrument, absent independent verification (A7) and enforcement consequences (A9). It does not rule out reputational pressure combined with stronger verification, which remains a live, unsettled rival on chain C3.

### Dead End: Named-source-as-bias-red-flag rival to C2

**What was tried:** Considered whether disclosing a *specific named* training-data source could itself function as an indirect bias signal, in cases where that exact source has independently documented demographic skew (e.g., a public dataset previously shown in the literature to be biased).

**Why abandoned:** Most training data used in hiring AI is not a single standardized public dataset with pre-existing bias literature attached — it typically includes an employer's own idiosyncratic historical applicant and hiring records mixed with licensed or scraped data (GT-9), for which no independent bias literature exists to attach to a bare source name. The mechanism does not generalize to the typical/default case this analysis addresses.

**What it ruled out:** Treating source-naming as a reliable general-purpose bias-detection proxy. It does not rule out the narrow special case of a well-studied, named public dataset, which is carried as an explicit scope-limit on C2 rather than a refutation of it.

### Dead End: Raw-training-data-publication reading of the rule

**What was tried:** Considered interpreting "publish training data sources" as requiring publication of the underlying raw data itself, not just source names — a reading that would make bias more directly inspectable and could strengthen the case that the rule achieves its stated aim.

**Why abandoned:** Raw applicant/hiring records are personally identifiable data about real, identifiable people (GT-9); a rule compelling their public release would collide with data-protection/purpose-limitation law far more severely than a routine source-naming disclosure. This reading is also not the wording either real closest analogue actually adopted (GT-1 requires an audit-result summary; GT-5 requires a training-content summary, not raw data) — a strong signal it is not the operative reading a real "publish training data sources" rule would take in practice.

**What it ruled out:** Raw-data publication as the working interpretation for this analysis (see A1). The analysis proceeds on the narrower, better-evidenced summary/category-name reading throughout chains C1–C4.

## 6. Conclusion

**Recommended approach:** Read the proposed rule as it is most likely to be implemented — a bare "publish training data sources" duty without a mandated statistical/outcome schema, independent verification, or enforcement funding (A6, A7, A9) — and expect three things to actually follow: categorical, low-specificity vendor disclosures rather than itemized data-source accounting (chain C1); a source-of-training-data disclosure that, however complete, cannot by itself reveal discriminatory bias, because bias is a property of outcome/feature statistics that source-naming does not convey (chain C2); and real-world compliance that is low and self-selected toward favorable results, mirroring the closest existing analogue (chain C3). Taken together, the rule as commonly proposed would generate compliance activity and modest secondary transparency value but would not, on the evidence assembled here, achieve the anti-discrimination/accountability aim usually invoked to justify it (chains C1, C2, C3).

**Key insight:** The rule's likely failure mode is not weak enforcement alone — it is a structural tension between two goals commonly bundled together under "AI hiring transparency." The specificity that would make a data-source disclosure diagnostic of bias (chain C2) is largely the same specificity that collides with data-protection law's purpose-limitation and minimization principles for the real people whose records are in that data (chain C4) — so the version of the disclosure that would be most useful for the stated aim is also the version regulators and firms have the strongest independent reasons not to require or publish.

**Trade-offs acknowledged:** A source-publication duty is not worthless: it can create secondary value for copyright/privacy enforcement and for researchers cross-referencing named datasets against independently documented bias properties in the narrow cases where those exist (chain C2), and its likely low real-world compliance mirrors a documented pattern in the closest existing analogue rather than a flaw unique to this proposal (chain C3). Adopting this design over a more direct instrument also risks crowding out political appetite for outcome-based bias audits with independent verification and enforcement funding — the instrument the evidence here suggests is the closer fit to the stated aim — no chain — flagged assumption only.

**Pre-check:** head C1 (LOW), C2 (MEDIUM), C3 (LOW), C4 (LOW) · ?-marked: none directly (carried via C1/C2/C4's own head inputs) · lowest cited: LOW · Inputs ceiling: LOW
**Confidence:** LOW — the headline claim rests most heavily on C1 (LOW) and C3 (LOW), each short on two axes because they are scoped to a rule design (A4–A10) that has not yet been drafted in any real jurisdiction and so carries a genuinely live, unsettled rival: a specific, better-designed implementing rule could avoid the pattern either chain describes. C2 (MEDIUM) is the most robust component — its logical core (source-naming ≠ bias-detection) does not depend on the rule's enforcement design at all, only on GT-4's disparate-impact definition, whose primary-source citation this analysis could not read directly (EEOC page 404; eCFR redirect-blocked — see §3 Phase 3 failure records). What would raise the band: (a) the actual statutory/regulatory text of a specific proposal, which would resolve C1's and C3's Rivals axis by fixing the disclosure schema and enforcement design; (b) a working citation confirming GT-4's four-fifths-rule/selection-rate definition; (c) post-enactment compliance data for the specific rule, analogous to the LL144 field study behind GT-2/GT-3.

## Appendix — process output

## §6→§4 closure ledger (process output)

- "the rule as commonly proposed would generate compliance activity and modest secondary transparency value but would not... achieve the anti-discrimination/accountability aim" → chains C1, C2, C3 ✓
- "The rule's likely failure mode is... a structural tension between two goals..." → chains C2, C4 ✓
- "A source-publication duty is not worthless... its likely low real-world compliance mirrors a documented pattern in the closest existing analogue" → chains C2, C3 ✓
- "crowding out political appetite for outcome-based bias audits with independent verification and enforcement funding" → no chain — flagged assumption only
- Confidence line (headline band and what would change it) → chains C1, C2, C3, C4 ✓

## Techniques not applied (process output)

- trade-off — not applicable — the question is evaluative/predictive ("would this rule achieve X"), not a choice among named alternative options; a composite-option scan does not apply to a single proposed rule
- estimate — not applicable — no magnitude-uncertain quantity is central to the conclusion; the cited compliance and impact-ratio percentages (GT-2, GT-3) are direct citations from a field study, not Fermi magnitude rebuilds
- theoretical-limit — not applicable — no request for a physical/quantitative ceiling; the analysis concerns institutional and behavioral response to a disclosure mandate, not a bound set by physical law
- fishbone — not applicable — the assumption space was small and directly enumerable via the inversion procedure's failure-condition scan (five conditions, A6–A10) without needing a category-based breadth brainstorm
- five-whys (causal mode) — not applicable — no recurring symptom needing causal-depth drilling; the reduce-to-primitives mode was used instead, at Phase 3, to establish GT-7/GT-8 from GT-4
- pre-mortem — not applicable — the headline conclusion is a predictive/evaluative claim, not a plan; Phase 5's adversarial-technique step used Inversion instead, per the technique's own decision rule (inversion also fired earlier, at Phase 2, on assumption A3)

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | closest real mandate resolved into banded categorical disclosure | none | n/a |
| C1 | 2 | regulated entities converge on least-specific compliant disclosure | A4 (already in table) | yes (pre-existing) |
| C1 | 3 | national rule would most plausibly be satisfied the same way | A6 (already in table) | yes (pre-existing) |
| C2 | 1 | discrimination test centers on selection-rate differentials | none | n/a |
| C2 | 2 | source list decoupled from that property | none | n/a |
| C2 | 3 | source disclosure not a detection/prevention mechanism | none | n/a |
| C3 | 1 | LL144 is the closest analogue with real statutory force | none | n/a |
| C3 | 2 | only ≈1 in 20 employers actually post | none | n/a |
| C3 | 3 | published disclosures skew favorable, consistent with self-selection | none | n/a |
| C3 | 4 | compliance driven by self-selection/litigation-avoidance | none | n/a |
| C3 | 5 [2nd] | duty routed to compliance counsel as risk management | A5, A7, A9 (already in table) | yes (pre-existing) |
| C3 | 6 [3rd] | intended audience least likely to encounter findable disclosures | A10 (already in table) | yes (pre-existing) |
| C3 | 7 | bare mandate would reproduce this pattern | none | n/a |
| C4 | 1 | both real patterns require summary posting, not raw release | none | n/a |
| C4 | 2 | category-name level sidesteps privacy collision but loses needed detail | none | n/a |
| C4 | 3 | privacy and bias-diagnostic goals pull specificity in opposite directions | none | n/a |

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-5, GT-6? | yes | n/a | yes | LOW | yes | none |
| C2 | GT-4?, GT-7, GT-8 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-1, GT-2, GT-3 | yes | n/a | yes | LOW | yes | none |
| C4 | GT-9?, GT-1 | yes | n/a | yes | LOW | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | colon closes bold span; assertion on same line | C1, C2, C3 |
| Key insight | bold lead-in | yes | colon closes bold span; assertion on same line | C2, C4 |
| Trade-offs acknowledged | bold lead-in | yes | colon closes bold span; assertion on same line; trailing caveat carries `no chain — flagged assumption only` marker (disclosed, still untraced for that clause) | C2, C3 |
| Pre-check (§6) | bold lead-in | yes | pre-check line is itself a claim, cited by the chains its own `head` names | C1, C2, C3, C4 |
| Confidence | bold lead-in | yes | colon closes bold span; assertion on same line | C1, C2, C3, C4 |

Scan complete: 4 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per construct in order — 5 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Adversarial pass (process output)

**Recompute.** All figures used are direct citations rather than combined/derived arithmetic, so recompute here means checking each citation's own arithmetic: 14/267 = 5.24% ≈ "5%" (GT-2, correct); 12/267 = 4.49% ≈ "4%" as reported (GT-2, correct, rounds down slightly but within the source's own stated figure); 11/267 = 4.12%, consistent with "both" being a subset of each (GT-2, correct); four-fifths = 4/5 = 0.80 = 80%, matching the EEOC threshold description (GT-4?, arithmetically trivial and correct). No chain in §4 combines these into a further computed headline number, so no compounded-figure recompute is applicable beyond this citation check.

**Sensitivity.** The single ground truth whose falsity would flip the most of this analysis is GT-2 (the ≈5%/4% "null compliance" finding); it is read-at-source and not `?`-marked. If a specific new national proposal turned out to be much better resourced and achieved materially higher verified compliance, chain C3 would weaken substantially. Chains C1 and C4 (definitional/schema arguments) do not depend on GT-2 and would be unaffected. Chain C2 — the analysis's logical core (source-naming ≠ bias-detection) — depends on GT-4?, not GT-2, and remains the most robust component regardless of how C3 resolves; weakest link overall: GT-4?'s unread primary citation (Phase 3 failure records in §3).

**Rival — headline conclusion.** Strongest rival: "a well-designed version of this rule (granular outcome-linked schema + independent verification + enforcement funding + private right of action) would achieve the stated aim." Not ruled out in general — it is the explicit scope-limit carried on the Conclusion's confidence line and in the Disposition entries below; it is ruled out only for the generic, as-commonly-proposed rule (A4–A10) this analysis addresses.

**Rival — each chain.** C1: "the specific new statute could itself prescribe a granular schema" — live, unsettled (see C1's own confidence line). C2: "a named source can be an indirect bias red flag when independently documented as biased" — ruled out for the general/default case by GT-9, via §5 Dead End 2. C3: "reputational/market deterrence alone drives compliance" — ruled out by GT-2/GT-3, via §5 Dead End 1; the broader rival "a differently designed enforcement regime could avoid this pattern" remains live and unsettled. C4: "anonymized/aggregated disclosure could serve both privacy and diagnostic goals" — live, unsettled, explicitly out of scope (see C4's own confidence line).

**Premise.** The headline conclusion is already false: the rule, as proposed, does successfully enable detection and reduction of discriminatory hiring bias.

**Causes (unfiltered, generated from the regulator's, the vendor's, the job-seeker/advocate's, the legislature's, and a competitor's viewpoints, before any grouping):**
1. (Regulator) The implementing regulations actually require a demographic/statistical breakdown alongside source names, not just names.
2. (Regulator) The regulator funds a dedicated audit/verification unit and randomly samples covered employers, unlike LL144's complaint-driven model.
3. (Legislature) The statute includes a private right of action or statutory damages, making noncompliance costly enough to drive high compliance, unlike Colorado's AG-only enforcement.
4. (Vendor) Large hiring-AI vendors voluntarily standardize on a disclosure template more granular than the legal minimum (echoing "datasheets for datasets"), because enterprise customers demand it contractually.
5. (Job seeker/advocate) A well-funded NGO or newsroom builds and maintains a public aggregator of disclosures, solving the findability problem GT-2's methodology measured directly, even if individual employer pages stay hard to find.
6. (Competitor) A rival vendor with cleaner data practices uses competitors' disclosed source lists in marketing to pressure the market, creating a reputational dynamic distinct from the employer-level pressure that failed under LL144.
7. (Regulator) The disclosure requirement is paired with a rebuttable legal presumption of discrimination triggered by incomplete or vague disclosure, giving firms a strong incentive to be specific.

**Clusters.**
- Cluster A — "Schema specificity fix" (causes 1, 7) — bears on C1, C2 (GT-7, GT-8): if the disclosure schema is legally forced to carry outcome/statistical content, C2's definitional gap closes.
- Cluster B — "Enforcement/verification fix" (causes 2, 3) — bears on C3 (GT-2, GT-3): materially stronger verification and penalties than LL144's could break the null-compliance pattern.
- Cluster C — "Third-party aggregation/market fix" (causes 4, 5, 6) — bears on C3's second- and third-order extension: external actors could substitute for weak individual-employer compliance.

**Disposition.**
- Cluster A — accepted as an explicit scope-limit on C1/C2/the headline conclusion: the Conclusion's confidence line and "what would raise the band" list both name a schema-mandating implementing rule as the specific, checkable condition that would flip this cluster from hypothetical to load-bearing; not resolved by revising the chains, because the conclusion is deliberately scoped to the rule "as commonly proposed" (A1, A4, A6).
- Cluster B — accepted as an explicit scope-limit on C3, already named on C3's own confidence line (A5, A7, A9) and bounded by §5 Dead End 1 (which rules out reputational deterrence *alone*, not stronger verification-plus-penalties).
- Cluster C — accepted as an explicit residual risk on the headline conclusion, flagged rather than incorporated as a finding because this analysis did not independently verify third-party-aggregation dynamics for the hiring-AI-disclosure domain specifically (it is observed in adjacent domains such as privacy-policy/cookie-consent tracking) — no chain — flagged assumption only.

**Falsification.** This conclusion is false if, following enactment of a rule of the generic type described here, independent post-enactment measurement (analogous to the LL144 field study behind GT-2/GT-3) finds that a materially large share of covered employers/vendors both comply with granular, outcome-relevant disclosure and that measured adverse-impact ratios in the affected hiring population improve beyond pre-rule baselines, with the improvement attributable to the disclosure requirement itself rather than to accompanying audit or enforcement provisions enacted alongside it.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "When a national regulator requires every AI system used in hiring to publish its training-data sources, what concrete institutional and behavioral responses actually follow, and does the resulting information regime give the regulator (or anyone else) the ability to detect or reduce discriminatory bias in hiring AI — the aim such rules are consistently justified by?"
Band: **Rigorous**
Justification: The statement names the underlying question (does the disclosed information actually enable bias detection) rather than restating the prompt's surface request or the triggering proposal, and each of the four success criteria is a checkable verb+subject+outcome test scannable against the Conclusion section without further interpretation.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "C1 | 2 | regulated entities converge on least-specific compliant disclosure | A4 (already in table) | yes (pre-existing)" together with the Assumptions Table's A4 row: "Accept — em-dash: expires only if a specific granular schema is legally mandated (see A6); not expired under the generic reading this analysis addresses."
Band: **Rigorous**
Justification: All ten rows use the four-type scheme correctly, every Verdict cell uses the token-then-em-dash form, every current-constraint row records its expiry condition in the em-dash justification, the inversion procedure surfaced five load-bearing untested beliefs (A6–A10) that the Assumption Audit scan confirms were already captured before Phase 4 needed them, and at least one assumption (A3) is explicitly challenged rather than merely accepted.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: GT-4, GT-6, GT-9 (3 of 9)." — checked against the Ground Truths list, which carries a `?` suffix on exactly GT-4, GT-6, and GT-9 and no others.
Band: **Rigorous**
Justification: The enumeration matches the list exactly (not merely a stated count), every unsuffixed GT (GT-1, GT-2, GT-3, GT-5, GT-7, GT-8) carries a specific source more precise than "common knowledge," GT-1/GT-2/GT-3/GT-5 name their exact read-at-source location, no chain in this analysis is rated HIGH so the "every unsuffixed GT feeding a HIGH chain names its read-at-source location" clause is vacuously satisfied, and the two GT-4 Phase 3 failure records name the specific unreachable sources and reasons rather than silently dropping the `?`.

**Criterion 4: Reason Upward**
Quoted span (from the Self-audit scan's chain-form table): "C1 | GT-5, GT-6? | yes | n/a | yes | LOW | yes | none" and the equivalent rows for C2–C4, all reading `Form conforming? = yes` and `Dependency clean? = yes`.
Band: **Rigorous**
Justification: All four chains parse in the prescribed head-then-arrow-led-hops form with no chain going directly from head to conclusion without a genuine intermediate, every chain step that introduces an assumption not already in the table is marked inline with `[Assumes: X]` (confirmed by the Assumption Audit scan above), no comparison to another jurisdiction's rule is used as standalone analogy — each is grounded in a named GT about that jurisdiction's own regime (GT-1, GT-5, GT-6) — and the Abandoned Reasoning section documents three dead ends using the What-was-tried/Why-abandoned/What-it-ruled-out structure with specific, non-generic reasons.

**Criterion 5: Validate**
Quoted span: "Cluster A — accepted as an explicit scope-limit on C1/C2/the headline conclusion: the Conclusion's confidence line and 'what would raise the band' list both name a schema-mandating implementing rule as the specific, checkable condition that would flip this cluster from hypothetical to load-bearing" (Disposition, Adversarial pass record).
Band: **Rigorous**
Justification: Every chain names its weakest link and the specific verification that would close it, every MEDIUM/LOW line names its own `GT-N?` inputs and/or unresolved Rivals axis without re-explaining a cited chain, no chain rated HIGH consumes a `GT-N?` input, the overall Conclusion's LOW rating matches its weakest contributing chains (C1, C3, both LOW), and the adversarial pass record is complete — Recompute, Sensitivity, Rival, Premise, an unfiltered multi-viewpoint Causes list, Clusters citing chain/GT ids, a named Disposition per cluster (scope-limit or explicitly accepted residual risk with a named mitigation), and Falsification are all present.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the Self-audit scan's claim-inventory table): "Key insight | bold lead-in | yes | colon closes bold span; assertion on same line | C2, C4" together with the reconciliation line "5 claims under R11, 0 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every one of the five section-6 claims traces to a specific named chain (or, for the one flagged clause, carries the disclosure marker rather than a silent gap), no new reasoning is introduced in section 6 that was not already established in section 4, and the Key Insight states a non-obvious structural tension (privacy-specificity trade-off) rather than restating the Recommended approach.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy (at most one permitted). Both clearing conditions are met — **gate cleared**.

