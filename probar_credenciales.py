#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from email_sender import EmailSender

def probar_credenciales():
    with app.app_context():
        print("🔍 PROBANDO CREDENCIALES ESPECÍFICAS")
        print("=" * 50)
        
        # Credenciales específicas
        email = "el_chicher@hotmail.com"
        password = "tszrmkdaqkjtllvd"
        
        print(f"📧 Email: {email}")
        print(f"🔑 App Password: {password[:4]}****{password[-4:]}")
        
        # Probar conexión
        print(f"\n🚀 Intentando conectar a Outlook...")
        sender = EmailSender(email=email, password=password)
        
        try:
            if sender.connect():
                print("✅ Conexión exitosa a Outlook!")
                
                # Probar envío de un email de prueba
                print(f"\n📧 Probando envío de email de prueba...")
                test_email = "guillermoromerog@gmail.com"
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
                
                success = sender.send_email(test_email, test_subject, test_content, "admin")
                
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
                print("   • App Password incorrecto")
                print("   • 2FA no configurado correctamente")
                print("   • Cuenta bloqueada o restringida")
                print("   • Problema con el servidor de Outlook")
                return False
                
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            return False

if __name__ == "__main__":
    from datetime import datetime
    probar_credenciales()
