@echo off
echo ============================================================
echo Election Tracker Web Server
echo ============================================================
echo.
echo Starting web server on http://localhost:4000
echo Press Ctrl+C to stop the server
echo.
echo Opening browser...
start http://localhost:4000
echo.
python app.py
pause
