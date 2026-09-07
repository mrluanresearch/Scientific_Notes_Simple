---
id: SAL-0001
year: null
doi: ""
tags: []
read_scope: partial
status: draft
---

# [Tiêu đề tài liệu]

## 1. Tài liệu và phạm vi đọc

[Trích dẫn đầy đủ: tác giả, năm, tên tài liệu, journal/book/report, volume(issue), pages/article number, DOI/URL nếu có.]

- **PDF/source canonical:** [tên tệp hoặc liên kết Drive; nếu có HTML/supplement/raw data thì liệt kê riêng].
- **Loại tài liệu:** [nghiên cứu thực nghiệm / giám sát / WGS / systematic review / meta-analysis / guideline / khác].
- **Phạm vi đã đọc:** [toàn văn hay phần cụ thể; bảng/hình/phụ lục nào đã kiểm tra trực quan].
- **Phần chưa có/chưa đọc:** [supplement, raw reads, accession, protocol, appendix...]; nếu không có thì ghi `Không`.
- **Ngày và người soát:** [YYYY-MM-DD; MRLUAN hoặc tên người thực sự đọc].
- **Lý do giữ `draft` nếu có:** [bất nhất số liệu, thiếu supplement, chưa kiểm tra raw data, chưa tái tính một chỉ số quan trọng...].

**Bản đồ nguồn cần quay lại:** ghi cụ thể vị trí của Methods, bảng/hình kết quả chính, supplement và data availability. Mục tiêu là người đọc có thể tìm lại đúng bằng chứng trong vài giây, không phải đọc lại toàn PDF.

## 2. Câu hỏi và đóng góp chính

### 2.1. Câu hỏi nghiên cứu

[Viết 1–3 câu hỏi cụ thể. Tách câu hỏi mô tả, so sánh, dự đoán, quan hệ phát sinh, source tracing, AMR/virulence... nếu nguồn có nhiều mục tiêu.]

### 2.2. Khoảng trống và đóng góp

[Khoảng trống mà tác giả muốn giải quyết; đối tượng/bối cảnh; đóng góp thực sự của nghiên cứu. Không lặp abstract.]

### 2.3. Kết luận trung tâm cần nhớ

[3–8 ý có số liệu hoặc phát hiện cụ thể. Mỗi ý phải mang theo mẫu số/đơn vị hoặc điều kiện diễn giải khi có thể.]

## 3. Thiết kế và phương pháp

*Mục này phải đủ chi tiết để hiểu nghiên cứu đã làm gì mà không cần mở lại PDF cho các thông tin đã được tác giả báo cáo. Không chỉ ghi tên phương pháp.*

### 3.1. Bối cảnh, quần thể và luồng mẫu/dữ liệu

[Địa điểm, thời gian, quần thể đích/quần thể nguồn, tiêu chí chọn–loại, cách chọn mẫu, đơn vị lấy mẫu, đơn vị phân tích, số lượng ở từng bước. Tách rõ sample, isolate, strain, genome, flock, farm, patient, paper...]

| Bước/nhóm | Số lượng ban đầu | Loại/thiếu | Số vào phân tích | Đơn vị | Ghi chú và vị trí nguồn |
| --- | ---: | ---: | ---: | --- | --- |
| [Bước] | [n] | [n/lý do] | [n] | [sample/isolate/genome...] | [Methods/Table/Figure/page] |

[Nếu không thể dựng flow vì nguồn không báo cáo đủ, ghi chính xác chỗ thiếu. Không tự suy từ các bảng rời.] 

### 3.2. Thu thập mẫu, nuôi cấy/đo lường và định danh

[Giữ các thông số có thể ảnh hưởng kết quả: khối lượng/thể tích, môi trường, pre-enrichment/enrichment, nhiệt độ, thời gian, tiêu chuẩn ISO/CLSI/EUCAST, breakpoint, kit, control, số lần lặp, cách gọi positive/negative. Với nghiên cứu không vi sinh, thay bằng quy trình thu thập/đo lường tương ứng.]

| Thành phần | Protocol/thiết bị/tiêu chuẩn | Thông số tác giả báo cáo | Điều không được báo cáo | Vị trí nguồn |
| --- | --- | --- | --- | --- |
| [Ví dụ: isolation/AST] | [ISO/CLSI/kit] | [nhiệt độ, thời gian, disc concentration...] | [nếu thiếu] | [trang/bảng] |

### 3.3. PCR/WGS/bioinformatics hoặc xét nghiệm phân tử

[Chỉ dùng khi phù hợp; nếu không phù hợp ghi `Không áp dụng`. Ghi primer/target/product size hoặc platform/library/read length/reference genome/tool/database/version/identity/coverage/SNP thresholds.]

| Bước | Target/input | Tool/kit/database + version | Threshold/parameter quan trọng | Output dùng trong bài | Vị trí nguồn |
| --- | --- | --- | --- | --- | --- |
| [PCR/WGS/assembly/AMR/phylogeny...] | [...] | [...] | [...] | [...] | [...] |

[Nếu primer có ý nghĩa sử dụng lại, giữ nguyên sequence 5′→3′ trong bảng con. Nếu nguồn không báo version/database date, ghi `không báo cáo` thay vì tự điền.] 

### 3.4. Phân tích thống kê

[Mô hình/test, outcome, predictor, reference group, đơn vị phân tích, CI, alpha, correction, software + version. Với meta-analysis: effect measure, model, heterogeneity, subgroup/meta-regression, publication bias, sensitivity analysis.]

### 3.5. Khả năng tái lập từ thông tin phương pháp

[Phân biệt ba mức: (a) có thể tái tính từ bảng trong note; (b) có thể tái chạy nếu lấy được raw/supplement; (c) chưa thể tái lập vì thiếu dữ liệu/parameter. Liệt kê chính xác thứ còn thiếu.]

