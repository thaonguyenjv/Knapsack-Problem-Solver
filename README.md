## 🪄 Giới thiệu
Đây là đồ án môn **Trí tuệ Nhân tạo**, với mục tiêu giải quyết bài toán **Knapsack Problem** bằng hai phương pháp tối ưu hóa hiện đại:

- 🧬 **Genetic Algorithm (GA)** – Giải thuật di truyền  
- 🐋 **Whale Optimization Algorithm (WOA)** – Thuật toán tối ưu hóa cá voi  

Ứng dụng cung cấp **giao diện trực quan** bằng **Tkinter**, hỗ trợ:
- Nhập tham số và cấu hình cho GA/WOA  
- Hiển thị nghiệm tối ưu và biểu đồ hội tụ  
- So sánh hiệu năng giữa GA và WOA  
- Tùy chỉnh dữ liệu, hiển thị biểu đồ và kết quả thống kê  

---

## 🚚 Bài toán thực tế: Hệ thống tối ưu vận tải
Giả định công ty vận tải có xe tải với giới hạn khối lượng tối đa **M**, và **n kiện hàng** (mỗi kiện có trọng lượng và giá trị khác nhau).  
Mục tiêu:  
> Chọn tập hợp kiện hàng sao cho **tổng trọng lượng ≤ M** và **tổng giá trị lớn nhất**.

Ứng dụng so sánh khả năng tối ưu của **GA** và **WOA** trong hai tình huống thực tế
- Th1: Khi số lượng đơn hàng thay đổi 
- Th2: Khi sức chứa xe thay đổi 

---
## ⚙️ Yêu cầu hệ thống
- Python ≥ 3.8  
- Thư viện:
  ```bash
  pip install numpy matplotlib tkinter
## 🚀 Chạy chương trình
- ```bash
  python gui_main.py
---

## 🧩 Hai tình huống Benchmark

### 🧱 Tình huống 1: **Quản lý đơn hàng** (Thay đổi số lượng kiện)
**Mục tiêu:** Đánh giá khả năng mở rộng (scalability) của thuật toán.  

Các kịch bản:
- 100 kiện → Đơn hàng cuối tuần (ít hàng)  
- 500 kiện → Ngày thường (vừa phải)  
- 1000 kiện → Cao điểm (nhiều hàng)  

**Câu hỏi:** Thuật toán nào duy trì hiệu năng khi quy mô tăng?

**Thiết lập**
- Số đơn hàng: Thay đổi (100 → 500 → 1000)
- Sức chứa xe = 50% tổng trọng lượng các kiện trong phạm vi chọn
    Ví dụ: 100 kiện = 10 tấn → xe chở tối đa 5 tấn

**Tính năng:**
- Chọn và tải file dữ liệu (`100/500/1000 kiện`)  
- Thêm / Sửa / Xóa kiện hàng trong danh sách  
- Chạy benchmark trên phạm vi chọn (vd: 0–100, 100–200, ...)  
- Thiết lập số lần chạy để lấy kết quả trung bình  
- Hiển thị kết quả: Giá trị trung bình, Thời gian, Tốc độ hội tụ, Thuật toán thắng  
- Biểu đồ trực quan: So sánh giá trị, thời gian và đường hội tụ  

---

### 🚗 Tình huống 2: **Thay đổi sức chứa**
**Mục tiêu:** Đánh giá khả năng thích ứng của thuật toán với các ràng buộc khác nhau.

Các kịch bản:
- **30% tổng trọng lượng** → vận chuyển nội thành
- **50% tổng trọng lượng** → vận chuyển liên tỉnh
- **70% tổng trọng lượng** → vận chuyển đường dài

**Câu hỏi:** Thuật toán nào linh hoạt hơn khi thay đổi điều kiện tải trọng?

**Thiết lập**
-Số đơn hàng:Giữ nguyên (vd: 1000 kiện)
-Sức chứa xe: Thay đổi theo % người nhập
 
**Tính năng:**
- Chọn file dữ liệu (`100/500/1000 kiện`)  
- Tùy chỉnh tỷ lệ sức chứa (vd: `30,50,70` hoặc `40,60,80`)  
- Thiết lập số lần chạy  
- So sánh kết quả giữa các loại xe  
- Biểu đồ tổng hợp thể hiện hiệu năng trên từng loại xe  
---
## Chi tiết chạy Benchmark

### 🔹 Tình huống 1 – So sánh theo **Quy mô**
1. Mở tab **“QUẢN LÝ ĐƠN HÀNG”**  
2. Chọn file dữ liệu (`100/500/1000`)  
3. Nhấn **“Tải dữ liệu”** để load dữ liệu  
4. (Tùy chọn) Thêm / Sửa / Xóa kiện hàng  
5. Chọn phạm vi chạy (vd: `0–100`)  
6. Đặt số lần chạy (khuyến nghị: `5`)  
7. Nhấn **“▶ CHẠY”**  
8. Xem kết quả và biểu đồ so sánh  

### 🔹 Tình huống 2 – So sánh theo **Loại xe**
1. Mở tab **“LỰA CHỌN LOẠI XE”**  
2. Chọn file dữ liệu (`100/500/1000`)  
3. Nhập tỷ lệ xe muốn test (vd: `30,50,70`)  
4. Đặt số lần chạy (vd: `5`)  
5. Nhấn **“▶ CHẠY”**  
6. Quan sát bảng kết quả và biểu đồ hiệu năng từng loại xe  

---
## 📊 Kết quả minh họa
- GA: Tốc độ hội tụ nhanh hơn ở quy mô nhỏ, nhưng thời gian tăng mạnh khi dữ liệu lớn
- WOA: Tối ưu ổn định, hiệu quả hơn khi số lượng kiện lớn hoặc giới hạn tải thay đổi.

