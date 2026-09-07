# Scientific Notes Simple

Một mẫu note cho 1.000 tài liệu. Sáu trường YAML; nội dung khoa học viết trực tiếp bằng Markdown.

## Thiết kế mới

Đây là gói viết lại từ đầu, không nâng cấp kiến trúc 9.1. Bỏ schema JSON, Evidence/Claim ID, hash/revision engine, điểm QC/relevance, cổng approve, YAML kết quả lồng nhiều tầng và phụ lục dữ liệu tự sinh. Mục tiêu là người đọc dùng được note.

| Thành phần | Vai trò |
| --- | --- |
| AGENTS.md | Hướng dẫn MRLUAN đọc nguồn và viết nội dung |
| NOTE_TEMPLATE.md | Mẫu duy nhất, sáu trường YAML và tám mục cố định |
| examples/SAL-0001.md | Note đã điền trên bài Neuert và cộng sự (2018), kèm nguồn và giới hạn đọc |
| notes.py | Tạo khung, kiểm tra hình thức, lập mục lục |
| requirements.txt | Một dependency: PyYAML |
| PROJECT.yaml | Ánh xạ canonical giữa GitHub, Google Drive và vai trò MRLUAN |

Script không tự viết phân tích, không gọi LLM, không đọc PDF tự động. Chất lượng nằm ở quá trình đọc/viết theo AGENTS và note mẫu. Có thể dùng bộ này ngay trong ChatGPT/Claude/Codex với tài liệu đính kèm; Python chỉ giúp quản lý tệp.

## Triển khai canonical

- Vai trò ghi và soát scientific note: **MRLUAN**. Mọi attribution về người/agent thực hiện dùng tên này hoặc tên người soát cụ thể.
- Mã nguồn, template, hướng dẫn và cấu hình: GitHub `https://github.com/mrluanresearch/Scientific_Notes_Simple`.
- Dữ liệu nghiên cứu và kết quả: Google Drive root `https://drive.google.com/drive/folders/1HxTYs2wg1B0K8QoF3AHuZHBeIpxUgDe_`.
- Cấu trúc Drive: `results/MD/` chứa note Markdown và `INDEX.md`; `results/PDF/` chứa PDF nguồn.
- `results/` bị loại khỏi Git bằng `.gitignore`; không đưa corpus MD/PDF lên GitHub. Ngược lại, không dùng Drive để lưu bản canonical của mã nguồn.
- Khi làm việc trên máy có Drive được đồng bộ/mount, trỏ `notes.py --notes` tới thư mục Drive `results/MD`. Script không tự upload và không chứa credential.

Bài mẫu giữ `draft` dù đã đọc toàn văn: việc tính lại phát hiện một hàng bảng nguồn có tổng không khớp cỡ mẫu. Note chỉ rõ phép tính, vị trí nguồn và phần có thể dùng lại; không tự sửa dữ liệu hay giấu bất nhất để đạt trạng thái đẹp.

## Mẫu thống nhất

YAML chỉ giữ `id`, `year`, `doi`, `tags`, `read_scope`, `status`. Tên bài và trích dẫn đầy đủ nằm trong thân note. Không lưu kết quả, phương pháp, appraisal hoặc claim vào YAML.

- id: SAL-0001 đến SAL-1000 và có thể mở rộng; filename khớp ID.
- year: năm xuất bản, chưa biết để null; doi: chưa có để chuỗi rỗng.
- tags: 3–6 chủ đề ổn định, chữ thường không dấu; ví dụ amr, wgs, sampling, genotype-phenotype, one-health. Không dùng mười cách viết cho cùng chủ đề.
- read_scope: full_text, partial hoặc abstract; phần chưa đọc/phụ lục chưa có giải thích ở mục 1.
- status: draft hoặc checked. checked chỉ nói đã soát theo phạm vi khai báo; tên MRLUAN hoặc người thực hiện ở mục 1. Script không nâng trạng thái.

Tám mục giữ nguyên tên và thứ tự: tài liệu/phạm vi; câu hỏi/đóng góp; phương pháp; kết quả/dữ liệu; diễn giải/phản biện; giá trị cho luận án; dùng lại/phần thiếu; đoạn tổng hợp. Có thể thêm tiêu đề cấp ba bên trong từng mục. Với loại nguồn khác nhau, thay nội dung cho phù hợp, giữ khung chung.

## Cách dùng với MRLUAN

Gửi AGENTS.md, NOTE_TEMPLATE.md, note mẫu và một tài liệu thật. Có thể dùng yêu cầu:

> Đọc tài liệu đính kèm và viết một source note tiếng Việt theo NOTE_TEMPLATE.md, tuân thủ AGENTS.md. Dùng note mẫu để hiểu độ cụ thể cần đạt; không sao chép dữ liệu của bài mẫu. Dành phần lớn nội dung cho thiết kế, dữ liệu, kết quả và phản biện. Giữ các bảng cần dùng lại ngay trong MD; ghi vị trí nguồn, mẫu số, đơn vị và phần chưa được tác giả báo cáo. Hoàn thiện từng tài liệu trước khi chuyển tài liệu kế tiếp. Chưa đủ nguồn thì ghi rõ và giữ draft; không viết dài bằng suy đoán.

