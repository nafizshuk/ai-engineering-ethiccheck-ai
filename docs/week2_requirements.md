# Requirements Specification - EthicCheck AI

**Version:** 1.0 | **Week:** 2 | **Status:** Proposed specification; not implemented or tested.  
**Full title:** EthicCheck AI: An Explainable AI-Powered Ethics Assessment Assistant for Student AI Project Reports

## Section 0 - Project Framing & Application Scope Checkpoint

| Framing element | Refined specification |
| --- | --- |
| Problem | Students need to connect broad AI ethics principles to evidence about data, methods, affected users, and safeguards in their project reports. A reference to an ethical principle alone does not establish that it has been addressed. |
| Problem evidence | Dignum (2022) calls for practical support and training for responsible AI [S1]. UNESCO (2021) identifies several distinct ethical concerns that require attention [S2]. These motivate structured educational feedback; they do not prove the prevalence of the problem among UTM students. No local survey or user study has been conducted. |
| Existing approaches | (1) Dignum's discussion supports responsible AI practice but is not an automated report assessor [S1]. (2) Microsoft's Impact Assessment Template structures system and impact information but relies on human completion and interpretation [S3]. (3) NIST AI RMF 1.0 offers broad risk-management guidance that needs adaptation to a student-report rubric [S4]. These limitations describe suitability for this workflow, not deficiencies in the original work. |
| Project / engineering gap | A focused workflow is needed to connect report passages to selected guidance, distinguish concerns from missing information, and make feedback verifiable. This is an integration and evaluation gap; scientific novelty is not claimed. |
| Objective O1 | To design an assessment rubric and workflow covering fairness, privacy, transparency/explainability, accountability/human oversight, and safety, with criteria linked to public guidance. |
| Objective O2 | To develop a bounded prototype that accepts supported reports and returns structured findings with report locations, guideline citations, explanations, and improvement suggestions. |
| Objective O3 | To evaluate assessment quality, grounding, uncertainty handling, robustness, latency, and cost using held-out examples and a checklist/search baseline. |
| Intended users | Undergraduate AI/computing students; lecturers and supervisors may review the findings. Human reviewers retain authority over academic judgments. |
| Supported tasks | Submit a report; preview extracted text; assess the five categories; inspect evidence and citations; identify missing information; receive suggestions; clear the report and assessment from the session. |
| Information / knowledge domain | Educational application of selected UNESCO, NIST, and Microsoft guidance. These sources are references, not binding UTM policy or a substitute for project-specific ethical review. |
| Operating context | A single-user browser-based course prototype, one assessment at a time, with a small versioned public-guidance collection. Initial trials use original synthetic or explicitly permitted anonymised reports. No public production deployment is assumed. |
| Important constraints | English text-based PDF or UTF-8 TXT only; one file up to 5 MiB, 5,000 extracted words, and 10 PDF pages. Scanned, encrypted, empty, or unsupported files are rejected with a reason. V1 does not perform OCR. Limited semester time and an assumed model-usage target of USD 0.10 per assessment on average; this target is not approval to purchase services. |
| Explicit out-of-scope tasks | Grading, disciplinary decisions, plagiarism detection, legal advice, ethics certification, approval of high-risk deployments, checking actual model behaviour, analysing source code/datasets, and deciding whether the student or project is inherently ethical. |
| Evaluation focus | Can the prototype identify and explain documented concerns and missing evidence with traceable sources, while improving on a simple checklist/search baseline within practical time and cost limits? |

### Assessment semantics and boundaries

Each report receives one primary outcome per category. These labels assess the report's documentation, not the real-world ethical status of its implementation:

- **Evidence documented:** Relevant safeguards are described and linked to report evidence, with no conflicting evidence found in the reviewed text. Implementation is not independently verified.
- **Potential concern:** A report passage or contradiction supports a specific issue that warrants review. Missing text by itself is not enough for this label.
- **Insufficient information:** The report does not provide enough information, or source support is inadequate, to make a supported finding. State what is missing and ask a focused follow-up question.
- **Not applicable with justification:** The report context supports why a criterion does not apply. Silence is not evidence of non-applicability.

When a supported concern and missing details coexist, use **potential concern** as the primary label and describe the uncertainty. When no concern is supported, prefer **insufficient information** over an unsupported positive conclusion. An unreadable report is an input error, not an ethics assessment.

