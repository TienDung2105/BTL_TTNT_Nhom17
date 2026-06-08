@echo off
title AI Image Retrieval BTL - Frontend
cd /d "%~dp0frontend"

set PY_CMD=python
where python >nul 2>nul
if errorlevel 1 set PY_CMD=py

echo [INFO] Chay frontend tinh tai:
echo   http://127.0.0.1:5173/
echo.
echo [INFO] Luu y: can chay backend bang run_backend.bat de API hoat dong.
echo.

"%PY_CMD%" -m http.server 5173 --bind 127.0.0.1

pause
