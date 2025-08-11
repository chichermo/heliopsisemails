#!/usr/bin/env python3
"""
Sistema de Envío de Emails Masivos
==================================

Este script permite enviar emails masivos a través de Outlook
con control de rate para evitar ser detectado como spam.
"""

import argparse
import sys
import os
from datetime import datetime
from email_sender import EmailSender
from config import Config
import logging

def setup_logging():
    """Configurar logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def validate_config():
    """Validar configuración"""
    try:
        Config.validate()
        return True
    except ValueError as e:
        print(f"Error de configuración: {e}")
        print("Por favor, crea un archivo .env con las siguientes variables:")
        print("OUTLOOK_EMAIL=tu_email@outlook.com")
        print("OUTLOOK_PASSWORD=tu_password")
        return False

def load_template(template_path: str) -> str:
    """Cargar template desde archivo"""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de template {template_path}")
        return None
    except Exception as e:
        print(f"Error al cargar template: {e}")
        return None

def create_sample_emails_file():
    """Crear archivo de ejemplo con emails"""
    sample_data = [
        {'email': 'ejemplo1@email.com', 'name': 'Juan Pérez', 'empresa': 'Empresa A'},
        {'email': 'ejemplo2@email.com', 'name': 'María García', 'empresa': 'Empresa B'},
        {'email': 'ejemplo3@email.com', 'name': 'Carlos López', 'empresa': 'Empresa C'},
    ]
    
    import pandas as pd
    df = pd.DataFrame(sample_data)
    df.to_csv(Config.EMAILS_FILE, index=False)
    print(f"Archivo de ejemplo creado: {Config.EMAILS_FILE}")

def create_sample_template():
    """Crear template de ejemplo"""
    template_content = """Hola {{name}},

Espero que este mensaje te encuentre bien. 

Te escribo desde {{empresa}} para compartir información importante contigo.

Saludos cordiales,
{{sender_name}}

---
Este es un email automático, por favor no responder directamente a este mensaje."""
    
    os.makedirs(Config.TEMPLATES_DIR, exist_ok=True)
    template_path = os.path.join(Config.TEMPLATES_DIR, 'template_ejemplo.html')
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"Template de ejemplo creado: {template_path}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Sistema de Envío de Emails Masivos')
    parser.add_argument('--emails', '-e', help='Archivo CSV con lista de emails')
    parser.add_argument('--template', '-t', help='Archivo de template HTML')
    parser.add_argument('--subject', '-s', help='Asunto del email')
    parser.add_argument('--sender-name', help='Nombre del remitente')
    parser.add_argument('--create-sample', action='store_true', help='Crear archivos de ejemplo')
    parser.add_argument('--test', action='store_true', help='Modo de prueba (solo 5 emails)')
    
    args = parser.parse_args()
    
    # Configurar logging
    setup_logging()
    
    # Crear archivos de ejemplo si se solicita
    if args.create_sample:
        create_sample_emails_file()
        create_sample_template()
        print("\nArchivos de ejemplo creados exitosamente!")
        print("1. Edita el archivo emails.csv con tus emails")
        print("2. Edita el template en templates/template_ejemplo.html")
        print("3. Configura tu archivo .env con tus credenciales")
        return
    
    # Validar configuración
    if not validate_config():
        return
    
    # Inicializar sender
    sender = EmailSender()
    
    # Conectar a Outlook
    print("Conectando a Outlook...")
    if not sender.connect():
        print("Error: No se pudo conectar a Outlook")
        return
    
    # Cargar emails
    emails_file = args.emails or Config.EMAILS_FILE
    if not os.path.exists(emails_file):
        print(f"Error: No se encontró el archivo {emails_file}")
        print("Usa --create-sample para crear archivos de ejemplo")
        return
    
    emails = sender.load_emails(emails_file)
    if not emails:
        print("Error: No se pudieron cargar emails")
        return
    
    # Modo de prueba
    if args.test:
        emails = emails[:5]
        print(f"Modo de prueba: Enviando solo {len(emails)} emails")
    
    # Cargar template
    template_path = args.template or os.path.join(Config.TEMPLATES_DIR, 'template_ejemplo.html')
    if not os.path.exists(template_path):
        print(f"Error: No se encontró el template {template_path}")
        print("Usa --create-sample para crear archivos de ejemplo")
        return
    
    template = load_template(template_path)
    if not template:
        return
    
    # Configurar asunto y remitente
    subject = args.subject or Config.DEFAULT_SUBJECT
    sender_name = args.sender_name or Config.DEFAULT_SENDER_NAME
    
    # Confirmar envío
    print(f"\nResumen del envío:")
    print(f"- Total de emails: {len(emails)}")
    print(f"- Asunto: {subject}")
    print(f"- Remitente: {sender_name}")
    print(f"- Template: {template_path}")
    
    confirm = input("\n¿Deseas continuar con el envío? (y/N): ")
    if confirm.lower() != 'y':
        print("Envío cancelado")
        return
    
    # Iniciar envío
    print(f"\nIniciando envío de {len(emails)} emails...")
    results = sender.send_bulk_emails(emails, subject, template, sender_name)
    
    # Mostrar resultados
    print(f"\n=== RESULTADOS DEL ENVÍO ===")
    print(f"Total procesados: {results['total']}")
    print(f"Enviados exitosamente: {results['sent']}")
    print(f"Fallidos: {results['failed']}")
    
    if results['errors']:
        print(f"\nErrores encontrados:")
        for error in results['errors'][:5]:  # Mostrar solo los primeros 5 errores
            print(f"- {error}")
        if len(results['errors']) > 5:
            print(f"... y {len(results['errors']) - 5} errores más")
    
    # Mostrar estadísticas
    stats = sender.get_sending_stats()
    if stats:
        print(f"\n=== ESTADÍSTICAS ===")
        print(f"Duración total: {stats['duration']}")
        print(f"Tasa de envío: {stats['rate_per_hour']} emails/hora")

if __name__ == "__main__":
    main() 