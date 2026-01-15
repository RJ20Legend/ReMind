@echo off
REM Start the ReMind backend
REM This script should be run from anywhere

echo.
echo 🧠 ReMind Backend Startup
echo ========================================
echo.

cd /d E:\ReMind\backend

echo Checking setup...
python verify_setup.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Setup verification failed!
    echo Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup verified!
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API documentation at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app:app --reload

pause
