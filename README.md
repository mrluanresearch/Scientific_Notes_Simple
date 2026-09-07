# Scientific Notes Simple

Hệ thống source-note và evidence-synthesis cho corpus khoa học lớn. Mỗi publication/source có một định danh ổn định `SAL-xxxx`, một main PDF, một Markdown note tự đứng được, một audit row verification và một row study-level trong evidence matrix. Mục tiêu là bảo toàn identity, denominator, methods, kết quả, bất nhất và giới hạn đủ để đọc lại, trích dẫn, so sánh và tái sử dụng bằng chứng có kiểm soát.

## Kiến trúc canonical

| Thành phần | Vai trò |
| --- | --- |
| `AGENTS.md` | Quy tắc MRLUAN đọc nguồn, bảo toàn dữ liệu, phản biện và QC |
| `NOTE_TEMPLATE.md` | Mẫu note: 6 trường YAML + 8 mục `##` + các tiểu mục chi tiết |
| `CITATION_RULES.md` | Metadata citation CSL-ready và publication identity |
| `REGISTRY_RULES.md` | Cấp SAL ID, đặt tên PDF/MD/asset và chống trùng |
| `VERIFICATION_RULES.md` | Quy tắc nâng `draft` → `checked` và audit source-level verification |
| `DRIVE_WRITE_RULES.md` | Read-before-write, update-in-place và chống duplicate canonical files |
| `EVIDENCE_MATRIX_RULES.md` | Schema và nguyên tắc tạo synthesis study-level từ checked notes |
| `registry.py` | Quản lý `SOURCE_REGISTRY.csv`: init/check/find/register/hash |
| `notes.py` | Tạo note, QC cấu trúc/độ sâu/citation, INDEX, CSL-JSON |
| `verification.py` | Kiểm tra traceability registry ↔ verification ↔ MD ↔ INDEX |
| `evidence_matrix.py` | Kiểm tra schema/provenance/staleness của `EVIDENCE_MATRIX.csv` |
| `PROJECT.yaml` | Ánh xạ GitHub ↔ Google Drive và policy canonical |

GitHub giữ **source code + template + rules + config**. Google Drive giữ **registry + verification + evidence matrix + PDF + MD results**. `results/` không được commit lên GitHub.

## Google Drive canonical

Root: `https://drive.google.com/drive/folders/1HxTYs2wg1B0K8QoF3AHuZHBeIpxUgDe_`

```text
Scientific_Notes_Simple/
└── results/
    ├── SOURCE_REGISTRY.csv
    ├── SOURCE_VERIFICATION.csv
    ├── EVIDENCE_MATRIX.csv
    ├── PDF/
    └── MD/
        ├── SAL-xxxx.md
        ├── INDEX.md
        └── references.csl.json
```

Vai trò của ba CSV được tách rõ:

- `SOURCE_REGISTRY.csv`: publication identity, duplicate control, lifecycle và file mapping.
- `SOURCE_VERIFICATION.csv`: audit source-level verification cho các note `checked`.
- `EVIDENCE_MATRIX.csv`: một row/source active, chuẩn hóa bằng chứng study-level để synthesis xuyên nghiên cứu.

`EVIDENCE_MATRIX.csv` không thay note và không phải long-form raw dataset cho meta-analysis. Nếu cần one-row-per-drug/gene/outcome, tạo dataset dẫn xuất riêng với provenance quay về SAL ID.

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

## Registry-first — chống trùng trước khi tạo note

Trước khi cấp SAL ID hoặc upload main PDF, kiểm tra theo thứ tự:

1. DOI exact sau chuẩn hóa.
2. PMID/PMCID exact.
3. PDF SHA-256 exact.
4. Exact normalized title + first author + year.
5. Exact title + năm cùng hoặc lệch ±1 để phát hiện online-first/preprint/version.
6. Fuzzy title chỉ tạo candidate review; không auto-merge.

Cùng DOI nhưng title khác = **identity conflict**. Cùng title nhưng DOI khác không tự động là duplicate vì có thể là preprint, correction hoặc publication khác. Chi tiết xem `REGISTRY_RULES.md`.

## Scientific note

Một `full_text` note phải tự đứng được. Nếu thông tin quan trọng có trong PDF nhưng phải mở PDF chỉ để nhớ lại thiết kế, denominator, protocol, primer, threshold, bảng số liệu, bibliographic metadata hoặc giới hạn, note chưa hoàn thành.

YAML canonical chỉ gồm:

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

Các nguyên tắc quan trọng:

- Không thay Methods/Results bằng abstract.
- Prevalence/proportion giữ tử số/mẫu số và unit of analysis.
- Phân biệt farm/flock/bird/sample/isolate/genome/study.
- AST giữ method/panel/concentration/standard/breakpoint khi nguồn có.
- PCR giữ target/primer/product size/cycling khi có giá trị tái sử dụng.
- WGS giữ platform/reference/tool/database/version/threshold/accession khi có.
- Meta-analysis giữ search strategy, study count, effect model, heterogeneity, subgroup, risk of bias và sensitivity/publication bias.
- `không báo cáo` là dữ liệu; không tự điền bằng thông lệ.
- Gene presence ≠ phenotype/expression; genomic relatedness ≠ direct transmission; association ≠ causality.
- Nếu Abstract ↔ Results ↔ Table ↔ Figure không khớp, giữ cả giá trị nguồn + phép tính lại + vị trí; không âm thầm sửa.

