#!/usr/bin/env python3
"""
Script para crear un ejecutable del Sistema de Emails Masivos
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Instalar PyInstaller si no está instalado"""
    try:
        import PyInstaller
        print("✓ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("✗ Error al instalar PyInstaller")
            return False

def create_executable():
    """Crear el ejecutable"""
    print("Creando ejecutable...")
    
    # Comando para crear el ejecutable
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=SistemaEmailsMasivos",
        "--add-data=templates;templates",
        "--add-data=env_example.txt;.",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        "main.py"
    ]
    
    # Remover elementos vacíos
    cmd = [item for item in cmd if item]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Ejecutable creado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error al crear el ejecutable: {e}")
        return False

def create_launcher():
    """Crear un launcher simple"""
    launcher_content = '''@echo off
title Sistema de Emails Masivos
color 0A

echo.
echo ========================================
echo    SISTEMA DE EMAILS MASIVOS
echo ========================================
echo.

REM Verificar si existe el ejecutable
if not exist "SistemaEmailsMasivos.exe" (
    echo ERROR: No se encontró el ejecutable SistemaEmailsMasivos.exe
    echo Por favor, ejecuta build_executable.py primero
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
    SistemaEmailsMasivos.exe --test
) else if "%opcion%"=="2" (
    echo.
    echo Iniciando envío completo...
    SistemaEmailsMasivos.exe
) else if "%opcion%"=="3" (
    echo.
    echo Creando archivos de ejemplo...
    SistemaEmailsMasivos.exe --create-sample
) else if "%opcion%"=="4" (
    echo.
    echo Mostrando ayuda...
    SistemaEmailsMasivos.exe --help
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
'''
    
    with open("SistemaEmailsMasivos.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✓ Launcher creado: SistemaEmailsMasivos.bat")

def main():
    """Función principal"""
    print("🚀 Creando ejecutable del Sistema de Emails Masivos")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("✗ Error: No se encontró main.py")
        print("Asegúrate de estar en el directorio del proyecto")
        return False
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return False
    
    # Crear ejecutable
    if not create_executable():
        return False
    
    # Crear launcher
    create_launcher()
    
    print("\n" + "=" * 50)
    print("✅ Ejecutable creado exitosamente!")
    print("\nArchivos generados:")
    print("- SistemaEmailsMasivos.exe (ejecutable principal)")
    print("- SistemaEmailsMasivos.bat (launcher)")
    print("\nPara usar el sistema:")
    print("1. Doble clic en 'SistemaEmailsMasivos.bat'")
    print("2. O ejecuta directamente 'SistemaEmailsMasivos.exe'")
    print("\n¡Listo para usar!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
