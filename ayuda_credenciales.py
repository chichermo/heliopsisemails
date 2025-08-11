#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from email_sender import EmailSender

def ayuda_credenciales():
    with app.app_context():
        print("🔧 AYUDA PARA CONFIGURAR CREDENCIALES DE OUTLOOK")
        print("=" * 60)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email actual: {user.outlook_email}")
        print(f"🔑 Password configurado: {'Sí' if user.outlook_password else 'No'}")
        
        print(f"\n🎯 PROBLEMA IDENTIFICADO:")
        print(f"   • Las credenciales no son válidas para Outlook")
        print(f"   • Necesitas un App Password (no tu contraseña normal)")
        print(f"   • Requiere 2FA habilitado")
        
        print(f"\n📋 SOLUCIÓN PASO A PASO:")
        print(f"1. Ve a: https://account.microsoft.com/security")
        print(f"2. Inicia sesión con: {user.outlook_email}")
        print(f"3. Busca 'Autenticación de dos factores'")
        print(f"4. Si no está habilitado, haz clic en 'Configurar'")
        print(f"5. Sigue las instrucciones para habilitar 2FA")
        print(f"6. Una vez habilitado, busca 'Contraseñas de aplicación'")
        print(f"7. Haz clic en 'Crear una nueva contraseña de aplicación'")
        print(f"8. Selecciona 'Correo' o 'Outlook'")
        print(f"9. Anota la contraseña de 16 caracteres")
        
        print(f"\n" + "=" * 60)
        print(f"🚀 CUANDO TENGAS EL APP PASSWORD:")
        print(f"1. Ejecuta: python configurar_credenciales_reales.py")
        print(f"2. Ingresa tu email: {user.outlook_email}")
        print(f"3. Ingresa el App Password (NO tu contraseña normal)")
        print(f"4. Confirma los cambios")
        
        print(f"\n💡 CONSEJOS IMPORTANTES:")
        print(f"   • Usa App Password, NO tu contraseña normal")
        print(f"   • El App Password tiene 16 caracteres")
        print(f"   • Solo aparece si tienes 2FA habilitado")
        print(f"   • Si no ves la opción, habilita 2FA primero")
        
        print(f"\n" + "=" * 60)
        print(f"🎯 ¿QUIERES CONTINUAR?")
        print(f"1. Ve a https://account.microsoft.com/security")
        print(f"2. Configura 2FA y App Password")
        print(f"3. Regresa aquí y ejecuta: python configurar_credenciales_reales.py")

if __name__ == "__main__":
    ayuda_credenciales()
