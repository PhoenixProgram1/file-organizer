@echo off
cd /d "%~dp0"
title File Organizer - Setup
color 0A

echo.
echo  +----------------------------------+
echo  |     File Organizer  v1.0.0       |
echo  |       Installing deps...         |
echo  +----------------------------------+
echo.

py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON=py
    goto :install
)

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON=python
    goto :install
)

echo  [ERROR] Python not found in PATH.
echo  Install from https://python.org and check "Add to PATH" during install.
pause
exit /b 1

:install
echo  [*] Python found. Using: %PYTHON%
echo  [*] Installing requirements...
%PYTHON% -m pip install --upgrade pip --quiet
%PYTHON% -m pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo  [OK] All dependencies installed!
    echo.
    echo  Usage:
    echo    python file_organizer.py run "C:\Users\You\Downloads"
    echo    python file_organizer.py run "C:\Users\You\Downloads" --dry-run
    echo    python file_organizer.py undo undo_20240101_120000.log
    echo.
) else (
    echo.
    echo  [ERROR] pip install failed. See output above.
    echo.
)

pause
