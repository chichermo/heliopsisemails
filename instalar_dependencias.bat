@echo off
title Instalación de Dependencias - Sistema de Emails Masivos
color 0B

echo.
echo ========================================
echo    INSTALACION DE DEPENDENCIAS
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    echo Asegúrate de marcar "Add to PATH" durante la instalación
    pause
    exit /b 1
)

echo Python encontrado:
python --version

echo.
echo Instalando dependencias...
echo.

REM Instalar dependencias una por una
echo Instalando exchangelib...
pip install exchangelib==5.4.0
if errorlevel 1 (
    echo ERROR: No se pudo instalar exchangelib
    pause
    exit /b 1
)

echo Instalando pandas...
pip install pandas>=2.0.0
if errorlevel 1 (
    echo ERROR: No se pudo instalar pandas
    pause
    exit /b 1
)

echo Instalando python-dotenv...
pip install python-dotenv==1.0.0
if errorlevel 1 (
    echo ERROR: No se pudo instalar python-dotenv
    pause
    exit /b 1
)

echo Instalando schedule...
pip install schedule==1.2.0
if errorlevel 1 (
    echo ERROR: No se pudo instalar schedule
    pause
    exit /b 1
)

echo Instalando tqdm...
pip install tqdm==4.66.1
if errorlevel 1 (
    echo ERROR: No se pudo instalar tqdm
    pause
    exit /b 1
)

echo Instalando colorama...
pip install colorama==0.4.6
if errorlevel 1 (
    echo ERROR: No se pudo instalar colorama
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo ✓ Todas las dependencias han sido instaladas correctamente
echo.
echo Ahora puedes:
echo 1. Ejecutar 'iniciar_sistema.bat' para usar el sistema
echo 2. O ejecutar 'python main.py --test' para hacer una prueba
echo.
pause
