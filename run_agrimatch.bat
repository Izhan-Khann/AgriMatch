
@echo off
title AgriMatch Launcher

cd /d "%~dp0"

echo Starting AgriMatch...
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Python virtual environment not found.
    echo Please check your .venv folder.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m streamlit run app.py --server.port 8503

pause
