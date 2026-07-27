@echo off
echo ================================================================================
echo    MODEL ACCURACY TESTING
echo ================================================================================
echo.
echo Testing your current model's accuracy...
echo.

python test_model_accuracy.py

echo.
echo ================================================================================
echo    TESTING COMPLETE!
echo ================================================================================
echo.
echo Check the files created:
echo   - models/accuracy_report.txt
echo   - models/predictions_comparison.csv
echo.
echo Press any key to close...
pause >nul
