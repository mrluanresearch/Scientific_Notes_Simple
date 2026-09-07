# Viết source note: nội dung khoa học là sản phẩm chính

Đọc README.md và NOTE_TEMPLATE.md; xem examples/SAL-0001.md để hiểu cách ghi bằng chứng. **Vai trò thực thi canonical là MRLUAN**; khi ghi người thực hiện/soát note, dùng MRLUAN hoặc tên người soát cụ thể. Dự án phục vụ Salmonella–AMR–WGS–One Health; ngữ cảnh luận án chưa xác minh không được coi là dữ liệu đã thực hiện.

## Nguyên tắc bắt buộc

Một note đạt yêu cầu phải **tự đứng được**. Nếu thông tin quan trọng đã có trong PDF nhưng người viết vẫn phải mở PDF chỉ để nhớ lại thiết kế, denominator, protocol, primer, threshold, bảng kết quả hoặc giới hạn, note đó chưa hoàn thành. PDF vẫn là nguồn gốc để xác minh, nhưng MD phải giữ đủ nội dung để hiểu, đánh giá, trích dẫn và tái tính các kết quả trọng yếu.

Không tối giản note để tiết kiệm token. Không dùng abstract như thay thế cho việc đọc Methods/Results/Tables/Figures. Không viết hàng loạt 10–20 note ngắn rồi coi đó là hoàn thành. Mỗi tài liệu được xử lý như một đơn vị khoa học độc lập.

## Quy trình cho từng tài liệu

1. Tra ID/DOI/tiêu đề trong kho để tránh trùng. Xác định file PDF canonical và supplement/raw data nếu có.
2. Đọc toàn bộ Methods, Results, tables, figure captions, Discussion/Limitations và Data availability. Với bảng/hình mà text extraction làm mất cấu trúc, phải kiểm tra trực quan.
3. Dựng **bản đồ dữ liệu** trước khi viết prose: population → sampling → laboratory/measurement → molecular/bioinformatics → statistics → primary results → negative results → limitations.
4. Viết mục 3 và 4 trước. Giữ các số lượng ở từng bước, unit of analysis, denominator, unit, protocol, version, threshold, control, reference group và source location.
5. Với PCR: giữ target, primer sequence khi có giá trị dùng lại, amplicon size, reaction/cycling condition nếu nguồn báo cáo. Với WGS: giữ platform/library/read length nếu có, reference genome, tool/database/version, identity/coverage/SNP thresholds, accession và cách tạo phylogeny. Với AST: giữ drug, disk concentration/MIC method, CLSI/EUCAST version hoặc năm, breakpoint nếu nguồn nêu. Với meta-analysis: giữ search dates/databases, inclusion/exclusion, effect model, heterogeneity, subgroup/meta-regression, publication-bias/sensitivity analysis.
6. Chép lại **các bảng con cần dùng lại** vào Markdown. Không ghi “xem Table X” thay cho số liệu. Không cần chép bảng không liên quan, nhưng các bảng quyết định kết luận phải có denominator và chú thích đủ để hiểu độc lập.
7. Tính lại các tỷ lệ/tổng/OR đơn giản có thể kiểm tra từ dữ liệu nguồn. So sánh Abstract ↔ Results ↔ Table ↔ Figure. Nếu không khớp, giữ nguyên các giá trị nguồn, ghi phép tính và vị trí từng giá trị; không tự sửa hoặc chọn số “hợp lý hơn”.
8. Viết mục 5 sau khi dữ liệu đã cố định. Tách ba lớp: **kết quả nguồn**, **diễn giải tác giả**, **nhận định MRLUAN**. Không biến giả thuyết cơ chế thành quan sát.
9. Viết mục 6–8 từ bằng chứng đã ghi, không từ trí nhớ. Đoạn tổng hợp phải có số liệu trung tâm, đúng mẫu số và giới hạn.
10. Tạm đóng PDF và tự kiểm tra: có thể trả lời nghiên cứu làm trên ai/cái gì, bằng phương pháp nào, số lượng ở từng bước, kết quả chính theo denominator nào, giới hạn gì, và có thể tính lại phần nào hay không? Nếu chưa, quay lại nguồn và bổ sung.

## Mức chi tiết tối thiểu theo loại nguồn

Đây là yêu cầu nội dung, không phải quota máy móc. Không thêm chữ vô nghĩa để đạt số từ.

- **Full-text nghiên cứu thực nghiệm/WGS/AMR:** thường khoảng **1.800–3.500 từ tiếng Việt**, chưa tính bảng. Nguồn nhiều pipeline hoặc nhiều outcome có thể dài hơn.
- **Systematic review/meta-analysis:** thường **2.000–4.000 từ**, vì phải giữ search strategy, risk of bias, model, heterogeneity, subgroup, pooled estimates và giới hạn.
- **Short communication/nguồn ngắn:** có thể ngắn hơn, nhưng vẫn phải giữ toàn bộ methods/results có ý nghĩa.
- `abstract`/`partial`: độ dài theo phần thật sự có; tuyệt đối không giả lập chi tiết toàn văn.

