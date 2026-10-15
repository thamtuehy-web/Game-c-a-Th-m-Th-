# 🚀 Hướng Dẫn Đưa Game "Thắm & Thơ Đi Học Về" Lên Cloud (Render.com)

Game đã được chuyển đổi hoàn tất thành phiên bản **Web App HTML5/Python** chuẩn đám mây, sẵn sàng triển khai lên **Render.com** để bất kỳ ai mở link trên máy tính, iPad hay điện thoại đều có thể chơi ngay lập tức mà không cần cài đặt gì thêm.

---

## 🌟 2 Cách Triển Khai Lên Render.com (Miễn Phí 100%)

### CÁCH 1: Triển Khai Dạng Web Service (Khuyên Dùng)

Dự án đã có sẵn các file cấu hình chuẩn của Render:
- `app.py`: Web server Flask tối ưu hóa tốc độ cao.
- `Procfile`: Lệnh khởi chạy server Gunicorn `web: gunicorn app:app --bind 0.0.0.0:$PORT`.
- `requirements.txt`: Chứa `flask` và `gunicorn`.
- `render.yaml`: Blueprint cấu hình tự động.

#### Các bước thực hiện:
1. **Đưa mã nguồn lên GitHub**:
   - Tạo một repository mới trên [GitHub.com](https://github.com) (ví dụ đặt tên: `tham-va-tho-game`).
   - Tải toàn bộ thư mục dự án lên repository đó.
2. **Đăng nhập vào Render.com**:
   - Truy cập [dashboard.render.com](https://dashboard.render.com) (đăng nhập bằng tài khoản GitHub).
3. **Tạo Web Service**:
   - Bấm nút **New +** ở góc trên bên phải ➔ Chọn **Web Service**.
   - Chọn repository GitHub `tham-va-tho-game` bạn vừa tạo ➔ Bấm **Connect**.
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
   - Bạn có thể gửi link này cho bé hoặc gia đình chơi trực tiếp trên mọi thiết bị!

---

### CÁCH 2: Triển Khai Dạng Static Site (Cực Nhanh & Mượt)

Thư mục `static` trong dự án chứa toàn bộ mã nguồn game HTML5 Canvas, âm thanh Web Audio và hình ảnh chân dung của 2 bé.

1. Tại Render Dashboard, bấm **New +** ➔ Chọn **Static Site**.
2. Chọn repository GitHub ➔ Bấm **Connect**.
3. Điền cấu hình:
   - **Publish directory**: `static`
4. Bấm **Create Static Site**.
   - Render sẽ triển khai toàn cầu qua mạng CDN siêu tốc trong vòng chưa đầy 30 giây!

---

## 💻 Cách Chơi Thử Phiên Bản Web Trực Tiếp Trên Máy Tính Của Bạn

Trước khi đưa lên cloud, bạn có thể kiểm tra trải nghiệm phiên bản web ngay trên máy tính của mình bằng cách:
1. Nhấp đúp vào file [`Choi_Game_Tren_Web.bat`](file:///C:/Users/Admin/Desktop/Choi_Game_Tren_Web.bat) ngay trên màn hình **Desktop**.
2. Trình duyệt web sẽ tự động mở trang `http://localhost:5000` với đầy đủ âm thanh, giọng nói và đồ họa sống động!
