@echo off
title URSUS AI - Trening modelu YOLO (RTX 4070 Ti)
cd /d "%~dp0"
echo ========================================================
echo   Uruchamianie treningu wlasnego modelu (NVIDIA CUDA)
echo ========================================================
echo.
.venv\Scripts\python.exe train_custom.py
echo.
pause
