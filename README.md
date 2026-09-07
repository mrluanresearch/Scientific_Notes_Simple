# Scientific Notes Simple

Hệ thống source note tối giản cho corpus khoa học lớn. Mỗi nguồn có một định danh `SAL-xxxx`, một main PDF và một Markdown note tự đứng được. Mục tiêu là hiểu, đánh giá, trích dẫn và tái tính bằng chứng mà không phải mở lại PDF chỉ vì note đã bỏ mất thông tin tác giả có báo cáo.

## Kiến trúc canonical

| Thành phần | Vai trò |
| --- | --- |
| `AGENTS.md` | Quy tắc MRLUAN đọc nguồn, bảo toàn dữ liệu, phản biện và QC |
| `NOTE_TEMPLATE.md` | Mẫu note: 6 trường YAML + 8 mục `##` + các tiểu mục chi tiết |
| `CITATION_RULES.md` | Metadata citation CSL-ready và publication identity |
| `REGISTRY_RULES.md` | Cấp SAL ID, đặt tên PDF/MD/asset và chống trùng |
| `registry.py` | Quản lý `SOURCE_REGISTRY.csv`: init/check/find/register/hash |
| `notes.py` | Tạo note, QC cấu trúc/độ sâu/citation, INDEX, CSL-JSON |
| `PROJECT.yaml` | Ánh xạ GitHub ↔ Google Drive và policy canonical |

GitHub giữ **source code + template + rules + config**. Google Drive giữ **registry + PDF + MD results**. `results/` không được commit lên GitHub.

## Google Drive canonical

Root: `https://drive.google.com/drive/folders/1HxTYs2wg1B0K8QoF3AHuZHBeIpxUgDe_`

```text
Scientific_Notes_Simple/
└── results/
    ├── SOURCE_REGISTRY.csv
    ├── PDF/
    └── MD/
```

- `results/SOURCE_REGISTRY.csv`: identity intake, duplicate control và file mapping.
- `results/PDF/`: main PDF và supporting assets.
- `results/MD/`: scientific notes, `INDEX.md`, `references.csl.json` khi sinh.

## Quy tắc đặt tên file

Identity canonical là SAL ID, không phải author–year–title.

### Main source

- PDF: `SAL-0001.pdf`
- Note: `SAL-0001.md`
- Citation key: `SAL-0001`
- H1 trong MD: **exact source title**

Một source active có tối đa một main PDF và một main MD cùng ID.

### Supporting assets

- `SAL-0001-supp-01.pdf`
- `SAL-0001-supp-02.xlsx`
- `SAL-0001-data-01.csv`
- `SAL-0001-data-02.xlsx`
- `SAL-0001-protocol-01.pdf`
- `SAL-0001-code-01.zip`

Không dùng `final`, `final2`, `new`, `old`, `(1)`, ngày xử lý, author/year/title hoặc trạng thái trong canonical filename. Tên file gốc lúc ingest được giữ trong `SOURCE_REGISTRY.csv.original_filename` để provenance.

ID không đổi khi sửa title/DOI/author metadata, không renumber khi sort lại corpus. Sau `SAL-9999` có thể mở rộng thành `SAL-10000`.

## SOURCE_REGISTRY.csv — chống trùng trước khi tạo note

Registry tồn tại vì `INDEX.md` và corpus MD không đủ để chống trùng ở giai đoạn intake. Một PDF có thể đã được cung cấp nhưng chưa có note; cùng bài báo có thể được upload dưới filename khác; DOI có thể thiếu; preprint và version of record có thể gần giống nhau.

Các khóa quan trọng trong registry:

- `title` + `title_key`
- `year`
- `first_author` + `first_author_key`
- `doi` + `doi_key`
- `pmid`, `pmcid`
- `journal`
- publication type/status/version relation
- `original_filename`
- canonical `pdf_filename`, `md_filename`
- `pdf_sha256`
- lifecycle/audit fields

