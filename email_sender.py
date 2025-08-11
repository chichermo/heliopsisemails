import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from exchangelib import Credentials, Account, DELEGATE, Configuration, Message, Mailbox
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from tqdm import tqdm
import pandas as pd
from config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

class EmailSender:
    def __init__(self, email=None, password=None):
        """Inicializar el sistema de envío de emails"""
        self.account = None
        self.credentials = None
        self.emails_sent = 0
        self.start_time = None
        self.last_sent_time = None
        self.email = email or Config.OUTLOOK_EMAIL
        self.password = password or Config.OUTLOOK_PASSWORD
        
    def connect(self):
        """Conectar a la cuenta de Outlook"""
        try:
            # Configurar credenciales
            self.credentials = Credentials(self.email, self.password)
            
            # Configuración específica para Hotmail/Outlook
            if 'hotmail.com' in self.email or 'outlook.com' in self.email:
                # Usar configuración específica para Hotmail
                try:
                    # Configuración específica para Hotmail usando EWS
                    config = Configuration(
                        service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx',
                        credentials=self.credentials,
                        auth_type='basic'
                    )
                    
                    self.account = Account(
                        primary_smtp_address=self.email,
                        config=config,
                        autodiscover=False,
                        access_type=DELEGATE
                    )
                    
                    # Verificar conexión
                    self.account.inbox
                    logging.info(f"Conectado exitosamente a {self.email} usando configuración específica")
                    return True
                    
                except Exception as e:
                    logging.warning(f"Configuración específica falló: {str(e)}")
                    
                    # Intentar con configuración alternativa para Hotmail
                    try:
                        config = Configuration(
                            service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx',
                            credentials=self.credentials,
                            auth_type='basic'
                        )
                        
                        self.account = Account(
                            primary_smtp_address=self.email,
                            config=config,
                            autodiscover=False,
                            access_type=DELEGATE
                        )
                        
                        # Verificar conexión
                        self.account.inbox
                        logging.info(f"Conectado exitosamente a {self.email} usando configuración alternativa")
                        return True
                        
                    except Exception as e2:
                        logging.warning(f"Configuración alternativa falló: {str(e2)}")
                        
                        # Intentar con autodiscover como último recurso
                        try:
                            self.account = Account(
                                primary_smtp_address=self.email,
                                credentials=self.credentials,
                                autodiscover=True,
                                access_type=DELEGATE
                            )
                            
                            # Verificar conexión
                            self.account.inbox
                            logging.info(f"Conectado exitosamente a {self.email} usando autodiscover")
                            return True
                            
                        except Exception as e3:
                            logging.error(f"Error con autodiscover: {str(e3)}")
                            return False
                        
            else:
                # Configuración general para otros dominios
                self.account = Account(
                    primary_smtp_address=self.email,
                    credentials=self.credentials,
                    autodiscover=True,
                    access_type=DELEGATE
                )
                
                logging.info(f"Conectado exitosamente a {self.email}")
                return True
            
        except Exception as e:
            logging.error(f"Error al conectar: {str(e)}")
            return False
    
    def load_emails(self, file_path: str = None) -> List[Dict]:
        """Cargar lista de emails desde archivo CSV"""
        if not file_path:
            file_path = Config.EMAILS_FILE
            
        try:
            df = pd.read_csv(file_path)
            emails = []
            
            for _, row in df.iterrows():
                email_data = {
                    'email': row.get('email', ''),
                    'name': row.get('name', ''),
                    'custom_data': {}
                }
                
                # Agregar datos personalizados si existen
                for col in df.columns:
                    if col not in ['email', 'name']:
                        email_data['custom_data'][col] = row.get(col, '')
                
                if email_data['email']:
                    emails.append(email_data)
            
            logging.info(f"Cargados {len(emails)} emails desde {file_path}")
            return emails
            
        except Exception as e:
            logging.error(f"Error al cargar emails: {str(e)}")
            return []
    
    def create_message(self, to_email: str, subject: str, body: str, 
                      sender_name: str = None) -> Message:
        """Crear un mensaje de email"""
        if not sender_name:
            sender_name = Config.DEFAULT_SENDER_NAME
            
        message = Message(
            account=self.account,
            subject=subject,
            body=body,
            to_recipients=[Mailbox(email_address=to_email)]
        )
        
        return message
    
    def personalize_content(self, template: str, custom_data: Dict) -> str:
        """Personalizar el contenido del email con datos específicos"""
        personalized = template
        
        for key, value in custom_data.items():
            placeholder = f"{{{{{key}}}}}"
            personalized = personalized.replace(placeholder, str(value))
        
        return personalized
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   sender_name: str = None) -> bool:
        """Enviar un email individual"""
        try:
            message = self.create_message(to_email, subject, body, sender_name)
            message.send()
            
            self.emails_sent += 1
            self.last_sent_time = datetime.now()
            
            logging.info(f"Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logging.error(f"Error al enviar email a {to_email}: {str(e)}")
            return False
    
    def calculate_delay(self) -> int:
        """Calcular el delay necesario para evitar límites de rate"""
        if not self.last_sent_time:
            return 0
        
        time_since_last = (datetime.now() - self.last_sent_time).total_seconds()
        min_delay = Config.DELAY_BETWEEN_EMAILS
        
        # Añadir variabilidad aleatoria para parecer más humano
        random_delay = random.randint(0, 10)
        
        return max(0, min_delay - time_since_last + random_delay)
    
    def send_bulk_emails(self, emails: List[Dict], subject: str, 
                        template: str, sender_name: str = None) -> Dict:
        """Enviar emails masivos con control de rate"""
        if not self.account:
            if not self.connect():
                return {'success': False, 'error': 'No se pudo conectar a Outlook'}
        
        self.start_time = datetime.now()
        results = {
            'total': len(emails),
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        logging.info(f"Iniciando envío de {len(emails)} emails")
        
        for i, email_data in enumerate(tqdm(emails, desc="Enviando emails")):
            try:
                # Personalizar contenido
                personalized_body = self.personalize_content(template, email_data.get('custom_data', {}))
                
                # Enviar email
                success = self.send_email(
                    email_data['email'],
                    subject,
                    personalized_body,
                    sender_name
                )
                
                if success:
                    results['sent'] += 1
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Error en {email_data['email']}")
                
                # Control de rate
                if i < len(emails) - 1:  # No esperar después del último email
                    delay = self.calculate_delay()
                    if delay > 0:
                        time.sleep(delay)
                
                # Pausa cada batch para evitar detección
                if (i + 1) % Config.BATCH_SIZE == 0:
                    logging.info(f"Pausa de 2 minutos después del batch {i + 1}")
                    time.sleep(120)
                
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Error en {email_data['email']}: {str(e)}")
                logging.error(f"Error procesando {email_data['email']}: {str(e)}")
        
        logging.info(f"Envio completado: {results['sent']} enviados, {results['failed']} fallidos")
        return results
    
    def get_sending_stats(self) -> Dict:
        """Obtener estadísticas del envío"""
        if not self.start_time:
            return {}
        
        duration = datetime.now() - self.start_time
        rate = self.emails_sent / (duration.total_seconds() / 3600) if duration.total_seconds() > 0 else 0
        
        return {
            'emails_sent': self.emails_sent,
            'duration': str(duration),
            'rate_per_hour': round(rate, 2),
            'start_time': self.start_time.isoformat(),
            'last_sent': self.last_sent_time.isoformat() if self.last_sent_time else None
        } 