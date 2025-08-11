#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def configurar_credenciales_db():
    """Configurar credenciales directamente en la base de datos"""
    
    # Ruta de la base de datos
    db_path = "instance/emails.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada en: {db_path}")
        return False
    
    print("🔧 CONFIGURANDO CREDENCIALES EN BASE DE DATOS")
    print("=" * 50)
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si existe la tabla user
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if not cursor.fetchone():
            print("❌ Tabla 'user' no encontrada")
            return False
        
        # Verificar usuario admin
        cursor.execute("SELECT id, username, outlook_email FROM user WHERE username='admin'")
        user = cursor.fetchone()
        
        if not user:
            print("❌ Usuario 'admin' no encontrado")
            return False
        
        user_id, username, current_email = user
        print(f"👤 Usuario encontrado: {username} (ID: {user_id})")
        print(f"📧 Email actual: {current_email}")
        
        # Configurar credenciales
        email = "el_chicher@hotmail.com"
        password = "tszrmkdaqkjtllvd"
        
        print(f"\n🔑 Configurando credenciales:")
        print(f"   Email: {email}")
        print(f"   Password: {password[:4]}****{password[-4:]}")
        
        # Actualizar credenciales
        cursor.execute("""
            UPDATE user 
            SET outlook_email = ?, outlook_password = ? 
            WHERE id = ?
        """, (email, password, user_id))
        
        # Verificar la actualización
        cursor.execute("SELECT outlook_email, outlook_password FROM user WHERE id = ?", (user_id,))
        updated_user = cursor.fetchone()
        
        if updated_user and updated_user[0] == email:
            print(f"\n✅ Credenciales actualizadas exitosamente!")
            print(f"📧 Email: {updated_user[0]}")
            print(f"🔑 Password: {updated_user[1][:4]}****{updated_user[1][-4:]}")
            
            # Commit de los cambios
            conn.commit()
            print(f"\n💾 Cambios guardados en la base de datos")
            
            return True
        else:
            print(f"❌ Error: Las credenciales no se actualizaron correctamente")
            return False
            
    except Exception as e:
        print(f"❌ Error configurando credenciales: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    configurar_credenciales_db()
