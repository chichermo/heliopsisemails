#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import time
import logging
from typing import List, Dict
import schedule
from tqdm import tqdm
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender_smtp.log'),
        logging.StreamHandler()
    ]
)

class EmailSenderSMTP:
    """Clase para enviar emails usando SMTP (especialmente para Hotmail)"""
    
    def __init__(self, email=None, password=None):
        """Inicializar con credenciales de Hotmail"""
        self.email = email or "el_chicher@hotmail.com"
        self.password = password or "tszrmkdaqkjtllvd"
        self.smtp_server = "smtp-mail.outlook.com"
        self.smtp_port = 587
        self.sent_count = 0
        self.failed_count = 0
        
    def test_connection(self):
        """Probar conexión SMTP con Hotmail"""
        try:
            # Crear contexto SSL
            context = ssl.create_default_context()
            
            # Conectar al servidor SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                logging.info(f"✅ Conexión SMTP exitosa con {self.email}")
                return True
                
        except Exception as e:
            logging.error(f"❌ Error de conexión SMTP: {str(e)}")
            return False
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_name: str = None) -> bool:
        """Enviar un email usando SMTP"""
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = f"{sender_name or 'Tu Nombre'} <{self.email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Agregar cuerpo del mensaje
            msg.attach(MIMEText(body, 'html'))
            
            # Crear contexto SSL
            context = ssl.create_default_context()
            
            # Conectar y enviar
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                text = msg.as_string()
                server.sendmail(self.email, to_email, text)
                
            self.sent_count += 1
            logging.info(f"✅ Email enviado a {to_email}")
            return True
            
        except Exception as e:
            self.failed_count += 1
            logging.error(f"❌ Error enviando email a {to_email}: {str(e)}")
            return False
    
    def personalize_content(self, template: str, custom_data: Dict) -> str:
        """Personalizar contenido del template"""
        try:
            content = template
            for key, value in custom_data.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))
            return content
        except Exception as e:
            logging.error(f"Error personalizando contenido: {str(e)}")
            return template
    
    def send_bulk_emails(self, emails: List[Dict], subject: str, 
                         template: str, sender_name: str = None) -> Dict:
        """Enviar emails en lote"""
        results = {
            'total': len(emails),
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        logging.info(f"🚀 Iniciando envío de {len(emails)} emails...")
        
        # Probar conexión primero
        if not self.test_connection():
            logging.error("❌ No se pudo establecer conexión SMTP")
            return results
        
        # Enviar emails con barra de progreso
        with tqdm(total=len(emails), desc="Enviando emails") as pbar:
            for email_data in emails:
                try:
                    # Personalizar contenido
                    personalized_body = self.personalize_content(template, email_data.get('custom_data', {}))
                    
                    # Enviar email
                    if self.send_email(
                        email_data['email'], 
                        subject, 
                        personalized_body, 
                        sender_name
                    ):
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                        results['errors'].append(f"Error enviando a {email_data['email']}")
                    
                    # Delay entre emails para evitar spam
                    time.sleep(2)
                    pbar.update(1)
                    
                except Exception as e:
                    results['failed'] += 1
                    results['errors'].append(f"Error con {email_data['email']}: {str(e)}")
                    pbar.update(1)
        
        logging.info(f"✅ Envío completado: {results['sent']} enviados, {results['failed']} fallidos")
        return results
    
    def get_sending_stats(self) -> Dict:
        """Obtener estadísticas de envío"""
        return {
            'sent': self.sent_count,
            'failed': self.failed_count,
            'total': self.sent_count + self.failed_count
        }

def main():
    """Función principal para probar el sistema SMTP"""
    print("🧪 PRUEBA DEL SISTEMA SMTP PARA HOTMAIL")
    print("=" * 50)
    
    # Crear instancia
    sender = EmailSenderSMTP()
    
    # Probar conexión
    print("🔌 Probando conexión SMTP...")
    if sender.test_connection():
        print("✅ Conexión exitosa!")
        
        # Lista de prueba
        test_emails = [
            {
                'email': 'el_chicher@hotmail.com',
                'name': 'El Chicher',
                'custom_data': {'name': 'El Chicher'}
            }
        ]
        
        # Template de prueba
        test_template = """
        <html>
        <body>
            <h2>¡Hola {{name}}!</h2>
            <p>Este es un email de prueba usando SMTP.</p>
            <p>Si recibes este email, significa que el sistema SMTP está funcionando correctamente.</p>
            <br>
            <p>Saludos,<br>Tu Sistema de Emails</p>
        </body>
        </html>
        """
        
        # Enviar email de prueba
        print("📧 Enviando email de prueba...")
        results = sender.send_bulk_emails(
            test_emails,
            "Prueba SMTP - Sistema Funcionando",
            test_template,
            "Sistema de Emails"
        )
        
        print(f"📊 Resultados: {results['sent']} enviados, {results['failed']} fallidos")
        
    else:
        print("❌ No se pudo establecer conexión")

if __name__ == "__main__":
    main()
