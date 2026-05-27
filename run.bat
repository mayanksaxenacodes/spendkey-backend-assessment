@echo off
title Bookstore API Server
echo ===================================================
echo   Starting Bookstore API Server on Port 8000...
echo ===================================================

set PYTHONUNBUFFERED=TRUE
set CORS_ORIGINS=http://localhost:3000
set DATABASE_URI=postgresql://postgres:postgres@127.0.0.1:5432/spendkey
set ENABLE_OPENAPI_DOCS=true
set OPENAI_KEY=dummy-key

.\venv\Scripts\python.exe -m uvicorn --factory app.server.factory:create_app --port 8000

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] The server exited with code %ERRORLEVEL%.
)
pause