Chi tiết xem `NOTE_TEMPLATE.md` và `AGENTS.md`.

## Trạng thái và source verification

Note:

- `draft`: đang viết hoặc chưa hoàn tất source-level verification.
- `checked`: identity và thông tin trung tâm đã được đối chiếu với source trong `read_scope` khai báo.

`checked` không có nghĩa source không có bias, discrepancy đã được giải quyết, supplement/raw data đã được tái lập hoặc kết luận của tác giả đã được xác nhận độc lập. Mọi discrepancy quan trọng vẫn phải nằm trong note và `SOURCE_VERIFICATION.csv`.

## EVIDENCE_MATRIX.csv

Matrix là lớp synthesis study-level. Mỗi `registry_status=active` phải có đúng một row cùng `SAL-xxxx`.

Nhóm trường chính gồm:

- identity: ID, year, author, title, DOI, journal, filenames, hashes;
- context/design: country/region, study design, population/sample context;
- denominator/prevalence;
- serovar;
- AST;
- AMR genes/mutations;
- virulence;
- WGS/MLST/plasmid/SNP/phylogeny;
- negative findings/exceptions;
- arithmetic/internal consistency;
- limitations;
- thesis use/comparison conditions/`do_not_conclude`;
- evidence reuse decision và quantitative reuse scope;
- verification severity/result/unresolved issues;
- `note_sha256` để phát hiện row stale khi MD thay đổi.

### Controlled vocabulary: quantitative reuse

- `prevalence_or_sample_level_conditional`
- `isolate_or_genome_level`
- `experimental_parameter_only`
- `review_pooled_estimates`
- `review_summary_only`

Không được biến selected isolates/genomes thành population prevalence; không biến experimental transfer parameter thành natural prevalence; không dùng review descriptive như pooled estimate.

### Matrix status

- `draft`
- `generated_from_checked_note`
- `checked_against_checked_note`

`checked_against_checked_note` chỉ xác nhận row đã được đối chiếu với checked note và verification provenance; không tự động đủ điều kiện meta-analysis.

Chi tiết xem `EVIDENCE_MATRIX_RULES.md`.

## Workflow canonical cho mỗi batch

1. Đọc identity tối thiểu và tính PDF SHA-256.
2. Duplicate check trong `SOURCE_REGISTRY.csv`.
3. Cấp SAL ID cho source mới.
4. Upload PDF canonical bằng read-before-write.
5. Viết note chi tiết bằng đúng SAL ID.
6. QC note và source-level verification.
7. Update registry + verification log + INDEX + CSL in-place.
8. Tạo/cập nhật đúng một row `EVIDENCE_MATRIX.csv` từ checked note.
9. Tính `note_sha256`; nếu note đổi, matrix row phải được review lại.
10. Chạy validators và post-write Drive inventory; không tạo file `final`, `v2` hoặc canonical duplicate.

## Chạy công cụ

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

### Registry

```bash
python registry.py --registry results/SOURCE_REGISTRY.csv check

python registry.py --registry results/SOURCE_REGISTRY.csv find \
  --title "Exact source title" \
  --year 2026 \
  --first-author "Family, Given" \
  --doi 10.xxxx/xxxxx
```

### Note / index / citation

```bash
python notes.py check
python notes.py index
python notes.py csl
```

### Verification

```bash
python verification.py \
  --registry results/SOURCE_REGISTRY.csv \
  --verification results/SOURCE_VERIFICATION.csv \
  --notes results/MD \
  --index results/MD/INDEX.md
```

### Evidence matrix

```bash
python evidence_matrix.py \
  --matrix results/EVIDENCE_MATRIX.csv \
  --registry results/SOURCE_REGISTRY.csv \
  --verification results/SOURCE_VERIFICATION.csv \
  --notes results/MD
```

`evidence_matrix.py` kiểm tra schema, identity, provenance, controlled vocabulary và `note_sha256` staleness. Script không tự trích xuất bằng chứng, không tự sửa denominator và không tự nâng scientific status.

## Tổ chức corpus lớn

Mỗi source active nên có:

- 1 row trong `SOURCE_REGISTRY.csv`;
- 1 main `SAL-xxxx.pdf`;
- 1 `SAL-xxxx.md`;
- 1 row trong `SOURCE_VERIFICATION.csv` khi note là `checked`;
- 1 row trong `EVIDENCE_MATRIX.csv`;
- supporting assets theo hậu tố chuẩn nếu có.

Sau mỗi batch 10–20 nguồn, chạy registry/verification/matrix validators và chọn một số note để đọc ngược với PDF. Nếu xuất hiện lỗi lặp lại, sửa rules/template/code trước khi mở rộng corpus.

Chất lượng corpus = **identity sạch + note chi tiết + verification truy vết được + synthesis không làm mất denominator/giới hạn**.
