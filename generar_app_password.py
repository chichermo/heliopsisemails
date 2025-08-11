#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def generar_app_password():
    print("🔧 GENERANDO NUEVO APP PASSWORD")
    print("=" * 50)
    
    print("🎯 PROBLEMA IDENTIFICADO:")
    print("   • El App Password actual no está funcionando")
    print("   • Necesitas generar uno nuevo")
    print("   • El problema puede ser que:")
    print("     - El App Password expiró")
    print("     - No tienes 2FA habilitado")
    print("     - La cuenta tiene restricciones")
    
    print(f"\n📋 SOLUCIÓN PASO A PASO:")
    print(f"1. Ve a: https://account.microsoft.com/security")
    print(f"2. Inicia sesión con: el_chicher@hotmail.com")
    print(f"3. Ve a 'Autenticación de dos factores'")
    print(f"4. Si no está habilitado, haz clic en 'Configurar'")
    print(f"5. Sigue las instrucciones para habilitar 2FA")
    print(f"6. Una vez habilitado, ve a 'Contraseñas de aplicación'")
    print(f"7. Haz clic en 'Crear una nueva contraseña de aplicación'")
    print(f"8. Selecciona 'Correo' o 'Outlook'")
    print(f"9. Anota la contraseña de 16 caracteres")
    print(f"10. Copia y pega la contraseña aquí")
    
    print(f"\n" + "=" * 50)
    
    # Solicitar nuevo App Password
    new_password = input("🔐 Ingresa el nuevo App Password (16 caracteres): ").strip()
    
    if len(new_password) != 16:
        print("❌ El App Password debe tener exactamente 16 caracteres")
        return False
    
    print(f"\n✅ App Password recibido: {new_password[:4]}****{new_password[-4:]}")
    print(f"📝 Guarda esta contraseña en un lugar seguro")
    
    # Actualizar en la base de datos
    try:
        from app import app, db, User
        
        with app.app_context():
            user = User.query.filter_by(username='admin').first()
            if user:
                user.outlook_password = new_password
                db.session.commit()
                print(f"✅ App Password actualizado en la base de datos")
                
                # Probar conexión
                print(f"\n🚀 Probando conexión...")
                from email_sender import EmailSender
                sender = EmailSender(email=user.outlook_email, password=new_password)
                
                if sender.connect():
                    print("✅ Conexión exitosa! El nuevo App Password funciona.")
                    print(f"\n🎉 ¡SISTEMA LISTO PARA ENVIAR EMAILS REALES!")
                    return True
                else:
                    print("❌ Error conectando. Verifica:")
                    print("   • Que tengas 2FA habilitado")
                    print("   • Que el App Password sea correcto")
                    print("   • Que la cuenta no tenga restricciones")
                    return False
            else:
                print("❌ Usuario admin no encontrado")
                return False
                
    except Exception as e:
        print(f"❌ Error actualizando App Password: {e}")
        return False

if __name__ == "__main__":
    generar_app_password()
