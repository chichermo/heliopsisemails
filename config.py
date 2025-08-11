import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    # Configuración de Outlook
    OUTLOOK_EMAIL = os.getenv('OUTLOOK_EMAIL') or "el_chicher@hotmail.com"
    OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD') or "tszrmkdaqkjtllvd"
    
    # Configuración de envío
    MAX_EMAILS_PER_HOUR = int(os.getenv('MAX_EMAILS_PER_HOUR', 50))
    DELAY_BETWEEN_EMAILS = int(os.getenv('DELAY_BETWEEN_EMAILS', 30))  # segundos
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
    
    # Configuración de contenido
    DEFAULT_SUBJECT = os.getenv('DEFAULT_SUBJECT', 'Mensaje importante')
    DEFAULT_SENDER_NAME = os.getenv('DEFAULT_SENDER_NAME', 'Tu Nombre')
    
    # Configuración de archivos
    EMAILS_FILE = os.getenv('EMAILS_FILE', 'emails.csv')
    TEMPLATES_DIR = os.getenv('TEMPLATES_DIR', 'templates')
    
    # Configuración de logs
    LOG_FILE = os.getenv('LOG_FILE', 'email_sender.log')
    
    @classmethod
    def validate(cls):
        """Validar que las configuraciones necesarias estén presentes"""
        if not cls.OUTLOOK_EMAIL:
            print("⚠️  OUTLOOK_EMAIL no está configurado, usando valor por defecto")
        if not cls.OUTLOOK_PASSWORD:
            print("⚠️  OUTLOOK_PASSWORD no está configurado, usando valor por defecto")
        
        # Verificar que las credenciales estén disponibles
        if not cls.OUTLOOK_EMAIL or not cls.OUTLOOK_PASSWORD:
            print("❌ Error: Las credenciales de Outlook no están configuradas")
            return False
        return True 