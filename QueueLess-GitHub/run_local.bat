@echo off
setlocal
cd /d %~dp0

echo ================================================
echo QueueLess - Local Windows Launcher
echo ================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set PYTHON_CMD=py
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON_CMD=python
    ) else (
        echo ERROR: Python was not found.
        echo Install Python 3.11 or newer from python.org.
        echo During installation, tick "Add Python to PATH".
        pause
        exit /b 1
    )
)

if not exist .venv (
    echo [1/4] Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
)

echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/4] Installing required Python packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Package installation failed.
    echo Check that the laptop has an internet connection, then run this file again.
    pause
    exit /b 1
)

echo [4/4] Initializing QueueLess demo database...
python seed.py
if errorlevel 1 (
    echo.
    echo ERROR: Database initialization failed.
    pause
    exit /b 1
)

echo.
echo QueueLess is starting at http://127.0.0.1:5000
echo.
echo CUSTOMER
echo Email: customer@queueless.local
echo Password: Demo123!
echo.
echo ADMIN
echo Email: admin@queueless.local
echo Password: Admin123!
echo.
echo Keep this window open while using QueueLess.
echo Press CTRL+C here to stop the server.
echo.

start "" /b python open_browser.py
python run.py

endlocal
