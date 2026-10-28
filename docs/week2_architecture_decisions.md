# V1 Architecture Decisions and Traceability - EthicCheck AI

**Version:** 1.0 | **Week:** 2 | **Status:** Conceptual design; no implementation, deployment, or test results claimed.

- [Architecture diagram](week2_architecture_v1.png)
- [Editable Draw.io source](week2_architecture_v1.drawio)
- [Requirements](week2_requirements.md)
- [Evaluation criteria](week2_evaluation_criteria.md)

## 1. Start with the Simplest Architecture

**Student report -> Application interface -> AI assessment capability -> Feedback.**

This basic flow supports interaction but does not by itself preserve report locations, supply approved references, enforce upload/privacy boundaries, validate citations, or provide repeatable evaluation. V1 adds only the capabilities needed for these requirements. Components are logical responsibilities; they can initially run within one small application rather than separate services.

## 2. Architecture Needs Derived from Requirements

| Requirement ID | What does the requirement need? | Architecture response |
| --- | --- | --- |
| FR1, FR2 | Supported-file checks and reviewable extracted text with locations. | C1 interface and C2 intake/extraction gate. |
| FR3, FR4, NFR2, RAI1, RAI2 | Relevant guidance, explicit outcome rules, report evidence, and verifiable references. | C3 temporary report context, C4 versioned knowledge access, C5 rubric/orchestration, C6 language-model capability, and C7 validation. |
| FR5, RAI6 | Readable feedback that does not assume grading or certification authority. | C8 feedback presentation with an uncertainty/limitation notice and human review. |
| FR6, RAI4 | Scope enforcement and separation of document text from instructions. | C2 input checks, C5 bounded assessment instructions, C6 with no tools or browsing, and C7 output checks. |
| FR7, RAI3 | Data minimisation, outbound privacy checks, and deletion of report-derived state. | C2 local privacy gate and C3 session lifecycle; all downstream application state is session-scoped. |
| NFR1, NFR3, NFR4 | A bounded request path, deadline handling, and observable runtime/usage. | C5 one assessment workflow with a 90-second deadline; C9 records non-content timing, status, and usage data. |
| NFR5 | Source replacement and version-aware references without unrelated code changes. | C4 source metadata and refresh capability, checked by C9. |
| RAI5 and objective O3 | Repeatable quality, style, privacy, and safety checks. | C9 offline evaluation harness using versioned synthetic fixtures and human-reviewed annotations. |

## 3. Component Responsibilities and Major Flows

| ID | Component | Responsibility and boundary |
| --- | --- | --- |
| K0 | Approved public guidance | The selected UNESCO, NIST, and Microsoft references. Use permitted local copies and preserve publisher/version/section provenance. Reference PDFs are not uploaded to this repository. |
| C1 | Student / application interface | Explain scope and processing; accept a file; show extraction preview; obtain confirmation to assess; allow clear-session; show errors and results. |
| C2 | Intake, extraction, and privacy gate | Check format/size/page/word limits, extract page or line references, and block detected identifiers before any external model request. Unreadable or disallowed inputs return a reason to C1. Detector success does not prove absence of personal information. |
| C3 | Temporary report session | Hold report-derived text and locations only for the active session. Do not add it to C4. Clear the file, text, prompts, cached outputs, and findings when the user clears the session or after 15 minutes of inactivity; cancel/discard in-flight work so it cannot repopulate a cleared session. |
| C4 | Versioned knowledge access | Prepare and retrieve relevant guidance with stable source identifiers and versions. Keep public reference material separate from uploaded reports. Search/retrieval technology will be selected later. |
| C5 | Assessment orchestration and rubric | Combine the rubric, permitted report evidence, and relevant guidance. Keep untrusted content separate from system instructions. Request the five-category structured result and enforce the deadline. A request with insufficient source support must abstain or return a clear error. |
| C6 | Language-model capability | Generate proposed findings and concise explanations from the supplied evidence. It has no arbitrary browsing, code execution, or action tools. Deployment location/model/provider remain undecided; only permitted input may cross an external boundary. |
| C7 | Evidence and output checks | Verify required fields, allowed outcome labels, source IDs, report locations, and prohibited grading/certification fields. Suppress malformed or nonexistent references. If checks fail, return an explicit assessment error or justified insufficient-information finding; never silently declare success. Semantic correctness still requires E4 human audit. |
| C8 | Feedback and human review | Show five outcomes, report evidence or a missing-information statement, source citations, explanations, and next actions. State that the review covers documentation only. Students and lecturers interpret and correct the findings. |
| C9 | Offline evaluation and measurements | Exercise C2-C8 with synthetic fixtures, apply E1-E12, and collect timing/status/usage without raw-report routine logs. Human review supplies semantic-support and clarity scores. The harness is a development capability, not a production learning or surveillance loop. |

### Information flow

1. K0 supplies approved guidance to C4; refresh sources separately from report processing.
2. The student uses C1 to submit a supported file. C2 validates and extracts it; C1 shows a preview for confirmation. Rejected inputs return a reason before assessment.
3. C3 holds the permitted report context temporarily. C5 receives that context and relevant, versioned evidence from C4.
4. C5 supplies an explicit rubric, bounded instructions, and evidence to C6. C6 returns a draft to C7.
5. C7 checks structure and references, then C8 presents checked feedback or a clear failure/insufficient-evidence result for human review.
6. C9 tests the components and records evaluation evidence. It does not ingest private reports or automatically retrain the system.

