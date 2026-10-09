@echo off
setlocal enableextensions
title Project Setup - Install & Reset

REM ============================================================
REM  Windows setup batch file
REM  1. Find project base folder (folder containing manage.py)
REM  2. Create virtual environment (venv)
REM  3. Activate venv
REM  4. Install packages from require.txt
REM  5. Run python manage.py makemigrations / migrate
REM  6. Execute table_reset.txt commands in python manage.py shell
REM ============================================================

REM ---------- 1. Find the base folder (where manage.py lives) ----------
set "BASE=%~dp0"
if not exist "%BASE%manage.py" (
    echo [*] manage.py not next to this script, searching...
    for /f "delims=" %%f in ('dir /b /s "%BASE%manage.py" 2^>nul') do (
        set "BASE=%%~dpf"
        goto :found
    )
)
:found
if not exist "%BASE%manage.py" (
    echo [ERROR] Could not find manage.py under "%~dp0"
    goto :end
)
cd /d "%BASE%"
echo [*] Base folder: %CD%
echo.

REM ---------- 2. Create virtual environment ----------
if not exist "%BASE%venv\Scripts\python.exe" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create venv. Is Python on PATH?
        goto :end
    )
) else (
    echo [*] Virtual environment already exists.
)
echo.

REM ---------- 3. Activate virtual environment ----------
echo [*] Activating virtual environment...
call "%BASE%venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate venv.
    goto :end
)
echo.

REM ---------- 4. Install packages from require.txt ----------
if not exist "%BASE%require.txt" (
    echo [ERROR] require.txt not found.
    goto :end
)
echo [*] Upgrading pip...
python -m pip install --upgrade pip
echo [*] Installing packages from require.txt...
python -m pip install -r require.txt
if errorlevel 1 (
    echo [ERROR] Package installation failed.
    goto :end
)
echo.

REM ---------- 5. Run migrations ----------
echo [*] Running makemigrations...
python manage.py makemigrations
echo [*] Running migrate...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Migrations failed.
    goto :end
)
echo.

REM ---------- 6. Execute table_reset.txt commands in Django shell ----------
if not exist "%BASE%table_reset.txt" (
    echo [WARN] table_reset.txt not found, skipping table reset.
    goto :success
)
echo [*] Preparing table reset commands from table_reset.txt...
findstr /C:"from " /C:"EmpMast" /C:"EnrollMast" /C:"MonitorData" /C:"DepartMast" /C:"DesMast" /C:"ReportLog" /C:"with connection" /C:"cursor.execute" "%BASE%table_reset.txt" > "%TEMP%\table_reset_cmds.py"

echo [*] Executing table reset inside python manage.py shell...
python manage.py shell < "%TEMP%\table_reset_cmds.py"
if errorlevel 1 (
    echo [ERROR] Table reset failed.
    goto :end
)

:success
echo.
echo [OK] Setup completed successfully.
goto :end

:end
echo.
pause
endlocal
