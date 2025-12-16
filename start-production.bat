@echo off
REM ========================================
REM Production startup script for Turkiye API v1.1.0
REM Usage: start-production.bat
REM ========================================

setlocal EnableDelayedExpansion

echo.
echo ========================================
echo   Turkiye API - Production Startup
echo   Version: 1.1.0
echo ========================================
echo.

REM Check for .env file
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo   For production, copy .env.production.recommended to .env
    echo   and configure all settings.
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo [ERROR] Startup cancelled.
        exit /b 1
    )
) else (
    echo [OK] Found .env file
)

REM Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo   Install Python from https://www.python.org/
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [WARNING] Virtual environment not found
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Gunicorn is installed
pip show gunicorn >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Gunicorn not found. Installing...
    pip install gunicorn
) else (
    echo [OK] Gunicorn is installed
)

REM Install/update dependencies
echo [INFO] Checking dependencies...
pip install -r requirements.txt --quiet

REM Security warnings
if exist ".env" (
    findstr /C:"HEALTH_CHECK_DETAILED=true" .env >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo [WARNING] HEALTH_CHECK_DETAILED=true in production
        echo   This exposes internal information. Set to 'false' for security.
    )

    findstr /C:"EXPOSE_SERVER_HEADER=true" .env >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        echo [WARNING] EXPOSE_SERVER_HEADER=true in production
        echo   This exposes technology stack. Set to 'false' for security.
    )
)

echo.
echo ========================================
echo   Starting Turkiye API...
echo ========================================
echo.
echo [INFO] Starting server with Gunicorn...
echo   Configuration: gunicorn.conf.py
echo.

REM Start the server
gunicorn -c gunicorn.conf.py app.main:app

endlocal
