#!/usr/bin/env python3
"""Manage SOURCE_REGISTRY.csv for stable SAL IDs and duplicate control."""

import argparse
import csv
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
from pathlib import Path
import re
import sys
import unicodedata

FIELDS = [
    "id", "title", "title_key", "year", "first_author", "first_author_key",
    "doi", "doi_key", "pmid", "pmcid", "journal", "publication_type",
    "publication_status", "relation_type", "related_id", "original_filename",
    "pdf_filename", "md_filename", "pdf_sha256", "canonical_url",
    "registry_status", "note_status", "registered_at", "updated_at",
    "duplicate_of", "duplicate_reason", "notes",
]
ID_RE = re.compile(r"SAL-\d{4,}$")
ACTIVE_STATUSES = {"active", "review", "superseded"}
REGISTRY_STATUSES = {"active", "review", "duplicate", "excluded", "superseded"}
NOTE_STATUSES = {"none", "draft", "checked"}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def doi_key(value):
    value = str(value or "").strip()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    return value.strip().casefold()


def title_key(value):
    value = unicodedata.normalize("NFKC", str(value or "")).casefold()
    value = "".join(ch if ch.isalnum() else " " for ch in value)
    return re.sub(r"\s+", " ", value).strip()


def author_key(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).casefold()
    value = "".join(ch if ch.isalnum() else " " for ch in value)
    return re.sub(r"\s+", " ", value).strip()


def pmid_key(value):
    value = str(value or "").strip()
    return re.sub(r"\D", "", value)


