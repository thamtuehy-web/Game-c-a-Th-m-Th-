@echo off
chcp 65001 >nul
cd /d "C:\Users\Admin\.gemini\antigravity\scratch\tham_va_tho_di_hoc_ve"
start http://localhost:5000
start "" "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" app.py
exit
