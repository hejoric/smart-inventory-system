@echo off
echo Starting Smart Inventory Backend Server...
echo ==========================================
cd backend

echo Creating virtual environment if not exists...
if not exist "venv" (
    echo Setting up Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting FastAPI server...
echo ==========================================
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
