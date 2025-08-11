#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from email_sender import EmailSender
from datetime import datetime

def probar_conexion_final():
    with app.app_context():
        print("🔍 PRUEBA FINAL DE CONEXIÓN CON CREDENCIALES ACTUALIZADAS")
        print("=" * 60)
        
        # Obtener usuario con credenciales actualizadas
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email: {user.outlook_email}")
        print(f"🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
        
        # Probar conexión
        print(f"\n🚀 Intentando conectar a Outlook...")
        sender = EmailSender(email=user.outlook_email, password=user.outlook_password)
        
        try:
            if sender.connect():
                print("✅ Conexión exitosa a Outlook!")
                
                # Probar envío de un email de prueba
                print(f"\n📧 Probando envío de email de prueba...")
                test_email = "guillermoromerog@gmail.com"
                test_subject = "Prueba de Sistema - " + datetime.now().strftime('%H:%M:%S')
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
                    print(f"\n🎉 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
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
    probar_conexion_final()
