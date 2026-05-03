@echo off
echo ==========================================
echo  BUILDING FISHING BOT EXECUTABLE
echo ==========================================
echo.

echo [1/4] Installing/updating dependencies...
pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install dependencies
    pause
    exit /b 1
)

echo [2/4] Installing PyInstaller...
pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ERROR: Could not install PyInstaller
    pause
    exit /b 1
)

echo [3/4] Cleaning previous builds...
if exist build rmdir /s /q build
if exist FishBot.exe del FishBot.exe
if exist FishBot.spec del FishBot.spec

echo [4/4] Creating executable...
python -m PyInstaller --onefile --windowed ^
    --name "FishBot" ^
    --distpath . ^
    --hidden-import pygetwindow ^
    --hidden-import psutil ^
    --hidden-import pynput.keyboard._win32 ^
    --hidden-import pynput.mouse._win32 ^
    --collect-all pygetwindow ^
    fishing_bot.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create executable
    echo Check error messages above
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  EXECUTABLE CREATED SUCCESSFULLY
echo ==========================================
echo.
echo Location: FishBot.exe
echo.
echo IMPORTANT: If antivirus blocks the exe,
echo add an exception for this folder.
echo.
pause
