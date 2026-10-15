@echo off
chcp 65001 >nul
title Thắm ^& Thơ Đi Học Về - Game Cho Trẻ Em
echo ===================================================
echo     ĐANG KHỞI ĐỘNG GAME: THẮM & THƠ ĐI HỌC VỀ
echo ===================================================
cd /d "%~dp0"
"%LOCALAPPDATA%\Programs\Python\Python311\python.exe" game.py
if %ERRORLEVEL% NEQ 0 (
    python game.py
)
pause
