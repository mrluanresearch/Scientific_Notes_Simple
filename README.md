# Scientific Notes Simple

Một mẫu note cho 1.000 tài liệu. Sáu trường YAML; nội dung khoa học viết trực tiếp bằng Markdown. Mục tiêu của dự án không phải tạo bản tóm tắt ngắn, mà tạo **source note tự đứng được** để hiểu, đánh giá, trích dẫn và tái tính bằng chứng mà không phải mở lại PDF cho những chi tiết tác giả đã báo cáo.

## Thiết kế

Đây là gói viết lại từ đầu, không nâng cấp kiến trúc 9.1. Bỏ schema JSON, Evidence/Claim ID, hash/revision engine, điểm QC/relevance, cổng approve, YAML kết quả lồng nhiều tầng và phụ lục dữ liệu tự sinh. Mục tiêu là nội dung khoa học có thể dùng được.

| Thành phần | Vai trò |
| --- | --- |
| AGENTS.md | Quy tắc MRLUAN đọc nguồn, bảo toàn dữ liệu, phản biện và QC |
| NOTE_TEMPLATE.md | Mẫu duy nhất: sáu trường YAML, tám mục cấp `##`, các tiểu mục chi tiết bắt buộc |
| examples/SAL-0001.md | Note đã điền trên bài Neuert và cộng sự (2018), kèm nguồn và giới hạn đọc |
| notes.py | Tạo khung, kiểm tra cấu trúc/độ sâu, lập mục lục |
| requirements.txt | Một dependency: PyYAML |
| PROJECT.yaml | Ánh xạ canonical giữa GitHub, Google Drive và vai trò MRLUAN |

Script không tự viết phân tích, không gọi LLM và không đọc PDF tự động. `notes.py check` chỉ kiểm tra cấu trúc và các dấu hiệu note quá mỏng; tính đúng khoa học vẫn do MRLUAN đối chiếu nguồn.

## Triển khai canonical

- Vai trò ghi và soát scientific note: **MRLUAN**.
- Mã nguồn, template, hướng dẫn và cấu hình: `https://github.com/mrluanresearch/Scientific_Notes_Simple`.
- Dữ liệu nghiên cứu và kết quả: Google Drive root `https://drive.google.com/drive/folders/1HxTYs2wg1B0K8QoF3AHuZHBeIpxUgDe_`.
- `results/MD/`: note Markdown + `INDEX.md`.
- `results/PDF/`: PDF nguồn canonical.
- `results/` bị loại khỏi Git; corpus MD/PDF không lên GitHub. Drive không giữ bản canonical của source code.

## Tiêu chuẩn note chi tiết

Một `full_text` note phải giữ đủ thông tin để trả lời, không cần mở lại PDF chỉ vì note đã bỏ mất chi tiết:

1. Nghiên cứu hỏi gì, trên quần thể/dữ liệu nào và trong bối cảnh nào?
2. Luồng mẫu/dữ liệu từ đầu tới tập phân tích là bao nhiêu ở từng bước? Unit là farm, flock, bird, sample, isolate, genome hay study?
3. Phương pháp thực hiện cụ thể ra sao: culture/enrichment, AST, PCR, primer, cycling, WGS platform, reference genome, tool/database/version, identity/coverage/SNP threshold, statistical model?
4. Kết quả chính có tử số/mẫu số, đơn vị, CI/p-value và phân tầng nào? Kết quả âm tính/ngoại lệ nào làm thay đổi diễn giải?
5. Abstract, Results, Table và Figure có khớp nhau không? MRLUAN tính lại được gì và có bất nhất nào?
6. Tác giả diễn giải gì, nhưng bằng chứng thực sự chỉ hỗ trợ tới đâu?
7. Có thể dùng kết quả nào trực tiếp cho luận án, kết quả nào phải cảnh báo, và cần supplement/raw data nào để tái lập sâu hơn?

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

YAML chỉ giữ `id`, `year`, `doi`, `tags`, `read_scope`, `status`. Tên bài và toàn bộ nội dung khoa học nằm trong thân note.

