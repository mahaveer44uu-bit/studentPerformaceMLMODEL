@echo off
echo ================================================================================
echo    TRAINING BEST MODEL WITH 5000 ROWS
echo ================================================================================
echo.

REM Create dataset folder if it doesn't exist
if not exist "dataset" mkdir dataset
if not exist "models" mkdir models

echo Running training script...
echo.

python train_best_model.py

echo.
echo ================================================================================
echo    TRAINING COMPLETE!
echo ================================================================================
echo.
echo Press any key to close...
pause >nul