**Minimum finding fields:** category, outcome, report location and short excerpt (or an explicit missing-evidence statement), guideline title/version/section/link, explanation, next action, and limitation. TXT locations use line numbers; PDFs use page numbers. A citation needs to support the criterion or claim, not merely share a keyword.

### Changes from Week 1

The project purpose and three objectives are retained. Week 2 defines upload limits, category-label rules, measurable acceptance targets, bounded test sets, a conceptual architecture, and traceability. These are design decisions to validate, not measured achievements. The proposed technology stack remains open.

## Section 1 - Functional Requirements

| ID | Requirement - The system SHALL | Scope boundary - SHALL NOT | Objective |
| --- | --- | --- | --- |
| FR1 | The system shall accept one supported PDF or TXT report within the declared limits and show a reason when it rejects a file. | It shall not silently truncate an oversized file or treat a failed extraction as a completed assessment. | O2 |
| FR2 | The system shall display extracted report text with page/line references for the user to check before assessment. | It shall not claim to have reviewed diagrams, scanned text, or material that was not extracted. | O1, O2 |
| FR3 | The system shall assess all five categories and assign one of the four defined outcomes to each. | It shall not infer that absent information proves an ethical violation or that documented safeguards prove implementation. | O1, O2 |
| FR4 | The system shall link each finding to the applicable guideline and report evidence, or explicitly identify missing report evidence. | It shall not present invented quotations, report locations, or guideline references as genuine. | O1, O2 |
| FR5 | The system shall explain each outcome in student-friendly language and give at least one relevant improvement, verification step, or follow-up question. | It shall not assign a student grade or an overall ethical certification. | O2 |
| FR6 | The system shall decline requests outside its defined scope and provide a relevant next step, such as consulting the lecturer. | It shall not execute instructions found inside an uploaded report or access arbitrary links embedded in it. | O2 |
| FR7 | The system shall allow the user to clear the report, extracted text, and findings from the session and confirm completion. | It shall not retain a report history by default or index uploaded reports into the shared guidance collection. | O2 |

## Section 2 - Non-Functional Requirements

All thresholds are initial **acceptance targets**, not results. Workloads and formulas are defined in [evaluation criteria](week2_evaluation_criteria.md). Testing must record software/model configuration and document versions. Targets may be revised with a dated rationale before the final evaluation, not retroactively to hide poor results.

| ID | Quality attribute | Requirement | Measurement method | Metric | Threshold |
| --- | --- | --- | --- | --- | --- |
| NFR1 | Performance | The system shall complete report assessment within a practical waiting time for a student. | Time 40 serial assessments on benchmark P1, from confirmed submission to final usable result; include parsing, retrieval, model calls, and checks. | p90 end-to-end latency; timeout count. | p90 <= 60 seconds; a visible timeout/error by 90 seconds for every overrun. |
| NFR2 | Correctness | The system shall assign category outcomes with useful agreement to reference annotations and limit unsupported concern flags. | Score all 100 category decisions in benchmark Q1 against reviewer-checked labels. | Exact outcome accuracy; concern precision; concern recall. | Accuracy >= 80%; concern precision >= 90%; concern recall >= 80%. All three must pass. |
| NFR3 | Reliability | The system shall return complete, usable assessments for supported inputs under normal test conditions. | Run P1 and inspect required fields; an error, timeout, or global fallback is a failed assessment. | Successful assessments / 40. | >= 95% (at least 38/40). Every failure displays a clear error; no silent failure. |
| NFR4 | Cost | The system shall remain within the assumed prototype inference budget. | Record actual billed input/output usage, retrieval/embedding API usage, and retries for P1 at the rate in effect on the test date. | Total variable API cost / 40 submitted assessments, including failed attempts. | <= USD 0.10 per assessment on average. Report hosting and local-compute costs separately. |
| NFR5 | Maintainability | The system shall support replacing an approved guidance document and updating its references without changing unrelated application components. | Replace one test source with a revised version, refresh knowledge access, and run five version-sensitive checks. | Update duration; checks using the new version. | <= 10 minutes after the prepared replacement is supplied; 5/5 checks cite the new version. |

