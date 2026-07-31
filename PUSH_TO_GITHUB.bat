@echo off
echo ================================
echo   PUSHING TO GITHUB
echo ================================
echo.

git add requirements.txt runtime.txt
git commit -m "Fix Render build: Use Python 3.9 with scikit-learn 1.0.2"
git push origin main

echo.
echo ================================
echo   PUSH COMPLETE!
echo   Wait 5-10 min for Render
echo ================================
pause
