@echo off
echo ==========================================
echo  CREANDO BOT DE PESCA EJECUTABLE
echo ==========================================
echo.

echo [1/4] Instalando/actualizando dependencias...
pip install --upgrade -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar dependencias
    pause
    exit /b 1
)

echo [2/4] Instalando PyInstaller...
pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ERROR: No se pudo instalar PyInstaller
    pause
    exit /b 1
)

echo [3/4] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist FishBot.exe del FishBot.exe
if exist FishBot.spec del FishBot.spec

echo [4/4] Creando ejecutable...
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
    echo ERROR: Fallo al crear el ejecutable
    echo Revisa los mensajes de error arriba
    pause
    exit /b 1
)

echo.
echo ==========================================
echo  EJECUTABLE CREADO CORRECTAMENTE
echo ==========================================
echo.
echo Ubicacion: FishBot.exe
echo.
echo IMPORTANTE: Si el antivirus bloquea el exe,
echo agrega una excepcion para esta carpeta.
echo.
pause
