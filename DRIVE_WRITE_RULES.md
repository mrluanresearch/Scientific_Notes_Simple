# Quy tắc ghi Google Drive và chống file trùng canonical

Tài liệu này quy định cách ghi dữ liệu của `Scientific_Notes_Simple` lên Google Drive. Mục tiêu là làm cho thao tác ghi **idempotent**: chạy lại cùng một bước không được tạo thêm một file `SAL-xxxx.pdf` hoặc `SAL-xxxx.md` có cùng tên.

## 1. Nguyên tắc bất biến

Trong các thư mục canonical:

- `results/PDF/` có tối đa **một** main PDF cho mỗi active SAL ID: `SAL-xxxx.pdf`.
- `results/MD/` có tối đa **một** main note cho mỗi active SAL ID: `SAL-xxxx.md`.
- Không được tồn tại hai Drive file khác ID nhưng cùng canonical filename trong cùng thư mục.
- `INDEX.md` và `references.csl.json` cũng là singleton; mỗi tên chỉ có một file hiện hành.
- `SOURCE_REGISTRY.csv` là singleton tại `results/` và là source of truth cho identity/file mapping.

Tên giống nhau trên Google Drive **không** có nghĩa là cùng một file. Vì Drive cho phép nhiều file cùng tên, duplicate phải được ngăn bằng workflow, không dựa vào filename uniqueness của nền tảng.

## 2. Read-before-write bắt buộc

Trước mọi lần ghi PDF, MD, INDEX, CSL hoặc registry lên Drive:

1. Liệt kê trực tiếp thư mục đích.
2. Tìm exact canonical filename cần ghi.
3. Phân nhánh theo số file hiện có:
   - **0 file:** upload mới đúng một lần.
   - **1 file:** nếu đây là revision của cùng artifact, **update bytes in place** và giữ nguyên Drive file ID; không upload thêm file cùng tên.
   - **>1 file:** dừng ghi mới. Xử lý duplicate trước, xác định revision canonical, loại bỏ bản obsolete, rồi mới tiếp tục.

Không dùng thao tác `upload` để thay thế một canonical file đã tồn tại. Khi thay nội dung cùng artifact phải dùng cơ chế update/replace-in-place của Drive.

## 3. Quy tắc revision

Một revision của `SAL-xxxx.md` không tạo `SAL-xxxx (1).md`, `SAL-xxxx-v2.md`, `SAL-xxxx-final.md` hoặc một file Drive mới vẫn mang tên `SAL-xxxx.md`.

Revision phải:

- giữ nguyên canonical filename;
- giữ nguyên SAL ID;
- giữ nguyên Drive file ID nếu file canonical đã tồn tại;
- thay bytes của file hiện hành;
- sau đó read-back để xác nhận size/content/metadata mong đợi.

Tương tự với PDF source: chỉ thay main PDF khi đã xác định rõ đây là version canonical của cùng source. Preprint/correction/version khác có ý nghĩa khoa học phải xử lý theo `REGISTRY_RULES.md`, không âm thầm thay PDF.

## 4. Xử lý duplicate đã lỡ tạo

Nếu phát hiện nhiều file cùng canonical filename:

1. Không tạo thêm file mới.
2. So sánh Drive file ID, thời điểm tạo/sửa, kích thước và nội dung/revision khi cần.
3. Xác định bản intended canonical dựa trên workflow và nội dung, không chỉ dựa vào tên.
4. Giữ một bản canonical duy nhất.
5. Xóa các bản upload obsolete chỉ khi chắc chắn chúng là bản trung gian do cùng workflow tạo ra; nếu có bất kỳ mơ hồ khoa học hoặc khác biệt nội dung chưa đánh giá, giữ lại để review thay vì xóa tự động.
6. Kiểm kê lại thư mục ngay sau cleanup.

## 5. Post-write inventory bắt buộc

Sau mỗi batch, phải read-back trực tiếp từ Drive và kiểm tra:

- số active record trong `SOURCE_REGISTRY.csv` = số main PDF canonical;
- mỗi registry `pdf_filename` xuất hiện đúng một lần trong `results/PDF/`;
- mỗi registry `md_filename` có `note_status != none` xuất hiện đúng một lần trong `results/MD/`;
- không có duplicate canonical filenames;
- `INDEX.md` xuất hiện đúng một lần;
- `references.csl.json` xuất hiện đúng một lần khi đã sinh CSL;
- SHA-256 trong registry khớp file PDF intake/canonical khi có thể tính lại;
- ID/title/year/DOI giữa registry, note YAML/H1/citation metadata vẫn đồng nhất.

Một batch chưa qua inventory này không được mô tả là hoàn tất canonical.

## 6. Trạng thái note và registry

`note_status` chỉ được cập nhật sau khi note canonical đã ghi thành công và read-back đúng ID/tên. Không nâng `checked` chỉ vì file tồn tại hoặc QC cấu trúc bằng 0 lỗi.

Nếu có lỗi write/read-back, duplicate Drive file hoặc mismatch registry ↔ PDF ↔ MD, giữ `draft`/trạng thái cần review cho tới khi xử lý xong.

## 7. Tính idempotent của workflow

Mọi workflow intake/update phải thỏa điều kiện:

> Chạy lại cùng input và cùng SAL ID không làm tăng số lượng canonical files.

Đây là invariant bắt buộc của project và cần được kiểm tra trong các lần triển khai tiếp theo.
