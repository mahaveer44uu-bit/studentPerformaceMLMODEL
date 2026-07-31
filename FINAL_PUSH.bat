@echo off
cls
echo.
echo ========================================
echo    FINAL DEPLOYMENT FIX
echo ========================================
echo.
echo Pushing to GitHub...
echo.

git add .
git commit -m "Final fix: Python 3.10 + compatible packages"
git push origin main

echo.
echo ========================================
echo    SUCCESS! 
echo    Wait 5-10 minutes for Render
echo ========================================
echo.
pause