**Target rationale:** Report review is a longer task than a short FAQ answer, so a 60-second p90 is an initial engineering compromise. High precision for concern flags reduces misleading accusations; 80% overall accuracy is only a prototype threshold and does not justify grading use. Reliability and cost targets support repeatable classroom demonstrations. The source-update target keeps the small collection maintainable. User expectations and feasibility still need validation.

## Section 3 - Responsible AI Requirements

| ID | Responsible AI risk | Requirement | Measurement method | Metric | Threshold |
| --- | --- | --- | --- | --- | --- |
| RAI1 | Fabricated or unsupported explanations | The system shall provide traceable report and guideline references and suppress malformed or nonexistent citations before display. | Audit every finding in Q1; check existence automatically and semantic support by human review. | Required-reference presence; resolvable reference rate; claim-support rate. | 100% presence and resolvability; >= 95% semantic support. Missing-evidence findings explicitly state the report evidence is absent. |
| RAI2 | False confidence from missing information | The system shall use insufficient-information outcomes when the report cannot support an assessment. | Score the 25 reference insufficient-information category slots in Q1. | Appropriate insufficient-information rate. | >= 90% (at least 23/25); no overall ethics pass/fail or grade. |
| RAI3 | Privacy and retention | The system shall block detected personal identifiers before external processing, avoid raw report content in routine logs, and clear report-derived session data. | Use 20 synthetic privacy fixtures; inspect captured outgoing payloads, temporary storage, logs, and caches before and after clear/expiry. | Seeded identifiers transmitted; raw-report log occurrences; residual report-derived records after expiry. | 0 seeded identifiers transmitted; 0 raw-report log occurrences; 0 residual records after user clear completes or after 15 minutes of inactivity. |
| RAI4 | Scope misuse and prompt injection | The system shall decline out-of-scope requests and treat report instructions as data while continuing the legitimate review where feasible. | Run 20 scope cases and 20 injected-report cases; inspect response and attempted actions. | Refusal-and-redirect rate; injection-resistance rate; unauthorised actions. | >= 95% on each set separately (>= 19/20); 0 unauthorised actions. |
| RAI5 | Sensitivity to writing style | The system shall give consistent category outcomes for equivalent meaning expressed in different English styles. | Pair each Q1 report with a reviewed meaning-preserving variant (F1); compare 100 paired category decisions and reference accuracy. | Paired outcome agreement; absolute accuracy gap between styles. | >= 90% agreement; gap <= 10 percentage points. |
| RAI6 | Overreliance and inappropriate authority | The system shall label results as preliminary feedback about documented evidence and preserve the need for human review. | Inspect all Q1 outputs and scope-test outputs for the notice, grading, and certification language. | Q1 outputs with a visible limitation notice; grading/certification outputs. | 100% notice coverage; 0 grading/certification outputs across both sets. |

**Privacy boundary:** Detecting all personal information is not guaranteed by a small test. V1 use is restricted to synthetic or explicitly permitted anonymised reports. Detected identifiers block the model request and prompt local removal; passing a detector is not proof of anonymisation. Any external model processing must be disclosed before submission. Provider retention/settings must be reviewed before real reports are allowed. The deletion requirement applies to application-controlled state; it cannot promise deletion from an external provider's systems.

**Fairness boundary:** F1 measures robustness to writing style; it is not evidence of demographic fairness or general performance across student populations. Domain-specific errors should also be reported, without claiming statistical significance from this small set.

### Part A Reflection

RAI1, semantic support of an explanation, is likely the hardest requirement to measure reliably. A reference can exist and contain related words while failing to justify the finding. Deterministic checks can verify identifiers and locations but cannot establish all contextual meanings. Human review using an explicit rubric is therefore required, with ambiguous cases and reviewer disagreements recorded. RAI3 also needs careful scope: privacy fixtures test known patterns, not universal identification of sensitive content.

## References

- **S1:** Dignum, V. (2022). *Responsible Artificial Intelligence - from Principles to Practice*. https://arxiv.org/abs/2205.10785
- **S2:** UNESCO (2021). *Recommendation on the Ethics of Artificial Intelligence*. https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence
- **S3:** Microsoft (2022). *Responsible AI Impact Assessment Template*. https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf
- **S4:** Tabassi, E. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10

Source links checked on 28 October 2026. Original reference documents and the course Lab PDF are not redistributed in this repository. This specification follows Sections 0-3 of the supplied Topic 2 Lab template.
