@echo off
title VOLT CARD STUDIO
cd /d "%~dp0"
echo ============================================================
echo   VOLT CARD STUDIO - Interactive Card & Template Editor
echo ============================================================
echo.
echo Starting Studio server on http://localhost:5050 ...
echo Opening your browser in 2 seconds...
start "" "http://localhost:5050"
python studio/server.py
pause
