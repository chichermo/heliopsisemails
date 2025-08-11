#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
import getpass

def solucionar_emails_reales():
    with app.app_context():
        print("🔧 SOLUCIONANDO ENVÍO DE EMAILS REALES")
        print("=" * 50)
        
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email actual: {user.outlook_email}")
        
        print(f"\n🎯 PROBLEMA IDENTIFICADO:")
        print(f"   • Los emails no se reciben porque el sistema está en modo PRUEBA")
        print(f"   • Necesitas un App Password válido para enviar emails reales")
        print(f"   • El App Password actual no está funcionando")
        
        print(f"\n📋 SOLUCIÓN PASO A PASO:")
        print(f"1. Ve a: https://account.microsoft.com/security")
        print(f"2. Inicia sesión con: {user.outlook_email}")
        print(f"3. Ve a 'Autenticación de dos factores'")
        print(f"4. Si no está habilitado, haz clic en 'Configurar'")
        print(f"5. Sigue las instrucciones para habilitar 2FA")
        print(f"6. Una vez habilitado, ve a 'Contraseñas de aplicación'")
        print(f"7. Haz clic en 'Crear una nueva contraseña de aplicación'")
        print(f"8. Selecciona 'Correo' o 'Outlook'")
        print(f"9. Anota la contraseña de 16 caracteres")
        print(f"\n" + "=" * 50)
        
        print(f"\n🔑 Configurar nuevas credenciales:")
        new_email = input("📧 Email de Outlook/Hotmail: ").strip()
        if not new_email:
            print("❌ Email requerido")
            return False
        
        print("🔐 Contraseña de aplicación (se ocultará al escribir):")
        new_password = getpass.getpass("Contraseña: ").strip()
        if not new_password:
            print("❌ Contraseña requerida")
            return False
        
        print(f"\n📋 Resumen:")
        print(f"   Email: {new_email}")
        print(f"   Password: {'*' * len(new_password)}")
        confirm = input("\n¿Confirmar cambios? (s/n): ").strip().lower()
        
        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Configuración cancelada")
            return False
        
        try:
            user.outlook_email = new_email
            user.outlook_password = new_password
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
    from datetime import datetime
    solucionar_emails_reales()
