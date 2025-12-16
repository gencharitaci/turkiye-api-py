@echo off
REM Sync guides folder from turkiye-api-docs repository
REM Usage: sync-guides.bat

setlocal EnableDelayedExpansion

set UPSTREAM_REPO=https://github.com/ubeydeozdmr/turkiye-api-docs.git
set GUIDES_DIR=guides
set TEMP_DIR=temp\turkiye-api-docs-sync

echo.
echo ========================================
echo   Syncing Guides from turkiye-api-docs
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    exit /b 1
)

REM Create temp directory
if not exist "temp" mkdir temp
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Clone or update the upstream repository
if exist "%TEMP_DIR%\.git" (
    echo [*] Updating existing clone...
    cd "%TEMP_DIR%"
    git fetch origin
    git reset --hard origin/main
    cd ..\..
) else (
    echo [*] Cloning turkiye-api-docs repository...
    git clone "%UPSTREAM_REPO%" "%TEMP_DIR%"
)

REM Backup current guides
if exist "%GUIDES_DIR%" (
    for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set BACKUP_DATE=%%c%%b%%a
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set BACKUP_TIME=%%a%%b
    set BACKUP_DIR=temp\guides-backup-!BACKUP_DATE!-!BACKUP_TIME!
    echo [*] Backing up current guides to !BACKUP_DIR!
    xcopy /E /I /Y "%GUIDES_DIR%" "!BACKUP_DIR!" >nul
)

REM Remove old guides content
if exist "%GUIDES_DIR%" (
    echo [*] Removing old guides...
    rd /s /q "%GUIDES_DIR%" 2>nul
)

REM Create guides directory
mkdir "%GUIDES_DIR%"

REM Copy new guides (exclude .git directory)
echo [*] Copying new guides...
xcopy /E /I /Y /EXCLUDE:sync-guides-exclude.txt "%TEMP_DIR%\*" "%GUIDES_DIR%" >nul 2>nul
if not exist sync-guides-exclude.txt (
    echo .git> sync-guides-exclude.txt
    echo .github>> sync-guides-exclude.txt
    xcopy /E /I /Y "%TEMP_DIR%\*" "%GUIDES_DIR%" >nul
)

echo.
echo [SUCCESS] Guides updated successfully!
echo.
echo Run 'git status' to see changes in guides folder.
echo.

endlocal
