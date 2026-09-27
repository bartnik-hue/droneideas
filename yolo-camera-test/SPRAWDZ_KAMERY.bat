@echo off
title URSUS AI - Skaner kamer
cd /d "%~dp0"
echo ========================================================
echo   Skanowanie indeksow kamer w systemie
echo ========================================================
echo.
.venv\Scripts\python.exe list_cameras.py
echo.
pause
