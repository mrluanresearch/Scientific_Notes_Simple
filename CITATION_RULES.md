# Quy tắc đặt tên note và metadata trích dẫn

Tài liệu này định nghĩa cách đặt tên file và cách lưu metadata thư mục để sau này có thể sinh trích dẫn APA 7, Vancouver, Harvard, Chicago, IEEE và các style khác mà không phải đọc lại PDF để dò thông tin bibliographic.

## 1. Nguyên tắc nền

**Không lưu chuỗi trích dẫn APA/Vancouver đã định dạng làm dữ liệu canonical.** Chuỗi đã định dạng phụ thuộc style và có thể thay đổi khi đổi style. Dự án lưu **raw bibliographic metadata** theo cấu trúc gần CSL-JSON; từ một metadata canonical có thể render nhiều style bằng Zotero, Pandoc/citeproc hoặc công cụ CSL khác.

`SAL-xxxx` là định danh nội bộ ổn định của evidence source và đồng thời là citation key. Tác giả, năm hoặc tiêu đề có thể được sửa sau khi kiểm tra metadata nhưng ID không đổi.

## 2. Quy tắc đặt tên file

### 2.1. Note Markdown

- Canonical: `SAL-0001.md`, `SAL-0002.md`, ...
- Chỉ dùng ID trong filename. **Không** dùng `Author_Year_Title.md`, không thêm `final`, `final2`, `checked`, ngày tháng hoặc version vào filename.
- H1 (`# ...`) phải là **tiêu đề tài liệu gốc chính xác**, không phải tiêu đề phân tích do MRLUAN tự đặt.
- Citation key dùng trong bản thảo/Pandoc/Zotero bridge: `SAL-0001`. Ví dụ citation markup: `[@SAL-0001]`.
- Khi metadata được sửa, filename và citation key không đổi.

### 2.2. PDF và tài sản liên quan

- PDF nguồn chính/version of record: `SAL-0001.pdf`.
- Supplement: `SAL-0001-supp-01.pdf`, `SAL-0001-supp-02.xlsx`, ...
- Dataset tải kèm: `SAL-0001-data-01.csv`, `SAL-0001-data-02.xlsx`, ...
- Protocol/code snapshot nếu cần giữ cùng evidence source: `SAL-0001-protocol-01.pdf`, `SAL-0001-code-01.zip`.
- Không đổi tên ID chỉ vì đổi journal title, corrected title hoặc DOI metadata.

### 2.3. Preprint, version of record, correction và retraction

- Nếu preprint và version of record về bản chất là cùng nghiên cứu, ưu tiên version of record làm source canonical; ghi quan hệ tới preprint ở mục 1. Không cần hai ID nếu không cần phân tích khác biệt phiên bản.
- Nếu hai phiên bản có thay đổi dữ liệu/kết luận đáng kể và cần đánh giá riêng, cấp hai SAL ID và ghi quan hệ `is-version-of`/`has-version`.
- Correction/erratum có nội dung khoa học cần theo dõi: cấp SAL ID riêng và liên kết `corrects`/`is-corrected-by`.
- Retraction notice: không xóa note gốc. Ghi trạng thái publication và liên kết retraction; bằng chứng bị rút không được sử dụng như bằng chứng hợp lệ mà không có cảnh báo.

## 3. Metadata citation canonical

Mỗi note phải có một block YAML `citation:` ở mục 1, được đánh dấu bằng `CITATION_METADATA_START/END`. Các tên trường ưu tiên tương thích CSL.

### 3.1. Trường lõi

| Trường | Quy tắc |
| --- | --- |
| `id` | Bắt buộc; đúng `SAL-xxxx`; khớp filename và YAML `id` |
| `type` | Bắt buộc; kiểu CSL như `article-journal`, `book`, `chapter`, `report`, `thesis`, `paper-conference`, `dataset`, `software`, `webpage` |
| `author` | Bắt buộc khi nguồn có tác giả; giữ đúng thứ tự xuất bản; mỗi người tách `family` và `given`; cơ quan dùng `literal` |
| `issued` | Bắt buộc khi biết ngày; CSL `date-parts`, ví dụ `[[2025, 9, 10]]`; ít nhất giữ năm |
| `title` | Bắt buộc; tiêu đề gốc chính xác, không tự sentence-case hoặc title-case lại |
| `container-title` | Journal/book/proceedings/site chứa tài liệu; bắt buộc cho journal article nếu nguồn có |
| `volume` | Volume gốc; giữ dạng chuỗi |
| `issue` | Issue/số; giữ dạng chuỗi |
| `page` | Trang hoặc article number dùng như locator xuất bản, ví dụ `38-47` hoặc `1278821` |
| `DOI` | DOI chuẩn, không thêm `https://doi.org/`; khớp YAML `doi` |
| `URL` | URL canonical nếu có; ưu tiên trang publisher/repository, không dùng URL tìm kiếm |
| `publisher` | Nhà xuất bản/cơ quan; đặc biệt quan trọng với book/report/guideline/dataset |
| `publisher-place` | Chỉ ghi khi nguồn cung cấp và loại tài liệu/style có thể cần; không tự suy từ địa chỉ tác giả |
| `edition` | Edition của book/manual/guideline nếu có |
| `editor` | Danh sách editor theo cấu trúc tên như `author` khi nguồn là chapter/book |
| `ISBN` / `ISSN` | Ghi khi có; hữu ích cho disambiguation, không thay DOI |
| `language` | Mã ngôn ngữ như `en`, `vi`; hữu ích cho xử lý title và style |
| `accessed` | Ngày truy cập cho webpage/dynamic content khi cần; không bắt buộc cho journal article có DOI |

