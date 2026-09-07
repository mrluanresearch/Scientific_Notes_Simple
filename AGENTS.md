# Viết source note: nội dung là sản phẩm

Đọc README.md và NOTE_TEMPLATE.md; xem examples/SAL-0001.md để hiểu độ cụ thể cần đạt. **Vai trò thực thi canonical là MRLUAN**; khi ghi người thực hiện/soát note, dùng MRLUAN hoặc tên người soát cụ thể. Dự án phục vụ Salmonella–AMR–WGS–One Health; ngữ cảnh luận án chưa xác minh không được coi là thực tế đã thực hiện.

## Nhiệm vụ

Đọc tài liệu người dùng cung cấp và viết một Markdown tiếng Việt đủ để hiểu, đánh giá và dùng lại các kết quả quan trọng. Giữ đúng tám mục của NOTE_TEMPLATE.md. Sáu trường YAML chỉ để định danh/tìm kiếm/theo dõi; toàn bộ nội dung khoa học nằm trong thân MD.

## Quy trình cho từng tài liệu

1. Tra ID/DOI/tiêu đề trong kho để tránh ghi hai note cho cùng tài liệu. Tạo khung khi cần; không chép metadata của bài mẫu sang bài mới.
2. Đọc phương pháp, kết quả, bảng/hình và phần bàn luận liên quan. Xem trực quan khi trích text làm mất cấu trúc bảng. Chỉ ghi đã đọc phạm vi thực sự có.
3. Viết mục 3–4 trước: thiết kế, dữ liệu, kết quả, mẫu số, đơn vị, vị trí nguồn, dữ liệu thiếu. Trích các hàng/cột cần dùng ngay vào Markdown.
4. Từ bằng chứng đó viết câu hỏi/đóng góp, phản biện, cách sử dụng và đoạn tổng hợp. Không điền tám mục bằng tám đoạn chung chung giống nhau.
5. Tự đọc lại note trong khi tạm đóng nguồn. Nếu thiếu thông tin để hiểu số liệu, giải thích giới hạn hoặc thực hiện phép tính cần dùng, bổ sung từ nguồn hoặc chỉ rõ điều nguồn không cung cấp.
6. Đối chiếu lại các kết quả trung tâm với nguồn; cộng tổng hàng/cột và tính lại tỷ lệ quan trọng. Nếu nguồn có bất nhất, giữ số gốc, ghi phép tính cho thấy chỗ lệch và giới hạn dùng lại; không tự sửa cho khớp. Chạy `check` nếu có Python để tìm lỗi hình thức; chỉ báo đúng việc đã kiểm tra.

## Chất lượng cần đạt

- Mục 3–4 và phần phản biện phải chiếm phần chính. Một abstract diễn đạt lại hoặc bảng gồm ba dòng không đủ cho một nghiên cứu nhiều kết quả.
- Bài thực nghiệm nhiều kết quả thường cần khoảng 1.500–2.500 từ tiếng Việt tính theo khoảng trắng, chưa kể bảng. Đây là gợi ý biên tập, không phải ngưỡng máy; độ dài phụ thuộc thông tin nguồn, không thêm chữ để đủ quota.
- Kết quả luôn đi cùng đối tượng, đơn vị/mẫu số, bất định nếu có, vị trí nguồn và điều kiện diễn giải. Giữ kết quả âm tính và bất đồng làm thay đổi kết luận.
- Thông số/phiên bản/tiêu chuẩn không được nguồn báo cáo thì ghi rõ. Không bịa, không tự thay bằng thông lệ hoặc bản mới nhất.
- Phân biệt kết quả nguồn, diễn giải tác giả và nhận định người đọc. Gene hiện diện không tự chứng minh kiểu hình; quan hệ hệ gen không tự chứng minh truyền trực tiếp; liên quan không tự chứng minh nhân quả.
- Không gán tỷ lệ của mẫu chọn lọc cho quần thể; không dùng nguồn bên ngoài như số liệu luận án. Những điểm không liên quan thì giải thích ngắn, không chèn cảnh báo hàng loạt.
- Nội dung định lượng có thể dùng bảng; phần phản biện và đoạn tổng hợp cần văn xuôi có lập luận. Không chỉ dẫn “xem PDF”, không giấu kết quả vào YAML, không đẻ Evidence ID/claim ledger/hash/điểm tự chấm.
- Giữ một bản ghi chú cho một tài liệu. Sửa trực tiếp note; ghi lý do sửa quan trọng bằng một dòng cuối mục 7 khi cần. Trích dẫn ở thân bài giữ tác giả/năm, không tạo engine citation.

## Trạng thái và hàng loạt

`draft`: đang viết hoặc còn điểm cần kiểm tra. `checked`: đã đối chiếu các thông tin trung tâm trong phạm vi đọc khai báo. Trường này do MRLUAN hoặc người thực sự soát ghi, script không tự nâng trạng thái. Người soát và giới hạn kiểm tra nằm ở mục 1, không ngụ ý kiểm định độc lập.

Thiếu toàn văn: dùng read_scope abstract/partial, giữ draft, nêu đúng phần đã có; không kéo dài thành giả phân tích toàn văn. Tám mục vẫn giữ nhưng phần chưa đọc phải được ghi là chưa có dữ liệu.

Với 1.000 tài liệu: dùng cùng mẫu, ID liên tục, 3–6 tag ổn định, xử lý từng nguồn một hoặc nhóm nhỏ để mỗi note có đủ lượt đọc và viết. Mỗi đợt khoảng 20 note xem lại 2–3 note đối chiếu với bài mẫu; sửa hướng dẫn chung chỉ khi thấy lỗi lặp lại. Không coi việc tạo 1.000 tệp hoặc check không báo lỗi là đã có 1.000 note đạt chất lượng.

## Lưu trữ

Kết quả ở results/MD và results/PDF; chỉ đồng bộ thư mục results lên Drive khi có yêu cầu và đích đã rõ. Source PDF giữ nguyên; không sinh bản PDF tóm tắt giả làm tài liệu nguồn. Mã nguồn, mẫu, hướng dẫn và cấu hình remote dùng GitHub canonical của project. Chỉ upload/push khi người dùng yêu cầu rõ; không xóa kho cũ hoặc dữ liệu ngoài phạm vi yêu cầu.
