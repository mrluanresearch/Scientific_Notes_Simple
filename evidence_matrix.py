#!/usr/bin/env python3
"""Validate the study-level EVIDENCE_MATRIX.csv for Scientific_Notes_Simple.

This script validates schema, identity, provenance, staleness, structural cleanliness,
and cross-file consistency. It never infers scientific evidence from PDFs/notes and
never upgrades scientific quality or matrix status automatically.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re
import sys

ID_RE = re.compile(r"SAL-\d{4,}$")
NOTE_STATUS_RE = re.compile(r"(?m)^status:\s*(draft|checked)\s*$")
NOTE_ID_RE = re.compile(r"(?m)^id:\s*(SAL-\d{4,})\s*$")
MARKDOWN_HEADING_RE = re.compile(r"(?m)^#{2,6}\s+")

MATRIX_FIELDS = [
    "id",
    "year",
    "first_author",
    "title",
    "doi",
    "journal",
    "country_region",
    "study_design",
    "tags",
    "population_sample_context",
    "denominator_prevalence_summary",
    "serovar_summary",
    "ast_summary",
    "amr_gene_summary",
    "virulence_summary",
    "genomics_mlst_plasmid_phylogeny_summary",
    "negative_findings_exceptions",
    "arithmetic_internal_consistency",
    "main_limitations",
    "thesis_use",
    "comparison_conditions",
    "do_not_conclude",
    "evidence_reuse_decision",
    "quantitative_reuse_scope",
    "source_discrepancy_severity",
    "source_verification_result",
    "unresolved_source_issues",
    "note_status",
    "matrix_status",
    "pdf_filename",
    "md_filename",
    "pdf_sha256",
    "note_sha256",
    "canonical_url",
    "matrix_generated_at",
]

# These are scientific-content cells, not Markdown note containers. A heading copied
# into one of these fields means section-boundary leakage occurred during extraction.
SYNTHESIS_TEXT_FIELDS = [
    "population_sample_context",
    "denominator_prevalence_summary",
    "serovar_summary",
    "ast_summary",
    "amr_gene_summary",
    "virulence_summary",
    "genomics_mlst_plasmid_phylogeny_summary",
    "negative_findings_exceptions",
    "arithmetic_internal_consistency",
    "main_limitations",
    "thesis_use",
    "comparison_conditions",
    "do_not_conclude",
    "evidence_reuse_decision",
]

EVIDENCE_DOMAIN_FIELDS = [
    "denominator_prevalence_summary",
    "serovar_summary",
    "ast_summary",
    "amr_gene_summary",
    "virulence_summary",
    "genomics_mlst_plasmid_phylogeny_summary",
]

ALLOWED_SCOPES = {
    "prevalence_or_sample_level_conditional",
    "isolate_or_genome_level",
    "experimental_parameter_only",
    "review_pooled_estimates",
    "review_summary_only",
}

ALLOWED_MATRIX_STATUS = {
    "draft",
    "generated_from_checked_note",
    "checked_against_checked_note",
}

ALLOWED_NOTE_STATUS = {"draft", "checked"}
ALLOWED_SEVERITY = {"none", "low", "moderate", "high"}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], [dict(row) for row in reader]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def norm_doi(value: str) -> str:
    value = (value or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):].strip()
    return value


def parse_note(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    id_match = NOTE_ID_RE.search(text)
    status_match = NOTE_STATUS_RE.search(text)
    return {
        "id": id_match.group(1) if id_match else "",
        "status": status_match.group(1) if status_match else "",
        "sha256": sha256_file(path),
    }


def duplicate_nonempty(rows, field):
    seen, duplicates = {}, []
    for row_number, row in enumerate(rows, start=2):
        value = (row.get(field) or "").strip()
        if not value:
            continue
        key = value.lower() if field == "doi" else value
        if key in seen:
            duplicates.append((value, seen[key], row_number))
        else:
            seen[key] = row_number
    return duplicates


def validate(args):
    errors, warnings = [], []

    matrix_fields, matrix_rows = read_csv(args.matrix)
    registry_fields, registry_rows = read_csv(args.registry)
    verification_fields, verification_rows = read_csv(args.verification)

    if matrix_fields != MATRIX_FIELDS:
        errors.append(
            "EVIDENCE_MATRIX.csv không đúng schema canonical. "
            f"Expected {MATRIX_FIELDS}, got {matrix_fields}"
        )

    required_registry = {
        "id", "year", "first_author", "title", "doi", "journal", "registry_status",
        "note_status", "pdf_filename", "md_filename", "pdf_sha256", "canonical_url",
    }
    missing_registry = sorted(required_registry - set(registry_fields))
    if missing_registry:
        errors.append("Registry thiếu cột: " + ", ".join(missing_registry))

    required_verification = {
        "id", "verification_result", "source_discrepancy_severity",
        "unresolved_source_issues", "note_status_decision",
    }
    missing_verification = sorted(required_verification - set(verification_fields))
    if missing_verification:
        errors.append("Verification log thiếu cột: " + ", ".join(missing_verification))

    active_registry = {
        row["id"].strip(): row
        for row in registry_rows
        if row.get("registry_status", "").strip() == "active"
    }
    verification = {row.get("id", "").strip(): row for row in verification_rows}

    matrix_by_id = {}
    status_counts = {status: 0 for status in ALLOWED_MATRIX_STATUS}

    for row_number, row in enumerate(matrix_rows, start=2):
        rid = (row.get("id") or "").strip()
        if not ID_RE.fullmatch(rid):
            errors.append(f"matrix row {row_number}: id không hợp lệ {rid!r}")
            continue
        if rid in matrix_by_id:
            errors.append(f"matrix row {row_number}: duplicate id {rid}")
        matrix_by_id[rid] = row

        scope = (row.get("quantitative_reuse_scope") or "").strip()
        if scope not in ALLOWED_SCOPES:
            errors.append(f"{rid}: quantitative_reuse_scope không hợp lệ: {scope!r}")

        status = (row.get("matrix_status") or "").strip()
        if status not in ALLOWED_MATRIX_STATUS:
            errors.append(f"{rid}: matrix_status không hợp lệ: {status!r}")
        else:
            status_counts[status] += 1

        note_status = (row.get("note_status") or "").strip()
        if note_status not in ALLOWED_NOTE_STATUS:
            errors.append(f"{rid}: note_status không hợp lệ: {note_status!r}")

        severity = (row.get("source_discrepancy_severity") or "").strip()
        if severity not in ALLOWED_SEVERITY:
            warnings.append(f"{rid}: source_discrepancy_severity ngoài controlled vocabulary")

        for field in (
            "title", "first_author", "journal", "country_region", "study_design",
            "population_sample_context", "main_limitations", "evidence_reuse_decision",
            "pdf_filename", "md_filename", "pdf_sha256", "note_sha256", "matrix_generated_at",
        ):
            if not (row.get(field) or "").strip():
                errors.append(f"{rid}: thiếu field bắt buộc {field}")

        # Structural guard: matrix cells are synthesis text, not copied note sections.
        for field in SYNTHESIS_TEXT_FIELDS:
            value = row.get(field) or ""
            if MARKDOWN_HEADING_RE.search(value):
                errors.append(
                    f"{rid}: {field} chứa Markdown heading — có khả năng section-boundary leakage"
                )

        if status == "checked_against_checked_note":
            if note_status != "checked":
                errors.append(f"{rid}: matrix checked nhưng note_status không phải checked")
            if not (row.get("source_verification_result") or "").strip():
                errors.append(f"{rid}: matrix checked nhưng thiếu source_verification_result")
            if not any((row.get(field) or "").strip() for field in EVIDENCE_DOMAIN_FIELDS):
                warnings.append(f"{rid}: matrix checked nhưng không có evidence-domain summary")

    matrix_ids = set(matrix_by_id)
    registry_ids = set(active_registry)
    for rid in sorted(registry_ids - matrix_ids):
        errors.append(f"{rid}: active registry record thiếu EVIDENCE_MATRIX row")
    for rid in sorted(matrix_ids - registry_ids):
        warnings.append(f"{rid}: matrix row không có active registry record")

    for rid in sorted(registry_ids & matrix_ids):
        m = matrix_by_id[rid]
        r = active_registry[rid]
        v = verification.get(rid)

        exact_pairs = [
            ("title", "title"),
            ("first_author", "first_author"),
            ("journal", "journal"),
            ("pdf_filename", "pdf_filename"),
            ("md_filename", "md_filename"),
            ("pdf_sha256", "pdf_sha256"),
            ("note_status", "note_status"),
        ]
        for mf, rf in exact_pairs:
            if (m.get(mf) or "").strip() != (r.get(rf) or "").strip():
                errors.append(f"{rid}: {mf} không khớp registry")

        if str(m.get("year", "")).strip() != str(r.get("year", "")).strip():
            errors.append(f"{rid}: year không khớp registry")
        if norm_doi(m.get("doi", "")) != norm_doi(r.get("doi", "")):
            errors.append(f"{rid}: DOI không khớp registry")
        if (m.get("canonical_url") or "").strip() != (r.get("canonical_url") or "").strip():
            errors.append(f"{rid}: canonical_url không khớp registry")

        if v:
            if (m.get("source_verification_result") or "").strip() != (v.get("verification_result") or "").strip():
                errors.append(f"{rid}: source_verification_result không khớp verification log")
            if (m.get("source_discrepancy_severity") or "").strip() != (v.get("source_discrepancy_severity") or "").strip():
                errors.append(f"{rid}: source_discrepancy_severity không khớp verification log")
            if (m.get("unresolved_source_issues") or "").strip() != (v.get("unresolved_source_issues") or "").strip():
                errors.append(f"{rid}: unresolved_source_issues không khớp verification log")
        elif (m.get("matrix_status") or "").strip() == "checked_against_checked_note":
            errors.append(f"{rid}: matrix checked nhưng thiếu verification row")

        note_path = Path(args.notes) / (m.get("md_filename") or f"{rid}.md")
        if note_path.exists():
            note = parse_note(note_path)
            if note["id"] != rid:
                errors.append(f"{rid}: YAML id trong note là {note['id']!r}")
            if note["status"] != (m.get("note_status") or "").strip():
                errors.append(f"{rid}: note status thực tế không khớp matrix")
            if note["sha256"] != (m.get("note_sha256") or "").strip():
                errors.append(f"{rid}: EVIDENCE_MATRIX row stale — note_sha256 không khớp file hiện tại")
        else:
            warnings.append(f"{rid}: không tìm thấy local note để kiểm tra note_sha256: {note_path}")

    for field in ("doi", "pdf_sha256", "note_sha256"):
        for value, first_row, second_row in duplicate_nonempty(matrix_rows, field):
            errors.append(f"duplicate {field}: {value!r} ở rows {first_row} và {second_row}")

    if args.require_all_checked:
        not_checked = sorted(
            rid for rid, row in matrix_by_id.items()
            if (row.get("matrix_status") or "").strip() != "checked_against_checked_note"
        )
        if not_checked:
            errors.append(
                "require-all-checked: còn row chưa checked_against_checked_note: "
                + ", ".join(not_checked)
            )

    return errors, warnings, len(active_registry), len(matrix_rows), status_counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, default=Path("results/EVIDENCE_MATRIX.csv"))
    parser.add_argument("--registry", type=Path, default=Path("results/SOURCE_REGISTRY.csv"))
    parser.add_argument("--verification", type=Path, default=Path("results/SOURCE_VERIFICATION.csv"))
    parser.add_argument("--notes", type=Path, default=Path("results/MD"))
    parser.add_argument(
        "--require-all-checked",
        action="store_true",
        help="Fail if any matrix row is not checked_against_checked_note.",
    )
    args = parser.parse_args()

    try:
        errors, warnings, active_count, matrix_count, status_counts = validate(args)
    except (OSError, ValueError, KeyError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2

    for message in errors:
        print("LỖI:", message)
    for message in warnings:
        print("CẦN XEM:", message)
    print(
        f"{active_count} active registry record; {matrix_count} matrix row; "
        f"checked={status_counts['checked_against_checked_note']}; "
        f"generated={status_counts['generated_from_checked_note']}; "
        f"draft={status_counts['draft']}; {len(errors)} lỗi; {len(warnings)} cảnh báo."
    )
    return 2 if errors else (1 if warnings else 0)


if __name__ == "__main__":
    raise SystemExit(main())
