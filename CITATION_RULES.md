# Metadata trích dẫn và publication identity

Tài liệu này định nghĩa cách lưu bibliographic metadata để sau này có thể sinh APA 7, Vancouver, Harvard, Chicago, IEEE và các style khác mà không phải đọc lại PDF để dò thông tin citation.

**Quy tắc cấp SAL ID, chống trùng và đặt tên file PDF/MD/asset nằm ở `REGISTRY_RULES.md`.** `SOURCE_REGISTRY.csv` quyết định identity intake/file mapping; citation block trong từng note quyết định full bibliographic metadata.

## 1. Nguyên tắc nền

**Không lưu chuỗi trích dẫn APA/Vancouver đã định dạng làm dữ liệu canonical.** Chuỗi đã định dạng phụ thuộc style và có thể thay đổi khi đổi style. Dự án lưu **raw bibliographic metadata** theo cấu trúc gần CSL-JSON; từ một metadata canonical có thể render nhiều style bằng Zotero, Pandoc/citeproc hoặc công cụ CSL khác.

`SAL-xxxx` là định danh nội bộ ổn định của evidence source và đồng thời là citation key. ID được cấp theo `SOURCE_REGISTRY.csv` trước khi tạo note. Tác giả, năm hoặc tiêu đề có thể được sửa sau khi kiểm tra metadata nhưng ID không đổi.

Một source active phải đồng nhất ở bốn nơi:

1. `SOURCE_REGISTRY.csv` — `id`, title/year/DOI và file mapping.
2. YAML đầu note — `id`, `year`, `doi`.
3. H1 + block `citation:` trong note.
4. Filename `SAL-xxxx.md` và main PDF `SAL-xxxx.pdf`.

Nếu title/year/DOI khác nhau giữa registry và note, coi đó là **identity conflict** cần đối chiếu source; không âm thầm chọn một bên.

## 2. Metadata citation canonical

Mỗi note phải có một block YAML `citation:` ở mục 1, được đánh dấu bằng `CITATION_METADATA_START/END`. Các tên trường ưu tiên tương thích CSL.

### 2.1. Trường lõi

| Trường | Quy tắc |
| --- | --- |
| `id` | Bắt buộc; đúng `SAL-xxxx`; khớp registry, filename và YAML `id` |
| `type` | Bắt buộc; kiểu CSL như `article-journal`, `book`, `chapter`, `report`, `thesis`, `paper-conference`, `dataset`, `software`, `webpage` |
| `author` | Bắt buộc khi nguồn có tác giả; giữ đúng thứ tự xuất bản; mỗi người tách `family` và `given`; cơ quan dùng `literal` |
| `issued` | Bắt buộc khi biết ngày; CSL `date-parts`, ví dụ `[[2025, 9, 10]]`; ít nhất giữ năm |
| `title` | Bắt buộc; tiêu đề gốc chính xác, không tự sentence-case hoặc title-case lại |
| `container-title` | Journal/book/report/proceedings/site chứa tài liệu; bắt buộc cho journal article nếu nguồn có |
| `volume` | Volume gốc; giữ dạng chuỗi |
| `issue` | Issue/số; giữ dạng chuỗi |
| `page` | Trang hoặc article number dùng như locator xuất bản, ví dụ `38-47` hoặc `1278821` |
| `DOI` | DOI chuẩn, không thêm `https://doi.org/`; khớp YAML `doi` và registry `doi` |
| `URL` | URL canonical nếu có; ưu tiên trang publisher/repository, không dùng URL tìm kiếm |
| `publisher` | Nhà xuất bản/cơ quan; đặc biệt quan trọng với book/report/guideline/dataset |
| `publisher-place` | Chỉ ghi khi nguồn cung cấp và loại tài liệu/style có thể cần; không tự suy từ địa chỉ tác giả |
| `edition` | Edition của book/manual/guideline nếu có |
| `editor` | Danh sách editor theo cấu trúc tên như `author` khi nguồn là chapter/book |
| `ISBN` / `ISSN` | Ghi khi có; hữu ích cho disambiguation, không thay DOI |
| `language` | Mã ngôn ngữ như `en`, `vi`; hữu ích cho xử lý title và style |
| `accessed` | Ngày truy cập cho webpage/dynamic content khi cần; không bắt buộc cho journal article có DOI |

