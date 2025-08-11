@echo off
title Sistema de Emails Masivos
color 0A

echo.
echo ========================================
echo    SISTEMA DE EMAILS MASIVOS
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si existe el archivo .env
if not exist ".env" (
    echo.
    echo ========================================
    echo    CONFIGURACION INICIAL
    echo ========================================
    echo.
    echo No se encontró el archivo .env
    echo Vamos a crearlo ahora...
    echo.
    
    REM Crear archivo .env básico
    echo # Configuración de Outlook > .env
    echo OUTLOOK_EMAIL=tu_email@outlook.com >> .env
    echo OUTLOOK_PASSWORD=tu_password >> .env
    echo. >> .env
    echo # Configuración de envío >> .env
    echo MAX_EMAILS_PER_HOUR=50 >> .env
    echo DELAY_BETWEEN_EMAILS=30 >> .env
    echo BATCH_SIZE=10 >> .env
    echo. >> .env
    echo # Configuración de contenido >> .env
    echo DEFAULT_SUBJECT=Mensaje importante >> .env
    echo DEFAULT_SENDER_NAME=Tu Nombre >> .env
    echo. >> .env
    echo # Configuración de archivos >> .env
    echo EMAILS_FILE=emails.csv >> .env
    echo TEMPLATES_DIR=templates >> .env
    echo LOG_FILE=email_sender.log >> .env
    
    echo Archivo .env creado exitosamente!
    echo.
    echo IMPORTANTE: Edita el archivo .env con tus credenciales reales
    echo antes de usar el sistema.
    echo.
    pause
)

REM Verificar si existen los archivos necesarios
if not exist "emails.csv" (
    echo Creando archivo de emails de ejemplo...
    python main.py --create-sample
)

echo.
echo ========================================
echo    MENU PRINCIPAL
echo ========================================
echo.
echo 1. Modo de prueba (5 emails)
echo 2. Envío completo
echo 3. Crear archivos de ejemplo
echo 4. Ver ayuda
echo 5. Salir
echo.
set /p opcion="Selecciona una opción (1-5): "

if "%opcion%"=="1" (
    echo.
    echo Iniciando modo de prueba...
    python main.py --test
) else if "%opcion%"=="2" (
    echo.
    echo Iniciando envío completo...
    python main.py
) else if "%opcion%"=="3" (
    echo.
    echo Creando archivos de ejemplo...
    python main.py --create-sample
) else if "%opcion%"=="4" (
    echo.
    echo Mostrando ayuda...
    python main.py --help
) else if "%opcion%"=="5" (
    echo.
    echo ¡Hasta luego!
    exit /b 0
) else (
    echo.
    echo Opción no válida. Por favor, selecciona 1-5.
    pause
    goto :eof
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul
