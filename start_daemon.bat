@echo off
title Volt Hybrid Daemon — Fast Reaction & Cloud Sync
cd /d "%~dp0"
echo ========================================================
echo   VOLT HYBRID AUTOMATION DAEMON (LOCAL + CLOUD)
echo ========================================================
echo   - Instant reaction to breaking news (every 3 minutes)
echo   - Automatic state sync with GitHub Actions
echo   - Renders cards with official Jozor templates
echo   - 100%% Free, 0 cost
echo ========================================================
python daemon.py 180
pause
