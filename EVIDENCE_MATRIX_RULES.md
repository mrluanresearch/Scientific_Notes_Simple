# EVIDENCE_MATRIX.csv — quy tắc synthesis study-level

`results/EVIDENCE_MATRIX.csv` là lớp dữ liệu tổng hợp **study-level** của `Scientific_Notes_Simple`. Nó nằm trên Google Drive cùng registry/verification và **không được commit lên GitHub**. GitHub chỉ giữ schema, rules và validator.

## Vai trò và ranh giới

- `SOURCE_REGISTRY.csv` trả lời: **nguồn này là tài liệu nào, có trùng không, file canonical nào?**
- `SAL-xxxx.md` trả lời: **nguồn báo cáo gì, bằng phương pháp nào, denominator nào, bất nhất và giới hạn gì?**
- `SOURCE_VERIFICATION.csv` trả lời: **note đã được cross-check với source trong phạm vi nào?**
- `EVIDENCE_MATRIX.csv` trả lời: **mỗi nguồn đóng góp lớp bằng chứng nào để so sánh xuyên nghiên cứu?**

Matrix không thay thế note, không thay thế PDF và không phải raw dataset cho meta-analysis. Khi cần one-row-per-outcome hoặc drug/gene-level pooling, tạo lớp dữ liệu long-form riêng thay vì nhồi nhiều outcome không tương thích vào một ô.

## Một source active = một row

Mỗi `registry_status=active` phải có đúng một row `EVIDENCE_MATRIX.csv` cùng `id`. Không tạo row riêng cho cùng một source chỉ vì có nhiều outcome. Supplement/data không có SAL ID riêng trừ khi được đăng ký như một publication/source độc lập theo `REGISTRY_RULES.md`.

## Nguồn sự thật của từng nhóm cột

- Identity (`id`, `year`, `first_author`, `title`, `doi`, `journal`, filenames, PDF hash, canonical URL): lấy từ `SOURCE_REGISTRY.csv`.
- Scientific evidence: chỉ rút từ **note canonical đã kiểm tra**, ưu tiên §§2.3, 3.1, 4.1–4.4, 5.3, 6.1–6.3, 7.3.
- Verification/severity/unresolved issues: lấy nguyên ý từ `SOURCE_VERIFICATION.csv`.
- `note_sha256`: SHA-256 của chính `SAL-xxxx.md` dùng để sinh/soát row; đây là khóa phát hiện matrix stale khi note thay đổi.

Không lấy một con số trực tiếp từ abstract/web để ghi matrix nếu note canonical chưa có và chưa kiểm tra con số đó.

## Schema canonical

Thứ tự cột được khóa trong `evidence_matrix.py`:

`id, year, first_author, title, doi, journal, country_region, study_design, tags, population_sample_context, denominator_prevalence_summary, serovar_summary, ast_summary, amr_gene_summary, virulence_summary, genomics_mlst_plasmid_phylogeny_summary, negative_findings_exceptions, arithmetic_internal_consistency, main_limitations, thesis_use, comparison_conditions, do_not_conclude, evidence_reuse_decision, quantitative_reuse_scope, source_discrepancy_severity, source_verification_result, unresolved_source_issues, note_status, matrix_status, pdf_filename, md_filename, pdf_sha256, note_sha256, canonical_url, matrix_generated_at`.

Không đổi tên/thứ tự cột âm thầm. Mọi migration schema phải sửa rules + validator + `PROJECT.yaml` và tạo migration rõ ràng.

## Denominator là bắt buộc về mặt ngữ nghĩa

`denominator_prevalence_summary` phải giữ đủ context để phân biệt:

- sample/farm/flock/bird/patient;
- positive sample vs recovered isolate;
- isolate tested by AST/PCR vs isolate sequenced;
- public genome/database record vs prospectively sampled unit;
- study count trong review/meta-analysis.

Không chuyển `x%` sang matrix nếu không biết mẫu số/đơn vị tạo ra tỷ lệ đó. Nếu source không báo đủ, giữ sự thiếu hụt/bất nhất thay vì tự suy.

## Các domain evidence

