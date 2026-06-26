@echo off
REM Benefits Integrity Cloud — FWA Demo
REM Run this script from the repo root to start the demo server.

echo.
echo  Benefits Integrity Cloud ^ FWA Detection ^& Prevention Demo
echo  ===========================================================
echo  Starting server on http://localhost:8000
echo  Press Ctrl+C to stop.
echo.

if not exist ".venv\Scripts\python.exe" (
  echo  Creating virtual environment...
  python -m venv .venv
  .venv\Scripts\python.exe -m pip install -r app\requirements.txt --quiet
  echo  Dependencies installed.
  echo.
)

.venv\Scripts\uvicorn.exe app.main:app --port 8000 --reload
