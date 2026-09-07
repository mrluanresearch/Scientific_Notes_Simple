# SOURCE_REGISTRY.csv — quy tắc định danh và chống trùng

Tài liệu này định nghĩa cách dùng `results/SOURCE_REGISTRY.csv` trên Google Drive để cấp ID, chống trùng và ánh xạ giữa PDF nguồn với note Markdown. CSV là **sổ đăng ký intake/identity**, không thay thế scientific note và không thay thế citation metadata chi tiết trong từng MD.

## 1. Vị trí và vai trò canonical

- File canonical: `results/SOURCE_REGISTRY.csv` trên Google Drive.
- Chỉ có **một** registry đang hoạt động cho project; không tạo `registry_final.csv`, `registry_copy.csv` hoặc nhiều bản song song.
- `SOURCE_REGISTRY.csv` dùng để: cấp/giữ `SAL-xxxx`, phát hiện tài liệu trùng trước khi upload, lưu tên file gốc, map PDF ↔ MD, giữ khóa DOI/title/author/hash và quan hệ version.
- Scientific content vẫn nằm trong `results/MD/SAL-xxxx.md`.
- Full bibliographic metadata vẫn nằm trong block `citation:` của note theo `CITATION_RULES.md`.
- `INDEX.md` là file dẫn xuất từ note; không dùng `INDEX.md` thay cho registry intake.

## 2. Quy tắc cấp ID

- ID có dạng `SAL-0001`, `SAL-0002`, ...; tối thiểu 4 chữ số. Sau `SAL-9999` có thể mở rộng tự nhiên thành `SAL-10000`; không renumber nguồn cũ.
- **Chỉ cấp ID mới sau khi kiểm tra trùng registry.**
- Một ID đã cấp không được tái sử dụng cho tài liệu khác, kể cả khi file bị loại, retracted, superseded hoặc duplicate.
- Nếu phát hiện một row được cấp nhầm cho duplicate sau đó, giữ row và ghi `registry_status=duplicate`, `duplicate_of=SAL-xxxx`; không xóa dấu vết nếu đã có asset/note liên quan.

## 3. Quy tắc tên file canonical

### 3.1. Main source và note

- Main PDF/version of record: `SAL-0001.pdf`.
- Scientific note: `SAL-0001.md`.
- Một source canonical có tối đa **một main PDF** và **một main MD** cùng ID.
- Filename không chứa author, year, journal, DOI, title, ngày xử lý, `final`, `checked`, `(1)` hoặc số copy tự sinh.
- Tên file người dùng tải lên được giữ nguyên trong cột `original_filename` của registry để truy vết, nhưng không dùng làm canonical filename.

### 3.2. Asset phụ được phép

- Supplement: `SAL-0001-supp-01.pdf`, `SAL-0001-supp-02.xlsx`, ...
- Dataset: `SAL-0001-data-01.csv`, `SAL-0001-data-02.xlsx`, ...
- Protocol: `SAL-0001-protocol-01.pdf` hoặc extension phù hợp.
- Code/archive snapshot: `SAL-0001-code-01.zip`.
- Các hậu tố đánh số từ `01`, tăng tuần tự trong cùng loại asset.
- Không dùng hậu tố mơ hồ như `extra`, `new`, `old`, `final`, `v2` nếu quan hệ version có thể mô tả chính xác hơn.

### 3.3. Version, preprint, correction, retraction

- Version of record được ưu tiên làm `SAL-xxxx.pdf`.
- Preprint và version of record không tự động coi là duplicate chỉ vì title gần giống; kiểm tra DOI, authors, nội dung và publication relation.
- Nếu preprint chỉ cần lưu như supporting version của cùng source và không cần appraisal riêng, ghi quan hệ trong registry/note; không cấp ID mới chỉ để lưu bản copy.
- Nếu hai version có thay đổi khoa học cần đánh giá riêng, cấp hai SAL ID và dùng `relation_type` + `related_id`.
- Correction/erratum/retraction notice có nội dung khoa học cần theo dõi có thể có SAL ID riêng theo `CITATION_RULES.md`.