- `serovar_summary`: serovar/serotype và denominator liên quan.
- `ast_summary`: phenotype, drug, numerator/denominator hoặc MIC/zone/effect khi có; giữ standard/breakpoint context trong note.
- `amr_gene_summary`: ARG/mutation; gene presence không đồng nghĩa phenotype.
- `virulence_summary`: virulence determinant/pathogenicity island; gene presence không đồng nghĩa expression hoặc clinical virulence.
- `genomics_mlst_plasmid_phylogeny_summary`: WGS subset, ST/MLST/cgMLST, plasmid/replicon, SNP/allele/clade/source-attribution inference.

Ô domain có thể để trống khi **không áp dụng/không được nguồn báo cáo**. Trống không được diễn giải thành kết quả âm tính; kết quả âm tính thật phải nằm ở `negative_findings_exceptions`.

## Controlled vocabulary: quantitative_reuse_scope

Chỉ dùng một trong năm giá trị:

- `prevalence_or_sample_level_conditional`: có denominator sample-level có thể dùng có điều kiện sau harmonization.
- `isolate_or_genome_level`: selected/archived/clinical/genomic isolates; không suy prevalence quần thể.
- `experimental_parameter_only`: transfer/intervention/lab experiment; dùng parameter/contrast, không dùng làm field prevalence.
- `review_pooled_estimates`: systematic review/meta-analysis; estimate phải đi cùng CI/heterogeneity/subgroup.
- `review_summary_only`: narrative/systematic descriptive review không có pooled effect phù hợp.

## matrix_status

- `draft`: row đang xây/soát.
- `generated_from_checked_note`: row được dựng từ checked note nhưng chưa hoàn tất row-level cross-check.
- `checked_against_checked_note`: identity, evidence summaries, limits và reuse decision đã được đối chiếu với checked note; verification fields khớp log; `note_sha256` khớp note hiện hành.

`checked_against_checked_note` **không** có nghĩa source không bias, discrepancy đã được giải quyết, hay estimate đủ điều kiện meta-analysis.

Không được để script tự nâng từ `draft` sang `checked_against_checked_note` chỉ vì schema hợp lệ.

## Bất nhất và giới hạn phải đi theo row

- `arithmetic_internal_consistency` giữ phép tính lại/Abstract↔Text↔Table↔Figure conflict.
- `main_limitations` giữ threats to validity cụ thể.
- `source_discrepancy_severity`, `source_verification_result`, `unresolved_source_issues` phải khớp `SOURCE_VERIFICATION.csv`.
- `do_not_conclude` khóa các overclaim thường gặp: prevalence từ selected isolates, gene→phenotype, gene→virulence, relatedness→direct transmission, association→causality.

Không “làm sạch” matrix bằng cách xóa conflict vì conflict chính là metadata quan trọng khi synthesis.

## Staleness và cập nhật

Sau khi bất kỳ `SAL-xxxx.md` nào thay đổi:

1. tính lại `note_sha256`;
2. row tương ứng được coi là stale cho đến khi evidence summary được review lại;
3. cập nhật `matrix_generated_at` và `matrix_status` thích hợp;
4. chạy `evidence_matrix.py`;
5. ghi `EVIDENCE_MATRIX.csv` lên Drive bằng **update-in-place**, giữ Drive file ID;
6. post-write inventory để bảo đảm chỉ có một `EVIDENCE_MATRIX.csv` canonical.

Batch mới phải cập nhật matrix sau registry + note + verification, không tạo `EVIDENCE_MATRIX_v2.csv`, `final.csv` hay duplicate filename.

## QC trước khi dùng để synthesis

Ít nhất phải kiểm tra:

1. active registry IDs = matrix IDs;
2. identity/DOI/PDF hash/filenames khớp registry;
3. verification fields khớp verification log;
4. checked row chỉ dựa trên checked note;
5. `note_sha256` khớp file MD hiện hành;
6. sample/isolate/genome denominators không bị trộn;
7. selected genomic set không bị biến thành prevalence;
8. source discrepancy vẫn còn trong row;
9. review/meta-analysis được phân biệt với primary study;
10. experimental transfer parameter không bị diễn giải như natural infection risk.

`evidence_matrix.py` chỉ kiểm tra schema/provenance/consistency. Nó không thay thế source-level scientific review.
