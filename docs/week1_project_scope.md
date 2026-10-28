# Week 1 Project Scope: EthicCheck AI

**Project:** EthicCheck AI: An Explainable AI-Powered Ethics Assessment Assistant for Student AI Project Reports  
**Domain:** AI Ethics / Responsible AI / Educational Technology  
**Stage:** Preliminary individual semester project scope, 28 October 2026. Design choices and evaluation targets will be refined in Topic 2. No prototype or evaluation results are claimed.

## 1. Project Name and Domain

EthicCheck AI helps students review how their AI project reports address responsible AI principles. It will identify relevant report passages, flag possible concerns or missing evidence, and provide understandable explanations grounded in selected public guidance.

Here, **explainable** means users can inspect the report evidence, assessment criterion, guideline citation, and suggested improvement behind a finding. It does not mean generated explanations reveal a language model's internal reasoning.

## 2. Problem Statement

Students preparing AI project reports need to explain fairness, privacy, transparency, accountability, and safety. Connecting these broad principles to specific project decisions can require consulting several guidance documents and interpreting whether their reports provide adequate evidence. A report may mention a principle without explaining how the project addresses it.

EthicCheck will support undergraduate AI and computing students with formative feedback before lecturer review. Natural-language processing and retrieval are appropriate because evidence can use varied wording and appear across several report sections. A language model can connect that evidence to retrieved guidance and explain potential improvements. A checklist and keyword search will serve as baselines to test whether AI adds value.

**Initial scope:** English-language, text-based PDF or TXT reports and five categories: fairness, privacy, transparency/explainability, accountability/human oversight, and safety. The system will assess documented evidence; it cannot verify that the underlying project implements its claimed safeguards. Scanned PDFs requiring OCR, autonomous grading, legal advice, plagiarism detection, ethics certification, and high-risk deployment approval are outside the initial scope. Students and lecturers retain final judgment.

## 3. Evidence of the Problem

**Evidence 1 - Practical support for applying principles.** Dignum (2022) argues for methods, tools, awareness, and training that support responsible AI practice [S1]. This motivates investigating an educational aid for applying principles to project documentation.

**Evidence 2 - Ethical review involves multiple concerns.** UNESCO's 2021 Recommendation addresses discrimination, privacy, transparency, and accountability [S2]. This breadth motivates structured review across categories rather than treating the presence of an ethics section as sufficient evidence.

**Evidence 3 - Assessment needs context.** Microsoft's 2022 Responsible AI Impact Assessment Template asks teams to document system information, intended uses, stakeholders, and impacts [S3]. This supports collecting project-specific evidence and asking follow-up questions.

**Evidence limitations:** These sources establish a general need for responsible AI practice and structured assessment. They do not quantify difficulties among UTM students, prove lecturer workload problems, or demonstrate EthicCheck's effectiveness. Those remain untested local assumptions. In Topic 2, seek voluntary student/lecturer feedback and review permitted, anonymised examples. Record methods and participant counts before making empirical claims.

## 4. Initial Related Work / Existing Approaches

The limitations below are preliminary interpretations of suitability for the proposed student-report workflow, not claims that the sources are defective.

| Study or solution | Relevance | Key limitation for this use case |
| --- | --- | --- |
| Dignum (2022), *Responsible Artificial Intelligence - from Principles to Practice* [S1] | Discusses practical support and attention to how AI is designed and used. | A conceptual discussion rather than an implemented assistant linking uploaded report passages to feedback. |
| Microsoft (2022), *Responsible AI Impact Assessment Template* [S3] | Provides structured prompts for documenting a system and its impacts. | Requires people to supply and interpret information; the template itself does not automatically assess a student's existing report. |
| NIST (2023), *AI Risk Management Framework (AI RMF 1.0)* [S4] | Provides a voluntary, cross-sector framework for managing AI risks. | Its broad organisational scope needs adaptation into a small educational rubric; it is not a student-report assessment application. |

## 5. Engineering Gap / Limitation

Within these reviewed approaches, there is an opportunity to investigate a focused workflow connecting report evidence, a versioned set of assessment criteria, and feedback that can be checked against the original guidance. This is a proposed integration and evaluation problem. The initial scan does not establish that no similar tool exists.

The main challenges are preserving report locations during extraction, retrieving relevant guidance, distinguishing missing documentation from a demonstrated concern, and preventing unsupported conclusions. The proposed pipeline is:

1. Validate the uploaded report and extract text with page or section references.
2. Retrieve passages from a curated, versioned guidance collection.
3. Apply an explicit rubric to produce a structured draft assessment.
4. Validate report references and guideline citations; flag unsupported findings for review.
5. Present evidence, explanations, uncertainty, and suggested next steps.

Each category will use one of four descriptive outcomes: **evidence documented**, **potential concern**, **insufficient information**, or **not applicable with justification**. A documented statement is not proof of actual ethical practice. Unsupported or conflicting evidence should trigger a limitation or follow-up question, not a confident pass/fail verdict. Model, retrieval library, hosting, and storage choices remain to be selected.

## 6. Initial Project Objectives

- **O1 - Design:** To design an evidence-based assessment rubric and document-grounded workflow for the five initial categories, with criteria mapped to public guidance and reviewed for suitability for student projects.
- **O2 - Develop:** To develop a prototype that accepts supported reports and generates findings with report references, guideline citations, concise explanations, and actionable suggestions, including an insufficient-information outcome.
- **O3 - Evaluate:** To evaluate finding quality, citation support, handling of missing evidence, latency, and robustness using independently annotated synthetic or permitted anonymised examples, compared with a checklist or keyword-search baseline.

