# Scientific Notes Simple

Một mẫu note cho 1.000 tài liệu. Sáu trường YAML; nội dung khoa học viết trực tiếp bằng Markdown. Mục tiêu không phải tạo bản tóm tắt ngắn, mà tạo **source note tự đứng được** để hiểu, đánh giá, trích dẫn và tái tính bằng chứng mà không phải mở lại PDF cho những chi tiết tác giả đã báo cáo.

## Thiết kế

Đây là gói viết lại từ đầu, không nâng cấp kiến trúc 9.1. Bỏ schema JSON, Evidence/Claim ID, hash/revision engine, điểm QC/relevance, cổng approve và YAML kết quả lồng nhiều tầng. Metadata citation được giữ trong một block CSL-ready ở thân note, không làm phình YAML quản lý.

| Thành phần | Vai trò |
| --- | --- |
| `AGENTS.md` | Quy tắc MRLUAN đọc nguồn, bảo toàn dữ liệu, phản biện và QC |
| `NOTE_TEMPLATE.md` | Mẫu duy nhất: sáu trường YAML, tám mục cấp `##`, các tiểu mục chi tiết bắt buộc |
| `CITATION_RULES.md` | Metadata citation và quy tắc publication/version |
| `REGISTRY_RULES.md` | Quy tắc cấp SAL ID, đặt tên PDF/MD và chống trùng qua `SOURCE_REGISTRY.csv` |
| `registry.py` | Khởi tạo/check/find/register source trong CSV registry; chuẩn hóa DOI/title/author và tính PDF SHA-256 |
| `examples/SAL-0001.md` | Note đã điền trên bài Neuert và cộng sự (2018), kèm nguồn và giới hạn đọc |
| `notes.py` | Tạo khung, kiểm tra cấu trúc/độ sâu/citation, lập mục lục, xuất CSL-JSON |
| `requirements.txt` | Một dependency: PyYAML |
| `PROJECT.yaml` | Ánh xạ canonical giữa GitHub, Google Drive và vai trò MRLUAN |

`notes.py` không tự viết phân tích, không gọi LLM và không đọc PDF tự động. `notes.py check` chỉ kiểm tra cấu trúc và các dấu hiệu note quá mỏng hoặc metadata citation không nhất quán; tính đúng khoa học vẫn do MRLUAN đối chiếu nguồn. `registry.py` chỉ quản lý identity/intake và duplicate candidates, không thay scientific appraisal.

## Triển khai canonical

- Vai trò ghi và soát scientific note: **MRLUAN**.
- Mã nguồn, template, hướng dẫn và cấu hình: `https://github.com/mrluanresearch/Scientific_Notes_Simple`.
- Dữ liệu nghiên cứu và kết quả: Google Drive root `https://drive.google.com/drive/folders/1HxTYs2wg1B0K8QoF3AHuZHBeIpxUgDe_`.
- `results/SOURCE_REGISTRY.csv`: sổ đăng ký source canonical, cấp ID/chống trùng/file mapping.
- `results/MD/`: note Markdown, `INDEX.md`, và có thể có `references.csl.json`.
- `results/PDF/`: PDF nguồn canonical và supplement/data liên quan.
- `results/` bị loại khỏi Git; corpus MD/PDF/CSV registry không lên GitHub. Drive không giữ bản canonical của source code.

## Quy tắc đặt tên file

Canonical identity là `SAL-xxxx`, không phải author-year-title. **ID được cấp sau khi kiểm tra `SOURCE_REGISTRY.csv`, không cấp trực tiếp từ filename người dùng.**

### Main files

- Note: `SAL-0001.md`.
- PDF chính/version of record: `SAL-0001.pdf`.
- Một source canonical có tối đa một main PDF và một main MD cùng SAL ID.
- H1 của note phải là **exact source title**.
- Citation key: `SAL-0001`; khi dùng Pandoc/CSL có thể gọi `[@SAL-0001]`.

### Asset phụ

- Supplement: `SAL-0001-supp-01.pdf`, `SAL-0001-supp-02.xlsx`, ...
- Dataset: `SAL-0001-data-01.csv`, `SAL-0001-data-02.xlsx`, ...
- Protocol: `SAL-0001-protocol-01.pdf`.
- Code/archive snapshot: `SAL-0001-code-01.zip`.

Không dùng filename kiểu `Abdallah_2023_final.md`, `paper(1).pdf`, `SAL-0001-final.pdf`, `final2`, ngày xử lý hoặc trạng thái. Tên file gốc lúc ingest được giữ trong `SOURCE_REGISTRY.csv` ở cột `original_filename`, không dùng làm canonical filename.

Sửa title/DOI/author metadata không đổi SAL ID. Không renumber vì sort lại year/title. Sau `SAL-9999`, ID có thể mở rộng tự nhiên thành `SAL-10000` mà không đổi ID cũ.

