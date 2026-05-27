@echo off
title Bookstore API Coverage Report
echo ===================================================
echo   Running Unit Tests & Gathering Code Coverage...
echo ===================================================
echo.

set PYTHONUNBUFFERED=TRUE

REM Execute the test suite under coverage tracking
.\venv\Scripts\python.exe -m coverage run --source app --module pytest -p no:warnings -vv tests/unit

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] The test suite failed with exit code %ERRORLEVEL%.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ===================================================
echo               CODE COVERAGE REPORT
echo ===================================================
echo.

REM Display the coverage report in the console
.\venv\Scripts\python.exe -m coverage report --show-missing --skip-empty

echo.
pause