Một note 1.000–1.300 từ cho một bài full-text nhiều bảng/phương pháp thường là tín hiệu thiếu nội dung và phải rà lại.

## Checklist bắt buộc cho mục 3 — Thiết kế và phương pháp

Phải trả lời được, khi nguồn có báo cáo:

- Địa điểm, thời gian, loại thiết kế.
- Quần thể nguồn, cách chọn, tiêu chí chọn/loại.
- Sample size ở từng tầng: farm/flock/bird/sample/isolate/genome/study.
- Unit of sampling và unit of analysis; chỉ rõ khi hai đơn vị khác nhau.
- Luồng mẫu/dữ liệu và số bị loại/missing.
- Nuôi cấy/định danh: môi trường, enrichment, nhiệt độ/thời gian, ISO hoặc phương pháp tham chiếu.
- AST: method, antimicrobial panel, concentration, standard/breakpoint, quality control.
- PCR: extraction, target, primer, product size, reaction/cycling, positive/negative controls.
- WGS/bioinformatics: sequencing, assembly/QC, reference, tool/database/version, cutoffs, phylogenetic model.
- Statistics: test/model, outcome/predictor, reference group, CI/alpha, software/version.
- Data availability/accession/supplement và phần còn thiếu cho reproducibility.

Nếu một chi tiết quan trọng **không được tác giả báo cáo**, note phải ghi `không báo cáo` thay vì bỏ qua im lặng.

## Checklist bắt buộc cho mục 4 — Kết quả và dữ liệu

- Mọi prevalence/proportion quan trọng có **tử số/mẫu số**, không chỉ %.
- Mọi effect estimate quan trọng có nhóm so sánh, reference, CI/p-value khi nguồn có.
- Giữ kết quả theo phân tầng quan trọng: source, sample type, serovar, antimicrobial, gene, ST, plasmid, clade, country/subgroup.
- Giữ kết quả âm tính và non-significant có ảnh hưởng diễn giải.
- Với AST, ưu tiên bảng từng thuốc nếu số thuốc không quá lớn; nếu nhiều, ít nhất giữ nhóm trọng yếu và toàn bộ pattern làm thay đổi kết luận.
- Với PCR/virulence/AMR genes, giữ numerator/denominator hoặc isolate-level pattern khi có thể.
- Với WGS, giữ SNP range/cluster/clade/ST/accession/AMR determinant/virulence/plasmid theo mức chi tiết nguồn cho phép.
- Với review/meta-analysis, giữ số record/study, pooled estimate + 95% CI, heterogeneity, subgroup chính, sensitivity/publication-bias results.
- Tách rõ **author-reported** và **MRLUAN-recalculated**.

## Phản biện khoa học

Không viết giới hạn chung chung. Mỗi nhận định phải nối vào một chi tiết cụ thể của nguồn. Các lỗi thường phải kiểm tra:

- selection bias / convenience or referral sampling;
- denominator thay đổi giữa abstract, text và table;
- sample, isolate và genome bị dùng lẫn nhau;
- không có comparator hoặc reference group phù hợp;
- phenotype ↔ genotype không đồng nghĩa tuyệt đối;
- gene presence không chứng minh expression/virulence;
- phylogenetic closeness không chứng minh direct transmission;
- time-scaled phylogeny phụ thuộc molecular-clock rate và sampling dates;
- multiple observations trên cùng unit nhưng bị diễn giải như độc lập;
- meta-analysis heterogeneity cao nhưng pooled estimate bị đọc như một prevalence chung;
- breakpoint/database/tool version không rõ hoặc không còn tái lập được.

## Trạng thái

`draft`: đang viết, còn bất nhất, thiếu supplement/raw data quan trọng, hoặc có kết quả trọng yếu chưa xác minh/tái tính. `checked`: đã đối chiếu nguồn và kiểm tra các thông tin trung tâm **trong phạm vi đọc được khai báo**. `checked` không có nghĩa peer review độc lập và script không tự nâng trạng thái.

Nếu phát hiện bất nhất khoa học, ưu tiên **giữ draft và giải thích** hơn là làm đẹp trạng thái.

## Kiểm tra bằng script

`notes.py check` chỉ là QC cấu trúc. Nó phải cảnh báo các note `full_text` quá ngắn, mục 3–4 quá mỏng, thiếu bảng dữ liệu hoặc còn placeholder. Cảnh báo script không thay thế appraisal khoa học; ngược lại, `0 warnings` cũng không chứng minh note đúng.

## Làm theo đợt

Với kho lớn, xử lý từng nguồn hoàn chỉnh rồi mới chuyển nguồn tiếp theo. Sau khoảng 10–20 nguồn, rà ngược 2–3 note với PDF để phát hiện lỗi lặp lại và cập nhật template/hướng dẫn. Không hy sinh chiều sâu để đạt số lượng.

## Lưu trữ

Kết quả ở `results/MD` và `results/PDF` trên Google Drive. Source PDF giữ nguyên. Mã nguồn, mẫu, hướng dẫn và cấu hình remote ở GitHub canonical. GitHub không chứa corpus MD/PDF; Drive không là canonical source-code repository.
