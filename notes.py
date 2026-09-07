#!/usr/bin/env python3
"""Create, check, index and export citation metadata from Markdown source notes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import os
import tempfile

import yaml

ROOT = Path(__file__).resolve().parent
FIELDS = {'id', 'year', 'doi', 'tags', 'read_scope', 'status'}
SCOPES = {'full_text', 'partial', 'abstract'}
STATUSES = {'draft', 'checked'}
ID = re.compile(r'SAL-\d{4,}$')
CITATION_RE = re.compile(
    r'<!--\s*CITATION_METADATA_START\s*-->\s*```ya?ml\s*(.*?)\s*```\s*<!--\s*CITATION_METADATA_END\s*-->',
    re.I | re.S,
)


def doi_key(value):
    return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', str(value or '').strip(), flags=re.I).lower()


def normalized_text(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip().casefold()


def headings(body, level=2):
    clean = re.sub(r'^(`{3,}|~{3,}).*?^\1\s*$', '', body, flags=re.M | re.S)
    marker = '#' * level
    matches = list(re.finditer(rf'^{re.escape(marker)} (.+)$', clean, re.M))
    return [(m[1], clean[m.end():matches[i+1].start() if i+1 < len(matches) else len(clean)].strip())
            for i, m in enumerate(matches)]


def word_count(text):
    """Approximate Unicode word count for Vietnamese/English scientific prose."""
    return len(re.findall(r'\b[^\W_]+(?:[-′’][^\W_]+)*\b', text, flags=re.UNICODE))


def table_count(text):
    """Count Markdown table separator rows, a useful proxy for reusable data tables."""
    return len(re.findall(r'^\s*\|(?:\s*:?-{3,}:?\s*\|){2,}\s*$', text, flags=re.M))


def load(path):
    raw = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    front = re.match(r'\A---\n(.*?)\n---\n(.*)\Z', raw, re.S)
    if not front:
        raise ValueError('Thiếu YAML đầu tệp hoặc dấu đóng ---')
    node = yaml.compose(front[1])
    if not isinstance(node, yaml.MappingNode):
        raise ValueError('YAML phải là mapping sáu trường')
    keys = [k.value for k, v in node.value]
    if len(keys) != len(set(keys)):
        raise ValueError('YAML có khóa trùng')
    data, body = yaml.safe_load(front[1]), front[2].lstrip('\n')
    if set(data) != FIELDS:
        raise ValueError('YAML chỉ gồm: id, year, doi, tags, read_scope, status')
    if not isinstance(data['id'], str) or not ID.fullmatch(data['id']) or path.stem != data['id']:
        raise ValueError('ID phải dạng SAL-0001 và khớp tên tệp')
    if data['year'] is not None and (type(data['year']) is not int or not 1000 <= data['year'] <= 9999):
        raise ValueError('year phải là năm hoặc null')
    if not isinstance(data['doi'], str):
        raise ValueError('doi phải là chuỗi; chưa có dùng ""')
    if not isinstance(data['tags'], list) or any(not isinstance(t, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', t) for t in data['tags']):
        raise ValueError('tags là danh sách chữ thường không dấu, ví dụ [amr, wgs]')
    if data['read_scope'] not in SCOPES or data['status'] not in STATUSES:
        raise ValueError('read_scope/status không hợp lệ; xem README')
    titles = re.findall(r'^# (.+)$', body, re.M)
    if len(titles) != 1:
        raise ValueError('Cần đúng một tiêu đề cấp #')
    return data, body, titles[0]


def scan(folder):
    items, errors, seen = [], [], {}
    for path in sorted(folder.glob('*.md')):
        if path.name == 'INDEX.md':
            continue
        try:
            if path.is_symlink():
                raise ValueError('Không dùng symlink cho source note')
            data, body, title = load(path)
            doi = doi_key(data['doi'])
            if doi and doi in seen:
                raise ValueError(f'DOI trùng với {seen[doi]}')
            if doi:
                seen[doi] = path.name
            items.append((path, data, body, title))
        except (ValueError, TypeError, OSError, yaml.YAMLError) as error:
            errors.append(f'{path.name}: {error}')
    return items, errors


def parse_citation(body):
    match = CITATION_RE.search(body)
    if not match:
        return None, ['Thiếu block CITATION_METADATA_START/END']
    try:
        payload = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        return None, [f'Citation YAML không hợp lệ: {error}']
    if not isinstance(payload, dict) or not isinstance(payload.get('citation'), dict):
        return None, ['Citation block phải chứa mapping `citation:`']
    return payload['citation'], []


def citation_issues(data, body, title):
    citation, errors = parse_citation(body)
    warnings = []
    if errors:
        return citation, errors, warnings

    for field in ('id', 'type', 'title'):
        if not str(citation.get(field, '')).strip():
            errors.append(f'citation.{field} bắt buộc')

    if citation.get('id') != data['id']:
        errors.append(f'citation.id phải khớp {data["id"]}')

    if normalized_text(citation.get('title')) != normalized_text(title):
        errors.append('citation.title phải khớp chính xác H1/exact source title')

    authors = citation.get('author')
    if not isinstance(authors, list) or not authors:
        warnings.append('citation.author đang rỗng; chỉ chấp nhận nếu nguồn thực sự không có tác giả')
    else:
        for i, author in enumerate(authors, 1):
            if not isinstance(author, dict):
                errors.append(f'citation.author[{i}] phải là mapping')
                continue
            literal = str(author.get('literal', '')).strip()
            family = str(author.get('family', '')).strip()
            given = str(author.get('given', '')).strip()
            if not literal and not family:
                errors.append(f'citation.author[{i}] cần `family` hoặc `literal`')
            if literal and (family or given):
                warnings.append(f'citation.author[{i}] dùng corporate `literal`; không nên đồng thời có family/given')

    issued = citation.get('issued')
    issued_year = None
    try:
        parts = issued['date-parts']
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            issued_year = parts[0][0]
    except (TypeError, KeyError):
        parts = None
    if issued_year is None:
        warnings.append('citation.issued chưa có năm; nếu nguồn có ngày xuất bản phải điền date-parts')
    elif type(issued_year) is not int or not 1000 <= issued_year <= 9999:
        errors.append('citation.issued.date-parts có năm không hợp lệ')
    elif data['year'] is not None and issued_year != data['year']:
        errors.append(f'citation issued year {issued_year} không khớp YAML year {data["year"]}')

    citation_doi = doi_key(citation.get('DOI', ''))
    yaml_doi = doi_key(data['doi'])
    if citation_doi != yaml_doi:
        errors.append('citation.DOI phải khớp YAML doi sau chuẩn hóa')

    ctype = str(citation.get('type', '')).strip()
    if ctype == 'article-journal':
        if not str(citation.get('container-title', '')).strip():
            warnings.append('Journal article thiếu citation.container-title')
        if not any(str(citation.get(k, '')).strip() for k in ('volume', 'issue', 'page')):
            warnings.append('Journal article chưa có volume/issue/page hoặc article number; kiểm tra version of record')

    if re.search(r'\bTODO(?:_[A-Z_]+)?\b', yaml.safe_dump(citation, allow_unicode=True), re.I):
        errors.append('Citation metadata còn TODO placeholder')

    return citation, errors, warnings


def content_warnings(body, template, data, title):
    actual, expected = headings(body, 2), headings(template, 2)
    warnings = []
    if [h for h, _ in actual] != [h for h, _ in expected]:
        warnings.append('Chưa đúng tám mục cấp ## của NOTE_TEMPLATE.md')
    originals = dict(expected)
    for heading, content in actual:
        if not content or content == originals.get(heading):
            warnings.append(f'{heading}: rỗng hoặc chưa thay hướng dẫn mẫu')
    if re.search(r'\bTODO(?:_[A-Z_]+)?\b', body):
        warnings.append('Còn TODO placeholder')
    if re.search(r'\[[^\]\n]+\](?!\()', body):
        warnings.append('Còn chỗ trong [ngoặc vuông]; kiểm tra placeholder hoặc ký hiệu hợp lệ')

    _, citation_errors, citation_warnings = citation_issues(data, body, title)
    warnings.extend('Citation: ' + issue for issue in citation_errors + citation_warnings)

    if data['read_scope'] == 'full_text':
        total = word_count(body)
        if total < 1800:
            warnings.append(f'full_text chỉ khoảng {total} từ; rà lại Methods/Results/Tables theo AGENTS.md (thường >=1800 từ cho nguồn nhiều dữ liệu)')

        sections = dict(actual)
        methods_results = ' '.join([
            sections.get('3. Thiết kế và phương pháp', ''),
            sections.get('4. Kết quả và dữ liệu cần giữ', '')
        ])
        mr_words = word_count(methods_results)
        if mr_words < 900:
            warnings.append(f'Mục 3–4 chỉ khoảng {mr_words} từ; chưa đủ chiều sâu để bảo toàn phương pháp và dữ liệu')

        tables = table_count(body)
        if tables < 3:
            warnings.append(f'Chỉ phát hiện {tables} bảng Markdown; full_text chi tiết thường cần metadata/source table, methods/flow và data table')

        expected_h3 = [h for h, _ in headings(template, 3)]
        actual_h3 = [h for h, _ in headings(body, 3)]
        missing_h3 = [h for h in expected_h3 if h not in actual_h3]
        if missing_h3:
            warnings.append('Thiếu các tiểu mục bắt buộc của mẫu chi tiết: ' + '; '.join(missing_h3))

        source_markers = len(re.findall(r'\b(?:trang|page|table|bảng|figure|hình|methods?|results?|supplement(?:ary)?|data availability)\b', body, flags=re.I))
        if source_markers < 10:
            warnings.append('Ít vị trí nguồn cụ thể; thêm trang/bảng/hình/mục để truy vết bằng chứng nhanh')

    return warnings


def index_text(items):
    counts = Counter(data['status'] for _, data, _, _ in items)
    lines = ['# Mục lục tài liệu', '',
             f'Tổng: {len(items)} | Đang viết: {counts["draft"]} | Đã soát theo khai báo: {counts["checked"]}', '',
             'Mục lục sinh từ note. Trạng thái là khai báo của MRLUAN/người đọc, không phải điểm chất lượng tự động.', '',
             '| ID | Năm | Tài liệu | DOI | Chủ đề | Phạm vi đọc | Trạng thái |',
             '| --- | --- | --- | --- | --- | --- | --- |']
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ').replace('[', '\\[').replace(']', '\\]')
    for path, data, _, title in sorted(items, key=lambda x: int(x[1]['id'][4:])):
        lines.append(f'| {data["id"]} | {data["year"] or ""} | [{cell(title)}]({path.name}) | '
                     f'{cell(data["doi"])} | {cell(", ".join(data["tags"]))} | {data["read_scope"]} | {data["status"]} |')
    return '\n'.join(lines) + '\n'


def atomic_write(target, text):
    if target.is_symlink():
        raise ValueError(f'{target.name} không được là symlink')
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + target.stem + '-', dir=target.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(text)
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def write_index(folder, items):
    target = folder / 'INDEX.md'
    atomic_write(target, index_text(items))
    return target


def clean_csl(value):
    if isinstance(value, dict):
        cleaned = {k: clean_csl(v) for k, v in value.items()}
        return {k: v for k, v in cleaned.items() if v not in ('', None, [], {})}
    if isinstance(value, list):
        cleaned = [clean_csl(v) for v in value]
        return [v for v in cleaned if v not in ('', None, [], {})]
    return value


def write_csl(folder, items, output=None):
    citations = []
    errors = []
    warnings = []
    for path, data, body, title in items:
        citation, c_errors, c_warnings = citation_issues(data, body, title)
        errors.extend(f'{path.name}: {e}' for e in c_errors)
        warnings.extend(f'{path.name}: {w}' for w in c_warnings)
        if citation is not None and not c_errors:
            citations.append(clean_csl(citation))
    if errors:
        raise ValueError('Không xuất CSL vì citation metadata có lỗi:\n' + '\n'.join(errors))
    target = output or (folder / 'references.csl.json')
    atomic_write(target, json.dumps(citations, ensure_ascii=False, indent=2) + '\n')
    return target, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notes', type=Path, default=ROOT / 'results/MD')
    sub = parser.add_subparsers(dest='command', required=True)
    new = sub.add_parser('new')
    new.add_argument('--id', help='SAL ID đã được registry cấp, ví dụ SAL-0001')
    new.add_argument('--title', required=True)
    new.add_argument('--year', type=int)
    new.add_argument('--doi', default='')
    new.add_argument('--tags', nargs='*', default=[])
    sub.add_parser('check')
    sub.add_parser('index')
    csl = sub.add_parser('csl')
    csl.add_argument('--out', type=Path)
    args = parser.parse_args(argv)
    try:
        if not args.notes.exists() and args.command != 'new':
            raise ValueError('Không tìm thấy thư mục note; kiểm tra --notes')
        if args.command == 'new':
            args.notes.mkdir(parents=True, exist_ok=True)
        items, errors = scan(args.notes)
        if errors:
            raise ValueError('\n'.join(errors))
        template = (ROOT / 'NOTE_TEMPLATE.md').read_text(encoding='utf-8').split('\n---\n', 1)[1].lstrip('\n')
        if args.command == 'new':
            title = ' '.join(args.title.split())
            if not title or (args.year is not None and not 1000 <= args.year <= 9999):
                raise ValueError('Tiêu đề/năm không hợp lệ')
            if any(not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', t) for t in args.tags):
                raise ValueError('Tag dùng chữ thường không dấu và dấu gạch nối')
            doi = doi_key(args.doi)
            if any((doi and doi_key(d['doi']) == doi) or title.casefold() == t.casefold() for _, d, _, t in items):
                raise ValueError('DOI/tiêu đề đã có; mở note hiện hành để rà trùng')
            if args.id:
                if not ID.fullmatch(args.id):
                    raise ValueError('--id phải dạng SAL-0001 trở lên')
                if any(d['id'] == args.id for _, d, _, _ in items):
                    raise ValueError(f'ID {args.id} đã có note')
                note_id = args.id
            else:
                next_id = 1 + max([int(d['id'][4:]) for _, d, _, _ in items], default=0)
                note_id = f'SAL-{next_id:04d}'
            data = dict(id=note_id, year=args.year, doi=doi, tags=list(dict.fromkeys(args.tags)), read_scope='partial', status='draft')
            body = template.replace('SAL-0001', data['id']).replace('TODO_EXACT_SOURCE_TITLE', title)
            if args.year is not None:
                body = body.replace('- [null]', f'- [{args.year}]', 1)
            if doi:
                body = body.replace('  DOI: ""', f'  DOI: "{doi}"', 1)
            path = args.notes / (data['id'] + '.md')
            with path.open('x', encoding='utf-8') as handle:
                handle.write('---\n' + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + '---\n\n' + body)
            if args.id:
                print(f'Đã tạo khung: {path} theo SAL ID do registry cấp. Điền citation metadata và nội dung theo AGENTS.md/CITATION_RULES.md/REGISTRY_RULES.md.')
            else:
                print(f'Đã tạo khung: {path}. Chưa truyền --id; chỉ dùng chế độ tự cấp ID khi không vận hành registry-first.')
            return 0
        if args.command == 'index':
            print(write_index(args.notes, items))
            return 0
        if args.command == 'csl':
            target, csl_warnings = write_csl(args.notes, items, args.out)
            for warning in csl_warnings:
                print('CẦN XEM CITATION:', warning)
            print(target)
            return 1 if csl_warnings else 0
        warning_count = 0
        for path, data, body, title in items:
            warnings = content_warnings(body, template, data, title)
            for warning in warnings:
                print(f'CẦN XEM {path.name}: {warning}')
            warning_count += len(warnings)
        print(f'{len(items)} note; {warning_count} điểm cần xem về cấu trúc/độ sâu/citation. Không tự đánh giá tính đúng khoa học.')
        return 1 if warning_count else 0
    except (ValueError, TypeError, OSError, yaml.YAMLError) as error:
        print('LỖI:', error)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())