Preprint/version of record/correction/retraction xử lý theo `CITATION_RULES.md` và `REGISTRY_RULES.md` để giữ provenance. Hai file có title gần giống không tự động là duplicate; version relationship phải được xác minh.

## SOURCE_REGISTRY.csv — lớp chống trùng trước note

`SOURCE_REGISTRY.csv` giải quyết khoảng trống mà `INDEX.md` và `notes.py new` không giải quyết được: một PDF có thể đã được đưa vào Drive nhưng chưa có note; cùng paper có thể được upload với tên file khác; DOI có thể thiếu; hoặc preprint/version of record có title gần nhau.

Registry giữ các khóa chính:

- exact `title` + machine `title_key`;
- `year`;
- `first_author` + `first_author_key`;
- `doi` + normalized `doi_key`;
- PMID/PMCID khi có;
- journal/container;
- publication type/status và version relation;
- original filename;
- canonical `pdf_filename` và `md_filename`;
- `pdf_sha256` để bắt exact binary duplicate;
- registry/note status và audit timestamps.

### Thứ tự duplicate check

1. DOI exact sau chuẩn hóa → hard duplicate candidate.
2. PMID/PMCID exact → hard duplicate candidate khi áp dụng cùng publication.
3. PDF SHA-256 exact → exact file duplicate.
4. Exact title key + first author + cùng năm → strong duplicate candidate.
5. Exact title key + năm cùng hoặc lệch ±1 → probable duplicate/version candidate.
6. Fuzzy title rất gần + cùng first author/journal/locator → review thủ công; không auto-merge.

Cùng DOI nhưng title khác là **identity conflict** và phải dừng intake để xác minh. Cùng title nhưng DOI khác không tự động là duplicate vì có thể là preprint, correction hoặc hai publication khác nhau.

Chi tiết schema, normalization và trạng thái xem `REGISTRY_RULES.md`.

## Workflow intake bắt buộc

Khi nhận một PDF/source mới:

1. Đọc bibliographic identity tối thiểu: exact title, first author, year, DOI/PMID nếu có.
2. Tính SHA-256 của PDF khi làm việc với file local.
3. Tìm duplicate/version candidate trong `SOURCE_REGISTRY.csv` **trước khi cấp SAL ID hoặc upload main PDF**.
4. Nếu duplicate chắc chắn: dùng SAL ID hiện có, không tạo source mới.
5. Nếu candidate mơ hồ: review version/metadata trước; chưa tạo active record mới.
6. Nếu source mới: cấp SAL ID kế tiếp trong registry.
7. Đổi main source thành `SAL-xxxx.pdf`, nhưng giữ `original_filename` trong registry.
8. Tạo `SAL-xxxx.md` cùng ID, H1 exact title và citation block.
9. Sau khi note tạo/soát, cập nhật `note_status`/`updated_at` trong registry.

Registry là canonical cho **identity intake + file mapping**. Note là canonical cho **scientific content + full citation metadata**. `INDEX.md` là file dẫn xuất để browse. Nếu registry và note khác title/year/DOI, coi đó là conflict cần đối chiếu nguồn, không âm thầm chọn một bên.

## Citation metadata: chuẩn bị cho APA và các style khác

Mỗi note có một block `citation:` ở mục 1 theo cấu trúc gần CSL-JSON. **Dữ liệu canonical là metadata thô, không phải câu citation đã format.** Cùng một record có thể render thành APA 7, Vancouver, Harvard, Chicago, IEEE hoặc style của journal khác chỉ bằng cách đổi CSL style.

Các trường quan trọng phải cố gắng giữ khi nguồn có:

- tất cả authors đúng thứ tự; cá nhân tách `family`/`given`, corporate author dùng `literal`;
- publication date qua `issued.date-parts`;
- exact title;
- journal/book/report/proceedings (`container-title`);
- volume, issue, pages hoặc article number;
- DOI chuẩn hóa và URL canonical;
- publisher, edition, editor, ISBN/ISSN khi phù hợp;
- language và accessed date cho webpage/dynamic content khi cần.

Journal article thường cần tối thiểu: author, issued, title, container-title, volume, issue, page/article number, DOI. Book/chapter/report/thesis/conference/dataset/software/webpage có bộ field riêng trong `CITATION_RULES.md`.

Không rút authors thành `et al.` trong metadata. Không dùng Google Scholar/search URL làm URL canonical. Không dùng ngày truy cập thay ngày xuất bản. DOI ở top YAML và block citation phải khớp.

## Tiêu chuẩn note chi tiết

Một `full_text` note phải giữ đủ thông tin để trả lời, không cần mở lại PDF chỉ vì note đã bỏ mất chi tiết:

