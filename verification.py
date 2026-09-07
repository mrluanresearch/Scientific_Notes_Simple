#!/usr/bin/env python3
"""Validate source-level verification audit state for Scientific_Notes_Simple.

This script validates traceability only. It never decides scientific quality and never
promotes a note from draft to checked automatically.
"""

import argparse
import csv
from pathlib import Path
import re
import sys

ID_RE = re.compile(r"SAL-\d{4,}$")
NOTE_STATUS_RE = re.compile(r"(?m)^status:\s*(draft|checked)\s*$")
NOTE_ID_RE = re.compile(r"(?m)^id:\s*(SAL-\d{4,})\s*$")
SCOPE_RE = re.compile(r"(?m)^read_scope:\s*([^\n]+)\s*$")
VERIFICATION_MARKER = "Source-level verification:"

VERIFICATION_FIELDS = [
    "id",
    "reviewer",
    "verified_at",
    "read_scope",
    "note_status_decision",
    "verification_result",
    "source_discrepancy_severity",
    "checks_completed",
    "unresolved_source_issues",
    "pdf_filename",
    "md_filename",
]


def read_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], [dict(row) for row in reader]


def parse_note(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    id_match = NOTE_ID_RE.search(text)
    status_match = NOTE_STATUS_RE.search(text)
    scope_match = SCOPE_RE.search(text)
    return {
        "id": id_match.group(1) if id_match else "",
        "status": status_match.group(1) if status_match else "",
        "read_scope": scope_match.group(1).strip() if scope_match else "",
        "has_verification_marker": VERIFICATION_MARKER in text,
        "text": text,
    }


def validate(args):
    errors, warnings = [], []

    registry_fields, registry_rows = read_csv(args.registry)
    required_registry = {"id", "registry_status", "note_status", "pdf_filename", "md_filename"}
    missing_registry = sorted(required_registry - set(registry_fields))
    if missing_registry:
        errors.append("Registry thiếu cột: " + ", ".join(missing_registry))

    verification_fields, verification_rows = read_csv(args.verification)
    if verification_fields != VERIFICATION_FIELDS:
        errors.append(
            "SOURCE_VERIFICATION.csv không đúng schema canonical. "
            f"Expected {VERIFICATION_FIELDS}, got {verification_fields}"
        )

    verification_by_id = {}
    for row_number, row in enumerate(verification_rows, start=2):
        rid = row.get("id", "").strip()
        if not ID_RE.fullmatch(rid):
            errors.append(f"verification row {row_number}: id không hợp lệ {rid!r}")
            continue
        if rid in verification_by_id:
            errors.append(f"verification row {row_number}: duplicate verification id {rid}")
        verification_by_id[rid] = row
        if not row.get("reviewer", "").strip():
            errors.append(f"{rid}: verification thiếu reviewer")
        if not row.get("verified_at", "").strip():
            errors.append(f"{rid}: verification thiếu verified_at")
        if row.get("note_status_decision", "").strip() != "checked":
            warnings.append(f"{rid}: verification decision không phải checked")
        if row.get("source_discrepancy_severity", "").strip() not in {"none", "low", "moderate", "high"}:
            warnings.append(f"{rid}: source_discrepancy_severity ngoài controlled vocabulary")

    active_rows = [r for r in registry_rows if r.get("registry_status", "").strip() == "active"]
    registry_ids = set()
    checked_registry_ids = set()

    for row in active_rows:
        rid = row.get("id", "").strip()
        if not ID_RE.fullmatch(rid):
            errors.append(f"registry: active id không hợp lệ {rid!r}")
            continue
        if rid in registry_ids:
            errors.append(f"registry: duplicate active id {rid}")
        registry_ids.add(rid)

        md_filename = row.get("md_filename", "").strip() or f"{rid}.md"
        pdf_filename = row.get("pdf_filename", "").strip() or f"{rid}.pdf"
        note_path = Path(args.notes) / md_filename
        if not note_path.exists():
            errors.append(f"{rid}: thiếu canonical note {note_path}")
            continue

        note = parse_note(note_path)
        if note["id"] != rid:
            errors.append(f"{rid}: YAML id trong {md_filename} là {note['id']!r}")

        registry_status = row.get("note_status", "").strip()
        if note["status"] != registry_status:
            errors.append(
                f"{rid}: note status mismatch — MD={note['status']!r}, registry={registry_status!r}"
            )

        if registry_status == "checked":
            checked_registry_ids.add(rid)
            audit = verification_by_id.get(rid)
            if not audit:
                errors.append(f"{rid}: checked nhưng thiếu SOURCE_VERIFICATION row")
                continue
            if audit.get("note_status_decision", "").strip() != "checked":
                errors.append(f"{rid}: registry checked nhưng verification decision không phải checked")
            if audit.get("md_filename", "").strip() != md_filename:
                errors.append(f"{rid}: verification md_filename không khớp registry")
            if audit.get("pdf_filename", "").strip() != pdf_filename:
                errors.append(f"{rid}: verification pdf_filename không khớp registry")
            if not note["has_verification_marker"]:
                errors.append(f"{rid}: checked note thiếu dòng '{VERIFICATION_MARKER}'")
            if note["read_scope"] and audit.get("read_scope", "").strip():
                if note["read_scope"] not in audit.get("read_scope", ""):
                    warnings.append(
                        f"{rid}: read_scope wording khác nhau giữa MD ({note['read_scope']}) và verification log"
                    )

    orphan_verification = sorted(set(verification_by_id) - registry_ids)
    for rid in orphan_verification:
        warnings.append(f"{rid}: verification row không có active registry record")

    missing_verification = sorted(checked_registry_ids - set(verification_by_id))
    for rid in missing_verification:
        errors.append(f"{rid}: checked registry record thiếu verification row")

    index_path = Path(args.index)
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8-sig")
        for rid in sorted(checked_registry_ids):
            pattern = re.compile(rf"(?m)^\|\s*\[{re.escape(rid)}\]\([^\n]+\).*\|\s*checked\s*\|\s*$")
            if not pattern.search(index_text):
                errors.append(f"{rid}: INDEX.md không hiển thị checked")
    else:
        warnings.append(f"Không tìm thấy INDEX: {index_path}")

    return errors, warnings, len(active_rows), len(checked_registry_ids), len(verification_rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("results/SOURCE_REGISTRY.csv"))
    parser.add_argument("--verification", type=Path, default=Path("results/SOURCE_VERIFICATION.csv"))
    parser.add_argument("--notes", type=Path, default=Path("results/MD"))
    parser.add_argument("--index", type=Path, default=Path("results/MD/INDEX.md"))
    args = parser.parse_args()

    try:
        errors, warnings, active_count, checked_count, verification_count = validate(args)
    except (OSError, ValueError) as exc:
        print(f"LỖI: {exc}", file=sys.stderr)
        return 2

    for message in errors:
        print("LỖI:", message)
    for message in warnings:
        print("CẦN XEM:", message)
    print(
        f"{active_count} active registry record; {checked_count} checked; "
        f"{verification_count} verification row; {len(errors)} lỗi; {len(warnings)} cảnh báo."
    )
    return 2 if errors else (1 if warnings else 0)


if __name__ == "__main__":
    raise SystemExit(main())
