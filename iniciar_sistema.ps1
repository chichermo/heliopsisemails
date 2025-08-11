# Sistema de Emails Masivos - Script de Inicio
# PowerShell Script

param(
    [switch]$Test,
    [switch]$Setup,
    [switch]$Help
)

# Configurar colores y título
$Host.UI.RawUI.WindowTitle = "Sistema de Emails Masivos"
$Host.UI.RawUI.ForegroundColor = "Green"

function Show-Banner {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "    SISTEMA DE EMAILS MASIVOS" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "✗ Python no está instalado o no está en el PATH" -ForegroundColor Red
        Write-Host "Por favor, instala Python desde https://python.org" -ForegroundColor Yellow
        return $false
    }
    return $false
}

function Install-Dependencies {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
            return $true
        } else {
            Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
        return $false
    }
}

function Create-EnvFile {
    if (-not (Test-Path ".env")) {
        Write-Host "Creando archivo .env..." -ForegroundColor Yellow
        
        $envContent = @"
# Configuración de Outlook
OUTLOOK_EMAIL=tu_email@outlook.com
OUTLOOK_PASSWORD=tu_password

# Configuración de envío
MAX_EMAILS_PER_HOUR=50
DELAY_BETWEEN_EMAILS=30
BATCH_SIZE=10

# Configuración de contenido
DEFAULT_SUBJECT=Mensaje importante
DEFAULT_SENDER_NAME=Tu Nombre

# Configuración de archivos
EMAILS_FILE=emails.csv
TEMPLATES_DIR=templates
LOG_FILE=email_sender.log
"@
        
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✓ Archivo .env creado" -ForegroundColor Green
        Write-Host "IMPORTANTE: Edita el archivo .env con tus credenciales reales" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Archivo .env ya existe" -ForegroundColor Green
    }
}

function Show-Menu {
    Show-Banner
    
    Write-Host "Opciones disponibles:" -ForegroundColor Cyan
    Write-Host "1. Modo de prueba (5 emails)" -ForegroundColor White
    Write-Host "2. Envío completo" -ForegroundColor White
    Write-Host "3. Crear archivos de ejemplo" -ForegroundColor White
    Write-Host "4. Configurar sistema" -ForegroundColor White
    Write-Host "5. Ver ayuda" -ForegroundColor White
    Write-Host "6. Salir" -ForegroundColor White
    Write-Host ""
    
    $opcion = Read-Host "Selecciona una opción (1-6)"
    
    switch ($opcion) {
        "1" {
            Write-Host "Iniciando modo de prueba..." -ForegroundColor Yellow
            python main.py --test
        }
        "2" {
            Write-Host "Iniciando envío completo..." -ForegroundColor Yellow
            python main.py
        }
        "3" {
            Write-Host "Creando archivos de ejemplo..." -ForegroundColor Yellow
            python main.py --create-sample
        }
        "4" {
            Write-Host "Configurando sistema..." -ForegroundColor Yellow
            python setup.py
        }
        "5" {
            Write-Host "Mostrando ayuda..." -ForegroundColor Yellow
            python main.py --help
        }
        "6" {
            Write-Host "¡Hasta luego!" -ForegroundColor Green
            exit
        }
        default {
            Write-Host "Opción no válida. Por favor, selecciona 1-6." -ForegroundColor Red
            Start-Sleep -Seconds 2
            Show-Menu
        }
    }
}

# Función principal
function Main {
    Show-Banner
    
    # Verificar Python
    if (-not (Test-Python)) {
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    
    # Instalar dependencias si es necesario
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "✗ No se encontró requirements.txt" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    
    # Crear archivo .env si no existe
    Create-EnvFile
    
    # Crear archivos de ejemplo si no existen
    if (-not (Test-Path "emails.csv")) {
        Write-Host "Creando archivos de ejemplo..." -ForegroundColor Yellow
        python main.py --create-sample
    }
    
    # Mostrar menú o ejecutar comando directo
    if ($Test) {
        Write-Host "Ejecutando modo de prueba..." -ForegroundColor Yellow
        python main.py --test
    } elseif ($Setup) {
        Write-Host "Ejecutando configuración..." -ForegroundColor Yellow
        python setup.py
    } elseif ($Help) {
        Write-Host "Mostrando ayuda..." -ForegroundColor Yellow
        python main.py --help
    } else {
        Show-Menu
    }
}

# Ejecutar función principal
Main