### 3.2. Tên tác giả

Tên phải được lưu ở dạng có cấu trúc để citation engine quyết định viết `Nguyen, V. A.`, `Nguyen VA`, `V. A. Nguyen` hay `Nguyen et al.` theo style.

```yaml
author:
  - family: Abdallah
    given: Enas F.
  - family: Sorour
    given: Hend K.
```

Tác giả tổ chức/corporate author dùng `literal`, không tách thành given/family:

```yaml
author:
  - literal: World Health Organization
```

Giữ đúng thứ tự tác giả của version of record. Không tự rút xuống `et al.` trong metadata.

### 3.3. Ngày xuất bản

Dùng CSL `date-parts`:

```yaml
issued:
  date-parts:
    - [2025, 9, 10]
```

Nếu chỉ biết năm:

```yaml
issued:
  date-parts:
    - [2025]
```

YAML `year` ở đầu note là field tìm kiếm nhanh và phải khớp năm trong `issued`.

## 4. Trường theo loại tài liệu

### Journal article

Tối thiểu cố gắng có: `author`, `issued`, `title`, `container-title`, `volume`, `issue`, `page`, `DOI`. Nếu journal dùng article number thay pages, ghi article number trong `page` để citeproc có locator xuất bản. Ghi ISSN nếu có nhưng không cần mở thêm nguồn chỉ để lấy ISSN khi DOI đã đủ định danh.

### Book

`author` hoặc `editor`, `issued`, `title`, `edition`, `publisher`, `publisher-place` nếu có, `ISBN`, `DOI/URL`.

### Chapter in edited book

`author`, `issued`, `title`, `container-title` = tên sách, `editor`, `page`, `publisher`, `edition`, `DOI/URL`.

### Report / guideline / standard

Tác giả cá nhân hoặc corporate author (`literal`), `issued`, `title`, `publisher`/issuing institution, report/standard number nếu có, edition/version, DOI/URL. Với nội dung web có thể thay đổi, thêm `accessed`.

### Thesis/dissertation

`author`, `issued`, `title`, `type: thesis`, loại bằng/genre ghi ở phần human-readable của note, `publisher` = institution, repository URL/DOI.

### Conference paper

`author`, `issued`, `title`, `container-title` = proceedings nếu có, event title ghi trong note, `page`, `publisher`, DOI/URL.

### Dataset / software

`author`/creator, `issued`, `title`, `version`, `publisher`/repository, DOI/URL. Với dữ liệu genomic, accession vẫn phải ghi riêng ở Methods/Data availability vì accession không thay thế citation metadata.

### Webpage

`author` hoặc corporate author, ngày published/updated nếu có, `title`, `container-title` = site, `URL`, `accessed`. Không dùng ngày truy cập làm năm xuất bản.

## 5. Xác minh metadata

Ưu tiên theo thứ tự:

1. Version of record trên PDF/publisher.
2. DOI landing page/Crossref metadata hoặc PubMed khi phù hợp.
3. Journal issue/table of contents.
4. Database/repository chính thức.

Không lấy tác giả/năm/title từ tên file do người dùng đặt nếu PDF hoặc publisher cho thông tin khác.

Khi PDF có metadata mâu thuẫn với publisher, giữ bản version of record làm canonical và ghi bất nhất trong mục 1. Ví dụ volume/page ở header PDF khác citation block của journal phải được nêu, không âm thầm chọn.

## 6. Quy tắc DOI và URL

- YAML `doi` và `citation.DOI` lưu dạng `10.xxxx/xxxxx`, không có `doi:` và không có URL prefix.
- DOI so sánh case-insensitive để phát hiện trùng, nhưng khi ghi có thể giữ capitalization do publisher cung cấp nếu cần.
- URL không thay DOI. Nếu có DOI, DOI là định danh ưu tiên cho citation.
- Không lưu Google Scholar, search result hoặc URL tạm thời làm URL canonical.

## 7. Sinh citation đa style

`notes.py csl` sẽ gom metadata citation từ các note thành một file CSL-JSON. Khi đó cùng một source có thể render bằng style khác nhau mà không sửa note:

- APA 7: author–date, journal/title/punctuation theo APA.
- Vancouver: đánh số theo thứ tự citation.
- Chicago/Harvard: author–date hoặc notes-bibliography tùy CSL style.
- IEEE: numeric style.

Dữ liệu canonical là metadata, **không phải câu citation đã format**. Khi cần thay style, đổi CSL style chứ không sửa từng note.

## 8. Kiểm tra trước khi coi citation metadata hoàn chỉnh

- ID khớp filename/YAML.
- H1 và `citation.title` khớp tiêu đề nguồn.
- Authors đủ, đúng thứ tự, không `et al.`.
- Năm `issued` khớp YAML `year`.
- Journal/container title không viết tắt tùy tiện nếu nguồn đưa tên đầy đủ; abbreviation chỉ do style xử lý nếu có dữ liệu riêng.
- Volume/issue/page hoặc article number đúng.
- DOI khớp YAML và resolve về đúng source khi có thể kiểm tra.
- Không dùng access date thay publication date.
- Correction/retraction/version relationship được ghi rõ nếu liên quan.
