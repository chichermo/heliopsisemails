#!/usr/bin/env python3
"""
Script para configurar credenciales de forma segura
"""

import os
import getpass

def configurar_credenciales():
    """Configurar credenciales de forma interactiva"""
    print("🔧 Configuración de Credenciales - Sistema de Emails Masivos")
    print("=" * 60)
    
    # Leer configuración actual
    config = {}
    if os.path.exists('.env'):
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    print("\n📧 Configuración de Outlook:")
    
    # Email
    current_email = config.get('OUTLOOK_EMAIL', '')
    if current_email and current_email != 'tu_email@outlook.com':
        print(f"Email actual: {current_email}")
        cambiar = input("¿Deseas cambiar el email? (y/N): ").strip().lower()
        if cambiar != 'y':
            email = current_email
        else:
            email = input("Nuevo email de Outlook: ").strip()
    else:
        email = input("Email de Outlook: ").strip()
    
    # Contraseña
    print("\n🔐 Contraseña de aplicación:")
    print("IMPORTANTE: Usa una contraseña de aplicación, no tu contraseña normal")
    print("Para generar una contraseña de aplicación:")
    print("1. Ve a https://account.microsoft.com")
    print("2. Seguridad → Contraseñas de aplicación")
    print("3. Crear nueva contraseña de aplicación")
    print("4. Elige 'Correo' como aplicación")
    
    password = getpass.getpass("Contraseña de aplicación: ")
    
    # Configuraciones adicionales
    print("\n⚙️  Configuraciones adicionales:")
    
    max_emails = input(f"Máximo emails por hora (default: 50): ").strip() or "50"
    delay = input(f"Delay entre emails en segundos (default: 30): ").strip() or "30"
    batch_size = input(f"Tamaño del batch (default: 10): ").strip() or "10"
    subject = input(f"Asunto por defecto (default: 'Mensaje importante'): ").strip() or "Mensaje importante"
    sender_name = input(f"Nombre del remitente (default: 'Tu Nombre'): ").strip() or "Tu Nombre"
    
    # Crear contenido del archivo .env
    env_content = f"""# Configuración de Outlook
OUTLOOK_EMAIL={email}
OUTLOOK_PASSWORD={password}

# Configuración de envío
MAX_EMAILS_PER_HOUR={max_emails}
DELAY_BETWEEN_EMAILS={delay}
BATCH_SIZE={batch_size}

# Configuración de contenido
DEFAULT_SUBJECT={subject}
DEFAULT_SENDER_NAME={sender_name}

# Configuración de archivos
EMAILS_FILE=emails.csv
TEMPLATES_DIR=templates
LOG_FILE=email_sender.log
"""
    
    # Guardar archivo
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"\n✅ Archivo .env actualizado exitosamente!")
        print(f"📧 Email configurado: {email}")
        print(f"👤 Remitente: {sender_name}")
        print(f"📝 Asunto: {subject}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")
        return False

def main():
    """Función principal"""
    if configurar_credenciales():
        print("\n🎯 Próximos pasos:")
        print("1. Verifica que tu cuenta de Outlook tenga autenticación de aplicaciones habilitada")
        print("2. Ejecuta: python verificar_configuracion.py")
        print("3. Ejecuta: python main.py --test")
    else:
        print("\n❌ Error en la configuración")
        print("Por favor, intenta nuevamente")

if __name__ == "__main__":
    main()
