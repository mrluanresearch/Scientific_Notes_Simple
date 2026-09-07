# Source-level verification và trạng thái note

Tài liệu này định nghĩa chính xác ý nghĩa của `draft` và `checked` trong `Scientific_Notes_Simple`, đồng thời quy định cách ghi audit trail vào `results/SOURCE_VERIFICATION.csv`.

## 1. Ý nghĩa trạng thái

### `draft`

`draft` nghĩa là note **chưa hoàn tất source-level verification trong `read_scope` đã khai báo**. Một note có thể đã dài, đúng cấu trúc và đã đọc full text nhưng vẫn là `draft` nếu các metadata, Methods, Results, denominator, bảng/hình trọng yếu hoặc phép tính trung tâm chưa được cross-check có hệ thống.

### `checked`

`checked` nghĩa là MRLUAN/người soát đã đối chiếu note với nguồn trong phạm vi `read_scope` và xác nhận rằng note phản ánh trung thành những gì nguồn báo cáo, bao gồm các bất nhất, giới hạn và dữ liệu thiếu quan trọng.

`checked` **không có nghĩa**:

- bài báo/source không có lỗi;
- các bất nhất nội tại đã được giải quyết;
- raw data, supplementary files hoặc accession ngoài main source đã được thu thập đầy đủ;
- toàn bộ phân tích thống kê/WGS/PCR đã được tái chạy;
- kết luận của tác giả đã được xác nhận độc lập;
- mọi con số trong nguồn đều đáng tin để dùng không cảnh báo.

Một source có lỗi denominator, mâu thuẫn Abstract–Table, thiếu supplement hoặc limitation nặng vẫn có thể có note `checked` nếu note đã **ghi đúng, ghi đủ và cảnh báo rõ** các vấn đề đó.

## 2. Checklist bắt buộc trước khi nâng `draft` → `checked`

Trong giới hạn source thực sự có, phải kiểm tra tối thiểu:

1. **Identity/metadata:** ID, exact title, authors, year/date, journal/container, DOI/URL; đồng nhất giữa filename, YAML, citation block và registry.
2. **Read scope:** main PDF/HTML/supplement nào đã đọc và phần nào chưa có phải được ghi rõ.
3. **Thiết kế và luồng mẫu:** population, sampling frame, sample size theo tầng, unit of sampling/unit of analysis, exclusions/missingness.
4. **Methods trọng yếu:** culture/AST/PCR/WGS/statistics hoặc phương pháp tương ứng; protocol/tool/version/threshold/control khi nguồn báo cáo.
5. **Kết quả trung tâm:** numerator/denominator, effect estimate, CI/p-value, subgroup, negative result và các bảng/hình quyết định kết luận.
6. **Kiểm tra số học:** tái tính các tỷ lệ/tổng/OR đơn giản có thể tái tính trực tiếp từ dữ liệu nguồn.
7. **Cross-check nội tại:** Abstract ↔ Methods ↔ Results ↔ Table ↔ Figure; mọi giá trị không khớp phải được giữ nguyên theo từng vị trí và gắn cảnh báo.
8. **Ranh giới diễn giải:** association ≠ causation; genetic relatedness ≠ direct transmission; gene presence ≠ expression/phenotype; selected sample ≠ population prevalence.
9. **Reproducibility gaps:** raw data, supplement, accession, software/database version hoặc parameter còn thiếu phải được liệt kê khi có ảnh hưởng.
10. **Usability decision:** note phải nói rõ kết quả nào dùng trực tiếp, dùng kèm cảnh báo hoặc chưa dùng.

Không được nâng `checked` chỉ vì script structural QC trả về 0 lỗi hoặc vì file đã tồn tại trên Drive.

## 3. Audit trail — `SOURCE_VERIFICATION.csv`

Drive canonical giữ một singleton `results/SOURCE_VERIFICATION.csv`. Một row tương ứng một SAL ID đã qua source-level verification.

Schema hiện hành:

- `id`
- `reviewer`
- `verified_at`
- `read_scope`
- `note_status_decision`
- `verification_result`
- `source_discrepancy_severity`
- `checks_completed`
- `unresolved_source_issues`
- `pdf_filename`
- `md_filename`

`verification_result` mô tả kết quả kiểm tra note, không phải chấm điểm chất lượng bài báo. Ví dụ: `pass`, `pass_with_source_discrepancies`, `pass_with_model_assumptions`, `pass_with_method_limitations`.

`source_discrepancy_severity` có thể dùng `none`, `low`, `moderate`, `high`; đây là mức độ vấn đề của **source hoặc khả năng dùng lại**, không làm thay đổi định nghĩa của `checked` nếu note đã ghi nhận đúng.

## 4. Đồng bộ sau verification

Khi một note được nâng `checked`, phải update-in-place theo `DRIVE_WRITE_RULES.md` và đồng bộ ít nhất:

1. YAML `status: checked` trong `SAL-xxxx.md`.
2. Dòng `Source-level verification` trong mục 1 của note, gồm ngày, reviewer và phạm vi.
3. `SOURCE_REGISTRY.csv`: `note_status=checked`, cập nhật `updated_at`.
4. `SOURCE_VERIFICATION.csv`: tạo/cập nhật row audit cho SAL ID.
5. `INDEX.md`: status hiển thị `checked`.
6. Post-write inventory: xác nhận không tạo duplicate Drive files và tất cả mapping vẫn khớp.

Nếu một verification sau này phát hiện note sai hoặc thiếu trọng yếu, hạ note về `draft`, ghi rõ lý do và cập nhật registry/log; không che lịch sử bất nhất bằng cách âm thầm sửa trạng thái.

## 5. Nguyên tắc bảo toàn bằng chứng

Không sửa số nguồn để làm chúng nhất quán. Khi source mâu thuẫn, note phải giữ:

- giá trị author-reported ở từng vị trí;
- phép tính MRLUAN khi có thể;
- assessment về mức ảnh hưởng;
- quyết định dùng lại có điều kiện.

Mục tiêu của `checked` là **độ trung thực và khả năng truy vết của note**, không phải cấp chứng nhận chất lượng cho source.