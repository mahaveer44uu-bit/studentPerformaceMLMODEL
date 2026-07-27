@echo off
echo ============================================================
echo Finding Your IP Address
echo ============================================================
echo.
echo Your computer's IP addresses:
echo.
ipconfig | findstr /i "IPv4"
echo.
echo ============================================================
echo Share this with your friend:
echo http://YOUR_IP_ADDRESS:5000
echo.
echo Example: http://192.168.1.5:5000
echo ============================================================
pause
