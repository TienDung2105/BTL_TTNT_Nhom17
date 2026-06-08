@echo off
title AI Image Retrieval BTL - Build Index
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

set PY_CMD=python
where python >nul 2>nul
if errorlevel 1 set PY_CMD=py

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    "%PY_CMD%" -m venv .venv
    call .venv\Scripts\activate.bat
)

set PY_CMD=%~dp0.venv\Scripts\python.exe

"%PY_CMD%" -m pip install -r requirements.txt

echo.
echo Dataset can dat:
echo   data\styles.csv
echo   data\images\*.jpg
echo.
echo Build nhanh 500 anh:
echo   "%PY_CMD%" -m backend.build_index --limit 500
echo.

"%PY_CMD%" -m backend.build_index

pause
