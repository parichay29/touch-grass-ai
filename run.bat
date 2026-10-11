# Touch Grass AI - Quick Start
# Double-click this file to run!

@echo off
chcp 65001 >nul 2>&1
echo.
echo  Touch Grass AI - Open-source Garden Planner
echo  ============================================
echo.

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  ERROR: Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

echo  Checking dependencies...
python -c "import llama_cpp" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo  Running garden planner for ZIP 97202 (Portland, OR)...
echo  Use --zip YOUR_ZIP to change location.
echo.
python garden_planner.py --zip 97202 --calendar

echo.
echo  --- Try these commands ---
echo  python garden_planner.py --zip 97202 --plant tomatoes
echo  python garden_planner.py --zip 97202 --ask "companion for garlic"
echo  python garden_planner.py --zip 97202 --list --nitrogen
echo  python garden_planner.py --zip 97202 --chat
echo.
pause