## 4. Kết quả và dữ liệu cần giữ

*Mục này là lõi của note. Phải giữ đủ số liệu để trích dẫn, so sánh và tính lại các kết quả quan trọng; không dùng câu “xem Table/Figure trong PDF” thay cho dữ liệu.*

### 4.1. Kết quả chính

| Outcome/phát hiện | Tử số / mẫu số hoặc giá trị | % / effect / CI / p | Nhóm/điều kiện | Vị trí nguồn | Ghi chú diễn giải |
| --- | --- | --- | --- | --- | --- |
| [Outcome] | [a/b, mean±SD, OR...] | [...] | [...] | [Table/Fig/page] | [đúng phạm vi] |

### 4.2. Bảng dữ liệu chi tiết có thể dùng lại

[Chép lại các hàng/cột trọng yếu: prevalence theo nguồn, serovar, AST theo từng thuốc, gene theo isolate/nhóm, ST, plasmid, SNP range, subgroup meta-analysis... Giữ header, đơn vị, denominator và chú thích quan trọng. Không chép bảng không liên quan.]

### 4.3. Kết quả âm tính, ngoại lệ và phân tầng

[Những gene/serovar/antibiotic không phát hiện; nhóm không có khác biệt; kết quả không có ý nghĩa thống kê; isolate ngoại lệ; missingness. Đây là dữ liệu, không được bỏ chỉ vì không hỗ trợ câu chuyện chính.]

### 4.4. Kiểm tra số học và nhất quán nội tại

- **Tác giả báo cáo:** [các số cần kiểm tra].
- **MRLUAN tính lại:** [công thức + phép thế số + kết quả].
- **Kết quả:** [khớp / sai do làm tròn / không khớp].
- **Bất nhất giữa Abstract–Text–Table–Figure:** [nếu có, ghi cả hai giá trị và vị trí; tuyệt đối không âm thầm chọn một].
- **Ảnh hưởng tới việc dùng lại:** [có thể dùng / chỉ dùng có cảnh báo / chưa dùng cho pooled analysis...].

## 5. Diễn giải và phản biện

### 5.1. Tác giả diễn giải gì

[Tóm tắt logic của tác giả, gồm cơ chế/nguồn truyền/ý nghĩa giám sát nếu họ đề xuất. Dùng từ như `tác giả cho rằng` khi đó là diễn giải chứ không phải quan sát trực tiếp.]

### 5.2. Bằng chứng thực sự hỗ trợ tới đâu

[Đối chiếu trực tiếp với mục 3–4. Phân biệt association với causation; genomic relatedness với direct transmission; gene presence với phenotype/virulence expression; mẫu chọn lọc với prevalence quần thể.]

### 5.3. Threats to validity / giới hạn

| Loại giới hạn | Chi tiết cụ thể trong nghiên cứu | Hướng sai lệch hoặc ảnh hưởng diễn giải |
| --- | --- | --- |
| Selection/sampling | [...] | [...] |
| Measurement/lab | [...] | [...] |
| Statistical/denominator | [...] | [...] |
| Genomic/bioinformatic | [...] | [...] |
| External validity | [...] | [...] |

[Không viết danh sách giới hạn chung chung. Chỉ giữ giới hạn gắn với thiết kế và dữ liệu thực tế của nguồn.]

## 6. Giá trị đối với luận án

### 6.1. Dùng ở đâu

[Nêu rõ: Tổng quan / Methods / Results comparison / Discussion / One Health framework / AMR / WGS / source attribution... và luận điểm cụ thể được nguồn hỗ trợ.]

### 6.2. So sánh với dữ liệu luận án cần điều kiện gì

[Population, matrix, serovar, antimicrobial panel, breakpoint, genome pipeline, geography, time, sampling frame... Những điều phải tương đồng hoặc phải điều chỉnh khi so sánh.]

### 6.3. Không dùng để kết luận

[Liệt kê các suy rộng nguồn không hỗ trợ. Đây là hàng rào chống overclaim khi viết luận án.] 

## 7. Cách dùng lại và phần còn thiếu

### 7.1. Các phép tính/tái tạo có thể thực hiện ngay từ note

[Viết công thức, phép thế số và kết quả. Ghi rõ đâu là số tác giả, đâu là số MRLUAN tính lại. Với bảng 2×2 có thể tính sensitivity/specificity; với prevalence tính numerator/denominator; với meta-analysis không tự tái tạo pooled estimate nếu thiếu study-level data.]

### 7.2. Dữ liệu/tệp cần để tái lập sâu hơn

| Mục tiêu tái lập | Đã có trong note/source | Còn thiếu | Nơi dự kiến lấy | Mức ảnh hưởng |
| --- | --- | --- | --- | --- |
| [Ví dụ: chạy lại WGS] | [accession/tool] | [raw reads/config/db snapshot] | [NCBI/Supplement] | [cao/vừa/thấp] |

### 7.3. Quyết định sử dụng bằng chứng

- **Có thể dùng trực tiếp:** [kết quả đã kiểm tra].
- **Chỉ dùng kèm cảnh báo:** [kết quả có limitation/bất nhất].
- **Chưa dùng:** [kết quả cần supplement/raw/đính chính].
- **Việc cần làm tiếp:** [1–5 hành động cụ thể, không viết chung chung].

## 8. Đoạn tổng hợp có thể sử dụng

[Viết 1–3 đoạn học thuật liền mạch, có tác giả–năm, số liệu trung tâm, mẫu số/đơn vị và giới hạn quan trọng. Đoạn này phải dùng được trong bản thảo sau khi điều chỉnh ngữ cảnh. Không chỉ viết lại abstract và không đưa nhận định vượt quá bằng chứng.]
