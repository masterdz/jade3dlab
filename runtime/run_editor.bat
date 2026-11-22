@echo off
cd /d "%~dp0"

if not exist "%~dp0SDL3.dll" (
    echo [ERROR] SDL3.dll not found in %~dp0
    pause
    exit /b 1
)

set BF_FILE=prince3_dev.bf
if not "%~1"=="" set BF_FILE=%~1

echo ===================================================
echo   Jade Engine Editor Launcher (Prince of Persia)
echo ===================================================
echo Project BigFile : %BF_FILE%
echo Working Dir     : %~dp0
echo.

start "" "%~dp0Jaded.exe" /editor /console /bf "%BF_FILE%"