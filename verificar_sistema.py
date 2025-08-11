#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, EmailCampaign, EmailContact, EmailTemplate, User, EmailList
from datetime import datetime, timezone

def verificar_sistema():
    with app.app_context():
        print("🔍 Verificando sistema de envío de emails...")
        print("=" * 50)
        
        # 1. Verificar usuario
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("❌ Usuario admin no encontrado")
            return False
        
        print(f"✅ Usuario: {user.username}")
        
        # 2. Verificar listas
        lists = EmailList.query.filter_by(user_id=user.id).all()
        print(f"✅ Listas encontradas: {len(lists)}")
        for lst in lists:
            contacts = EmailContact.query.filter_by(list_id=lst.id).all()
            print(f"   📋 {lst.name}: {len(contacts)} contactos")
        
        # 3. Verificar templates
        templates = EmailTemplate.query.filter_by(user_id=user.id).all()
        print(f"✅ Templates encontrados: {len(templates)}")
        for template in templates:
            print(f"   📝 {template.name}")
        
        # 4. Verificar campañas
        campaigns = EmailCampaign.query.filter_by(user_id=user.id).all()
        print(f"✅ Campañas encontradas: {len(campaigns)}")
        
        for campaign in campaigns:
            print(f"\n📧 Campaña: {campaign.name}")
            print(f"   ID: {campaign.id}")
            print(f"   Estado: {campaign.status}")
            print(f"   Total: {campaign.total_count}")
            print(f"   Enviados: {campaign.sent_count}")
            
            # Verificar contactos
            contacts = EmailContact.query.filter_by(list_id=campaign.list_id).all()
            print(f"   Contactos reales: {len(contacts)}")
            
            # Verificar si los números coinciden
            if campaign.total_count == len(contacts):
                print(f"   ✅ Conteo correcto")
            else:
                print(f"   ⚠️  Conteo incorrecto (esperado: {len(contacts)}, actual: {campaign.total_count})")
        
        print("\n" + "=" * 50)
        print("🎯 RESUMEN DEL SISTEMA:")
        print(f"   • Usuario: {user.username}")
        print(f"   • Listas: {len(lists)}")
        print(f"   • Templates: {len(templates)}")
        print(f"   • Campañas: {len(campaigns)}")
        
        # Verificar si hay credenciales configuradas
        if user.outlook_email and user.outlook_password:
            print(f"   • Credenciales: ✅ Configuradas ({user.outlook_email})")
        else:
            print(f"   • Credenciales: ⚠️  No configuradas (modo PRUEBA)")
        
        print("\n✅ Sistema verificado correctamente!")
        return True

if __name__ == "__main__":
    verificar_sistema()