## 4. Schema cố định của SOURCE_REGISTRY.csv

Thứ tự cột canonical:

```text
id,title,title_key,year,first_author,first_author_key,doi,doi_key,pmid,pmcid,journal,publication_type,publication_status,relation_type,related_id,original_filename,pdf_filename,md_filename,pdf_sha256,canonical_url,registry_status,note_status,registered_at,updated_at,duplicate_of,duplicate_reason,notes
```

### 4.1. Field chính

| Field | Ý nghĩa |
| --- | --- |
| `id` | SAL ID ổn định |
| `title` | Exact source title đã xác minh tốt nhất tại thời điểm đăng ký |
| `title_key` | Title đã chuẩn hóa để so trùng; field máy, không dùng để cite |
| `year` | Năm xuất bản canonical nếu biết |
| `first_author` | Tác giả đầu tiên ở dạng đọc được |
| `first_author_key` | Tác giả đầu đã chuẩn hóa cho matching |
| `doi` | DOI canonical dạng `10.xxxx/...` |
| `doi_key` | DOI lower-case sau chuẩn hóa; dùng cho matching |
| `pmid`, `pmcid` | Identifier bổ sung khi có |
| `journal` | Journal/container để disambiguation |
| `publication_type` | article-journal, report, thesis, dataset, preprint... |
| `publication_status` | version-of-record, preprint, corrected, retracted, unknown... |
| `relation_type`, `related_id` | Quan hệ version/correction/retraction với SAL khác |
| `original_filename` | Tên file lúc người dùng/source cung cấp |
| `pdf_filename` | Main PDF canonical, ví dụ `SAL-0001.pdf` |
| `md_filename` | Main note canonical, ví dụ `SAL-0001.md` |
| `pdf_sha256` | SHA-256 của main PDF khi có thể tính; dùng phát hiện exact binary duplicate |
| `canonical_url` | Publisher/repository URL nếu có |
| `registry_status` | `active`, `review`, `duplicate`, `excluded`, `superseded` |
| `note_status` | `none`, `draft`, `checked` để phản ánh trạng thái MD |
| `registered_at`, `updated_at` | ISO 8601 datetime/date theo quy trình triển khai |
| `duplicate_of`, `duplicate_reason` | Ghi SAL nguồn gốc và lý do nếu record là duplicate |
| `notes` | Ghi chú intake ngắn; không chứa scientific appraisal dài |

## 5. Chuẩn hóa khóa so trùng

### DOI

- `doi`: bỏ `doi:` và `https://doi.org/`; ví dụ `10.3389/fmicb.2023.1278821`.
- `doi_key`: trim whitespace và lowercase để so sánh case-insensitive.
- DOI giống nhau sau chuẩn hóa là tín hiệu duplicate mạnh nhất ở mức bibliographic source.

### Title

`title_key` chỉ dùng matching và được tạo từ `title` theo nguyên tắc:

1. Unicode NFKC.
2. casefold/lowercase.
3. Thay punctuation/ký tự phân cách bằng khoảng trắng khi không làm mất chữ/số có ý nghĩa.
4. Collapse nhiều whitespace thành một khoảng trắng.
5. Trim đầu/cuối.

Không sửa `title` canonical theo `title_key`. Exact title vẫn giữ nguyên trong registry và note.

### First author

`first_author_key` chuẩn hóa case/whitespace/punctuation để tăng recall. Có thể bỏ dấu diacritic **chỉ trong key matching**, nhưng `first_author` canonical phải giữ đúng spelling nguồn.

### PDF hash

- `pdf_sha256` là lowercase hex SHA-256 của bytes main PDF.
- Hash giống nhau = exact binary duplicate dù original filename khác.
- Hash khác nhau không chứng minh hai tài liệu khác nhau: publisher PDF, accepted manuscript và preprint có thể khác bytes nhưng cùng nghiên cứu.

## 6. Thứ tự kiểm tra duplicate

