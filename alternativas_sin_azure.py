#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ALTERNATIVAS SIN AZURE PARA ENVÍO DE EMAILS
============================================

Este script te muestra todas las opciones disponibles para enviar emails
sin necesidad de configurar Azure o OAuth2.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

def mostrar_menu_principal():
    """Mostrar menú principal con todas las opciones"""
    
    print("🚀 ALTERNATIVAS SIN AZURE PARA ENVÍO DE EMAILS")
    print("=" * 60)
    print()
    print("❌ PROBLEMA IDENTIFICADO:")
    print("   Microsoft ha deshabilitado la autenticación básica")
    print("   para Hotmail/Outlook")
    print()
    print("✅ SOLUCIONES DISPONIBLES:")
    print()
    print("1. 🔐 Configurar Gmail (RECOMENDADO)")
    print("2. 📧 Usar servicios de email transaccional")
    print("3. 🔧 Configuración alternativa de Hotmail")
    print("4. 📱 Usar API de servicios externos")
    print("5. 🚪 Salir")
    print()
    
    while True:
        try:
            opcion = input("Selecciona una opción (1-5): ").strip()
            if opcion in ['1', '2', '3', '4', '5']:
                return opcion
            else:
                print("❌ Opción inválida. Selecciona 1, 2, 3, 4 o 5.")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            return '5'

def configurar_gmail():
    """Configurar Gmail paso a paso"""
    
    print("\n📧 CONFIGURACIÓN DE GMAIL")
    print("=" * 30)
    print()
    print("✅ VENTAJAS:")
    print("   • Gratis y confiable")
    print("   • Autenticación básica habilitada")
    print("   • Límites generosos (500 emails/día)")
    print("   • Configuración simple")
    print()
    print("🔧 PASOS REQUERIDOS:")
    print("1. Ir a https://myaccount.google.com/security")
    print("2. Habilitar 'Verificación en dos pasos'")
    print("3. Ir a 'Contraseñas de aplicación'")
    print("4. Generar nueva contraseña para 'Correo'")
    print("5. Usar esa contraseña en el sistema")
    print()
    
    respuesta = input("¿Quieres continuar con Gmail? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        return crear_config_gmail()
    else:
        print("✅ Opción cancelada.")
        return False

def crear_config_gmail():
    """Crear archivo de configuración para Gmail"""
    
    print("\n📝 CONFIGURACIÓN DE GMAIL")
    print("=" * 30)
    
    email = input("Ingresa tu email de Gmail: ").strip()
    password = input("Ingresa la contraseña de aplicación: ").strip()
    
    if not email or not password:
        print("❌ Email y contraseña son requeridos")
        return False
    
    # Crear archivo de configuración
    config_content = f'''# Configuración Gmail
GMAIL_EMAIL = "{email}"
GMAIL_PASSWORD = "{password}"
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587

# El sistema usará Gmail en lugar de Hotmail
'''
    
    try:
        with open('config_gmail.env', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Archivo config_gmail.env creado")
        
        # Crear también el sistema SMTP para Gmail
        crear_sistema_gmail(email, password)
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo: {e}")
        return False

def crear_sistema_gmail(email, password):
    """Crear sistema de envío de emails usando Gmail"""
    
    gmail_system = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import logging
from typing import List, Dict
from tqdm import tqdm

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gmail_sender.log'),
        logging.StreamHandler()
    ]
)

