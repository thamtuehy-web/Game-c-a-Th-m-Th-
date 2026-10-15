# 🚀 Hướng Dẫn Đưa Game "Thắm & Thơ Đi Học Về" Lên Cloud (Render.com) & Chơi Full Màn Hình iPhone / iPad

Game đã được tối ưu hóa toàn diện thành phiên bản **Web App HTML5/Python Full Màn Hình & Xoay Ngang Tự Động**, sẵn sàng triển khai lên **Render.com** để các bé có thể chơi mượt mà trên iPhone, iPad, máy tính bảng hay laptop mà không cần cài đặt bất cứ phần mềm nào.

---

## 📱 Trải Nghiệm Full Màn Hình & Xoay Ngang Trên iPhone / iPad

1. **Tự động thích ứng & phóng to hết cỡ (Edge-to-Edge)**:
   - Trò chơi tự động đo kích thước màn hình thiết bị và phóng to toàn diện, không còn bị giới hạn tỷ lệ cũ.
2. **Hướng dẫn xoay ngang thông minh**:
   - Khi cầm máy dọc, màn hình sẽ hiển thị hướng dẫn xoay ngang trực quan kèm hoạt ảnh dễ thương để bé xoay ngang máy.
   - Nếu máy bật khóa xoay (Orientation Lock), bé có thể nhấn nút *"Tiếp tục chơi dọc"* để chơi ngay.
3. **Nút "Phóng To" (Toàn Màn Hình)**:
   - Bấm nút **⛶ Phóng To** ở góc trên bên phải để vào chế độ toàn màn hình (Hỗ trợ iPad, máy tính Windows, Mac, điện thoại Android).
4. **Mẹo chơi 100% không viền (Full viền như App thật) trên iPhone**:
   - Mở link game trên Safari iPhone.
   - Nhấn nút **Chia sẻ** (biểu tượng ô vuông mũi tên chỉ lên `⎋` ở thanh dưới cùng Safari).
   - Chọn **"Thêm vào Màn hình chính" (Add to Home Screen)** ➔ Nhấn **Thêm**.
   - Biểu tượng game hình bé Thắm sẽ xuất hiện trên màn hình iPhone. Khi mở lên, game sẽ chạy **100% toàn màn hình tràn viền**, ẩn hoàn toàn thanh địa chỉ của trình duyệt!

---

## 🌟 2 Cách Triển Khai / Cập Nhật Lên Render.com (Miễn Phí 100%)

File zip trọn gói mới nhất đã được tạo sẵn tại Desktop:
📂 `C:\Users\Admin\Desktop\tham_va_tho_game_render.zip`

### CÁCH 1: Triển Khai Dạng Web Service (Khuyên Dùng)

Dự án đã có sẵn các file cấu hình chuẩn của Render:
- `app.py`: Web server Flask tối ưu hóa tốc độ cao, hỗ trợ tự phục vụ file không sợ lỗi 404.
- `Procfile`: Lệnh khởi chạy server Gunicorn `web: gunicorn app:app --bind 0.0.0.0:$PORT`.
- `requirements.txt`: Chứa `flask` và `gunicorn`.
- `render.yaml`: Blueprint cấu hình tự động.

#### Các bước thực hiện:
1. **Đưa mã nguồn lên GitHub**:
   - Giải nén `tham_va_tho_game_render.zip` trên Desktop.
   - Tải các file lên repository trên [GitHub.com](https://github.com) (ví dụ: `tham-va-tho-game`).
   *(Nếu đã có repo từ trước, chỉ cần tải đè các file mới lên và Commit)*.
2. **Đăng nhập vào Render.com**:
   - Truy cập [dashboard.render.com](https://dashboard.render.com) (đăng nhập bằng tài khoản GitHub).
3. **Tạo Web Service (hoặc bấm Manual Deploy nếu đã có Web Service)**:
   - Nếu tạo mới: Bấm **New +** ➔ Chọn **Web Service** ➔ Chọn repository GitHub `tham-va-tho-game` ➔ Bấm **Connect**.
   - Nếu đã có sẵn Web Service: Vào Service đó ➔ Bấm **Manual Deploy** ➔ Chọn **Deploy latest commit**.
4. **Cấu hình (Render thường tự động điền sẵn)**:
   - **Name**: `tham-va-tho-di-hoc-ve` (hoặc tên tùy thích).
   - **Language**: `Python 3`.
   - **Branch**: `main`.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: Chọn **Free**.
5. **Bấm "Deploy Web Service"**:
   - Render sẽ tự động dựng server và cung cấp đường dẫn công khai miễn phí dạng:
     `https://tham-va-tho-di-hoc-ve.onrender.com`
   - Gửi link này cho 2 bé hoặc người thân mở trên iPhone/iPad là chơi được ngay!

---

### CÁCH 2: Triển Khai Dạng Static Site (Siêu Nhanh & Mượt)

Thư mục `static` trong dự án chứa toàn bộ mã nguồn game HTML5 Canvas, âm thanh Web Audio và hình ảnh chân dung của 2 bé.

1. Tại Render Dashboard, bấm **New +** ➔ Chọn **Static Site**.
2. Chọn repository GitHub ➔ Bấm **Connect**.
3. Điền cấu hình:
   - **Publish directory**: `static`
4. Bấm **Create Static Site**.
   - Render sẽ triển khai toàn cầu qua mạng CDN siêu tốc trong vòng chưa đầy 30 giây!

---

## 💻 Cách Chơi Thử Phiên Bản Web Trực Tiếp Trên Máy Tính Của Bạn

Trước khi gửi link cho mọi người, bạn có thể kiểm tra trải nghiệm phiên bản web ngay trên máy tính của mình bằng cách:
1. Nhấp đúp vào file [`Choi_Game_Tren_Web.bat`](file:///C:/Users/Admin/Desktop/Choi_Game_Tren_Web.bat) ngay trên màn hình **Desktop**.
2. Trình duyệt web sẽ tự động mở trang `http://localhost:5000` với đầy đủ âm thanh, giọng nói "Yêu Thắm Thơ", nút Phóng To và xoay màn hình tự động!