### 2.2. Tên tác giả

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

### 2.3. Ngày xuất bản

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

YAML `year` ở đầu note là field tìm kiếm nhanh và phải khớp năm trong `issued` và registry `year`.

## 3. Trường theo loại tài liệu

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

## 4. Xác minh metadata

Ưu tiên theo thứ tự:

1. Version of record trên PDF/publisher.
2. DOI landing page/Crossref metadata hoặc PubMed khi phù hợp.
3. Journal issue/table of contents.
4. Database/repository chính thức.

Không lấy tác giả/năm/title từ tên file do người dùng đặt nếu PDF hoặc publisher cho thông tin khác. Tên file gốc chỉ được giữ trong registry `original_filename` để provenance.

Khi PDF có metadata mâu thuẫn với publisher, giữ bản version of record làm canonical và ghi bất nhất trong mục 1. Ví dụ volume/page ở header PDF khác citation block của journal phải được nêu, không âm thầm chọn.

Sau khi xác minh metadata, phải đối chiếu registry: title/year/DOI canonical cần đồng nhất. Nếu registry được tạo từ metadata intake sơ bộ và sau đó phát hiện sai, cập nhật registry + note cùng lúc, nhưng **không đổi SAL ID**.

## 5. Quy tắc DOI và URL

- YAML `doi`, registry `doi` và `citation.DOI` lưu dạng `10.xxxx/xxxxx`, không có `doi:` và không có URL prefix.
- DOI so sánh case-insensitive để phát hiện trùng; registry giữ `doi_key` lower-case cho matching.
- URL không thay DOI. Nếu có DOI, DOI là định danh ưu tiên cho citation và duplicate control.
- Không lưu Google Scholar, search result hoặc URL tạm thời làm URL canonical.

## 6. Publication version, correction và retraction

Quy tắc lưu file/ID nằm ở `REGISTRY_RULES.md`; metadata citation phải phản ánh đúng publication đang được note đánh giá.

- Preprint và version of record có thể có DOI khác nhau; không tự merge chỉ vì title gần giống.
- Nếu cùng một nghiên cứu được giữ dưới một ID với version of record là canonical, citation block phải mô tả version of record; preprint relation ghi ở mục 1/registry.
- Nếu hai version cần appraisal riêng vì thay đổi dữ liệu/kết luận, dùng hai SAL ID và relationship rõ.
- Correction/erratum/retraction notice có ID riêng khi cần đánh giá độc lập; note gốc không bị xóa để giữ provenance.
- Bằng chứng retracted không được dùng như evidence bình thường mà không có cảnh báo.

## 7. Sinh citation đa style

`notes.py csl` gom metadata citation từ các note thành một file CSL-JSON. Khi đó cùng một source có thể render bằng style khác nhau mà không sửa note:

- APA 7: author–date, journal/title/punctuation theo APA.
- Vancouver: đánh số theo thứ tự citation.
- Chicago/Harvard: author–date hoặc notes-bibliography tùy CSL style.
- IEEE: numeric style.

Dữ liệu canonical là metadata, **không phải câu citation đã format**. Khi cần thay style, đổi CSL style chứ không sửa từng note.

## 8. Kiểm tra trước khi coi citation metadata hoàn chỉnh

- ID khớp registry, filename và YAML.
- H1, registry `title` và `citation.title` khớp tiêu đề nguồn.
- Authors đủ, đúng thứ tự, không `et al.`.
- Năm `issued` khớp YAML `year` và registry `year`.
- Journal/container title không viết tắt tùy tiện nếu nguồn đưa tên đầy đủ; abbreviation chỉ do style xử lý nếu có dữ liệu riêng.
- Volume/issue/page hoặc article number đúng.
- DOI khớp YAML + registry và resolve về đúng source khi có thể kiểm tra.
- Không dùng access date thay publication date.
- Correction/retraction/version relationship được ghi rõ nếu liên quan.
- Nếu registry và note còn identity conflict, chưa coi metadata hoàn chỉnh và chưa nâng `checked`.