Trước khi cấp SAL ID hoặc upload main PDF, kiểm tra theo thứ tự:

1. **DOI exact sau chuẩn hóa** → hard duplicate candidate. Không cấp ID mới trước khi xác minh.
2. **PMID/PMCID exact** → hard duplicate candidate khi identifier áp dụng cho cùng publication.
3. **PDF SHA-256 exact** → exact file duplicate. Không upload copy mới.
4. **`title_key` exact + `first_author_key` exact + cùng năm** → strong duplicate candidate; yêu cầu review nếu DOI thiếu/khác.
5. **`title_key` exact + năm bằng hoặc lệch ±1** → probable duplicate/version candidate; kiểm tra online-first vs issue year, preprint vs VoR.
6. **Title rất gần + cùng first author/journal/volume/pages** → possible duplicate; review thủ công.

Không tự động merge chỉ dựa trên fuzzy title.

## 7. Xử lý conflict và version

- **Cùng DOI nhưng title khác:** block intake và xác minh metadata/version; không cấp hai ID.
- **Cùng title nhưng DOI khác:** không tự kết luận duplicate; kiểm tra correction, preprint, version of record hoặc hai bài khác nhau có title giống nhau.
- **Cùng hash nhưng DOI/title khác:** coi là metadata conflict; dùng PDF/source để xác minh trước khi tiếp tục.
- **Preprint → version of record:** nếu giữ cùng nghiên cứu dưới một ID, version of record trở thành main canonical source; preprint relation phải được ghi lại. Nếu appraisal riêng là cần thiết, dùng ID riêng và relationship rõ.

## 8. Workflow intake bắt buộc

1. Đọc trang đầu/metadata source để lấy exact title, first author, year, DOI và identifier có sẵn.
2. Tính `pdf_sha256` khi có file PDF local.
3. Tìm trong `SOURCE_REGISTRY.csv` theo DOI/PMID/hash/title key trước.
4. Nếu duplicate chắc chắn: không cấp ID mới; báo SAL hiện có và lý do match.
5. Nếu candidate mơ hồ: đặt `registry_status=review` hoặc tạm chưa ghi row active; so sánh version trước.
6. Nếu source mới: cấp SAL ID kế tiếp, ghi row registry trước hoặc đồng thời với upload.
7. Đổi main PDF thành `SAL-xxxx.pdf`; giữ `original_filename` trong registry.
8. Tạo `SAL-xxxx.md` cùng ID; H1 là exact source title.
9. Sau khi note tạo/soát, cập nhật `note_status` và `updated_at`.

## 9. Quan hệ giữa registry, note và INDEX

- Registry quyết định identity intake/file mapping và chống trùng.
- MD quyết định nội dung khoa học + full citation metadata.
- `INDEX.md` được sinh từ MD để browse, không phải nơi cấp ID.
- Nếu registry và note khác title/year/DOI, phải xem là **identity conflict** và sửa sau khi đối chiếu nguồn; không âm thầm ưu tiên một bên.

## 10. Quy tắc chỉnh sửa CSV

- Giữ encoding UTF-8; khi tạo mới ưu tiên UTF-8 with BOM để Excel đọc tiếng Việt ổn định.
- Không đổi header hoặc thứ tự cột nếu chưa cập nhật mã nguồn/quy tắc tương ứng.
- Không xóa row active chỉ để làm registry đẹp; dùng status/duplicate relation để bảo toàn audit trail.
- Không sort rồi gán lại ID. SAL ID là immutable identity.
- Drive version history là lịch sử file; không tạo nhiều bản CSV song song để backup thủ công.

## 11. Kết luận vận hành

CSV registry là lớp chống trùng trước khi scientific note tồn tại. Nó bổ sung cho kiểm tra DOI/title hiện có trong `notes.py`, đặc biệt bắt được: PDF trùng nhưng chưa có MD, file người dùng đổi tên, DOI thiếu, online-first vs issue metadata, và các version gần giống nhau cần review.
