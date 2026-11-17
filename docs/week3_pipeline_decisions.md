# Week 3 pipeline decisions - EthicCheck AI

The [Week 3 workflow](week3_pipeline_diagram.png) expands **C4 versioned knowledge access** from the [Week 2 design](week2_architecture_decisions.md). It prepares the reference side of FR4 and RAI1 and records the source identity needed for NFR5. Work on user report intake (C2-C3), semantic citation checking (C7), assessment generation and the E4/E12 evaluations follows the Week 2 plan.

## Preparation comparison

Both configurations processed the same five normalised criterion sections from S01 and S02 with a maximum of 520 characters, no overlap and no crossing of a criterion heading. A within-paragraph cut is a chunk boundary inside a paragraph. A word split separates adjacent alphanumeric characters at the boundary.

| Criterion | Fixed records / within-paragraph cuts / word splits | Paragraph-aware records / within-paragraph cuts / word splits |
| --- | --- | --- |
| PRI-01 | 2 / 1 / 0 | 2 / 0 / 0 |
| FAI-01 | 2 / 1 / 1 | 2 / 0 / 0 |
| SAF-01 | 2 / 1 / 1 | 2 / 0 / 0 |
| ACC-01 | 1 / 0 / 0 | 1 / 0 / 0 |
| EXP-01 | 1 / 0 / 0 | 1 / 0 / 0 |
| **Total** | **8 / 3 / 2** | **8 / 0 / 0** |

**Selected configuration** groups complete paragraphs within each heading where they fit. A long paragraph can split at whitespace. The sample preserved all paragraph and word boundaries while keeping the same record count. This supports FR4 and RAI1 by keeping each criterion's evidence together and retaining its source lines. For example, `S01-PRI-01-01` covers line 3 of S01 and links the privacy criterion to NIST §3.6. NIST is the reference for the criterion and the TXT file is the immediate source of the chunk.

**Accepted limitations** include shorter chunks near some boundaries and the possibility that context spans two chunks. The 520-character cap is a lab setting and does not establish a retrieval or token-length optimum. The comparison measures boundaries on a small, structured TXT corpus. Retrieval relevance and semantic support still require E4 and the next quality lab.

## Workflow and stage contracts

| Stage | Contract and observed evidence | Failure response |
| --- | --- | --- |
| Select / ingest | Two exact paths, known UTF-8 files and SHA-256 values, with ownership and rights in the [inventory](week3_data_inventory.md). | Missing input stops the run. Edit the approved input list and fingerprints only after reviewing a deliberate source change. |
| Inspect | Both files decode. All five expected criterion IDs are assigned and every criterion has text. | Stop for undecodable text, a missing or malformed heading, or an empty section. |
| Prepare | Apply the chosen 520-character paragraph-aware method. Preserve physical line ranges and normalised offsets. | Stop on an unbreakable over-limit token or a missing line mapping. |
| Validate and load | Read JSONL back and check eight unique non-empty records, text coverage, offsets, source paths, hashes, locations and reference metadata. | Halt when validation fails. Both integrated runs are staged and compared before replacing the committed output. |
| Record lineage | The Part B manifest and Part C run manifest map both source fingerprints to the exact output fingerprint and per-source record count. | Stop on missing mappings or mismatched fingerprints. |
| Rerun | Repeat Part C using the same inputs in a separate temporary directory. Input hashes, settings, bytes, record counts, output hash and mappings matched. | Stop when outputs drift. Review source bytes, parsing or configuration before replacing the export. |

**Batch ETL** fits a versioned collection updated on demand. The notebook extracts and inspects the approved inputs, transforms and validates criterion records, then loads prepared JSONL. A streaming consumer would add upkeep without a data freshness need for this corpus. The inputs remain separate from the generated data so future source refreshes can be checked against the previous version.

## Execution and locations

The notebook cells ran in sequence using Python 3.12.14. The eight Part B records total **7,549 bytes**, with SHA-256 `960ea4ccb1a529328242101f4228d7b765303981c1b5030b2dddaed83967123c`. The two Part C runs matched, and their JSONL was byte-identical to the Part B export. Timestamps are execution metadata and may vary between runs. Both original source mappings and sample record output are visible in the notebook.

| Checkpoint | Location |
| --- | --- |
| Code and recorded outputs | [notebooks/week3_pipeline.ipynb](../notebooks/week3_pipeline.ipynb) |
| Part B prepared data and provenance | [data/processed/prepared_text.jsonl](../data/processed/prepared_text.jsonl) · [data/week3_manifest.json](../data/week3_manifest.json) |
| Part C prepared data and run evidence | [data/pipeline_v1/text/prepared_text.jsonl](../data/pipeline_v1/text/prepared_text.jsonl) · [pipeline_manifest.json](../data/pipeline_v1/text/pipeline_manifest.json) |

Colab can fetch these exact project-authored source files from this repository if they are absent in its working directory. The recorded execution used local Python. For the course's Colab checkpoint, open the notebook in Colab, run all cells, and download the generated data ZIP before disconnecting. Traceability covers prepared text and its sources. It does not independently establish that the guidance is comprehensive or suitable for grading.
