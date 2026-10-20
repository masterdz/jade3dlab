@echo off
cd /d "%~dp0"

if exist "%~dp0jaded-src\runtime\Jaded.exe" (
    cd /d "%~dp0jaded-src\runtime"
) else if exist "%~dp0jaded-src\Jaded.exe" (
    cd /d "%~dp0jaded-src"
)

if not exist "SDL3.dll" (
    echo [ERROR] SDL3.dll not found in %CD%
    pause
    exit /b 1
)

set BF_FILE=prince3_dev.bf
if not "%~1"=="" set BF_FILE=%~1

echo ===================================================
echo   Jade Engine Editor Launcher (Prince of Persia)
echo ===================================================
echo Project BigFile : %BF_FILE%
echo Working Dir     : %CD%
echo.

start "" "Jaded.exe" /editor /console /bf "%BF_FILE%"
