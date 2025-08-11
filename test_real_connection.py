#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from email_sender import EmailSender

def test_real_connection():
    with app.app_context():
        print("🔍 Probando conexión real a Outlook...")
        print("=" * 50)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email configurado: {user.outlook_email}")
        print(f"🔑 Password configurado: {'Sí' if user.outlook_password else 'No'}")
        
        if not user.outlook_email or not user.outlook_password:
            print("❌ Credenciales no configuradas")
            return False
        
        # Probar conexión
        print(f"\n🚀 Intentando conectar a Outlook...")
        sender = EmailSender(email=user.outlook_email, password=user.outlook_password)
        
        try:
            if sender.connect():
                print("✅ Conexión exitosa a Outlook!")
                
                # Probar envío de un email de prueba
                print(f"\n📧 Probando envío de email de prueba...")
                test_email = "guillermoromerog@gmail.com"  # Email de prueba
                test_subject = "Prueba de Sistema - " + str(datetime.now().strftime('%H:%M:%S'))
                test_content = """
                <html>
                <body>
                    <h2>Prueba del Sistema de Envío de Emails</h2>
                    <p>Este es un email de prueba para verificar que el sistema funciona correctamente.</p>
                    <p><strong>Fecha:</strong> {}</p>
                    <p><strong>Hora:</strong> {}</p>
                    <hr>
                    <p><em>Este email fue enviado automáticamente por el sistema de envío masivo.</em></p>
                </body>
                </html>
                """.format(datetime.now().strftime('%d/%m/%Y'), datetime.now().strftime('%H:%M:%S'))
                
                success = sender.send_email(test_email, test_subject, test_content, user.username)
                
                if success:
                    print(f"✅ Email de prueba enviado exitosamente a: {test_email}")
                    print(f"📧 Revisa tu bandeja de entrada para confirmar la recepción")
                    return True
                else:
                    print(f"❌ Error enviando email de prueba a: {test_email}")
                    return False
                    
            else:
                print("❌ Error conectando a Outlook")
                print("💡 Posibles causas:")
                print("   • Credenciales incorrectas")
                print("   • App Password no configurado")
                print("   • 2FA habilitado sin App Password")
                print("   • Cuenta bloqueada o restringida")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            return False

if __name__ == "__main__":
    from datetime import datetime
    test_real_connection()
