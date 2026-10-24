@echo off
setlocal
cd /d %~dp0

if exist instance\queueless.db (
    del /q instance\queueless.db
    echo Existing demo database removed.
)

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    python seed.py
    echo QueueLess demo database recreated.
) else (
    echo Run run_local.bat first so the virtual environment is created.
)

pause
endlocal
