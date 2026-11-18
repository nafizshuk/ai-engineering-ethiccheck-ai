"""Reproduce the Topic 4 data quality audit of the original EthicCheck dataset."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.request import urlopen

REPOSITORY = "nafizshuk/ai-engineering-ethiccheck-ai"
SNAPSHOT = "6a669588a9f8cb08d679b809f2eee79bbda1f609"
PART_C = "data/pipeline_v1/text/prepared_text.jsonl"
PART_B = "data/processed/prepared_text.jsonl"
SOURCES = {
    "S01": "data/sources/data_and_fairness.txt",
    "S02": "data/sources/risk_and_oversight.txt",
}
EXPECTED_BLOBS = {
    PART_C: "ef5449a85e4b4e8bade209f39f7fbd899a227ec8",
    PART_B: "ef5449a85e4b4e8bade209f39f7fbd899a227ec8",
    SOURCES["S01"]: "5af36d3a2084e8fc8f6308f54eba1b58f80e00a4",
    SOURCES["S02"]: "123fb5740ff6084d7ccf1a22751a3688523d4f0a",
}
SECTIONS = {
    "SAF-01": "3.2", "ACC-01": "3.4", "EXP-01": "3.5",
    "PRI-01": "3.6", "FAI-01": "3.7",
}
FIELDS = frozenset(
    "record_id source_id source source_version source_sha256 criterion_id category "
    "heading_line line_start line_end char_start char_end text reference_title "
    "reference_version reference_section reference_url processing".split()
)
LOCATION_FIELDS = ("heading_line", "line_start", "line_end", "char_start", "char_end")
REFERENCE_URL = "https://doi.org/10.6028/NIST.AI.100-1"


def load_inputs(repo_root):
    """Read and verify the exact four files used by these checks."""
    files = {}
    for name, expected in EXPECTED_BLOBS.items():
        if repo_root is None:
            url = f"https://raw.githubusercontent.com/{REPOSITORY}/{SNAPSHOT}/{name}"
            with urlopen(url, timeout=30) as response:
                payload = response.read()
        else:
            payload = (repo_root / name).read_bytes()
        header = f"blob {len(payload)}\0".encode("ascii")
        if hashlib.sha1(header + payload).hexdigest() != expected:
            raise ValueError(f"File differs from the audited GitHub snapshot: {name}")
        files[name] = payload
    return files


def normalise(text):
    return " ".join(text.split())


def section_text(lines, heading):
    """Rebuild the criterion's normalised text with each paragraph's line range."""
    paragraphs = []
    current = []
    for number, line in enumerate(lines[heading:], heading + 1):
        if line.startswith("## "):
            break
        cleaned = normalise(line)
        if cleaned:
            current.append((number, cleaned))
        elif current:
            paragraphs.append(current)
            current = []
    if current:
        paragraphs.append(current)

    text_parts = []
    spans = []
    start = 0
    for paragraph in paragraphs:
        text = " ".join(content for _, content in paragraph)
        end = start + len(text)
        spans.append((start, end, paragraph[0][0], paragraph[-1][0]))
        text_parts.append(text)
        start = end + 2
    return "\n\n".join(text_parts), spans


def traceability_issues(record, files):
    missing = sorted(key for key in FIELDS if record.get(key) is None or
                     isinstance(record[key], str) and not record[key].strip())
    if missing:
        return missing, ["Required fields missing"]
    if any(type(record[key]) is not int for key in LOCATION_FIELDS):
        return [], ["Invalid location field type"]
    if any(not isinstance(record[key], str) for key in FIELDS.difference(LOCATION_FIELDS)):
        return [], ["Invalid text field type"]

    source_path = SOURCES.get(record["source_id"])
    if source_path is None or source_path != record["source"]:
        return [], ["Unrecognised source ID or filename"]

    source = files[source_path]
    lines = source.decode("utf-8-sig").splitlines()
    heading, lo, hi, start, end = (record[key] for key in LOCATION_FIELDS)
    if not 1 <= heading < lo <= hi <= len(lines):
        return [], ["Invalid heading or source line range"]

    errors = []
    if hashlib.sha256(source).hexdigest() != record["source_sha256"]:
        errors.append("Source hash mismatch")
    if lines[heading-1] != f"## {record['criterion_id']} | {record['category']}":
        errors.append("Criterion heading mismatch")
    text, spans = section_text(lines, heading)
    if not 0 <= start < end <= len(text) or text[start:end] != record["text"]:
        errors.append("Text differs from the declared source slice")
    touched = [span for span in spans if span[0] < end and span[1] > start]
    if not touched or (touched[0][2], touched[-1][3]) != (lo, hi):
        errors.append("Source lines do not match the prepared chunk")
    if record["source_version"] != "1.0":
        errors.append("Source version mismatch")
    if (
        record["reference_title"] != "NIST AI RMF 1.0"
        or record["reference_version"] != "NIST AI 100-1, January 2023"
        or record["reference_url"] != REFERENCE_URL
        or record["reference_section"] != SECTIONS.get(record["criterion_id"])
    ):
        errors.append("Reference metadata mismatch")
    return [], errors


def audit(files):
    records = [json.loads(line) for line in files[PART_C].splitlines() if line.strip()]
    if not records or any(not isinstance(row, dict) for row in records):
        raise ValueError("Expected a non-empty JSONL export of objects")

    missing_fields = 0
    failed_traceability = []
    for number, record in enumerate(records, 1):
        missing, issues = traceability_issues(record, files)
        missing_fields += len(missing)
        if issues:
            failed_traceability.append({
                "row": number, "record_id": record.get("record_id"),
                "missing": missing, "issues": issues,
            })

    identities = [record.get("record_id") for record in records]
    record_texts = [record.get("text") for record in records]
    id_counts = Counter(key for key in identities if isinstance(key, str) and key.strip())
    text_counts = Counter(normalise(text).casefold() for text in record_texts
                          if isinstance(text, str) and text.strip())
    duplicate_ids = sorted(key for key, count in id_counts.items() if count > 1)
    duplicate_texts = sorted(text for text, count in text_counts.items() if count > 1)
    uniqueness_passed = 0
    for key, text in zip(identities, record_texts):
        if isinstance(key, str) and isinstance(text, str):
            uniqueness_passed += id_counts[key] == text_counts[normalise(text).casefold()] == 1

    sample = next(record for record in records if record.get("record_id") == "S01-PRI-01-01")
    return {
        "repository": REPOSITORY,
        "snapshot": SNAPSHOT,
        "prepared_file": PART_C,
        "records_inspected": len(records),
        "expected_fields_per_record": len(FIELDS),
        "rule_1": {
            "passing_records": len(records) - len(failed_traceability),
            "missing_required_fields": missing_fields,
            "failed_records": failed_traceability,
        },
        "rule_2": {
            "passing_records": uniqueness_passed,
            "duplicate_record_ids": duplicate_ids,
            "duplicate_normalised_texts": duplicate_texts,
        },
        "part_b_and_part_c_match": files[PART_B] == files[PART_C],
        "prepared_export_bytes": len(files[PART_C]),
        "prepared_export_sha256": hashlib.sha256(files[PART_C]).hexdigest(),
        "supporting_record": sample,
    }


def print_results(result):
    total = result["records_inspected"]
    first = result["rule_1"]
    second = result["rule_2"]
    print("EthicCheck AI | Topic 4 data quality audit")
    print(f"GitHub snapshot: {result['snapshot']}")
    print(f"Export: {result['prepared_file']}")
    print(f"Records inspected: {total} | Required fields per record: {result['expected_fields_per_record']}")
    print()
    for label, rule in (("Rule 1 - Source traceability", first), ("Rule 2 - Record uniqueness", second)):
        passed = rule["passing_records"]
        status = "PASS" if passed == total else "FAIL"
        print(f"{label}: {status} ({passed}/{total})")
        if rule is first:
            print(f"  Missing required fields: {first['missing_required_fields']}")
            print(f"  Records with traceability issues: {len(first['failed_records'])}")
        else:
            print(f"  Duplicate record IDs: {len(second['duplicate_record_ids'])}")
            print(f"  Duplicate normalised texts: {len(second['duplicate_normalised_texts'])}")
    print()
    print(f"Part B and Part C match byte-for-byte: {result['part_b_and_part_c_match']}")
    print(f"Prepared export: {result['prepared_export_bytes']:,} bytes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, help="Use a local copy of the pinned repository files.")
    parser.add_argument("--output", type=Path, default=Path("topic4_audit_results.json"),
                        help="Destination for the detailed JSON results.")
    args = parser.parse_args()
    result = audit(load_inputs(args.repo_root))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print_results(result)


if __name__ == "__main__":
    main()