**Failure behaviour:** Input failure stops before model processing. Retrieval failure produces an explicit source-unavailable error rather than general model advice. Malformed findings are suppressed; V1 does not require an automatic retry. A model timeout returns an error by 90 seconds. Any later retry policy must be bounded, measured for cost/latency, and documented. Clear-session also invalidates pending results.

## 4. Architecture Decision Records

| Decision | Requirement / constraint | Alternatives considered | Selected option | Trade-off accepted |
| --- | --- | --- | --- | --- |
| ADR1 - Ground assessment in a small approved collection | FR4, NFR2, RAI1; verifiable sources required. | Model memory only; manual checklist/search only; grounded generation with knowledge access. | C4 retrieves guidance and C5 passes it with source IDs to C6. Retain the checklist/search baseline for E2. | More preparation and reference-handling work than model-only generation; retrieval can still miss relevant guidance. Better traceability must be demonstrated rather than assumed. |
| ADR2 - Use explicit rubric and descriptive outcomes | FR3, RAI2, RAI6; feedback must not become autonomous ethical judgment. | Free-form commentary; a single numerical ethics score; five categories with four defined outcomes. | C5 enforces category rules and C7 validates the output schema; C8 displays limitations. | Less flexible output and more rubric-design work, but clearer evaluation and appropriate abstention. |
| ADR3 - Keep reports session-scoped and separate from guidance | FR7, RAI3; no default report history. | Save all reports; mix reports into the knowledge index; use temporary report context. | C3 holds report-derived state temporarily; C2 checks outbound content; C4 stores approved guidance only. | Users cannot retrieve previous reports automatically and must resubmit after expiry. Extra lifecycle testing is required. |
| ADR4 - Combine mechanical checks with human semantic evaluation | RAI1, NFR2; a valid citation can still be irrelevant. | Prompt instructions alone; automated citation checks alone; mechanical checks plus offline human audit. | C7 checks existence/structure and C9 supports reviewer audits for meaning. | Human review is slower and may vary between reviewers; automatic checks alone cannot establish correctness. |
| ADR5 - Bound V1 inputs and execution | FR1, NFR1, NFR3, NFR4; semester feasibility and limited budget. | Arbitrary report sizes and OCR; bounded text inputs; extensive multi-agent workflow. | Text PDF/TXT limits, one request at a time, a compact orchestration path, and no automatic retry by default. | Rejects scanned/long reports and may be less capable on complex cases, but creates a testable scope. |

No vendor, foundation model, vector database, UI framework, or evaluation platform is mandated in V1. No multi-agent workflow, web crawler, user-account system, or persistent report-history service is justified at this stage.

## 5. Initial Requirements Traceability Matrix

The evidence column lists **future artefacts**, not existing test results. O3 evaluates the behaviours designed under O1 and implemented under O2.

| Objective | Requirement | Evaluation criterion | Architecture element | Later evidence |
| --- | --- | --- | --- | --- |
| O2 | FR1, FR2 | E1 input and extraction checks | C1, C2 | U1 outcome checklist and 12 checked passage locations. |
| O1, O2, O3 | FR3, NFR2 | E2 assessment quality | C3-C7 | Q1 reference labels, predictions, confusion matrix, and baseline comparison. |
| O1, O2, O3 | FR4, RAI1 | E4 citation support | C4-C7, C9 | Source/report reference audit and reviewer claim-support scores. |
| O2, O3 | FR3, RAI2 | E3 incomplete evidence | C5, C7, C8 | Outcomes for the 25 reference insufficient-information slots. |
| O2 | FR5 | E5 clarity | C6, C8, C9 | Four-item clarity scores with reviewer failure explanations. |
| O2, O3 | NFR1, NFR3 | E6 latency and reliability | C2-C8, C9 | All 40 timed attempts, errors, p90, and usable-completion count. |
| O3 | NFR4 | E7 variable API cost | C5, C6, C9 | Usage totals, dated unit rates, and average including failed attempts. |
| O2 | FR7, RAI3 | E8 privacy and clearing | C1-C3 and session-scoped C5-C8 | Synthetic outbound-payload audit and clear/expiry/failure cleanup checks. |
| O2, O3 | FR6, RAI4 | E9 scope and injection | C2, C5-C7, C9 | Separate S1/J1 case outcomes and attempted-action audit. |
| O3 | RAI5 | E10 equivalent styles | C5, C6, C9 | Q1/F1 paired labels, agreement, and accuracy-gap calculation. |
| O2 | FR5, RAI6 | E11 human authority | C5, C7, C8 | Notice-presence checks and grading/certification audit. |
| O1, O3 | NFR5 | E12 source refresh | C4, C9 | M1 update timing, source-version manifest, and five reference checks. |

## 6. V1 Design Review

- Each major component maps to an input, evidence, privacy, output, or evaluation requirement in the tables above.
- The diagram includes the student/interface, approved guidance, report handling, AI capability, output, and evaluation point. Report content and public knowledge are separated.
- The first prototype can use one application process plus a model capability; the diagram does not require a separate service for each box.
- Source search, model selection, privacy implementation, and hosting are deferred until later technical work. No specific stack is being presented as already implemented.
- Mechanical citation validation does not prove semantic truth. E4 and the reference-label review remain necessary.
- Threshold feasibility, local student needs, model/provider data handling, and human review availability remain open validation items.

## Part C Reflection

ADR1 has the most important usefulness trade-off. FR4 and RAI1 require findings that students can verify, so approved knowledge access and source identifiers are included instead of relying only on model memory. This adds preparation work, retrieval failure modes, and processing time. The trade-off is justified only if E2 and E4 show useful assessment quality and evidence support within E6/E7 limits. If those benefits are not observed, the project should simplify or revise its approach rather than claim that a more complex architecture is automatically better.
