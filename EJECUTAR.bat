@echo off
title MVP Delivery - Servidor
echo.
echo ========================================
echo   MVP Delivery Local - Iniciando...
echo ========================================
echo.
cd /d "%~dp0"
set PYTHONPATH=%CD%\backend;%CD%

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: No se encontro Python. Instala Python y vuelve a intentar.
    pause
    exit /b 1
)

if not exist "data\orders.json" (
    echo Inicializando datos por primera vez...
    python backend\init_data.py
    echo.
)

echo.
echo Iniciando servidor en http://127.0.0.1:8000
echo.
echo Abre en el navegador:
echo   - Inicio:    http://127.0.0.1:8000
echo   - Delivery:  http://127.0.0.1:8000/delivery
echo   - Jumbo:     http://127.0.0.1:8000/jumbo
echo   - Seguimiento: http://127.0.0.1:8000/tracking
echo.
echo Para detener: presiona CTRL+C
echo ========================================
echo.

REM En Windows --reload suele dar error; usar sin --reload
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

pause
