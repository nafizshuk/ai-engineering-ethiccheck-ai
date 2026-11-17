# Week 3 data inventory - EthicCheck AI

**Pathway A, UTF-8 TXT.** Lab 3 uses two small, project-authored guides as the first corpus for the **C4 versioned knowledge access** component in the [Week 2 architecture](week2_architecture_v1.png). The guides are retrieval inputs covering five ethics categories. They contain review prompts and original examples for student AI reports. The official NIST reference for each criterion is tracked separately.

## A1. Requirement-to-data mapping

| Week 2 requirement | Data needed | Selected source and usable boundary |
| --- | --- | --- |
| FR4 | A rubric criterion, the source section behind it and a precise location | S01 and S02 contain named criteria. Each output carries the local TXT line range and the relevant [NIST AI RMF section](https://doi.org/10.6028/NIST.AI.100-1). Student report evidence will be supplied separately later. |
| RAI1 | Source identity and resolvable references for later evidence checks | Source filenames, version 1.0, SHA-256, line locations and official section numbers are recorded in each record. E4 will still need a reviewer to verify whether a claim is supported. |
| NFR5 | Versioned input and repeatable updates | Both inputs and exports have content fingerprints. The pipeline rejects unexpected byte changes and reruns after deliberate source updates. Week 2's five citation checks and ten-minute update target remain future E12 tests. |

## A3-A4. Inspected sources

| ID | Filename and authoritative reference | Format and purpose | Version, date, owner | Access and rights | Observed ingestion evidence |
| --- | --- | --- | --- | --- | --- |
| S01 | [data_and_fairness.txt](../data/sources/data_and_fairness.txt). [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) §§3.6-3.7. | UTF-8 TXT. Privacy and fairness review criteria. | EthicCheck guide 1.0, 17 November 2026, EthicCheck AI project. NIST reference published January 2023. | Original project material authored for the public repository. The cited framework is [publicly accessible from NIST](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf). | 1,170 bytes, 11 lines, 2 sections and 4 paragraphs. PRI-01 line 3 asks which information enters the application and who can access it. |
| S02 | [risk_and_oversight.txt](../data/sources/risk_and_oversight.txt). [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) §§3.2, 3.4 and 3.5. | UTF-8 TXT. Safety, accountability/human oversight and transparency/explainability review criteria. | EthicCheck guide 1.0, 17 November 2026, EthicCheck AI project. NIST reference published January 2023. | Original project material authored for the public repository. The cited framework is [publicly accessible from NIST](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf). | 1,644 bytes, 17 lines, 3 sections and 6 paragraphs. SAF-01 line 3 asks for a plausible failure and who could be affected. |

Both files decoded and all five expected headings were found. Blank lines separated the paragraphs. The parser accepts an optional UTF-8 BOM and handles line endings while preserving physical line numbering. Source line numbers refer to these TXT guides. For the original guidance, use the recorded report number, year and section link.

The Week 2 scope listed NIST, UNESCO and Microsoft as candidate guidance. This first batch uses NIST-linked project criteria because the two direct NIST PDF download endpoints returned HTTP 403 in the execution environment. The guides contain original instructional text rather than downloaded PDF content. Their shallow coverage and interpretation of guidance still need reviewer input. Expansion to original documents with page-level provenance is later work.

## Storage and lineage

- Raw project inputs live in [data/sources](../data/sources). Private reports, reference PDFs and the course handout stay outside the public corpus.
- The Part B [export](../data/processed/prepared_text.jsonl) and [lineage manifest](../data/week3_manifest.json) capture the preparation comparison and source-to-output links.
- The Part C [export](../data/pipeline_v1/text/prepared_text.jsonl) and [run manifest](../data/pipeline_v1/text/pipeline_manifest.json) capture executed outputs and repeatability evidence.
- The [notebook](../notebooks/week3_pipeline.ipynb) saves these outputs below its working directory. Colab uses temporary storage at `/content/ethiccheck-week3`.
