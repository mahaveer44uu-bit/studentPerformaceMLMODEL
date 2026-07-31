@echo off
cls
echo.
echo ========================================
echo    CLEAN DEPLOYMENT - No Config Conflicts
echo ========================================
echo.
echo Removing render.yaml (using runtime.txt only)
echo Pushing clean configuration...
echo.

git add .
git commit -m "Remove render.yaml, use runtime.txt for Python 3.9"
git push origin main

echo.
echo ========================================
echo    PUSHED! Wait 5-10 minutes
echo    Manual Render config may be needed
echo ========================================
echo.
pause
