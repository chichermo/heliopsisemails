#!/usr/bin/env python3
"""
Script de configuración inicial para el Sistema de Emails Masivos
"""

import os
import sys
import getpass
from pathlib import Path

def create_env_file():
    """Crear archivo .env con las credenciales del usuario"""
    print("=== Configuración del Sistema de Emails Masivos ===\n")
    
    # Verificar si ya existe el archivo .env
    if os.path.exists('.env'):
        overwrite = input("El archivo .env ya existe. ¿Deseas sobrescribirlo? (y/N): ")
        if overwrite.lower() != 'y':
            print("Configuración cancelada.")
            return False
    
    print("Por favor, proporciona la siguiente información:")
    
    # Obtener credenciales de Outlook
    outlook_email = input("Email de Outlook: ").strip()
    if not outlook_email:
        print("Error: El email es obligatorio.")
        return False
    
    outlook_password = getpass.getpass("Contraseña de Outlook (o contraseña de aplicación): ")
    if not outlook_password:
        print("Error: La contraseña es obligatoria.")
        return False
    
    # Configuraciones opcionales
    print("\nConfiguraciones opcionales (presiona Enter para usar valores por defecto):")
    
    max_emails_per_hour = input("Máximo emails por hora (default: 50): ").strip() or "50"
    delay_between_emails = input("Delay entre emails en segundos (default: 30): ").strip() or "30"
    batch_size = input("Tamaño del batch (default: 10): ").strip() or "10"
    default_subject = input("Asunto por defecto (default: 'Mensaje importante'): ").strip() or "Mensaje importante"
    default_sender_name = input("Nombre del remitente (default: 'Tu Nombre'): ").strip() or "Tu Nombre"
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración de Outlook
OUTLOOK_EMAIL={outlook_email}
OUTLOOK_PASSWORD={outlook_password}

# Configuración de envío
MAX_EMAILS_PER_HOUR={max_emails_per_hour}
DELAY_BETWEEN_EMAILS={delay_between_emails}
BATCH_SIZE={batch_size}

# Configuración de contenido
DEFAULT_SUBJECT={default_subject}
DEFAULT_SENDER_NAME={default_sender_name}

# Configuración de archivos
EMAILS_FILE=emails.csv
TEMPLATES_DIR=templates
LOG_FILE=email_sender.log
"""
    
    # Escribir archivo .env
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"\n✅ Archivo .env creado exitosamente!")
        return True
        
    except Exception as e:
        print(f"Error al crear el archivo .env: {e}")
        return False

def create_directories():
    """Crear directorios necesarios"""
    directories = ['templates', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directorio {directory}/ creado")

def main():
    """Función principal del setup"""
    print("🚀 Configurando Sistema de Emails Masivos\n")
    
    # Crear directorios
    print("Creando directorios necesarios...")
    create_directories()
    
    # Crear archivo .env
    print("\nConfigurando credenciales...")
    if not create_env_file():
        sys.exit(1)
    
    # Crear archivos de ejemplo si no existen
    if not os.path.exists('emails.csv'):
        print("\nCreando archivo de emails de ejemplo...")
        os.system('python main.py --create-sample')
    
    print("\n" + "="*50)
    print("✅ Configuración completada exitosamente!")
    print("\nPróximos pasos:")
    print("1. Edita el archivo 'emails.csv' con tu lista de emails")
    print("2. Edita el template en 'templates/template_ejemplo.html'")
    print("3. Ejecuta 'python main.py --test' para hacer una prueba")
    print("4. Ejecuta 'python main.py' para enviar emails masivos")
    print("\n¡Listo para usar!")

if __name__ == "__main__":
    main() 