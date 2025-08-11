#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User

def actualizar_credenciales():
    with app.app_context():
        print("🔧 ACTUALIZANDO CREDENCIALES EN LA BASE DE DATOS")
        print("=" * 50)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        # Credenciales específicas
        email = "el_chicher@hotmail.com"
        password = "tszrmkdaqkjtllvd"
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email actual: {user.outlook_email}")
        print(f"📧 Email nuevo: {email}")
        print(f"🔑 Password nuevo: {password[:4]}****{password[-4:]}")
        
        # Actualizar credenciales
        try:
            user.outlook_email = email
            user.outlook_password = password
            db.session.commit()
            
            print(f"\n✅ Credenciales actualizadas exitosamente!")
            print(f"📧 Email: {user.outlook_email}")
            print(f"🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error actualizando credenciales: {e}")
            return False

if __name__ == "__main__":
    actualizar_credenciales()