1. Nghiên cứu hỏi gì, trên quần thể/dữ liệu nào và trong bối cảnh nào?
2. Luồng mẫu/dữ liệu từ đầu tới tập phân tích là bao nhiêu ở từng bước? Unit là farm, flock, bird, sample, isolate, genome hay study?
3. Phương pháp thực hiện cụ thể ra sao: culture/enrichment, AST, PCR, primer, cycling, WGS platform, reference genome, tool/database/version, identity/coverage/SNP threshold, statistical model?
4. Kết quả chính có tử số/mẫu số, đơn vị, CI/p-value và phân tầng nào? Kết quả âm tính/ngoại lệ nào làm thay đổi diễn giải?
5. Abstract, Results, Table và Figure có khớp nhau không? MRLUAN tính lại được gì và có bất nhất nào?
6. Tác giả diễn giải gì, nhưng bằng chứng thực sự chỉ hỗ trợ tới đâu?
7. Có thể dùng kết quả nào trực tiếp cho luận án, kết quả nào phải cảnh báo, và cần supplement/raw data nào để tái lập sâu hơn?
8. Có thể tạo citation đúng từ metadata trong note mà không mở lại PDF hay không?

Với bài full-text nhiều phương pháp/kết quả, note thường khoảng **1.800–3.500 từ tiếng Việt chưa tính bảng**; systematic review/meta-analysis thường **2.000–4.000 từ**. Đây là chuẩn biên tập, không phải quota: nguồn ngắn có thể ngắn hơn, nhưng không được cắt bỏ dữ liệu để đạt sự ngắn gọn.

### Quy tắc bảo toàn thông tin

- Không thay Methods/Results bằng abstract.
- Không ghi `xem Table X trong PDF` nếu dữ liệu bảng đó cần cho luận án; chép lại bảng con cần dùng vào MD.
- Prevalence/proportion phải ưu tiên `numerator/denominator`, không chỉ `%`.
- AST phải giữ panel và concentration/breakpoint/standard khi nguồn có.
- PCR phải giữ target/primer/product size và condition quan trọng khi có.
- WGS phải giữ tool/database/version/threshold/reference/accession khi có.
- Meta-analysis phải giữ search strategy, study count, model, heterogeneity, subgroup, risk-of-bias và sensitivity/publication-bias results khi có.
- `không báo cáo` là thông tin quan trọng; không im lặng bỏ trống và không tự thay bằng thông lệ.
- Gene presence không tự chứng minh phenotype/virulence expression; phylogenetic relatedness không tự chứng minh direct transmission; association không tự chứng minh causality.
- Nếu số liệu nguồn không khớp, giữ nguyên số gốc, ghi phép tính và vị trí từng con số. Không âm thầm sửa để làm note “sạch”.

## Mẫu thống nhất

YAML chỉ giữ `id`, `year`, `doi`, `tags`, `read_scope`, `status`. Tên bài, citation metadata và toàn bộ nội dung khoa học nằm trong thân note.

- `id`: SAL-0001 trở đi; filename khớp ID.
- `year`: năm xuất bản hoặc `null`.
- `doi`: DOI chuẩn hóa; chưa có dùng `""`.
- `tags`: 3–6 tag chữ thường không dấu.
- `read_scope`: `full_text`, `partial`, `abstract`.
- `status`: `draft`, `checked`.

Tám mục cấp `##` giữ nguyên tên và thứ tự: tài liệu/phạm vi; câu hỏi/đóng góp; phương pháp; kết quả/dữ liệu; diễn giải/phản biện; giá trị cho luận án; dùng lại/phần thiếu; đoạn tổng hợp. `NOTE_TEMPLATE.md` định nghĩa các tiểu mục `###` bên trong để buộc bảo toàn chi tiết.

## Trạng thái

`draft` khi note đang viết, còn bất nhất, thiếu supplement/raw data quan trọng, citation metadata chưa xác minh hoặc còn kết quả trọng yếu chưa xác minh. `checked` chỉ có nghĩa MRLUAN/người đọc đã đối chiếu source identity và các thông tin trung tâm trong phạm vi đọc được khai báo; không ngụ ý peer review độc lập.

Không nâng `checked` chỉ vì file đủ mục hoặc script báo 0 warning.

## Cách dùng với MRLUAN

Yêu cầu khuyến nghị:

> Trước khi xử lý source, kiểm tra `SOURCE_REGISTRY.csv` theo DOI/title/first author/PDF hash để chống trùng và cấp SAL ID đúng. Sau đó đọc toàn văn tài liệu đính kèm và viết source note tiếng Việt theo NOTE_TEMPLATE.md, AGENTS.md, CITATION_RULES.md và REGISTRY_RULES.md. Note phải tự đứng được: xác minh bibliographic identity và điền citation block đủ để xuất CSL; giữ đầy đủ luồng mẫu, unit of analysis, protocol, tool/version/threshold, bảng kết quả cần dùng lại, tử số/mẫu số, kết quả âm tính, kiểm tra số học, bất nhất nội tại, giới hạn và phần cần để tái lập. Không rút gọn Methods/Results thành abstract. Nếu thông tin không được nguồn báo cáo, ghi rõ `không báo cáo`. Nếu phát hiện bất nhất thì giữ nguyên số nguồn, tính lại và giữ `draft`.