**Preliminary evaluation plan:** Begin with approximately 20 short cases held out from prompt development. Include clear concerns, documented safeguards, missing evidence, contradictions, paraphrases, and instructions embedded in report text. Seek a lecturer or suitable reviewer to check the rubric and annotations; disclose any single-annotator limitation. Measure category-level precision/recall for concerns, reviewer-checked citation support, appropriate abstention on incomplete cases, and median/95th-percentile latency on a stated setup. Compare equivalent content written in different styles. Set numerical acceptance thresholds in Topic 2 before testing. No results or performance guarantees are available in Week 1.

## 7. Target Users

**Primary users:** Undergraduate AI Engineering and computing students preparing project reports, initially within the course context.

**Secondary users:** Lecturers and project supervisors reviewing students' ethical reasoning and discussing improvements. The system will not rank students, assign marks, or decide disciplinary outcomes.

## 8. Data Sources

| Public document | URL | Proposed use |
| --- | --- | --- |
| UNESCO (2021), *Recommendation on the Ethics of Artificial Intelligence* | https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence | Establish ethical categories and support explanations. |
| NIST (2023), *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* | https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10 | Inform risk-related criteria and the assessment workflow; the publication page provides the document. |
| Microsoft (2022), *Responsible AI Impact Assessment Template* | https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf | Inform questions about project context, stakeholders, and impacts. |

These are proposed references for retrieval and rubric design, not labelled training data or proof that a student project is ethical. Record title, publisher, version/date, URL, section, and retrieval date when building the collection. Review permitted uses before ingestion. Preserve source-specific provenance where guidance differs and do not treat it as binding UTM policy.

Only source URLs and original project documentation are included in this repository. Reference PDFs and the course Lab PDF are excluded. Student reports will not be committed. Evaluation will initially use original synthetic examples; real reports require permission, removal of identifiers, and an agreed handling process. Source pages were checked on 28 October 2026.

## 9. Comparison with EduAdvisor

This comparison follows the EduAdvisor example in the supplied Topic 1 Lab, particularly pages 7-8 and 11-12.

| Aspect | Similar to EduAdvisor | Different from EduAdvisor |
| --- | --- | --- |
| Purpose | Focused educational assistance grounded in a defined document collection. | EduAdvisor answers academic-advising questions; EthicCheck gives formative feedback on report evidence. |
| Data and input | Document preparation and retrieval are required. | EduAdvisor uses university documents and a question; EthicCheck uses ethics guidance and an uploaded report. |
| Output | Source citations and understandable responses are needed. | EthicCheck also links findings to report locations and distinguishes concerns from missing information. |
| Controls | Scope checks, citation checks, evaluation, and feedback are needed. | EthicCheck additionally needs upload privacy controls, rubric validation, and tests against embedded report instructions. |
| Evaluation | Quality, groundedness, and latency matter. | EthicCheck also measures agreement with reference findings and abstention on incomplete evidence. |

EduAdvisor's named components demonstrate one possible architecture. EthicCheck's technology choices remain preliminary and will be selected based on scope, cost, privacy, and evaluation needs.

## 10. Responsible AI Risks

| Risk | Who may be harmed and how | Proposed mitigation and check |
| --- | --- | --- |
| Unsupported findings or invented citations | Students may receive misleading advice or be falsely accused of an ethical failure. | Require verifiable report/guideline references, allow insufficient-information outcomes, and review citation support on test cases. |
| Overreliance and false reassurance | Students or lecturers may treat a well-written report as proof that the actual system is ethical. | Label feedback as preliminary and limited to documented evidence; avoid certification or overall ethical scores; test unsupported claims. |
| Privacy and confidentiality | Reports may disclose student identities, participants' information, or unpublished work. | Start with synthetic examples; minimise collection, disclose external processing, avoid raw-report logs, and provide deletion controls before real-user testing. |
| Unequal feedback across styles or domains | Less fluent writers or students in unfamiliar domains may receive poorer feedback. | Disclose initial English-only support, compare equivalent paraphrases, examine domain-specific errors, and allow human correction. |
| Prompt injection in report text | Embedded instructions may suppress concerns or redirect the assistant. | Treat uploaded content as untrusted evidence, separate it from system instructions, validate outputs, and test adversarial passages. |
| Conflicting or outdated guidance | Advice may overlook context or differ from course expectations. | Version the collection and rubric, identify sources, disclose disagreements, and refer unresolved course-policy questions to the lecturer. |

## References

- **[S1]** Dignum, V. (2022). *Responsible Artificial Intelligence - from Principles to Practice*. https://arxiv.org/abs/2205.10785
- **[S2]** UNESCO. (2021). *Recommendation on the Ethics of Artificial Intelligence*. https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence
- **[S3]** Microsoft. (2022). *Responsible AI Impact Assessment Template*. https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf
- **[S4]** Tabassi, E. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10

**Assignment alignment:** Prepared using the Topic 1 Lab scoping template (pages 12-13) and Part C instructions. The course PDF remains outside the repository. Parts A and B remain pending; see [group file status](week1_group_files_pending.md).
