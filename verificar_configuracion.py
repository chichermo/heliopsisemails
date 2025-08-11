#!/usr/bin/env python3
"""
Script para verificar la configuración del Sistema de Emails Masivos
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Verificar si existe y está configurado el archivo .env"""
    print("🔍 Verificando archivo .env...")
    
    if not os.path.exists('.env'):
        print("❌ No se encontró el archivo .env")
        print("💡 Solución: Ejecuta 'copy env_example.txt .env' y edita el archivo")
        return False
    
    # Leer archivo .env
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar credenciales
        if 'tu_email@outlook.com' in content or 'tu_password' in content:
            print("⚠️  El archivo .env tiene valores de ejemplo")
            print("💡 Necesitas editar el archivo con tus credenciales reales")
            return False
        
        # Verificar que existan las variables necesarias
        required_vars = ['OUTLOOK_EMAIL', 'OUTLOOK_PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if f'{var}=' not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Faltan variables en .env: {', '.join(missing_vars)}")
            return False
        
        print("✅ Archivo .env configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al leer .env: {e}")
        return False

def check_dependencies():
    """Verificar si las dependencias están instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    required_packages = [
        'exchangelib',
        'pandas', 
        'python-dotenv',
        'schedule',
        'tqdm',
        'colorama'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - No instalado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Para instalar dependencias faltantes:")
        print("   Ejecuta: pip install -r requirements.txt")
        print("   O ejecuta: instalar_dependencias.bat")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def check_files():
    """Verificar si existen los archivos necesarios"""
    print("\n🔍 Verificando archivos necesarios...")
    
    required_files = [
        'main.py',
        'email_sender.py',
        'config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - No encontrado")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Faltan archivos: {', '.join(missing_files)}")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    return True

def test_connection():
    """Probar conexión con Outlook"""
    print("\n🔍 Probando conexión con Outlook...")
    
    try:
        from config import Config
        from email_sender import EmailSender
        
        # Validar configuración
        try:
            Config.validate()
        except ValueError as e:
            print(f"❌ Error de configuración: {e}")
            return False
        
        # Intentar conectar
        sender = EmailSender()
        if sender.connect():
            print("✅ Conexión exitosa con Outlook")
            return True
        else:
            print("❌ No se pudo conectar con Outlook")
            print("💡 Verifica:")
            print("   - Credenciales correctas en .env")
            print("   - Autenticación de aplicaciones habilitada")
            print("   - Contraseña de aplicación generada")
            return False
            
    except Exception as e:
        print(f"❌ Error al probar conexión: {e}")
        return False

def show_config_summary():
    """Mostrar resumen de la configuración"""
    print("\n📊 RESUMEN DE CONFIGURACIÓN")
    print("=" * 40)
    
    # Leer configuración actual
    try:
        from config import Config
        print(f"📧 Email: {Config.OUTLOOK_EMAIL}")
        print(f"👤 Remitente: {Config.DEFAULT_SENDER_NAME}")
        print(f"📝 Asunto: {Config.DEFAULT_SUBJECT}")
        print(f"⚡ Rate máximo: {Config.MAX_EMAILS_PER_HOUR} emails/hora")
        print(f"⏱️  Delay: {Config.DELAY_BETWEEN_EMAILS} segundos")
        print(f"📦 Batch size: {Config.BATCH_SIZE}")
    except Exception as e:
        print(f"❌ Error al leer configuración: {e}")

def main():
    """Función principal"""
    print("🚀 Verificador de Configuración - Sistema de Emails Masivos")
    print("=" * 60)
    
    all_ok = True
    
    # Verificar archivo .env
    if not check_env_file():
        all_ok = False
    
    # Verificar dependencias
    if not check_dependencies():
        all_ok = False
    
    # Verificar archivos
    if not check_files():
        all_ok = False
    
    # Probar conexión solo si todo lo demás está bien
    if all_ok:
        if not test_connection():
            all_ok = False
    
    # Mostrar resumen
    show_config_summary()
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 ¡Configuración completada exitosamente!")
        print("\n✅ Tu sistema está listo para enviar emails")
        print("\n📋 Próximos pasos:")
        print("1. Edita emails.csv con tu lista de emails")
        print("2. Personaliza el template en templates/template_ejemplo.html")
        print("3. Ejecuta: python main.py --test (para probar)")
        print("4. Ejecuta: python main.py (para envío completo)")
    else:
        print("⚠️  Hay problemas en la configuración")
        print("\n🔧 Pasos para solucionar:")
        print("1. Ejecuta: instalar_dependencias.bat")
        print("2. Edita el archivo .env con tus credenciales")
        print("3. Verifica que tu cuenta de Outlook esté configurada")
        print("4. Ejecuta este script nuevamente")
    
    print("\n📖 Para más información, consulta: GUIA_CONFIGURACION.md")

if __name__ == "__main__":
    main()
