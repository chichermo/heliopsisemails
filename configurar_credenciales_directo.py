#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User

def configurar_credenciales_directo():
    with app.app_context():
        print("🔧 CONFIGURANDO CREDENCIALES DIRECTAMENTE")
        print("=" * 50)
        
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email actual: {user.outlook_email}")
        
        # Configurar credenciales directamente
        email = "el_chicher@hotmail.com"
        password = "tszrmkdaqkjtllvd"  # App Password que proporcionaste
        
        print(f"\n🔑 Configurando credenciales:")
        print(f"   Email: {email}")
        print(f"   Password: {password[:4]}****{password[-4:]}")
        
        try:
            user.outlook_email = email
            user.outlook_password = password
            db.session.commit()
            
            print(f"\n✅ Credenciales actualizadas exitosamente!")
            print(f"📧 Email: {user.outlook_email}")
            
            # Probar conexión inmediatamente
            print(f"\n🚀 Probando conexión...")
            from email_sender import EmailSender
            sender = EmailSender(email=user.outlook_email, password=user.outlook_password)
            
            if sender.connect():
                print("✅ Conexión exitosa! Las credenciales son correctas.")
                print(f"\n🎉 ¡SISTEMA LISTO PARA ENVIAR EMAILS REALES!")
                
                # Probar envío de un email real
                print(f"\n📧 Probando envío de email real...")
                from datetime import datetime
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
                    print(f"✅ Email real enviado exitosamente a: {test_email}")
                    print(f"📧 Revisa tu bandeja de entrada para confirmar la recepción")
                    print(f"\n🎉 ¡SISTEMA 100% FUNCIONAL PARA EMAILS REALES!")
                    return True
                else:
                    print(f"❌ Error enviando email real a: {test_email}")
                    return False
            else:
                print("❌ Error conectando. Verifica:")
                print("   • Que el email sea correcto")
                print("   • Que uses un App Password (no tu contraseña normal)")
                print("   • Que tengas 2FA habilitado")
                print("   • Que el App Password no haya expirado")
                return False
                
        except Exception as e:
            print(f"❌ Error actualizando credenciales: {e}")
            return False

if __name__ == "__main__":
    configurar_credenciales_directo()