Không dồn 1.000 toàn văn vào một lượt rồi yêu cầu tóm tắt hàng loạt. Bắt đầu với khoảng 10 nguồn khác loại để điều chỉnh mẫu bằng chất lượng note thực; sau đó xử lý theo đợt khoảng 20. Đây là cách tổ chức công việc, không phải cổng xin phê duyệt. Trong một đợt vẫn viết lần lượt từng note để không cắt ngắn nội dung vì giới hạn đầu ra.

## Chạy công cụ

Python 3.10 trở lên. Chạy từ thư mục gốc:

```bash
python -m pip install -r requirements.txt
python notes.py new --title "Tên tài liệu thật" --year 2026 --tags amr wgs
python notes.py check
python notes.py index
```

`new` tạo SAL-0001.md hoặc ID tiếp theo, từ chối DOI/tiêu đề đã có và không ghi đè note. Điền note bằng MRLUAN/người đọc rồi `check`; sửa các chỗ cần xem và chạy `index` sau mỗi đợt. Có thể thêm `--doi` khi tạo.

Kho ở nơi khác: đặt `--notes` trước tên lệnh. Ví dụ:

```bash
python notes.py --notes /duong-dan/kho/MD check
python notes.py --notes /duong-dan/kho/MD index
```

INDEX.md được dựng lại từ các note; không sửa tay. Các note draft vẫn có trong mục lục để không mất việc đang làm. Nếu YAML hỏng hoặc DOI trùng, script báo lỗi để sửa trước khi lập mục lục. `check` có thể nhắc nhầm một ký hiệu trong ngoặc vuông là placeholder; người đọc quyết định. Không lấy kết quả check làm thang chất lượng khoa học.

## Tổ chức 1.000 tài liệu

Mỗi nguồn một tệp `SAL-xxxx.md`, sửa trực tiếp bản hiện hành; không tạo final/final2. PDF tương ứng là `SAL-xxxx.pdf`; phụ lục PDF thêm hậu tố `-supp-01`. Không đổi ID khi đổi tiêu đề. Chỉ dùng một người/tiến trình cấp ID trong cùng thư mục; khi tạo trùng cùng lúc, chương trình từ chối ghi đè.

Đặt tất cả MD và INDEX.md trong `results/MD`; PDF nguồn trong `results/PDF`. Mục lục có ID, năm, tiêu đề, DOI, chủ đề, phạm vi đọc và trạng thái. Có thể tìm theo tag/DOI/từ khóa ngay trên mục lục và toàn văn note; chưa cần database.

Google Drive chỉ lưu nội dung `results/`: MD/PDF. Mã nguồn, mẫu, hướng dẫn và cấu hình remote ở GitHub. Gói không có chức năng upload, tài khoản hoặc secrets. Nếu cần bản PDF của note, xuất từ trình đọc Markdown; không bổ sung một renderer riêng ở giai đoạn này.

Không chạy script cũ trên kho mới. Giữ dữ liệu cũ để đối chiếu; chuyển từng note có giá trị bằng cách giữ văn bản/số liệu/nguồn, đưa vào tám mục và sáu trường mới. Không nhập hàng loạt YAML cũ sang cấu trúc lồng tầng tương đương. Với ID cũ cần truy vết, ghi một dòng ở mục 1.

## Đánh giá chất lượng thực

Tạm đóng PDF và thử năm câu hỏi: nghiên cứu hỏi gì; làm trên ai/bằng dữ liệu nào; kết quả cụ thể và mẫu số là gì; kết luận bị giới hạn bởi điều gì; dùng vào luận án và tính/kiểm tra lại được phần nào?

Nếu phải mở PDF chỉ vì note bỏ mất một thông tin quan trọng đã có trong nguồn, bổ sung note. Nếu bản thân nguồn không có thông tin thì nêu rõ phần thiếu. Kiểm tra phần trọng yếu với nguồn trước khi dùng vào bản thảo. Một note dài nhưng không trả lời được năm câu hỏi trên vẫn chưa đạt.

Các phép thử quản lý 1.000 tệp chỉ đánh giá khả năng tạo/đọc/index, không đại diện cho chất lượng 1.000 tài liệu khoa học. Bài mẫu là một ví dụ có giới hạn đọc được khai báo; cần đối chiếu thêm trên những loại nguồn thực tế của người dùng.

Đã chạy kiểm tra trên Python 3.12.13 và PyYAML 6.0.3: UTF-8, từ chối DOI/tiêu đề trùng, giữ nguyên note và trạng thái, bảo toàn mục lục khi YAML lỗi, và lập đúng 1.000 hàng mục lục từ 1.000 tệp giả lập. Dữ liệu giả lập không nằm trong gói.
