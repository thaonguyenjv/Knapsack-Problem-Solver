# Knapsack Problem Solver: Genetic Algorithm & Whale Optimization Algorithm

## Giới thiệu
Đây là đồ án môn **Trí tuệ nhân tạo**, với mục tiêu giải quyết bài toán **Knapsack Problem** bằng hai phương pháp:
- **Giải thuật Di truyền (Genetic Algorithm - GA)**
- **Thuật toán Tối ưu hóa Cá voi (Whale Optimization Algorithm - WOA)**

Chương trình có giao diện trực quan bằng **Tkinter**, hỗ trợ:
- Nhập tham số cho GA/WOA
- Hiển thị kết quả nghiệm tốt nhất
- Vẽ biểu đồ hội tụ
- Animation quá trình tìm kiếm
- ...

#  HỆ THỐNG TỐI ƯU VẬN TẢI - SO SÁNH GA & WOA
Hệ thống so sánh hiệu năng của Genetic Algorithm (GA) và Whale Optimization Algorithm (WOA) trong bài toán Knapsack với ngữ cảnh thực tế:
Bài toán thực tế: Công ty vận tải có xe tải với giới hạn khối lượng chở tối đa M. Có n kiện hàng cần vận chuyển, mỗi kiện có trọng lượng và giá trị cước phí khác nhau. Công ty cần chọn những kiện hàng nào để:
Tổng khối lượng không vượt quá sức chứa xe
Tổng giá trị vận chuyển đạt cao nhất
## 2 TÌNH HUỐNG BENCHMARK
*Tình huống 1: QUẢN LÝ ĐƠN HÀNG (Thay đổi Số lượng Kiện)*
**Mục tiêu:** Đánh giá khả năng mở rộng (scalability) của thuật toán
- Công ty nhận các đơn hàng với số lượng kiện khác nhau:
   100 kiện: Đơn hàng cuối tuần (ít hàng)
   500 kiện: Đơn hàng ngày thường (vừa phải)
   1000 kiện: Đơn hàng cao điểm (nhiều hàng)
**Câu hỏi:** Thuật toán nào xử lý tốt hơn khi quy mô tăng?
**Tính năng:**
- Load file dữ liệu (100/500/1000 kiện)
- Thêm/Sửa/Xóa kiện hàng trong đơn
- Chọn phạm vi kiện hàng để chạy (ví dụ: từ kiện 0-50, 100-200...)
- Cấu hình số lần chạy để lấy kết quả trung bình
- Hiển thị kết quả: Giá trị, Thời gian, Tốc độ hội tụ, Thuật toán thắng
- Biểu đồ so sánh: Giá trị TB, Thời gian TB, Đường hội tụ

*Tình huống 2: LỰA CHỌN LOẠI XE (Thay đổi Sức chứa)*
**Mục tiêu:** Đánh giá khả năng thích ứng với ràng buộc
- Công ty có nhiều loại xe với sức chứa khác nhau:
   30% tổng trọng lượng: Xe nhỏ (vận chuyển nội thành)
   50% tổng trọng lượng: Xe vừa (vận chuyển liên tỉnh)
   70% tổng trọng lượng: Xe lớn (vận chuyển xa)
**Câu hỏi:** Thuật toán nào thích ứng tốt hơn với các ràng buộc khác nhau?
**Tính năng:**
- Chọn file dữ liệu (100/500/1000 kiện)
- Chọn loại xe muốn test: 30%, 50%, 70% hoặc cả 3 cùng lúc
- Tùy chỉnh tỷ lệ sức chứa (ví dụ: 30,50,70 hoặc 40,60,80...)
- Cấu hình số lần chạy
- So sánh kết quả giữa các loại xe
- Biểu đồ hiển thị hiệu năng trên xe đại diện 


## HƯỚNG DẪN SỬ DỤNG
*Tình huống 1: So sánh theo Quy mô*
- Chọn tab "TH1: QUẢN LÝ ĐƠN HÀNG"
- Chọn file data (100/500/1000)
- Nhấn "TẢI FILE" để load dữ liệu
- (Tùy chọn) Thêm/Sửa/Xóa kiện hàng
- Chọn phạm vi chạy (ví dụ: 0-100)
- Đặt số lần chạy (khuyến nghị: 5 lần)
- Nhấn "CHẠY BENCHMARK"
*Tình huống 2: So sánh theo Loại xe*
- Chọn tab "TH2: LỰA CHỌN LOẠI XE"
- Chọn file data
- Nhập tỷ lệ xe muốn test (ví dụ 30,50,70:test cả 3 loại xe hoặc chọn từng tỷ lễ để test từng loại)
- Đặt số lần chạy
- Nhấn "CHẠY BENCHMARK"
- Xem so sánh giữa các loại xe trong bảng kết quả


