@echo off
chcp 65001 >nul
title Game Thắm & Thơ Đi Học Về (Bản Web)
cd /d "C:\Users\Admin\.gemini\antigravity\scratch\tham_va_tho_di_hoc_ve"

echo =======================================================
echo    ĐANG KHỞI ĐỘNG GAME THẮM & THƠ (PHIÊN BẢN WEB)
echo =======================================================
echo Đang mở trình duyệt web...

start "" "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" app.py
timeout /t 2 /nobreak >nul
start http://localhost:5000

echo.
echo Nếu trình duyệt báo lỗi kết nối, bạn hãy bấm vào cửa sổ trình duyệt và bấm F5 để tải lại nhé!
echo (Đừng tắt cửa sổ này khi đang chơi game)
echo.
pause
