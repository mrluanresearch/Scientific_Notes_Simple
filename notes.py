#!/usr/bin/env python3
"""Create, check and index Markdown notes. MRLUAN/reader writes the content."""
import argparse
from collections import Counter
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


def doi_key(value):
    return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)', '', value.strip(), flags=re.I).lower()


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


def content_warnings(body, template, data):
    actual, expected = headings(body, 2), headings(template, 2)
    warnings = []
    if [h for h, _ in actual] != [h for h, _ in expected]:
        warnings.append('Chưa đúng tám mục cấp ## của NOTE_TEMPLATE.md')
    originals = dict(expected)
    for heading, content in actual:
        if not content or content == originals.get(heading):
            warnings.append(f'{heading}: rỗng hoặc chưa thay hướng dẫn mẫu')
    if re.search(r'\[[^\]\n]+\](?!\()', body):
        warnings.append('Còn chỗ trong [ngoặc vuông]; kiểm tra placeholder hoặc ký hiệu hợp lệ')

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
        if tables < 2:
            warnings.append(f'Chỉ phát hiện {tables} bảng Markdown; full_text thường cần bảng luồng/phương pháp và bảng dữ liệu dùng lại')

        expected_h3 = [h for h, _ in headings(template, 3)]
        actual_h3 = [h for h, _ in headings(body, 3)]
        missing_h3 = [h for h in expected_h3 if h not in actual_h3]
        if missing_h3:
            warnings.append('Thiếu các tiểu mục bắt buộc của mẫu chi tiết: ' + '; '.join(missing_h3))

        source_markers = len(re.findall(r'\b(?:trang|page|table|bảng|figure|hình|methods?|results?|supplement(?:ary)?)\b', body, flags=re.I))
        if source_markers < 8:
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


def write_index(folder, items):
    target = folder / 'INDEX.md'
    if target.is_symlink():
        raise ValueError('INDEX.md không được là symlink')
    fd, name = tempfile.mkstemp(prefix='.index-', dir=folder)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(index_text(items))
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notes', type=Path, default=ROOT / 'results/MD')
    sub = parser.add_subparsers(dest='command', required=True)
    new = sub.add_parser('new')
    new.add_argument('--title', required=True)
    new.add_argument('--year', type=int)
    new.add_argument('--doi', default='')
    new.add_argument('--tags', nargs='*', default=[])
    sub.add_parser('check')
    sub.add_parser('index')
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
            next_id = 1 + max([int(d['id'][4:]) for _, d, _, _ in items], default=0)
            data = dict(id=f'SAL-{next_id:04d}', year=args.year, doi=doi, tags=list(dict.fromkeys(args.tags)), read_scope='partial', status='draft')
            body = template.replace('# [Tiêu đề tài liệu]', '# ' + title, 1)
            path = args.notes / (data['id'] + '.md')
            with path.open('x', encoding='utf-8') as handle:
                handle.write('---\n' + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + '---\n\n' + body)
            print(f'Đã tạo khung: {path}. Chưa có phân tích; viết theo AGENTS.md.')
            return 0
        if args.command == 'index':
            print(write_index(args.notes, items))
            return 0
        warning_count = 0
        for path, data, body, _ in items:
            warnings = content_warnings(body, template, data)
            for warning in warnings:
                print(f'CẦN XEM {path.name}: {warning}')
            warning_count += len(warnings)
        print(f'{len(items)} note; {warning_count} điểm cần xem về cấu trúc/độ sâu. Không tự đánh giá tính đúng khoa học.')
        return 1 if warning_count else 0
    except (ValueError, TypeError, OSError, yaml.YAMLError) as error:
        print('LỖI:', error)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