Schema và normalization đầy đủ nằm trong `REGISTRY_RULES.md`.

### Thứ tự duplicate check

1. DOI exact sau chuẩn hóa → hard duplicate candidate.
2. PMID/PMCID exact → hard candidate khi cùng publication.
3. PDF SHA-256 exact → exact binary duplicate.
4. Exact `title_key` + first author + cùng năm → strong candidate.
5. Exact title + năm cùng hoặc lệch ±1 → probable duplicate/version candidate.
6. Fuzzy title rất gần + author/journal/locator phù hợp → review thủ công, không auto-merge.

Cùng DOI nhưng title khác = **identity conflict**. Cùng title nhưng DOI khác không tự động là duplicate vì có thể là preprint, correction hoặc publication khác.

## Workflow intake bắt buộc

1. Đọc bibliographic identity tối thiểu: exact title, first author, year, DOI/PMID/PMCID nếu có.
2. Tính PDF SHA-256 khi có file local.
3. Check `SOURCE_REGISTRY.csv` trước khi cấp SAL ID hoặc upload main PDF.
4. Duplicate chắc chắn → dùng SAL ID hiện có; không tạo source mới.
5. Candidate mơ hồ → review version/metadata trước.
6. Source mới → `registry.py register` cấp SAL ID.
7. Main PDF được lưu thành `SAL-xxxx.pdf`; original filename giữ trong registry.
8. Tạo note bằng **chính SAL ID registry đã cấp**.
9. Sau khi note tạo/soát, cập nhật registry `note_status`/`updated_at`.

Registry là canonical cho **identity intake + file mapping**. MD là canonical cho **scientific content + full citation metadata**. `INDEX.md` là file dẫn xuất để browse.

## Citation metadata

Mỗi note có block `citation:` ở mục 1 theo cấu trúc gần CSL-JSON. Không lưu một câu APA/Vancouver đã format làm dữ liệu canonical.

Journal article thường cần: authors đầy đủ, `issued`, exact title, journal/container, volume, issue, pages/article number, DOI, URL canonical nếu có. DOI ở registry, YAML note và citation block phải khớp sau chuẩn hóa.

Chi tiết xem `CITATION_RULES.md`.

## Tiêu chuẩn scientific note

Một `full_text` note phải giữ đủ thông tin để người đọc trả lời được:

1. Nghiên cứu hỏi gì, ở đâu, trên quần thể/dữ liệu nào?
2. Luồng farm/flock/bird/sample/isolate/genome/study ra sao?
3. Methods cụ thể: culture, AST, PCR, WGS, tool/database/version/threshold, statistics?
4. Kết quả nào với tử số/mẫu số, unit, CI/p-value, subgroup?
5. Kết quả âm tính/ngoại lệ nào ảnh hưởng diễn giải?
6. Abstract ↔ Results ↔ Table ↔ Figure có khớp không; MRLUAN tính lại được gì?
7. Tác giả diễn giải gì và bằng chứng thực sự hỗ trợ tới đâu?
8. Dùng lại/tái lập được gì; thiếu supplement/raw data/parameter nào?
9. Có thể tạo citation đúng mà không mở lại PDF hay không?

Full-text experimental/WGS/AMR thường khoảng **1.800–3.500 từ tiếng Việt chưa tính bảng**; systematic review/meta-analysis thường **2.000–4.000 từ**. Đây là chuẩn biên tập, không phải quota.

Các nguyên tắc bắt buộc:

- Không thay Methods/Results bằng abstract.
- Không ghi `xem Table X trong PDF` nếu số liệu đó cần dùng lại; chép bảng con cần thiết vào MD.
- Prevalence/proportion ưu tiên tử số/mẫu số, không chỉ `%`.
- AST giữ panel/concentration/standard/breakpoint khi nguồn có.
- PCR giữ target/primer/product size/cycling khi có.
- WGS giữ platform/reference/tool/database/version/threshold/accession khi có.
- Meta-analysis giữ search strategy, study count, model, heterogeneity, subgroup, risk of bias, sensitivity/publication bias.
- `không báo cáo` là dữ liệu quan trọng; không tự điền bằng thông lệ.
- Gene presence ≠ phenotype/expression; genomic relatedness ≠ direct transmission; association ≠ causality.
- Nếu số nguồn không khớp, giữ số gốc + phép tính + vị trí; không âm thầm sửa.

