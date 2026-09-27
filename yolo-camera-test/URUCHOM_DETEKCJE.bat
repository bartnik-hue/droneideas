@echo off
title URSUS AI - Detekcja YOLO na zywo
cd /d "%~dp0"
echo ========================================================
echo   Uruchamianie detekcji obiektow YOLO (NVIDIA CUDA)
echo ========================================================
echo.
.venv\Scripts\python.exe detect_yolo.py
if errorlevel 1 (
    echo.
    echo Wystapil blad podczas uruchamiania.
    pause
)
