@echo off
title AI Image Retrieval BTL - Backend
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

set PY_CMD=python
where python >nul 2>nul
if errorlevel 1 set PY_CMD=py

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [INFO] Tao .venv moi...
    "%PY_CMD%" -m venv .venv
    call .venv\Scripts\activate.bat
)

set PY_CMD=%~dp0.venv\Scripts\python.exe

echo [INFO] Cai dependencies neu thieu...
"%PY_CMD%" -m pip install -r requirements.txt

echo.
echo [INFO] Chay backend va frontend tai:
echo   http://127.0.0.1:8000/
echo.

"%PY_CMD%" -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

pause
