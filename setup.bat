@echo off
REM Monero Mining - Quick Setup Script for Windows

echo ==============================================
echo   Monero Mining - Quick Windows Setup
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if wallet address is configured
findstr "YOUR_MONERO_WALLET_ADDRESS_HERE" main.py >nul
if not errorlevel 1 (
    echo [WARNING] Wallet address not configured!
    echo Please edit main.py and set your Monero wallet address
    echo.
    set /p WALLET_ADDR="Enter your Monero wallet address (or press Enter to skip): "
    
    if not "!WALLET_ADDR!"=="" (
        powershell -Command "(gc main.py) -replace 'YOUR_MONERO_WALLET_ADDRESS_HERE', '!WALLET_ADDR!' | Out-File -encoding ASCII main.py"
        echo [OK] Wallet address configured
    )
)

echo.
echo ==============================================
echo   Setup Options
echo ==============================================
echo 1. Run now
echo 2. Run in background (minimized)
echo 3. Create startup shortcut
echo 4. Exit
echo.
set /p OPTION="Choose option [1-4]: "

if "%OPTION%"=="1" (
    echo.
    echo Starting miner...
    echo Press Ctrl+C to stop
    echo.
    python main.py
) else if "%OPTION%"=="2" (
    echo.
    echo Starting miner in background...
    start /min "Monero Miner" python main.py
    echo [OK] Miner started in minimized window
    echo Check Task Manager to stop: "Monero Miner"
) else if "%OPTION%"=="3" (
    echo.
    echo Creating startup shortcut...
    set SCRIPT_PATH=%~dp0main.py
    set SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\MoneroMiner.bat
    
    echo @echo off > "%SHORTCUT_PATH%"
    echo cd /d "%~dp0" >> "%SHORTCUT_PATH%"
    echo start /min python main.py >> "%SHORTCUT_PATH%"
    
    echo [OK] Startup shortcut created
    echo Miner will start automatically on Windows login
    echo Location: %SHORTCUT_PATH%
) else if "%OPTION%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid option
    exit /b 1
)

echo.
echo ==============================================
echo   Setup Complete!
echo ==============================================
pause
