# EthicCheck AI

## An Explainable AI-Powered Ethics Assessment Assistant for Student AI Project Reports

> A proposed educational assistant that helps students identify possible ethical concerns and missing evidence in AI project reports, with understandable explanations linked to public guidance.

**Individual AI Engineering semester project - Week 1 scoping stage.** The application has not yet been implemented. The README and project scope are prepared; the Part A observation sheet and Part B system map are pending. GitHub publication and lecturer access still need verification.

## Problem Statement

Students writing AI project reports need to connect broad ethical principles to their specific data, methods, users, and safeguards. Relevant evidence may be spread across sections, and mentioning a principle does not show how it has been addressed. EthicCheck proposes document retrieval and language-based analysis to provide formative feedback, with a checklist/search baseline used to evaluate whether AI adds value.

## Evidence of the Problem

- Dignum (2022) calls for practical tools and training to support responsible AI practice. This motivates investigating a learning aid for students. [Source](https://arxiv.org/abs/2205.10785)
- UNESCO's Recommendation covers multiple ethical concerns, motivating a structured review rather than a single yes/no judgment. [Source](https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence)
- Microsoft's Impact Assessment Template requires information about a system and its impacts, showing the importance of project context. [Source](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf)

These sources support the general motivation. No local survey, lecturer workload measurement, or evidence of EthicCheck's effectiveness has been collected. Student needs and feasibility will be validated in later topics.

## Initial Related Work / Existing Approaches

| Study or solution | Contribution | Limitation for this project |
| --- | --- | --- |
| [Dignum (2022), Responsible Artificial Intelligence - from Principles to Practice](https://arxiv.org/abs/2205.10785) | Discusses support needed for responsible AI practice. | Does not provide an implemented student-report assessment assistant. |
| [Microsoft (2022), Responsible AI Impact Assessment Template](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf) | Structures impact-assessment information. | Relies on people to complete and interpret the assessment. |
| [NIST (2023), AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) | Provides broad guidance for AI risk management. | Requires adaptation into an educational report rubric. |

These are preliminary suitability comparisons, not a comprehensive literature review.

## Engineering Gap / Limitation

The proposed contribution is a focused workflow connecting report evidence, selected guidance, and actionable feedback. It must distinguish a documented concern from information that is absent, uncertain, or outside scope. Whether this workflow improves on a simple checklist remains an evaluation question; no claim of a unique or first-of-its-kind system is made.

## Project Objectives

- **O1:** Design a grounded assessment rubric covering fairness, privacy, transparency/explainability, accountability/human oversight, and safety.
- **O2:** Develop a prototype that accepts supported reports and generates findings with report references, guideline citations, explanations, and suggested improvements.
- **O3:** Evaluate finding quality, citation support, appropriate abstention, latency, and robustness against independently annotated examples and a checklist/search baseline.

## Target Users

The primary users are undergraduate AI and computing students preparing project reports. Lecturers and supervisors are secondary users who can use the feedback for discussion while retaining final judgment.

## Data Sources

1. **UNESCO (2021), Recommendation on the Ethics of Artificial Intelligence:** [public document](https://www.unesco.org/en/legal-affairs/recommendation-ethics-artificial-intelligence).
2. **NIST (2023), Artificial Intelligence Risk Management Framework (AI RMF 1.0):** [publication and document download](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10).
3. **Microsoft (2022), Responsible AI Impact Assessment Template:** [public PDF](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2022/06/Microsoft-RAI-Impact-Assessment-Template.pdf).

These documents are proposed reference material, not labelled training data or binding university policy. Only links are included here. Reference PDFs, the Lab manual, private reports, and credentials must remain outside the repository. Evaluation will start with original synthetic examples; any real reports require permission and anonymisation.

## Proposed Behaviour and Boundaries

The initial prototype will support English text-based PDFs and TXT reports. It will extract text, retrieve relevant guidance, draft category-level feedback, check references, and show the result for human review. Each finding should identify report evidence, a guideline citation, a short explanation, and a suggested action.

Planned outcomes are **evidence documented**, **potential concern**, **insufficient information**, and **not applicable with justification**. Explainability means traceable evidence and sources; it does not establish access to the model's internal reasoning. The system will assess what a report documents, not certify the ethics of the real system or assign student grades. OCR, legal advice, plagiarism detection, and autonomous approval are outside the initial scope.

## Responsible AI and Evaluation

Key risks are unsupported findings, overreliance, upload privacy, unequal feedback across writing styles, prompt injection, and conflicting guidance. Planned controls include source validation, explicit uncertainty, minimal retention, human review, and adversarial testing. These controls are proposed and have not yet been implemented.

Initial evaluation will use approximately 20 held-out synthetic or permitted anonymised cases, with reviewer-checked reference annotations where feasible. Measures include precision/recall for concerns, citation support, abstention on missing evidence, and median/95th-percentile latency. Numerical targets will be set in Topic 2; no results are available yet. See the [complete project scope](docs/week1_project_scope.md) for details and limitations.

## Repository Structure

```text
ai-engineering-ethiccheck-ai/
|-- README.md
|-- .gitignore
|-- docs/
|   |-- week1_project_scope.md
|   `-- week1_group_files_pending.md
|-- data/.gitkeep
|-- src/.gitkeep
|-- notebooks/.gitkeep
|-- evaluation/.gitkeep
`-- prompts/.gitkeep
```

The completed group files must later be added as `docs/week1_observation_sheet.md` and `docs/week1_system_map.png`. They are absent until the actual group work is supplied. The [pending-files note](docs/week1_group_files_pending.md) records the outstanding requirements.

## Weekly Progress

| Week | Focus | Deliverable | Status |
| --- | --- | --- | --- |
| W1 | Individual project framing and public-source review | README and ten-field project scope | Prepared; preliminary scope for student review |
| W1 | Initial project organisation | Required folders with `.gitkeep` placeholders | Prepared locally |
| W1 | Part A group observations | `docs/week1_observation_sheet.md` | Pending actual completed group file |
| W1 | Part B group system map | `docs/week1_system_map.png` | Pending actual completed group file |
| W1 | Publish and verify individual repository | GitHub commits and lecturer-accessible URL | Pending publication and verification |
| W1 | Course portal submission | Repository URL submitted through Moodle | Pending student submission |

**Week 1 is not yet fully complete.** After publishing, verify the file list and commit, check lecturer access, and update this table. Add the actual group files when available, then submit the exact GitHub repository URL through Moodle.

## Current Usage

This repository currently contains project documentation only. There is no executable application, dependency installation, or demonstration to run. Read the [Week 1 project scope](docs/week1_project_scope.md) first. Implementation and setup instructions will be added as the project develops.
