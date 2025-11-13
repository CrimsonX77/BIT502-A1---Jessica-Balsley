@echo off
REM ============================================================================
REM Aurora Archive System Launcher (Windows)
REM Automated setup, dependency checking, and GUI launcher
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo    THE AURORA ARCHIVE - Extended Implementation Launcher
echo ============================================================
echo.

REM ============================================================================
REM STEP 1: Check Python Installation
REM ============================================================================

echo [1/7] Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found

REM Check if version is 3.10+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if !MAJOR! LSS 3 (
    echo [WARNING] Python 3.10+ recommended, found %PYTHON_VERSION%
    echo Some features may not work correctly
) else if !MAJOR! EQU 3 if !MINOR! LSS 10 (
    echo [WARNING] Python 3.10+ recommended, found %PYTHON_VERSION%
    echo Some features may not work correctly
)

echo.

REM ============================================================================
REM STEP 2: Check/Create Virtual Environment
REM ============================================================================

echo [2/7] Checking virtual environment...

if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        echo.
        echo Try installing it with: python -m pip install virtualenv
        echo.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

echo.

REM ============================================================================
REM STEP 3: Activate Virtual Environment
REM ============================================================================

echo [3/7] Activating virtual environment...

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment activation script not found
    echo Recreating virtual environment...
    rmdir /s /q venv
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.

REM ============================================================================
REM STEP 4: Install/Update Dependencies
REM ============================================================================

echo [4/7] Checking dependencies...

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [INFO] Creating requirements.txt...
    (
        echo PyQt6^>=6.4.0
        echo cryptography^>=41.0.0
        echo Pillow^>=10.0.0
        echo requests^>=2.31.0
        echo numpy^>=1.24.0
    ) > requirements.txt
    echo [OK] requirements.txt created
)

echo [INFO] Installing/updating dependencies...
echo This may take a few minutes on first run...
echo.

python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo [WARNING] Could not upgrade pip
)

python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo.
    echo Please check your internet connection and try again
    echo Or manually install with: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [OK] All dependencies installed

echo.

REM ============================================================================
REM STEP 5: Check for Stable Diffusion (Optional)
REM ============================================================================

echo [5/7] Checking for Stable Diffusion...

curl -s http://localhost:7860/sdapi/v1/sd-models >nul 2>&1
if errorlevel 1 (
    echo [INFO] Stable Diffusion WebUI not detected (optional)
    echo [INFO] Card generation will use fallback methods
    set SD_AVAILABLE=false
) else (
    echo [OK] Stable Diffusion WebUI detected at localhost:7860
    set SD_AVAILABLE=true
)

echo.

REM ============================================================================
REM STEP 6: Create Config Directory
REM ============================================================================

echo [6/7] Setting up configuration...

if not exist "config" (
    mkdir config
    echo [OK] Config directory created
) else (
    echo [OK] Config directory exists
)

REM Create sample data directories
if not exist "data" mkdir data
if not exist "data\cards" mkdir data\cards
if not exist "data\members" mkdir data\members

echo [OK] Data directories ready

echo.

REM ============================================================================
REM STEP 7: Launch Applications
REM ============================================================================

echo [7/7] Launching Aurora Archive System...
echo.
echo ============================================================
echo.

REM Give user a moment to read
timeout /t 2 /nobreak >nul

echo Starting applications in sequence...
echo.
echo [INFO] Close each window when you're done exploring
echo [INFO] Press Ctrl+C at any time to stop all launches
echo.

REM ============================================================================
REM Launch Sequence
REM ============================================================================

REM Check if Python files exist
set ERROR_COUNT=0

if not exist "archive_sanctum.py" (
    echo [WARNING] archive_sanctum.py not found - skipping
    set /a ERROR_COUNT+=1
) else (
    echo [1/4] Launching Archive Sanctum ^(Member Portal^)...
    start "Aurora - Archive Sanctum" python archive_sanctum.py
    timeout /t 2 /nobreak >nul
)

if not exist "aurora_pyqt6_main.py" (
    echo [WARNING] aurora_pyqt6_main.py not found - skipping
    set /a ERROR_COUNT+=1
) else (
    echo [2/4] Launching Aurora Card Generator...
    start "Aurora - Card Generator" python aurora_pyqt6_main.py
    timeout /t 2 /nobreak >nul
)

if not exist "member_registration_app.py" (
    echo [WARNING] member_registration_app.py not found - skipping
    set /a ERROR_COUNT+=1
) else (
    echo [3/4] Launching Member Registration...
    start "Aurora - Registration" python member_registration_app.py
    timeout /t 2 /nobreak >nul
)

if not exist "obelisk_customs.py" (
    echo [WARNING] obelisk_customs.py not found - skipping
    set /a ERROR_COUNT+=1
) else (
    echo [4/4] Launching Obelisk Authentication...
    start "Aurora - Obelisk" python obelisk_customs.py
    timeout /t 2 /nobreak >nul
)

echo.
echo ============================================================

if !ERROR_COUNT! GTR 0 (
    echo.
    echo [WARNING] Some components could not be launched
    echo [INFO] !ERROR_COUNT! file^(s^) missing
    echo.
    echo This is normal if you only have the core assignment file.
    echo The extended implementation requires all Python files.
)

echo.
echo ============================================================
echo     All available applications have been launched!
echo ============================================================
echo.
echo GUI windows should now be open. Explore the system features:
echo   - Archive Sanctum: Member portal with dashboard
echo   - Card Generator: AI-powered card creation
echo   - Registration: New member signup workflow  
echo   - Obelisk: Authentication gateway
echo.
echo Close this window when you're done, or keep it open
echo to see any error messages from the applications.
echo.
echo ============================================================

REM Keep window open to catch any errors
pause

REM Deactivate virtual environment on exit
deactivate

exit /b 0
