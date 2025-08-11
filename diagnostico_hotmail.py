#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, User
from email_sender import EmailSender
from exchangelib import Credentials, Configuration, Account, DELEGATE
import logging

def diagnostico_hotmail():
    with app.app_context():
        print("🔍 DIAGNÓSTICO ESPECÍFICO PARA HOTMAIL")
        print("=" * 50)
        
        # Obtener usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"👤 Usuario: {user.username}")
        print(f"📧 Email: {user.outlook_email}")
        print(f"🔑 Password: {user.outlook_password[:4]}****{user.outlook_password[-4:]}")
        
        # Credenciales
        email = user.outlook_email
        password = user.outlook_password
        
        print(f"\n🚀 Iniciando diagnóstico...")
        
        # Paso 1: Verificar credenciales básicas
        print(f"\n1️⃣ Verificando credenciales básicas...")
        if not email or not password:
            print("❌ Credenciales faltantes")
            return False
        print("✅ Credenciales presentes")
        
        # Paso 2: Crear credenciales
        print(f"\n2️⃣ Creando objeto Credentials...")
        try:
            credentials = Credentials(email, password)
            print("✅ Objeto Credentials creado")
        except Exception as e:
            print(f"❌ Error creando Credentials: {e}")
            return False
        
        # Paso 3: Probar autodiscover
        print(f"\n3️⃣ Probando autodiscover...")
        try:
            account = Account(
                primary_smtp_address=email,
                credentials=credentials,
                autodiscover=True,
                access_type=DELEGATE
            )
            
            # Verificar conexión
            inbox = account.inbox
            print("✅ Autodiscover exitoso")
            print(f"   📧 Bandeja de entrada: {len(inbox)} elementos")
            return True
            
        except Exception as e:
            print(f"❌ Autodiscover falló: {e}")
        
        # Paso 4: Probar configuración específica
        print(f"\n4️⃣ Probando configuración específica...")
        try:
            config = Configuration(
                service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx',
                credentials=credentials
            )
            
            account = Account(
                primary_smtp_address=email,
                config=config,
                autodiscover=False,
                access_type=DELEGATE
            )
            
            # Verificar conexión
            inbox = account.inbox
            print("✅ Configuración específica exitosa")
            print(f"   📧 Bandeja de entrada: {len(inbox)} elementos")
            return True
            
        except Exception as e:
            print(f"❌ Configuración específica falló: {e}")
        
        print(f"\n❌ Todos los métodos fallaron")
        return False

if __name__ == "__main__":
    diagnostico_hotmail()
