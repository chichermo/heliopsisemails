#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
import requests
import base64

def verificar_app_password():
    with app.app_context():
        print("🔍 VERIFICANDO APP PASSWORD")
        print("=" * 40)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email: {user.outlook_email}")
        print(f"🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
        
        # Verificar si el App Password tiene el formato correcto
        password = user.outlook_password
        if len(password) != 16:
            print(f"❌ App Password debe tener 16 caracteres, actual: {len(password)}")
            return False
        
        print("✅ App Password tiene formato correcto (16 caracteres)")
        
        # Verificar si contiene solo caracteres válidos
        valid_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        if not all(c in valid_chars for c in password.lower()):
            print("❌ App Password contiene caracteres inválidos")
            return False
        
        print("✅ App Password contiene solo caracteres válidos")
        
        print(f"\n💡 INFORMACIÓN IMPORTANTE:")
        print(f"   • El App Password parece estar en formato correcto")
        print(f"   • Si sigue fallando, puede ser que:")
        print(f"     1. El App Password haya expirado")
        print(f"     2. La cuenta tenga restricciones adicionales")
        print(f"     3. Necesites generar un nuevo App Password")
        print(f"     4. La cuenta tenga 2FA habilitado de manera diferente")
        
        print(f"\n🔧 RECOMENDACIONES:")
        print(f"   1. Ve a: https://account.microsoft.com/security")
        print(f"   2. Inicia sesión con: {user.outlook_email}")
        print(f"   3. Ve a 'Contraseñas de aplicación'")
        print(f"   4. Elimina la contraseña actual")
        print(f"   5. Crea una nueva contraseña de aplicación")
        print(f"   6. Usa la nueva contraseña en el sistema")
        
        return True

if __name__ == "__main__":
    verificar_app_password()