## Mẫu note

YAML chỉ gồm:

```yaml
id: SAL-0001
year: 2025
doi: "10.xxxx/xxxxx"
tags: [amr, wgs]
read_scope: full_text
status: draft
```

Tám mục `##` cố định:

1. Tài liệu và phạm vi đọc
2. Câu hỏi và đóng góp chính
3. Thiết kế và phương pháp
4. Kết quả và dữ liệu cần giữ
5. Diễn giải và phản biện
6. Giá trị đối với luận án
7. Cách dùng lại và phần còn thiếu
8. Đoạn tổng hợp có thể sử dụng

`NOTE_TEMPLATE.md` định nghĩa các tiểu mục chi tiết bắt buộc.

## Trạng thái

Note:
- `draft`: đang viết, còn bất nhất, thiếu supplement/raw data quan trọng hoặc citation/scientific result chưa xác minh.
- `checked`: đã đối chiếu source identity và thông tin trung tâm trong phạm vi đọc khai báo; không có nghĩa peer review độc lập.

Registry có lifecycle riêng: `active`, `review`, `duplicate`, `excluded`, `superseded`.

## Chạy công cụ

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

### 1. Registry

```bash
python registry.py --registry results/SOURCE_REGISTRY.csv check

python registry.py --registry results/SOURCE_REGISTRY.csv find \
  --title "Exact source title" \
  --year 2026 \
  --first-author "Family, Given" \
  --doi 10.xxxx/xxxxx

python registry.py --registry results/SOURCE_REGISTRY.csv register \
  --title "Exact source title" \
  --year 2026 \
  --first-author "Family, Given" \
  --doi 10.xxxx/xxxxx \
  --original-filename original.pdf
```

Nếu có local PDF, dùng `--pdf path/to/file.pdf` để script tính SHA-256. `register` từ chối hard duplicate và dừng ở probable duplicate/version candidate trừ khi đã review rồi dùng `--allow-candidate`.

### 2. Tạo note bằng ID registry đã cấp

Ví dụ registry trả `SAL-0001`:

```bash
python notes.py new \
  --id SAL-0001 \
  --title "Exact source title" \
  --year 2026 \
  --doi 10.xxxx/xxxxx \
  --tags amr wgs
```

`notes.py new --id` bảo đảm note dùng đúng ID registry. Chế độ không truyền `--id` chỉ giữ để tương thích khi chưa vận hành registry-first; không dùng trong workflow canonical mới.

### 3. QC / index / citation export

```bash
python notes.py check
python notes.py index
python notes.py csl
python registry.py --registry results/SOURCE_REGISTRY.csv check
```

`notes.py check` là heuristic QC cấu trúc/độ sâu/citation, không chứng minh tính đúng khoa học. `registry.py check` kiểm tra schema, canonical filenames, exact duplicate keys và probable title/version candidates.

## Tổ chức 1.000 tài liệu

Mỗi source active nên có:

- 1 row trong `SOURCE_REGISTRY.csv`
- 1 main `SAL-xxxx.pdf`
- 1 `SAL-xxxx.md`
- supporting assets theo hậu tố chuẩn nếu có

Sau mỗi đợt 10–20 nguồn, chạy registry check và chọn 2–3 note để đọc ngược với PDF. Nếu xuất hiện lỗi lặp lại, sửa rules/template/code trước khi mở rộng batch.

Chất lượng corpus = **identity sạch + note chi tiết + provenance truy vết được**, không phải chỉ số lượng file.