Không dồn nhiều full-text vào một lượt để lấy tốc độ. Xử lý từng tài liệu hoàn chỉnh rồi chuyển tài liệu tiếp theo.

## Chạy công cụ

Python 3.10 trở lên:

```bash
python -m pip install -r requirements.txt

# Registry — chạy trên thư mục results đã sync/mount từ Drive
python registry.py --registry results/SOURCE_REGISTRY.csv check
python registry.py --registry results/SOURCE_REGISTRY.csv find \
  --title "Exact source title" --year 2026 --first-author "Family, Given" --doi 10.xxxx/xxxxx
python registry.py --registry results/SOURCE_REGISTRY.csv register \
  --title "Exact source title" --year 2026 --first-author "Family, Given" \
  --doi 10.xxxx/xxxxx --original-filename original.pdf

# Note
python notes.py new --title "Exact source title" --year 2026 --doi 10.xxxx/xxxxx --tags amr wgs
python notes.py check
python notes.py index
python notes.py csl
```

`registry.py register` chuẩn hóa DOI/title/first author, có thể tính `pdf_sha256` nếu truyền `--pdf`, từ chối hard duplicate và dừng khi gặp probable duplicate/version candidate trừ khi đã review và dùng `--allow-candidate`.

`notes.py new` vẫn kiểm tra DOI/tiêu đề trong corpus MD. Khi dùng workflow registry-first, SAL ID trong MD/PDF phải khớp row đã đăng ký; không dùng `notes.py new` như cơ chế cấp ID độc lập nếu registry đã có dữ liệu.

`notes.py check` cảnh báo khi:

- sai tám mục cấp `##`;
- còn placeholder;
- citation block thiếu hoặc YAML citation lỗi;
- citation ID/title/year/DOI không khớp note;
- journal metadata thiếu container hoặc locator quan trọng;
- note `full_text` quá ngắn;
- tổng nội dung mục 3–4 quá mỏng;
- thiếu bảng Markdown cần cho dữ liệu tái sử dụng;
- thiếu các tiểu mục chi tiết của template;
- thiếu dấu vết vị trí nguồn.

`notes.py csl` gom các citation block hợp lệ thành `references.csl.json`. Nếu có lỗi identity nghiêm trọng như title/year/DOI không khớp, script từ chối export để tránh tạo thư mục tài liệu sai.

Các cảnh báo là **heuristic QC**, không phải điểm khoa học. `0 warnings` không chứng minh số liệu đúng; vẫn phải đối chiếu PDF.

## Tổ chức 1.000 tài liệu

Mỗi source active có một row trong `SOURCE_REGISTRY.csv`, một `SAL-xxxx.md` và tối đa một main `SAL-xxxx.pdf`; phụ lục/data theo hậu tố chuẩn. Không tạo `final`, `final2`; sửa trực tiếp note hiện hành và giữ ID ổn định.

Sau mỗi đợt khoảng 10–20 nguồn, chạy registry check và chọn 2–3 note để đọc ngược với PDF. Nếu phát hiện một kiểu mất thông tin, lỗi bibliographic hoặc duplicate pattern lặp lại, sửa `AGENTS.md`, `NOTE_TEMPLATE.md`, `CITATION_RULES.md` hoặc `REGISTRY_RULES.md` trước khi tiếp tục. Chất lượng corpus được xây từ note chi tiết từng nguồn và identity sạch, không từ việc tạo đủ số lượng file.

## Đánh giá chất lượng thực

Tạm đóng PDF và thử trả lời: nghiên cứu hỏi gì; lấy mẫu/dữ liệu thế nào; phương pháp có thể mô tả đủ để người khác hiểu không; kết quả nào với mẫu số nào; số liệu có tự khớp không; giới hạn nào quan trọng; dùng lại và tái tính được gì; và có thể xuất bibliographic record đúng để render APA/Vancouver/Chicago/IEEE hay không?

Trước đó, cũng phải trả lời được: source này đã được đăng ký chưa; DOI/title/hash có trùng SAL nào không; main PDF và MD có cùng ID không; original filename có được truy vết trong registry không?

Nếu phải mở PDF chỉ vì note đã bỏ mất thông tin mà nguồn có, bổ sung note. Nếu bản thân nguồn thiếu thông tin, note phải nói rõ phần thiếu đó.