def pmcid_key(value):
    value = re.sub(r"\s+", "", str(value or "")).upper()
    if value and not value.startswith("PMC") and value.isdigit():
        value = "PMC" + value
    return value


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_registry(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError(
                "Header SOURCE_REGISTRY.csv không đúng schema canonical. "
                f"Expected {FIELDS}, got {reader.fieldnames}"
            )
        return [dict(row) for row in reader]


def write_registry(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name("." + path.name + ".tmp")
    with temp.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def next_id(rows):
    numbers = []
    for row in rows:
        value = row.get("id", "")
        if ID_RE.fullmatch(value):
            numbers.append(int(value[4:]))
    return f"SAL-{max(numbers, default=0) + 1:04d}"


def year_int(value):
    try:
        return int(value) if str(value).strip() else None
    except ValueError:
        return None


def match_candidates(rows, *, title="", year=None, first_author="", doi="", pmid="", pmcid="", sha256=""):
    tkey = title_key(title)
    akey = author_key(first_author)
    dkey = doi_key(doi)
    pkey = pmid_key(pmid)
    pckey = pmcid_key(pmcid)
    hkey = str(sha256 or "").strip().casefold()
    candidates = []

    for row in rows:
        reasons = []
        hard = False
        if row.get("registry_status") == "duplicate":
            continue
        if dkey and row.get("doi_key") == dkey:
            reasons.append("DOI exact")
            hard = True
        if pkey and row.get("pmid") and pmid_key(row.get("pmid")) == pkey:
            reasons.append("PMID exact")
            hard = True
        if pckey and row.get("pmcid") and pmcid_key(row.get("pmcid")) == pckey:
            reasons.append("PMCID exact")
            hard = True
        if hkey and row.get("pdf_sha256", "").casefold() == hkey:
            reasons.append("PDF SHA256 exact")
            hard = True

        row_tkey = row.get("title_key", "")
        row_akey = row.get("first_author_key", "")
        row_year = year_int(row.get("year"))
        if tkey and row_tkey == tkey:
            if akey and row_akey == akey and year is not None and row_year == year:
                reasons.append("title + first author + year exact")
            elif year is None or row_year is None or abs((row_year or 0) - (year or 0)) <= 1:
                reasons.append("title exact; year same/near")
        elif tkey and row_tkey and akey and row_akey == akey:
            ratio = SequenceMatcher(None, tkey, row_tkey).ratio()
            if ratio >= 0.97 and (year is None or row_year is None or abs(row_year - year) <= 1):
                reasons.append(f"title fuzzy {ratio:.3f} + first author")

        if reasons:
            candidates.append({"id": row.get("id", ""), "hard": hard, "reasons": reasons, "row": row})
    return candidates


def validate(rows):
    errors, warnings = [], []
    seen_ids = {}
    active_keys = {"doi_key": {}, "pmid": {}, "pmcid": {}, "pdf_sha256": {}}

    for idx, row in enumerate(rows, start=2):
        rid = row.get("id", "")
        if not ID_RE.fullmatch(rid):
            errors.append(f"row {idx}: id không hợp lệ: {rid!r}")
        elif rid in seen_ids:
            errors.append(f"row {idx}: id trùng {rid} với row {seen_ids[rid]}")
        else:
            seen_ids[rid] = idx

        status = row.get("registry_status", "")
        if status not in REGISTRY_STATUSES:
            errors.append(f"row {idx} {rid}: registry_status không hợp lệ: {status!r}")
        note_status = row.get("note_status", "")
        if note_status not in NOTE_STATUSES:
            errors.append(f"row {idx} {rid}: note_status không hợp lệ: {note_status!r}")

        if row.get("title_key", "") != title_key(row.get("title", "")):
            errors.append(f"row {idx} {rid}: title_key không khớp title")
        if row.get("first_author_key", "") != author_key(row.get("first_author", "")):
            errors.append(f"row {idx} {rid}: first_author_key không khớp first_author")
        if row.get("doi_key", "") != doi_key(row.get("doi", "")):
            errors.append(f"row {idx} {rid}: doi_key không khớp doi")

        if rid and status != "duplicate":
            expected_pdf = f"{rid}.pdf"
            expected_md = f"{rid}.md"
            if row.get("pdf_filename") and row.get("pdf_filename") != expected_pdf:
                errors.append(f"row {idx} {rid}: pdf_filename phải là {expected_pdf}")
            if row.get("md_filename") and row.get("md_filename") != expected_md:
                errors.append(f"row {idx} {rid}: md_filename phải là {expected_md}")

        if status == "duplicate":
            if not row.get("duplicate_of"):
                errors.append(f"row {idx} {rid}: duplicate cần duplicate_of")
            if row.get("duplicate_of") == rid:
                errors.append(f"row {idx} {rid}: duplicate_of không được trỏ chính nó")

        related = row.get("related_id", "")
        if related and not ID_RE.fullmatch(related):
            errors.append(f"row {idx} {rid}: related_id không hợp lệ: {related!r}")
        if bool(related) != bool(row.get("relation_type", "")):
            warnings.append(f"row {idx} {rid}: relation_type và related_id nên đi cùng nhau")

        if status in ACTIVE_STATUSES:
            for field in active_keys:
                value = row.get(field, "").strip().casefold()
                if not value:
                    continue
                bucket = active_keys[field]
                if value in bucket:
                    errors.append(f"row {idx} {rid}: {field} trùng active record {bucket[value]}")
                else:
                    bucket[value] = rid

    active_rows = [r for r in rows if r.get("registry_status") in ACTIVE_STATUSES]
    for i, left in enumerate(active_rows):
        for right in active_rows[i + 1:]:
            if not left.get("title_key") or not right.get("title_key"):
                continue
            if left["title_key"] == right["title_key"]:
                ly, ry = year_int(left.get("year")), year_int(right.get("year"))
                if ly is None or ry is None or abs(ly - ry) <= 1:
                    warnings.append(
                        f"probable duplicate/version: {left.get('id')} vs {right.get('id')} — exact title key, year same/near"
                    )
    return errors, warnings


def cmd_init(args):
    path = Path(args.registry)
    if path.exists() and not args.force:
        raise ValueError(f"Registry đã tồn tại: {path}. Dùng --force chỉ khi thực sự muốn tạo lại header rỗng.")
    write_registry(path, [])
    print(path)
    return 0


def print_candidates(candidates):
    for c in candidates:
        kind = "HARD" if c["hard"] else "REVIEW"
        row = c["row"]
        print(f"{kind}\t{c['id']}\t{'; '.join(c['reasons'])}\t{row.get('title','')}\t{row.get('doi','')}")


def cmd_find(args):
    rows = read_registry(args.registry)
    digest = args.sha256
    if args.pdf:
        digest = sha256_file(args.pdf)
    candidates = match_candidates(
        rows, title=args.title, year=args.year, first_author=args.first_author,
        doi=args.doi, pmid=args.pmid, pmcid=args.pmcid, sha256=digest,
    )
    print_candidates(candidates)
    return 0 if candidates else 1


def cmd_register(args):
    rows = read_registry(args.registry)
    digest = args.sha256
    if args.pdf:
        digest = sha256_file(args.pdf)
    candidates = match_candidates(
        rows, title=args.title, year=args.year, first_author=args.first_author,
        doi=args.doi, pmid=args.pmid, pmcid=args.pmcid, sha256=digest,
    )
    hard = [c for c in candidates if c["hard"]]
    review = [c for c in candidates if not c["hard"]]
    if hard:
        print("Không đăng ký: phát hiện hard duplicate candidate.", file=sys.stderr)
        print_candidates(hard)
        return 2
    if review and not args.allow_candidate:
        print("Chưa đăng ký: có probable duplicate/version candidate; review trước hoặc dùng --allow-candidate sau khi đã xác minh.", file=sys.stderr)
        print_candidates(review)
        return 3

    rid = next_id(rows)
    timestamp = now_iso()
    row = {field: "" for field in FIELDS}
    row.update({
        "id": rid,
        "title": args.title.strip(),
        "title_key": title_key(args.title),
        "year": str(args.year or ""),
        "first_author": args.first_author.strip(),
        "first_author_key": author_key(args.first_author),
        "doi": doi_key(args.doi),
        "doi_key": doi_key(args.doi),
        "pmid": pmid_key(args.pmid),
        "pmcid": pmcid_key(args.pmcid),
        "journal": args.journal.strip(),
        "publication_type": args.publication_type.strip(),
        "publication_status": args.publication_status.strip(),
        "relation_type": args.relation_type.strip(),
        "related_id": args.related_id.strip(),
        "original_filename": args.original_filename.strip() or (Path(args.pdf).name if args.pdf else ""),
        "pdf_filename": f"{rid}.pdf",
        "md_filename": f"{rid}.md",
        "pdf_sha256": str(digest or "").strip().casefold(),
        "canonical_url": args.url.strip(),
        "registry_status": "active",
        "note_status": "none",
        "registered_at": timestamp,
        "updated_at": timestamp,
        "notes": args.notes.strip(),
    })
    rows.append(row)
    errors, warnings = validate(rows)
    if errors:
        raise ValueError("Registry sau khi thêm row không hợp lệ:\n" + "\n".join(errors))
    write_registry(args.registry, rows)
    for warning in warnings:
        print("CẦN XEM:", warning, file=sys.stderr)
    print(f"{rid}\t{rid}.pdf\t{rid}.md")
    return 0


def cmd_check(args):
    rows = read_registry(args.registry)
    errors, warnings = validate(rows)
    for error in errors:
        print("LỖI:", error)
    for warning in warnings:
        print("CẦN XEM:", warning)
    print(f"{len(rows)} record; {len(errors)} lỗi; {len(warnings)} cảnh báo.")
    return 2 if errors else (1 if warnings else 0)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=Path("results/SOURCE_REGISTRY.csv"))
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create empty registry with canonical header")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    check = sub.add_parser("check", help="Validate registry and flag duplicate candidates")
    check.set_defaults(func=cmd_check)

    find = sub.add_parser("find", help="Search for duplicate/version candidates")
    find.add_argument("--title", default="")
    find.add_argument("--year", type=int)
    find.add_argument("--first-author", default="")
    find.add_argument("--doi", default="")
    find.add_argument("--pmid", default="")
    find.add_argument("--pmcid", default="")
    find.add_argument("--sha256", default="")
    find.add_argument("--pdf", type=Path)
    find.set_defaults(func=cmd_find)

    register = sub.add_parser("register", help="Allocate the next SAL ID after duplicate checks")
    register.add_argument("--title", required=True)
    register.add_argument("--year", type=int)
    register.add_argument("--first-author", default="")
    register.add_argument("--doi", default="")
    register.add_argument("--pmid", default="")
    register.add_argument("--pmcid", default="")
    register.add_argument("--journal", default="")
    register.add_argument("--publication-type", default="article-journal")
    register.add_argument("--publication-status", default="version-of-record")
    register.add_argument("--relation-type", default="")
    register.add_argument("--related-id", default="")
    register.add_argument("--original-filename", default="")
    register.add_argument("--sha256", default="")
    register.add_argument("--pdf", type=Path)
    register.add_argument("--url", default="")
    register.add_argument("--notes", default="")
    register.add_argument("--allow-candidate", action="store_true")
    register.set_defaults(func=cmd_register)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as error:
        print("LỖI:", error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
