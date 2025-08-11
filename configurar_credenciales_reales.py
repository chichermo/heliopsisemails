#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from werkzeug.security import generate_password_hash
import getpass

def configurar_credenciales():
    with app.app_context():
        print("🔧 CONFIGURACIÓN DE CREDENCIALES DE OUTLOOK")
        print("=" * 50)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario actual: {user.username}")
        print(f"📧 Email actual: {user.outlook_email or 'No configurado'}")
        
        print(f"\n📋 INSTRUCCIONES IMPORTANTES:")
        print(f"1. Necesitas un App Password de Microsoft")
        print(f"2. Ve a: https://account.microsoft.com/security")
        print(f"3. Inicia sesión con tu cuenta de Outlook/Hotmail")
        print(f"4. Ve a 'Seguridad' → 'Contraseñas de aplicación'")
        print(f"5. Crea una nueva contraseña de aplicación")
        print(f"6. Usa esa contraseña aquí (NO tu contraseña normal)")
        
        print(f"\n" + "=" * 50)
        
        # Solicitar nuevas credenciales
        print(f"\n🔑 Configurar nuevas credenciales:")
        
        # Email
        new_email = input("📧 Email de Outlook/Hotmail: ").strip()
        if not new_email:
            print("❌ Email requerido")
            return False
        
        # Password (oculto)
        print("🔐 Contraseña de aplicación (se ocultará al escribir):")
        new_password = getpass.getpass("Contraseña: ").strip()
        if not new_password:
            print("❌ Contraseña requerida")
            return False
        
        # Confirmar
        print(f"\n📋 Resumen:")
        print(f"   Email: {new_email}")
        print(f"   Password: {'*' * len(new_password)}")
        
        confirm = input("\n¿Confirmar cambios? (s/n): ").strip().lower()
        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Configuración cancelada")
            return False
        
        # Actualizar credenciales
        try:
            user.outlook_email = new_email
            user.outlook_password = new_password
            db.session.commit()
            
            print(f"\n✅ Credenciales actualizadas exitosamente!")
            print(f"📧 Email: {user.outlook_email}")
            
            # Probar conexión
            print(f"\n🚀 Probando conexión...")
            from email_sender import EmailSender
            sender = EmailSender(email=user.outlook_email, password=user.outlook_password)
            
            if sender.connect():
                print("✅ Conexión exitosa! Las credenciales son correctas.")
                return True
            else:
                print("❌ Error conectando. Verifica:")
                print("   • Que el email sea correcto")
                print("   • Que uses un App Password (no tu contraseña normal)")
                print("   • Que tengas 2FA habilitado")
                return False
                
        except Exception as e:
            print(f"❌ Error actualizando credenciales: {e}")
            return False

if __name__ == "__main__":
    configurar_credenciales()