class GmailSender:
    """Sistema de envío de emails usando Gmail SMTP"""
    
    def __init__(self, email=None, password=None):
        self.email = email or "{email}"
        self.password = password or "{password}"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sent_count = 0
        self.failed_count = 0
        
    def test_connection(self):
        """Probar conexión SMTP con Gmail"""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                logging.info(f"✅ Conexión Gmail exitosa con {{self.email}}")
                return True
        except Exception as e:
            logging.error(f"❌ Error de conexión Gmail: {{str(e)}}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_name: str = None) -> bool:
        """Enviar un email usando Gmail SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{{sender_name or 'Tu Nombre'}} <{{self.email}}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                text = msg.as_string()
                server.sendmail(self.email, to_email, text)
                
            self.sent_count += 1
            logging.info(f"✅ Email enviado a {{to_email}}")
            return True
            
        except Exception as e:
            self.failed_count += 1
            logging.error(f"❌ Error enviando email a {{to_email}}: {{str(e)}}")
            return False
    
    def send_bulk_emails(self, emails: List[Dict], subject: str, 
                         template: str, sender_name: str = None) -> Dict:
        """Enviar emails en lote"""
        results = {{'total': len(emails), 'sent': 0, 'failed': 0, 'errors': []}}
        
        if not self.test_connection():
            logging.error("❌ No se pudo establecer conexión Gmail")
            return results
        
        with tqdm(total=len(emails), desc="Enviando emails") as pbar:
            for email_data in emails:
                try:
                    # Personalizar contenido
                    personalized_body = template.replace("{{{{name}}}}", email_data.get('name', ''))
                    
                    if self.send_email(email_data['email'], subject, personalized_body, sender_name):
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Error enviando a {{email_data['email']}}")
                    
                    time.sleep(2)  # Delay entre emails
                    pbar.update(1)
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Error con {{email_data['email']}}: {{str(e)}}")
                    pbar.update(1)
        
        logging.info(f"✅ Envío completado: {{results['sent']}} enviados, {{results['failed']}} fallidos")
        return results

def main():
    """Función principal para probar Gmail"""
    print("🧪 PRUEBA DEL SISTEMA GMAIL")
    print("=" * 40)
    
    sender = GmailSender()
    
    if sender.test_connection():
        print("✅ Conexión Gmail exitosa!")
        
        # Email de prueba
        test_emails = [
            {{'email': '{email}', 'name': 'Tu Nombre'}}
        ]
        
        test_template = """
        <html>
        <body>
            <h2>¡Hola {{name}}!</h2>
            <p>Este es un email de prueba usando Gmail SMTP.</p>
            <p>✅ El sistema está funcionando correctamente!</p>
            <br>
            <p>Saludos,<br>Sistema de Emails</p>
        </body>
        </html>
        """
        
        results = sender.send_bulk_emails(
            test_emails,
            "Prueba Gmail - Sistema Funcionando",
            test_template,
            "Sistema de Emails"
        )
        
        print(f"📊 Resultados: {{results['sent']}} enviados, {{results['failed']}} fallidos")
    else:
        print("❌ No se pudo establecer conexión Gmail")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('gmail_sender.py', 'w', encoding='utf-8') as f:
            f.write(gmail_system)
        print("✅ Sistema Gmail creado: gmail_sender.py")
        print("🚀 Ejecuta: python gmail_sender.py")
        return True
    except Exception as e:
        print(f"❌ Error creando sistema Gmail: {e}")
        return False

def servicios_email_transaccional():
    """Mostrar opciones de servicios de email transaccional"""
    
    print("\n📧 SERVICIOS DE EMAIL TRANSACCIONAL")
    print("=" * 40)
    print()
    print("✅ VENTAJAS:")
    print("   • APIs fáciles de usar")
    print("   • No requieren configuración de servidor")
    print("   • Límites generosos")
    print("   • Reportes detallados")
    print()
    print("🔧 OPCIONES DISPONIBLES:")
    print()
    print("1. 📬 SendGrid")
    print("   • Gratis: 100 emails/día")
    print("   • API simple")
    print("   • Documentación excelente")
    print()
    print("2. 📮 Mailgun")
    print("   • Gratis: 5,000 emails/mes")
    print("   • API RESTful")
    print("   • Muy confiable")
    print()
    print("3. 📨 Postmark")
    print("   • Gratis: 100 emails/mes")
    print("   • Excelente para transaccionales")
    print("   • Entrega garantizada")
    print()
    print("4. ☁️ Amazon SES")
    print("   • Muy barato: $0.10 por 1000 emails")
    print("   • Escalable")
    print("   • Requiere cuenta AWS")
    print()
    
    respuesta = input("¿Quieres configurar alguno de estos servicios? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        return configurar_servicio_transaccional()
    else:
        print("✅ Opción cancelada.")
        return False

def configurar_servicio_transaccional():
    """Configurar servicio de email transaccional"""
    
    print("\n🎯 SELECCIONA UN SERVICIO:")
    print("1. SendGrid (Recomendado para principiantes)")
    print("2. Mailgun")
    print("3. Postmark")
    print("4. Amazon SES")
    print("5. Volver")
    
    opcion = input("Selecciona (1-5): ").strip()
    
    if opcion == '1':
        return configurar_sendgrid()
    elif opcion == '2':
        return configurar_mailgun()
    elif opcion == '3':
        return configurar_postmark()
    elif opcion == '4':
        return configurar_amazon_ses()
    else:
        return False

def configurar_sendgrid():
    """Configurar SendGrid"""
    
    print("\n📬 CONFIGURACIÓN DE SENDGRID")
    print("=" * 30)
    print()
    print("📋 PASOS:")
    print("1. Ir a https://signup.sendgrid.com/")
    print("2. Crear cuenta gratuita")
    print("3. Verificar tu email")
    print("4. Ir a Settings > API Keys")
    print("5. Crear nueva API Key")
    print("6. Copiar la API Key")
    print()
    
    api_key = input("Ingresa tu API Key de SendGrid: ").strip()
    if not api_key:
        print("❌ API Key es requerida")
        return False
    
    # Crear sistema SendGrid
    crear_sistema_sendgrid(api_key)
    return True

def crear_sistema_sendgrid(api_key):
    """Crear sistema de envío usando SendGrid"""
    
    sendgrid_system = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import logging
from typing import List, Dict
from tqdm import tqdm

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sendgrid_sender.log'),
        logging.StreamHandler()
    ]
)

class SendGridSender:
    """Sistema de envío de emails usando SendGrid API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or "{api_key}"
        self.base_url = "https://api.sendgrid.com/v3"
        self.headers = {{
            "Authorization": f"Bearer {{self.api_key}}",
            "Content-Type": "application/json"
        }}
        self.sent_count = 0
        self.failed_count = 0
        
    def test_connection(self):
        """Probar conexión con SendGrid"""
        try:
            response = requests.get(f"{{self.base_url}}/user/profile", headers=self.headers)
            if response.status_code == 200:
                user_data = response.json()
                logging.info(f"✅ Conexión SendGrid exitosa para {{user_data.get('email', 'usuario')}}")
                return True
            else:
                logging.error(f"❌ Error de conexión SendGrid: {{response.status_code}}")
                return False
        except Exception as e:
            logging.error(f"❌ Error de conexión SendGrid: {{str(e)}}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_name: str = None, from_email: str = None) -> bool:
        """Enviar un email usando SendGrid"""
        try:
            data = {{
                "personalizations": [
                    {{
                        "to": [{{"email": to_email}}]
                    }}
                ],
                "from": {{
                    "email": from_email or "noreply@yourdomain.com",
                    "name": sender_name or "Tu Nombre"
                }},
                "subject": subject,
                "content": [
                    {{
                        "type": "text/html",
                        "value": body
                    }}
                ]
            }}
            
            response = requests.post(
                f"{{self.base_url}}/mail/send",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 202:
                self.sent_count += 1
                logging.info(f"✅ Email enviado a {{to_email}}")
                return True
            else:
                self.failed_count += 1
                logging.error(f"❌ Error enviando email a {{to_email}}: {{response.status_code}}")
                return False
                
        except Exception as e:
            self.failed_count += 1
            logging.error(f"❌ Error enviando email a {{to_email}}: {{str(e)}}")
            return False
    
    def send_bulk_emails(self, emails: List[Dict], subject: str, 
                         template: str, sender_name: str = None, from_email: str = None) -> Dict:
        """Enviar emails en lote"""
        results = {{'total': len(emails), 'sent': 0, 'failed': 0, 'errors': []}}
        
        if not self.test_connection():
            logging.error("❌ No se pudo establecer conexión SendGrid")
            return results
        
        with tqdm(total=len(emails), desc="Enviando emails") as pbar:
            for email_data in emails:
                try:
                    # Personalizar contenido
                    personalized_body = template.replace("{{{{name}}}}", email_data.get('name', ''))
                    
                    if self.send_email(email_data['email'], subject, personalized_body, sender_name, from_email):
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Error enviando a {{email_data['email']}}")
                    
                    time.sleep(1)  # Delay entre emails
                    pbar.update(1)
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Error con {{email_data['email']}}: {{str(e)}}")
                    pbar.update(1)
        
        logging.info(f"✅ Envío completado: {{results['sent']}} enviados, {{results['failed']}} fallidos")
        return results

def main():
    """Función principal para probar SendGrid"""
    print("🧪 PRUEBA DEL SISTEMA SENDGRID")
    print("=" * 40)
    
    sender = SendGridSender()
    
    if sender.test_connection():
        print("✅ Conexión SendGrid exitosa!")
        
        # Email de prueba
        test_emails = [
            {{'email': 'test@example.com', 'name': 'Usuario de Prueba'}}
        ]
        
        test_template = """
        <html>
        <body>
            <h2>¡Hola {{name}}!</h2>
            <p>Este es un email de prueba usando SendGrid API.</p>
            <p>✅ El sistema está funcionando correctamente!</p>
            <br>
            <p>Saludos,<br>Sistema de Emails</p>
        </body>
        </html>
        """
        
        results = sender.send_bulk_emails(
            test_emails,
            "Prueba SendGrid - Sistema Funcionando",
            test_template,
            "Sistema de Emails"
        )
        
        print(f"📊 Resultados: {{results['sent']}} enviados, {{results['failed']}} fallidos")
    else:
        print("❌ No se pudo establecer conexión SendGrid")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('sendgrid_sender.py', 'w', encoding='utf-8') as f:
            f.write(sendgrid_system)
        print("✅ Sistema SendGrid creado: sendgrid_sender.py")
        print("🚀 Ejecuta: python sendgrid_sender.py")
        return True
    except Exception as e:
        print(f"❌ Error creando sistema SendGrid: {e}")
        return False

def configurar_mailgun():
    """Configurar Mailgun"""
    print("\n📮 CONFIGURACIÓN DE MAILGUN")
    print("=" * 30)
    print("📋 PASOS:")
    print("1. Ir a https://signup.mailgun.com/")
    print("2. Crear cuenta gratuita")
    print("3. Verificar tu dominio")
    print("4. Obtener API Key")
    print("5. Configurar en el sistema")
    print()
    print("⚠️  Requiere verificación de dominio")
    return False

def configurar_postmark():
    """Configurar Postmark"""
    print("\n📨 CONFIGURACIÓN DE POSTMARK")
    print("=" * 30)
    print("📋 PASOS:")
    print("1. Ir a https://postmarkapp.com/")
    print("2. Crear cuenta gratuita")
    print("3. Verificar tu dominio")
    print("4. Obtener API Key")
    print("5. Configurar en el sistema")
    print()
    print("⚠️  Requiere verificación de dominio")
    return False

def configurar_amazon_ses():
    """Configurar Amazon SES"""
    print("\n☁️ CONFIGURACIÓN DE AMAZON SES")
    print("=" * 30)
    print("📋 PASOS:")
    print("1. Crear cuenta AWS")
    print("2. Ir a Amazon SES")
    print("3. Verificar tu email")
    print("4. Obtener credenciales")
    print("5. Configurar en el sistema")
    print()
    print("⚠️  Requiere cuenta AWS")
    return False

def configuracion_alternativa_hotmail():
    """Mostrar configuraciones alternativas para Hotmail"""
    
    print("\n🔧 CONFIGURACIÓN ALTERNATIVA DE HOTMAIL")
    print("=" * 40)
    print()
    print("⚠️  ADVERTENCIA: Estas opciones pueden no funcionar")
    print("   debido a las restricciones de Microsoft")
    print()
    print("🔍 OPCIONES A PROBAR:")
    print()
    print("1. 🔑 App Password (si tienes 2FA)")
    print("2. 🔐 Configuración específica del servidor")
    print("3. 📱 Usar aplicación móvil")
    print("4. 🌐 Usar webmail directamente")
    print()
    
    respuesta = input("¿Quieres probar alguna de estas opciones? (s/n): ").lower().strip()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        return probar_configuraciones_alternativas()
    else:
        print("✅ Opción cancelada.")
        return False

def probar_configuraciones_alternativas():
    """Probar configuraciones alternativas"""
    
    print("\n🧪 PROBANDO CONFIGURACIONES ALTERNATIVAS")
    print("=" * 40)
    print()
    print("1️⃣ Verificando si tienes 2FA habilitado...")
    print("   Ve a: https://account.live.com/proofs/AppPassword")
    print()
    
    tiene_2fa = input("¿Tienes 2FA habilitado? (s/n): ").lower().strip()
    if tiene_2fa in ['s', 'si', 'sí', 'y', 'yes']:
        print("✅ ¡Excelente! Puedes usar App Password")
        print("1. Ve a la URL anterior")
        print("2. Genera nueva contraseña de aplicación")
        print("3. Usa esa contraseña en el sistema")
        return True
    else:
        print("❌ Sin 2FA no puedes usar App Password")
        print("💡 RECOMENDACIÓN: Usa Gmail o SendGrid")
        return False

def main():
    """Función principal"""
    
    print("🚀 SISTEMA DE ALTERNATIVAS SIN AZURE")
    print("=" * 50)
    print()
    
    while True:
        opcion = mostrar_menu_principal()
        
        if opcion == '1':
            if configurar_gmail():
                print("\n✅ Gmail configurado exitosamente!")
                print("🚀 Ejecuta: python gmail_sender.py")
                break
        elif opcion == '2':
            servicios_email_transaccional()
        elif opcion == '3':
            configuracion_alternativa_hotmail()
        elif opcion == '4':
            print("\n📱 APIs externas disponibles:")
            print("• Gmail SMTP (gratis)")
            print("• SendGrid (gratis hasta 100/día)")
            print("• Mailgun (gratis hasta 5,000/mes)")
            print("• Postmark (gratis hasta 100/mes)")
            print("• Amazon SES (muy barato)")
        elif opcion == '5':
            print("\n👋 ¡Hasta luego!")
            break
        
        print("\n" + "="*50 + "\n")
    
    print("\n📚 RESUMEN DE RECOMENDACIONES:")
    print("🥇 1. Gmail (más simple, funciona inmediatamente)")
    print("🥈 2. SendGrid (API fácil, 100 emails gratis/día)")
    print("🥉 3. Mailgun (5,000 emails gratis/mes)")
    print()
    print("💡 RECOMENDACIÓN FINAL: Empieza con Gmail")

if __name__ == "__main__":
    main()

