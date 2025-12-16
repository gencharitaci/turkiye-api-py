@echo off
REM Sync app/data folder from turkiye-api repository
REM Usage: sync-data.bat

setlocal EnableDelayedExpansion

set UPSTREAM_REPO=https://github.com/ubeydeozdmr/turkiye-api.git
set DATA_DIR=app\data
set TEMP_DIR=temp\turkiye-api-sync

echo.
echo ========================================
echo   Syncing Data from turkiye-api
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    exit /b 1
)

REM Create temp directory
if not exist "temp" mkdir temp

REM Clone or update the upstream repository
if exist "%TEMP_DIR%\.git" (
    echo [*] Updating existing clone...
    cd "%TEMP_DIR%"
    git fetch origin
    git reset --hard origin/main
    cd ..\..
) else (
    echo [*] Cloning turkiye-api repository...
    git clone "%UPSTREAM_REPO%" "%TEMP_DIR%"
)

REM Check for changes (simple check - compare file count)
set OLD_COUNT=0
set NEW_COUNT=0

for /f %%i in ('dir /b /a-d "%DATA_DIR%\*.json" 2^>nul ^| find /c /v ""') do set OLD_COUNT=%%i
for /f %%i in ('dir /b /a-d "%TEMP_DIR%\src\data\*.json" 2^>nul ^| find /c /v ""') do set NEW_COUNT=%%i

echo [INFO] Current data files: %OLD_COUNT%
echo [INFO] Upstream data files: %NEW_COUNT%

REM Backup current data
if exist "%DATA_DIR%" (
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set BACKUP_DATE=%%c%%b%%a
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set BACKUP_TIME=%%a%%b
    set BACKUP_TIME=!BACKUP_TIME: =0!
    set BACKUP_DIR=temp\data-backup-!BACKUP_DATE!-!BACKUP_TIME!

    echo [*] Backing up current data to !BACKUP_DIR!
    mkdir "!BACKUP_DIR!" 2>nul
    xcopy /E /I /Y "%DATA_DIR%" "!BACKUP_DIR!\data" >nul
)

REM Remove old data
echo [*] Removing old data files...
if exist "%DATA_DIR%" (
    del /Q "%DATA_DIR%\*.json" 2>nul
)

REM Create data directory if it doesn't exist
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

REM Copy new data files
echo [*] Copying new data files...
xcopy /Y "%TEMP_DIR%\src\data\*.json" "%DATA_DIR%\" >nul 2>nul

if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Data files updated successfully!
) else (
    echo [ERROR] Failed to copy data files!
    exit /b 1
)

REM List updated files
echo.
echo [INFO] Updated data files:
dir /b "%DATA_DIR%\*.json"

REM Validate JSON files
echo.
echo [*] Validating JSON files...
set VALIDATION_FAILED=0

for %%f in ("%DATA_DIR%\*.json") do (
    echo   Checking %%~nxf...
    python -m json.tool "%%f" >nul 2>nul
    if !ERRORLEVEL! equ 0 (
        echo   [OK] %%~nxf - Valid JSON
    ) else (
        echo   [ERROR] %%~nxf - Invalid JSON!
        set VALIDATION_FAILED=1
    )
)

echo.
if !VALIDATION_FAILED! equ 1 (
    echo [WARNING] Some JSON files failed validation!
    echo   You may need to restore from backup: !BACKUP_DIR!
) else (
    echo [SUCCESS] All JSON files validated successfully!
)

echo.
echo [SUCCESS] Data sync completed!
echo.

endlocal