- `id`: SAL-0001 trở đi; filename khớp ID.
- `year`: năm xuất bản hoặc `null`.
- `doi`: DOI chuẩn hóa; chưa có dùng `""`.
- `tags`: 3–6 tag chữ thường không dấu.
- `read_scope`: `full_text`, `partial`, `abstract`.
- `status`: `draft`, `checked`.

Tám mục cấp `##` giữ nguyên tên và thứ tự: tài liệu/phạm vi; câu hỏi/đóng góp; phương pháp; kết quả/dữ liệu; diễn giải/phản biện; giá trị cho luận án; dùng lại/phần thiếu; đoạn tổng hợp. `NOTE_TEMPLATE.md` định nghĩa các tiểu mục `###` bên trong để buộc bảo toàn chi tiết.

## Trạng thái

`draft` khi note đang viết, còn bất nhất, thiếu supplement/raw data quan trọng hoặc còn kết quả trọng yếu chưa xác minh. `checked` chỉ có nghĩa MRLUAN/người đọc đã đối chiếu các thông tin trung tâm trong phạm vi đọc được khai báo; không ngụ ý peer review độc lập.

Không nâng `checked` chỉ vì file đủ mục hoặc script báo 0 warning.

## Cách dùng với MRLUAN

Yêu cầu khuyến nghị:

> Đọc toàn văn tài liệu đính kèm và viết source note tiếng Việt theo NOTE_TEMPLATE.md và AGENTS.md. Note phải tự đứng được: giữ đầy đủ luồng mẫu, unit of analysis, protocol, tool/version/threshold, bảng kết quả cần dùng lại, tử số/mẫu số, kết quả âm tính, kiểm tra số học, bất nhất nội tại, giới hạn và phần cần để tái lập. Không rút gọn Methods/Results thành abstract. Nếu thông tin không được nguồn báo cáo, ghi rõ `không báo cáo`. Nếu phát hiện bất nhất thì giữ nguyên số nguồn, tính lại và giữ `draft`.

Không dồn nhiều full-text vào một lượt để lấy tốc độ. Xử lý từng tài liệu hoàn chỉnh rồi chuyển tài liệu tiếp theo.

## Chạy công cụ

Python 3.10 trở lên:

```bash
python -m pip install -r requirements.txt
python notes.py new --title "Tên tài liệu thật" --year 2026 --tags amr wgs
python notes.py check
python notes.py index
```

Kho ở nơi khác:

```bash
python notes.py --notes /duong-dan/kho/MD check
python notes.py --notes /duong-dan/kho/MD index
```

`notes.py check` cảnh báo khi:

- sai tám mục cấp `##`;
- còn placeholder;
- note `full_text` quá ngắn;
- tổng nội dung mục 3–4 quá mỏng;
- thiếu bảng Markdown cần cho dữ liệu tái sử dụng;
- thiếu các tiểu mục chi tiết của template;
- thiếu dấu vết vị trí nguồn.

Các cảnh báo này là **heuristic QC**, không phải điểm khoa học. `0 warnings` không chứng minh số liệu đúng; vẫn phải đối chiếu PDF.

## Tổ chức 1.000 tài liệu

Mỗi nguồn một `SAL-xxxx.md`; PDF tương ứng `SAL-xxxx.pdf`; phụ lục PDF thêm `-supp-01`. Không tạo `final`, `final2`; sửa trực tiếp note hiện hành và giữ ID ổn định.

Sau mỗi đợt khoảng 10–20 nguồn, chọn 2–3 note để đọc ngược với PDF. Nếu phát hiện một kiểu mất thông tin lặp lại, sửa `AGENTS.md` và `NOTE_TEMPLATE.md` trước khi tiếp tục. Chất lượng corpus được xây từ note chi tiết từng nguồn, không từ việc tạo đủ số lượng file.

## Đánh giá chất lượng thực

Tạm đóng PDF và thử trả lời: nghiên cứu hỏi gì; lấy mẫu/dữ liệu thế nào; phương pháp có thể mô tả đủ để người khác hiểu không; kết quả nào với mẫu số nào; số liệu có tự khớp không; giới hạn nào quan trọng; dùng lại và tái tính được gì?

Nếu phải mở PDF chỉ vì note đã bỏ mất thông tin mà nguồn có, bổ sung note. Nếu bản thân nguồn thiếu thông tin, note phải nói rõ phần thiếu đó.
